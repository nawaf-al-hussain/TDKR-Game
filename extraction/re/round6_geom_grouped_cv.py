#!/usr/bin/env python3
"""Round-6 ask 2 — THE GEOMETRY TEST WITH GROUPED CV.

Session-18's geometry-profile classifier (nearest-centroid, 5-fold) used
RANDOM folds.  City batches contain near-duplicate geometry (the same
building template instanced across zone blocks), so random folds leak
template copies between train and test and can inflate accuracy.

This script re-scores the geometry test under leakage-controlled schemes:

  random5       5-fold random (baseline; should reproduce session 18)
  by_material   groups = +40 material id (all segments of a material --
                i.e. every instance of one template -- stay in one fold;
                the test fold contains materials never seen in training)
  by_space      groups = 256u grid cell of the segment centroid (controls
                spatially-adjacent copies across materials)
  dedup_random  random 5-fold after exact-duplicate vertex buffers are
                collapsed to one representative

Labels scored on the SAME folds: +40 fine families (fam40 of the +40
diffuse stem), v5 fine families, and a permuted-label null (K=12) under
each scheme.  Metrics: accuracy, always-majority floor, accuracy-floor,
z vs the matched null, per-class recall (+40, by_material).

Also banks per-segment geometry features + labels to
round6_geom_features.json so later rounds never re-parse the zones.

Outputs: extraction/re/round6_geom_grouped_cv.json + stdout tables.
"""
import collections
import hashlib
import json
import random
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import parse_island, bind_segment, cross_sections, \
    ISLANDS, strip_to_tris
from round4_street_evidence import stem_of, fam40, m40_list
from round5_t2_evidence import geom_features

RE = "/home/z/my-project/repo/extraction/re"
K_NULL = 12
FOLDS = 5
EPS = 1e-6


def assign_group_folds(group_ids, n_items, k=FOLDS, seed=18):
    """Greedy balanced assignment of groups to k folds (by item count)."""
    rng = random.Random(seed)
    groups = collections.defaultdict(list)
    for i, g in enumerate(group_ids):
        groups[g].append(i)
    order = list(groups)
    rng.shuffle(order)
    order.sort(key=lambda g: -len(groups[g]))
    fold_load = [0] * k
    fold_of_group = {}
    for g in order:
        f = min(range(k), key=lambda j: fold_load[j])
        fold_of_group[g] = f
        fold_load[f] += len(groups[g])
    return np.array([fold_of_group[g] for g in group_ids])


def random_folds(n_items, k=FOLDS, seed=18):
    rng = np.random.default_rng(seed)
    return rng.permutation(n_items) % k


def cv_accuracy(labels, folds, F, k=FOLDS):
    """Nearest-centroid accuracy with the given fold array."""
    labs = np.asarray(labels, dtype=object)
    accs, recalls = [], collections.defaultdict(list)
    classes = sorted({l for l in labs})
    for f in range(k):
        te = np.where(folds == f)[0]
        tr = np.where(folds != f)[0]
        if len(te) == 0 or len(tr) == 0:
            continue
        cents = {}
        for lv in classes:
            m = labs[tr] == lv
            if m.sum() >= 1:
                cents[lv] = F[tr][m].mean(0)
        pred = []
        for i in te:
            d = {lv: float(np.linalg.norm(F[i] - c))
                 for lv, c in cents.items()}
            pred.append(min(d, key=d.get))
        pred = np.array(pred, dtype=object)
        accs.append(float(np.mean(pred == labs[te])))
        for lv in classes:
            m = labs[te] == lv
            if m.sum() >= 4:
                recalls[lv].append(float(np.mean(pred[m] == lv)))
    return (float(np.mean(accs)),
            {lv: round(float(np.mean(r)), 3) for lv, r in recalls.items()
             if len(r) >= 3})


def prep_features(gfeats, GF):
    F = np.column_stack([gfeats[k] for k in GF])
    F = F.copy()
    for j, k in enumerate(GF):
        if k in ("area", "size_xy", "zext"):
            F[:, j] = np.log1p(np.abs(F[:, j]))
    return F


def main():
    rng = random.Random(6018)
    report = {}
    bank = {}
    GF = ("zext", "size_xy", "up_frac", "horiz_frac", "area", "planarity")

    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        segs = parse_island(islname)
        m40s = m40_list(islname)
        n = len(segs)
        assert n == len(m40s)
        rows = json.load(open(
            f"{RE}/runtime_mats_{islname}.json"))
        p40_stem = [stem_of(rows[m].get("DiffuseMap")) for m in m40s]
        fams = [fam40(st) for st in p40_stem]

        XSECS = {k: cross_sections(k) for k in (
            "GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
            "GothamCity_Road_Island_2", "gothamcity_roads_details",
            "GothamCity_Road_Crossings_Island_1",
            "GothamCity_Road_Crossings_Island_2")}
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}
        v5 = [bind_segment(s, isl, xs) for s in segs]
        v5_stem = [t or None for t, mode in v5]
        v5_fams = [fam40(st) if st else "dark" for st in v5_stem]

        # geometry + centroid + exact-dup detection
        gfeats = collections.defaultdict(list)
        centroids = np.zeros((n, 2))
        dup_key = {}
        dup_id = [None] * n
        for i, s in enumerate(segs):
            g = geom_features(s)
            for k in GF:
                gfeats[k].append(g[k])
            p = s["pos"]
            centroids[i] = (p[:, 0].mean(), p[:, 1].mean())
            h = hashlib.md5(p.tobytes()).hexdigest()[:12] + \
                hashlib.md5(np.asarray(s["idx"], np.int32).tobytes()
                            ).hexdigest()[:12]
            if h in dup_key:
                dup_id[i] = dup_key[h]
            else:
                dup_key[h] = i
                dup_id[i] = i
        garr = {k: np.array(gfeats[k]) for k in GF}
        dup_sizes = collections.Counter(dup_id)
        n_dup_groups = sum(1 for c in dup_sizes.values() if c > 1)
        n_in_dups = sum(c for c in dup_sizes.values() if c > 1)
        matsz = collections.Counter(m40s)
        n_multi_mats = sum(1 for c in matsz.values() if c >= 2)
        n_on_multi = sum(c for c in matsz.values() if c >= 2)
        print(f"segments={n}; exact-dup groups={n_dup_groups} covering "
              f"{n_in_dups} segments ({n_in_dups / n:.1%}); materials={len(matsz)}"
              f" ({n_multi_mats} with >=2 segs, holding {n_on_multi} segs "
              f"= {n_on_multi / n:.0%})")

        # labels: keep the class floor away from unbound/dark
        lab40 = [fams[i] if fams[i] != "unbound" else None for i in range(n)]
        labv5 = [v5_fams[i] if v5_fams[i] != "dark" else None
                 for i in range(n)]

        # fold schemes
        grid_ids = [(int(cx // 256), int(cy // 256)) for cx, cy in centroids]
        schemes = {
            "random5": random_folds(n),
            "by_material": assign_group_folds(m40s, n),
            "by_space": assign_group_folds(grid_ids, n),
        }
        # dedup: one representative per exact-dup group
        reps = sorted(set(dup_id))
        rep_idx = {r: j for j, r in enumerate(reps)}

        def run_scheme(name, folds, labels, F, idx=None):
            if idx is None:
                idx = np.arange(n)
            labs = [labels[i] for i in idx]
            keep = np.array([j for j, l in enumerate(labs) if l is not None])
            cnt = collections.Counter([labs[j] for j in keep])
            keep = np.array([j for j in keep if cnt[labs[j]] >= 8])
            if len(keep) < 40 or len(cnt) < 2:
                return None
            labs_k = [labs[j] for j in keep]
            Fk = F[keep]
            fk = folds[keep]
            floor = max(collections.Counter(labs_k).values()) / len(labs_k)
            acc, recalls = cv_accuracy(labs_k, fk, Fk)
            nulls = []
            lr = np.array(labs_k, dtype=object)
            npr = np.random.default_rng(6018)
            for _ in range(K_NULL):
                perm = lr[npr.permutation(len(lr))]
                a, _ = cv_accuracy(perm, fk, Fk)
                nulls.append(a)
            nm, ns = float(np.mean(nulls)), float(np.std(nulls))
            return dict(n=len(keep), n_classes=len(cnt), floor=round(floor, 3),
                        acc=round(acc, 3), acc_minus_floor=round(acc - floor, 3),
                        null=round(nm, 3), null_sd=round(ns, 3),
                        z_vs_null=round((acc - nm) / (ns + EPS), 1),
                        recalls=recalls)

        out = {}
        for name, folds in schemes.items():
            F = prep_features(garr, GF)
            # standardise once (same as session 18)
            keep_all = np.array([i for i in range(n)
                                 if lab40[i] is not None
                                 and collections.Counter(
                                     [l for l in lab40 if l])[lab40[i]] >= 8])
            mu = F[keep_all].mean(0)
            sd = F[keep_all].std(0) + EPS
            F = (F - mu) / sd
            out[name] = dict(
                plus40=run_scheme(name, folds, lab40, F),
                v5=run_scheme(name, folds, labv5, F))
            r40 = out[name]["plus40"]
            rv5 = out[name]["v5"]
            print(f"\n-- scheme {name}:")
            print(f"   +40: acc {r40['acc']} (floor {r40['floor']}, "
                  f"+{r40['acc_minus_floor']}) null {r40['null']}"
                  f"±{r40['null_sd']} z={r40['z_vs_null']} "
                  f"[n={r40['n']}, {r40['n_classes']} classes]")
            print(f"   v5 : acc {rv5['acc']} (floor {rv5['floor']}, "
                  f"{rv5['acc_minus_floor']:+.3f}) null {rv5['null']}"
                  f"±{rv5['null_sd']} z={rv5['z_vs_null']} "
                  f"[n={rv5['n']}, {rv5['n_classes']} classes]")

        # dedup_random: random folds on deduped representatives
        F = prep_features(garr, GF)
        keep_all = np.array([i for i in range(n)
                             if lab40[i] is not None
                             and collections.Counter(
                                 [l for l in lab40 if l])[lab40[i]] >= 8])
        mu, sd = F[keep_all].mean(0), F[keep_all].std(0) + EPS
        F = (F - mu) / sd
        folds_rep = random_folds(len(reps), seed=19)
        out["dedup_random5"] = dict(
            plus40=run_scheme("dedup", folds_rep, lab40, F,
                              idx=np.array(reps)),
            v5=run_scheme("dedup", folds_rep, labv5, F,
                          idx=np.array(reps)))
        r40 = out["dedup_random5"]["plus40"]
        rv5 = out["dedup_random5"]["v5"]
        print(f"\n-- scheme dedup_random5 (one representative per exact-dup "
              f"group; n={len(reps)}):")
        print(f"   +40: acc {r40['acc']} (floor {r40['floor']}, "
              f"+{r40['acc_minus_floor']}) null {r40['null']}±"
              f"{r40['null_sd']} z={r40['z_vs_null']}")
        print(f"   v5 : acc {rv5['acc']} (floor {rv5['floor']}, "
              f"{rv5['acc_minus_floor']:+.3f}) null {rv5['null']}±"
              f"{rv5['null_sd']} z={rv5['z_vs_null']}")

        # per-class recall under by_material (+40) — what carries the signal
        rc = out["by_material"]["plus40"]["recalls"]
        print("\n-- +40 per-class recall under by_material CV "
              "(n>=8 segments, recall reported if seen in >=3 folds):")
        sup = collections.Counter([lab40[i] for i in range(n)
                                   if lab40[i] is not None])
        for lv, r in sorted(rc.items(), key=lambda kv: -sup[kv[0]]):
            print(f"   {lv:26s} n={sup[lv]:4d} recall={r}")

        report[islname] = dict(
            n_segments=n,
            dup_groups=n_dup_groups, segs_in_dup_groups=n_in_dups,
            cv=out,
            class_support={k: v for k, v in sup.items() if v >= 8})

        bank[islname] = dict(
            features={k: [round(float(x), 6) for x in garr[k]]
                      for k in GF},
            centroid_xy=[[round(float(a), 2), round(float(b), 2)]
                         for a, b in centroids],
            m40=m40s,
            fam40=lab40,
            fam_v5=labv5,
            dup_rep=[int(d) for d in dup_id])

    json.dump(report, open(f"{RE}/round6_geom_grouped_cv.json", "w"),
              indent=1)
    json.dump(bank, open(f"{RE}/round6_geom_features.json", "w"))
    print(f"\nwrote {RE}/round6_geom_grouped_cv.json + "
          f"round6_geom_features.json")


if __name__ == "__main__":
    main()
