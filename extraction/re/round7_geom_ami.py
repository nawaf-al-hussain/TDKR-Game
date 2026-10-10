#!/usr/bin/env python3
"""Round-7 ask 3 — ADJUSTED MUTUAL INFORMATION between an unsupervised
clustering of segment geometry and the +40 / v5 / shuffled labels, at
MATCHED class counts.

Round-6 established: random-CV z~50 vs permuted nulls (segments sharing a
+40 value are geometrically homogeneous), but leave-material-out CV
collapses because family is nearly a function of material.  The reviewer
asks for the remaining granularity-matched comparison: cluster the
standardized geometry into k = number of label classes, then AMI between
clusters and each label set.  AMI is chance-corrected, so it is comparable
across label sets with different k, and the permuted-label null gives the
z.

Protocol (both islands):
  features = round6_geom_features.json (zext, size_xy, up_frac, horiz_frac,
             area, planarity; log1p on the size-like axes -- same as round 6)
  keep     = fam40 not None and class support >= 8 (same as round 6)
  STANDARDIZE (z-score) on the kept set   <- explicitly confirmed here
  cluster  = KMeans(k classes, n_init=10, seed 6018) on standardized features
  score    = AMI(clusters, labels) for
             +40      (k = #fam40 classes)
             shuffled (permutation of the +40 labels, SAME clusters, k same
                      -> this is the label-permutation null centre)
             v5       (k = #v5 classes, own clustering; plus v5 scored
                      against the +40-k clusters as a granularity check)
  null     = AMI(clusters, permuted labels) over K=200 permutations with the
             same class-count histogram -> mean +- sd -> z

Caveat carried in the output: geometry CANNOT check the index->texture-name
mapping (that rests on the compiled self-indexing 307/307 + renders); AMI
only quantifies label-geometry association.

Outputs: extraction/re/round7_geom_ami.json + stdout table.
"""
import collections
import json

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_mutual_info_score

RE = "/home/z/my-project/repo/extraction/re"
K_NULL = 200
SEED = 6018
GF = ("zext", "size_xy", "up_frac", "horiz_frac", "area", "planarity")


def ami_vs_null(labels, clus):
    """AMI(labels, clus) + permutation null over the labels."""
    obs = float(adjusted_mutual_info_score(labels, clus))
    rng = np.random.default_rng(SEED)
    lab = np.asarray(labels, dtype=object)
    nulls = [float(adjusted_mutual_info_score(lab[rng.permutation(len(lab))],
                                              clus))
             for _ in range(K_NULL)]
    nm, ns = float(np.mean(nulls)), float(np.std(nulls))
    z = (obs - nm) / (ns + 1e-9)
    return obs, nm, ns, z


def main():
    bank = json.load(open(f"{RE}/round6_geom_features.json"))
    report = {}
    for islname, B in bank.items():
        print(f"\n########## {islname}")
        n = len(B["m40"])
        F = np.column_stack([B["features"][k] for k in GF])
        F = F.copy()
        for j, k in enumerate(GF):
            if k in ("area", "size_xy", "zext"):
                F[:, j] = np.log1p(np.abs(F[:, j]))
        fam40 = B["fam40"]
        famv5 = B["fam_v5"]

        sup40 = collections.Counter(l for l in fam40 if l is not None)
        keep = np.array([i for i in range(n)
                         if fam40[i] is not None and sup40[fam40[i]] >= 8])
        Fk = F[keep]
        mu, sd = Fk.mean(0), Fk.std(0) + 1e-6
        Fs = (Fk - mu) / sd                      # <- explicit standardisation

        L40 = np.array([fam40[i] for i in keep], dtype=object)
        Lv5 = np.array([famv5[i] for i in keep], dtype=object)
        hasv5 = np.array([l not in (None, "dark") for l in Lv5])
        k40 = len(set(L40))
        kv5 = len(set(Lv5[hasv5]))
        print(f"n={n} kept={len(keep)} (support>=8); classes: +40 {k40}, "
              f"v5 {kv5} (on {int(hasv5.sum())} rows)")
        print(f"standardised features: mu={np.round(mu, 2)} "
              f"sd={np.round(sd, 2)}")

        out = {}
        # +40 and shuffled share ONE clustering at k40
        km40 = KMeans(n_clusters=k40, n_init=10, random_state=SEED).fit(Fs)
        obs, nm, ns, z = ami_vs_null(L40, km40.labels_)
        out["plus40"] = dict(k=k40, ami=round(obs, 4), null=round(nm, 4),
                             null_sd=round(ns, 4), z=round(z, 1))
        print(f"   +40       k={k40:3d} AMI={obs:.3f} "
              f"null {nm:.3f}+-{ns:.3f} z={z:.0f}")

        rng = np.random.default_rng(SEED + 1)
        Lshuf = L40[rng.permutation(len(L40))]
        obs, nm, ns, z = ami_vs_null(Lshuf, km40.labels_)
        out["shuffled"] = dict(k=k40, ami=round(obs, 4), null=round(nm, 4),
                               null_sd=round(ns, 4), z=round(z, 1))
        print(f"   shuffled  k={k40:3d} AMI={obs:.3f} "
              f"null {nm:.3f}+-{ns:.3f} z={z:.0f}")

        # v5 at its own granularity
        kmv5 = KMeans(n_clusters=kv5, n_init=10, random_state=SEED).fit(Fs)
        obs, nm, ns, z = ami_vs_null(Lv5[hasv5], kmv5.labels_[hasv5])
        out["v5"] = dict(k=kv5, ami=round(obs, 4), null=round(nm, 4),
                         null_sd=round(ns, 4), z=round(z, 1))
        print(f"   v5        k={kv5:3d} AMI={obs:.3f} "
              f"null {nm:.3f}+-{ns:.3f} z={z:.0f}")

        # v5 against the +40-k clusters (granularity cross-check)
        obs, nm, ns, z = ami_vs_null(Lv5[hasv5], km40.labels_[hasv5])
        out["v5_at_k40"] = dict(k=k40, ami=round(obs, 4), null=round(nm, 4),
                                null_sd=round(ns, 4), z=round(z, 1))
        print(f"   v5@k40    k={k40:3d} AMI={obs:.3f} "
              f"null {nm:.3f}+-{ns:.3f} z={z:.0f}")

        report[islname] = out

    json.dump(report, open(f"{RE}/round7_geom_ami.json", "w"), indent=1)
    print(f"\nwrote {RE}/round7_geom_ami.json")


if __name__ == "__main__":
    main()
