#!/usr/bin/env python3
"""T1 addendum — (4,2)-only enrichment split (v17's uv0 is a real uv only
when a TexCoord1 stream exists; for (4,1) w4 is the NORMAL, so v17's uv0 is
structurally invalid there and enrichment 'prefers' it via content density).
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re/session22")
sys.path.insert(0, "/home/z/my-project/scripts")
import batch_parser  # noqa: E402
from t1_diffuse import (island_segments, tex_mask, engine_uv, v17_uv,
                        sample_rate, stem, family_of)  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
rng = np.random.default_rng(20231014)

out = {}
for isl in ("GothamCity", "GothamCity_Island2"):
    recs = batch_parser.parse_island(isl)
    rows = json.load(open(f"{RE}/runtime_mats_{isl}.json"))
    segs = island_segments(isl)
    bymat = {}
    for si, s in enumerate(segs):
        bymat.setdefault(s["m40"], []).append(si)
    mats = []
    for m in bymat:
        if m >= len(recs):
            continue
        rec = recs[m]
        if (rec["n"], rec["K"]) != (4, 2):
            continue
        d = stem(rows[m].get("DiffuseMap"))
        if not d or tex_mask(d) is None:
            continue
        i0 = next((i for i, dd in enumerate(rec["descs"])
                   if dd["attr"] == 1), None)
        if i0 is None:
            continue
        w3 = np.concatenate([segs[si]["w3"] for si in bymat[m]
                             if segs[si]["w3"] is not None])
        w4 = np.concatenate([segs[si]["w4"] for si in bymat[m]
                             if segs[si]["w4"] is not None])
        if not len(w3):
            continue
        mats.append(dict(m=m, d=d, rec=rec, i0=i0, w3=w3, w4=w4,
                         fam=family_of(d, rows[m].get("name"))))

    # per-family pooled enrichment, engine vs v17, + permuted null
    def pooled(mode, pmap=None):
        num, den = {}, {}
        for mu in mats:
            src = mu
            if pmap is not None:
                src = pmap.get(mu["m"], mu)
                # swapped params: use src's pair but mu's words+texture
            if mode == "engine":
                sc, of = src["rec"]["pairs"][src["i0"]]
                u, v = engine_uv(mu["w3"], sc, of)
            else:
                u, v = v17_uv(mu["w4"])
            mask_A, W, H = tex_mask(mu["d"])
            r = sample_rate(u, v, mask_A, W, H)
            unif = float(1.0 - mask_A.mean())
            f = mu["fam"]
            num[f] = num.get(f, 0.0) + r * len(mu["w3"])
            den[f] = den.get(f, 0.0) + unif * len(mu["w3"])
        return {f: num[f] / den[f] for f in num if den[f]}

    obs_e = pooled("engine")
    obs_v = pooled("v17")
    null = {}
    mlist = [mu["m"] for mu in mats]
    pairmap = {mu["m"]: (mu["rec"], mu["i0"]) for mu in mats}
    for _ in range(100):
        perm = rng.permutation(len(mats))
        pmap = {mlist[i]: dict(rec=pairmap[mats[perm[i]]["m"]][0],
                               i0=pairmap[mats[perm[i]]["m"]][1])
                for i in range(len(mats))}
        # rebuild: for each material use permuted (rec,i0) but own w3/d
        ne, nd = {}, {}
        for mu in mats:
            rec, i0 = pmap[mu["m"]]["rec"], pmap[mu["m"]]["i0"]
            sc, of = rec["pairs"][i0]
            u, v = engine_uv(mu["w3"], sc, of)
            mask_A, W, H = tex_mask(mu["d"])
            r = sample_rate(u, v, mask_A, W, H)
            unif = float(1.0 - mask_A.mean())
            f = mu["fam"]
            ne[f] = ne.get(f, 0.0) + r * len(mu["w3"])
            nd[f] = nd.get(f, 0.0) + unif * len(mu["w3"])
        for f in ne:
            if nd[f]:
                null.setdefault(f, []).append(ne[f] / nd[f])
    print(f"\n### {isl} — (4,2)-only enrichment")
    print(f"   {'family':16s} {'engine':>7s} {'v17':>7s} "
          f"{'null':>16s} {'z_eng':>6s} {'z_v17':>6s} n_mats")
    rows_out = {}
    for f in sorted(obs_e):
        e1, e2 = obs_e[f], obs_v.get(f)
        nl = null.get(f, [])
        if len(nl) > 1 and np.std(nl) > 0:
            mu_, sd_ = float(np.mean(nl)), float(np.std(nl))
            z1 = (e1 - mu_) / sd_
            z2 = (e2 - mu_) / sd_ if e2 is not None else None
            nstr = f"{mu_:.3f}+/-{sd_:.3f}"
        else:
            mu_ = float(np.mean(nl)) if nl else None
            z1 = z2 = None
            nstr = "nc"
        nm = sum(1 for mu in mats if mu["fam"] == f)
        print(f"   {f:16s} {e1:7.3f} {(e2 if e2 is not None else float('nan')):7.3f} "
              f"{nstr:>16s} "
              f"{('%6.2f' % z1) if z1 is not None else '    nc'} "
              f"{('%6.2f' % z2) if z2 is not None else '    nc'} {nm}")
        rows_out[f] = dict(engine=e1, v17=e2, null_mean=mu_, null_sd=sd_,
                           z_engine=z1, z_v17=z2, n_materials=nm)
    out[isl] = rows_out

json.dump(out, open("/home/z/my-project/work/t1_diffuse_class42.json", "w"),
          indent=1)
print("\nwrote /home/z/my-project/work/t1_diffuse_class42.json")
