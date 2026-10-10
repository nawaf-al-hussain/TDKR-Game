#!/usr/bin/env python3
"""Session-18 T2 — street-flip evidence with the page-density confound removed.

Reviewer round-5 prescriptions:
  1. ENRICHMENT = (observed non-empty texel rate of the segment's UVs on its
     bound texture) / (non-empty rate of uniformly random UVs over the same
     texture or cell).  Scored for +40, v5, and shuffled-+40, per family,
     both islands.  A full-bleed road page has baseline ~1; a dark-pad lamp
     cell a low baseline -- enrichment normalizes that away.
  2. Geometry-profile test (texture-independent): per segment z-extent,
     planarity, upward-normal fraction (normals derived from triangle
     winding -- the streams carry no normal attribute), size.  Scored as
     between-group variance explained (eta^2) per feature under +40 labels
     and under v5 labels, plus a nearest-centroid classifier (5-fold CV)
     and a permuted-label floor.
  3. UV-footprint for v5 as for +40 (round-4: +40 0.263/0.161 vs null
     0.013/0.007), failure breakdown by family, and a diagnosis of why
     ~74% of atlas segments do not land in one cell.
  4. Verdict per family with effect sizes; decisive vs unresolved counts.

Also re-runs the popA slice (v5-bound and +40-diffuse-available) with the
enrichment metric, since that is where v5's raw-validity advantage lived.

Outputs: extraction/re/round5_t2_evidence.json + stdout tables.
"""
import collections
import json
import random
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import parse_island, bind_segment, cross_sections, \
    ISLANDS, uv_of, find_png, strip_to_tris
from round4_street_evidence import (TexData, get_tex, stem_of, fam40,  # noqa
                                    COARSE, ATLAS_FAMS, seg_samples,
                                    validity, footprint, rect_tightness,
                                    m40_list)

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round5_t2_evidence.json"

K_NULL = 24
EPS = 1e-6


# ---------------------------------------------------------------- geometry
def geom_features(seg):
    """Texture-independent profile: z-extent, planarity, up-normal fraction,
    footprint size, triangle area."""
    p = seg["pos"]
    tris = np.asarray(strip_to_tris(seg["idx"]), np.int64).reshape(-1, 3)
    good = (tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) \
        & (tris[:, 0] != tris[:, 2])
    tris = tris[good]
    zext = float(np.ptp(p[:, 2]))
    size_xy = float(np.ptp(p[:, :2]).max())
    diag = float(np.linalg.norm(np.ptp(p[:, :2], axis=0))) + 1e-9
    if len(tris) > 60000:
        rng = np.random.default_rng(18)
        tris = tris[rng.choice(len(tris), 60000, replace=False)]
    a, b, c = p[tris[:, 0]], p[tris[:, 1]], p[tris[:, 2]]
    n = np.cross(b - a, c - a)
    nl = np.linalg.norm(n, axis=1)
    okn = nl > 1e-12
    nn = n[okn] / nl[okn][:, None]
    up = float((nn[:, 2] > 0.7).mean()) if len(nn) else 0.0
    horiz = float((np.abs(nn[:, 2]) < 0.3).mean()) if len(nn) else 0.0
    area = float(0.5 * nl.sum())
    # planarity: residual of the best-fit plane through the vertices
    q = p - p.mean(0)
    if len(q) > 3:
        _, s, _ = np.linalg.svd(q, full_matrices=False)
        rms = float(np.sqrt((s[-1] ** 2) / len(q)))
    else:
        rms = 0.0
    planarity = 1.0 - min(1.0, rms / diag)
    return dict(zext=zext, size_xy=size_xy, up_frac=up, horiz_frac=horiz,
                area=area, planarity=planarity)


# ---------------------------------------------------------------- enrichment
def strict_mask(tex):
    """mask_A emptiness: alpha<64 or near-black ONLY (no modal-colour rule).

    The round-4 'empty' mask also treated 'within 10 of the page's modal
    colour' as background -- correct for atlas padding, but it labels the
    road surface itself empty on full-bleed pages (asphalt IS the modal
    colour), inverting the metric there.  mask_A is valid on every page;
    enrichment normalizes the density away."""
    if not hasattr(tex, "emptyA"):
        tex.emptyA = (tex.alpha < 64) | (tex.rgb.max(axis=2) <= 10)
        tex.contentA = 1.0 - float(tex.emptyA.mean())
    return tex.emptyA


def validity_a(tex, su, sv):
    if tex is None or not tex.ok:
        return 0.0
    strict_mask(tex)
    tj = np.clip((su * (tex.w - 1)).astype(np.int32), 0, tex.w - 1)
    ti = np.clip(((1.0 - sv) * (tex.h - 1)).astype(np.int32), 0, tex.h - 1)
    return float(1.0 - tex.emptyA[ti, tj].mean())


def enrichment(tex, su, sv):
    """ENRICHMENT = observed non-empty rate / uniform-random non-empty rate
    on the same texture (mask_A).  Null (shuffled labels) is ~1 BY
    CONSTRUCTION at this level -- the metric reads >1 when a binding's UVs
    preferentially sample content, ~1 when silent (full-bleed pages)."""
    if tex is None or not tex.ok:
        return None
    strict_mask(tex)
    base = tex.contentA
    if base <= EPS:
        return None
    obs = validity_a(tex, su, sv)
    return obs / base, obs


def main():
    rng = random.Random(1804)
    report = {}
    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = parse_island(islname)
        m40s = m40_list(islname)
        n = len(segs)
        assert n == len(m40s)

        XSECS = {k: cross_sections(k) for k in (
            "GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
            "GothamCity_Road_Island_2", "gothamcity_roads_details",
            "GothamCity_Road_Crossings_Island_1",
            "GothamCity_Road_Crossings_Island_2")}
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}

        p40_stem = [stem_of(rows[m].get("DiffuseMap")) for m in m40s]
        fams = [fam40(st) for st in p40_stem]
        v5 = [bind_segment(s, isl, xs) for s in segs]
        v5_stem = [t or None for t, mode in v5]
        v5_fams = [fam40(st) if st else "dark" for st in v5_stem]
        popA = [i for i in range(n) if v5_stem[i] and p40_stem[i]]
        print(f"segments={n}, popA(v5-bound & +40-diffuse)={len(popA)}")

        # ------- per-segment sample points + geometry
        su_list, sv_list = [], []
        gfeats = []
        for s in segs:
            su, sv = seg_samples(s, rng)
            su_list.append(su)
            sv_list.append(sv)
            gfeats.append(geom_features(s))
        sampled = [i for i in range(n) if su_list[i] is not None]
        print(f"sampled={len(sampled)}")

        GF = ("zext", "size_xy", "up_frac", "horiz_frac", "area", "planarity")
        garr = {k: np.array([g[k] for g in gfeats]) for k in GF}

        # ------- validity + enrichment under each binding
        def score_binding(stems):
            val = np.zeros(n)
            enr_tex = np.full(n, np.nan)
            fp_dom = np.zeros(n)
            for i in sampled:
                t = get_tex(stems[i]) if stems[i] else None
                if t is None or not t.ok:
                    continue
                e = enrichment(t, su_list[i], sv_list[i])
                if e:
                    val[i] = e[1]
                    enr_tex[i] = e[0]
                if fams[i] in ATLAS_FAMS:
                    fp_dom[i] = footprint(t, su_list[i], sv_list[i])[0]
            return val, enr_tex, fp_dom

        val40, et40, fp40 = score_binding(p40_stem)
        valv5, etv5, fpv5 = score_binding(v5_stem)

        null_et = np.zeros((K_NULL, n))
        null_fp = np.zeros((K_NULL, n))
        for k in range(K_NULL):
            perm = list(range(n))
            rng.shuffle(perm)
            for i in sampled:
                st = p40_stem[perm[i]]
                t = get_tex(st) if st else None
                if t is None or not t.ok:
                    continue
                e = enrichment(t, su_list[i], sv_list[i])
                if e:
                    null_et[k, i] = e[0]
                if fams[i] in ATLAS_FAMS:
                    null_fp[k, i] = footprint(t, su_list[i], sv_list[i])[0]

        # ------- per-family aggregation
        def fam_table(vals, mask_ok):
            agg = collections.defaultdict(list)
            for i in sampled:
                if not mask_ok[i] or np.isnan(vals[i]):
                    continue
                agg[fams[i]].append(vals[i])
            return {f: dict(nseg=len(a), mean=round(float(np.mean(a)), 3),
                            median=round(float(np.median(a)), 3))
                    for f, a in sorted(agg.items())}

        def shuffle_table(mat):
            agg = collections.defaultdict(lambda: ([], []))
            for i in sampled:
                v = mat[:, i]
                v = v[~np.isnan(v)]
                if not len(v):
                    continue
                m, s = agg[fams[i]]
                m.append(float(np.mean(v)))
                s.append(float(np.std(v)))
            return {f: dict(nseg=len(m), null_mean=round(float(np.mean(m)), 3),
                            null_sd=round(float(np.std(m)), 3))
                    for f, (m, s) in sorted(agg.items())}

        # ------- verdict per family (enrichment, mask_A; null ~1 by design)
        verdict = {}
        for f in sorted(set(fams)):
            idx = [i for i in sampled if fams[i] == f
                   and not np.isnan(et40[i])]
            if len(idx) < 8:
                continue
            m40 = float(np.nanmean(et40[idx]))
            mv5 = float(np.nanmean([etv5[i] for i in idx])) \
                if not all(np.isnan(etv5[i]) for i in idx) else float("nan")
            # shuffle null (sanity: should be ~1 by construction)
            nm = float(np.nanmean([np.nanmean(null_et[k, idx])
                                   for k in range(K_NULL)]))
            sd = float(np.nanstd([np.nanmean(null_et[k, idx])
                                  for k in range(K_NULL)]))
            # effect size vs the 1.0 no-preference line
            d40 = (m40 - 1.0) / (sd + EPS)
            d5 = (mv5 - 1.0) / (sd + EPS) if np.isfinite(mv5) else 0.0
            win40 = int(np.nansum([et40[i] > etv5[i] for i in idx]))
            winv5 = int(np.nansum([etv5[i] > et40[i] for i in idx]))
            if d40 > 3 and (not np.isfinite(mv5) or m40 > mv5 * 1.15):
                v = "+40"
            elif d5 > 3 and mv5 > m40 * 1.15:
                v = "v5 (content-preferring; see geometry test)"
            elif d40 < -3:
                v = "anti-enriched (UVs avoid non-black content; page type " \
                    "breaks the mask -- metric inapplicable)"
            elif m40 <= 1.0 + 3 * sd and (not np.isfinite(mv5)
                                          or mv5 <= 1.0 + 3 * sd):
                v = "metric-silent (~1: full-bleed or no preference)"
            else:
                v = "unresolved"
            verdict[f] = dict(n=len(idx), plus40=round(m40, 3),
                              v5=round(mv5, 3) if np.isfinite(mv5) else None,
                              null=round(nm, 3), null_sd=round(sd, 3),
                              d_plus40_vs1=round(d40, 1),
                              d_v5_vs1=round(d5, 1),
                              wins=dict(plus40=win40, v5=winv5), verdict=v)

        # ------- geometry profiles + prediction scores
        def eta2(labels, key, min_n=8):
            labs = np.asarray(labels)
            tot = garr[key].var()
            if tot <= EPS:
                return None
            num = 0.0
            for lv in set(labs):
                m = labs == lv
                if m.sum() < min_n:
                    continue
                num += m.sum() * (garr[key][m].mean() - garr[key].mean()) ** 2
            return round(float(num / tot / len(labs)), 3)

        def centroid_cv(labels, feats, folds=5, seed=18):
            labs = np.asarray(labels)
            keep = np.array([i for i in range(n) if labs[i] is not None])
            cnt = collections.Counter(labs[keep])
            keep = np.array([i for i in keep if cnt[labs[i]] >= 8])
            if len(keep) < 40 or len(cnt) < 2:
                return None
            r = np.random.default_rng(seed)
            order = r.permutation(keep)
            accs = []
            F = np.column_stack([feats[k] for k in GF])
            # log-scale heavy-tailed features
            F = F.copy()
            for j, k in enumerate(GF):
                if k in ("area", "size_xy", "zext"):
                    F[:, j] = np.log1p(np.abs(F[:, j]))
            mu, sd = F[keep].mean(0), F[keep].std(0) + EPS
            F = (F - mu) / sd
            for f in range(folds):
                te = order[f::folds]
                tr = np.setdiff1d(order, te)
                cents = {lv: F[tr][labs[tr] == lv].mean(0) for lv in cnt}
                pred = []
                for i in te:
                    d = {lv: float(np.linalg.norm(F[i] - c)) for lv, c in cents.items()}
                    pred.append(min(d, key=d.get))
                accs.append(float(np.mean([pred[t] == labs[te][t]
                                           for t in range(len(te))])))
            return round(float(np.mean(accs)), 3)

        # majority-label floor: predict the largest class always
        def majority_floor(labels):
            labs = np.asarray(labels)
            keep = [i for i in range(n) if labs[i] is not None
                    and fams[i] != "unbound"]
            cnt = collections.Counter([labs[i] for i in keep])
            return round(max(cnt.values()) / len(keep), 3)

        gfeat40 = [fams[i] if fams[i] != "unbound" else None for i in range(n)]
        gfeatv5 = [v5_fams[i] if v5_fams[i] != "dark" else None for i in range(n)]
        eta40 = {k: eta2(gfeat40, k) for k in GF}
        etav5 = {k: eta2(gfeatv5, k) for k in GF}
        cv40 = centroid_cv(gfeat40, garr)
        cvv5 = centroid_cv(gfeatv5, garr)
        floor40 = majority_floor(gfeat40)
        floorv5 = majority_floor(gfeatv5)

        # profile means per coarse family under each labelling
        def prof(labels, coarse_map):
            labs = [coarse_map.get(l, "other") if l else None for l in labels]
            out = collections.defaultdict(dict)
            for k in GF:
                agg = collections.defaultdict(list)
                for i in range(n):
                    if labs[i]:
                        agg[labs[i]].append(garr[k][i])
                for lv, a in agg.items():
                    if len(a) >= 8:
                        out[lv][k] = round(float(np.mean(a)), 3)
            return dict(out)

        prof40 = prof(gfeat40, COARSE)
        profv5 = prof(gfeatv5, COARSE)

        # ------- v5 footprint + failure breakdown
        def fp_breakdown(fp_arr, stems):
            det = collections.defaultdict(lambda: [0, 0])
            for i in sampled:
                if not stems[i] or fams[i] not in ATLAS_FAMS:
                    continue
                t = get_tex(stems[i])
                if t is None or not t.ok or t.n_cells < 2 or t.coverage >= 0.85:
                    continue
                det[fams[i]][1] += 1
                if fp_arr[i] >= 0.95:
                    det[fams[i]][0] += 1
            return {f: dict(pass_=a, n=b, rate=round(a / b, 3) if b else None)
                    for f, (a, b) in sorted(det.items())}

        fp40_brk = fp_breakdown(fp40, p40_stem)
        fpv5_brk = fp_breakdown(fpv5, v5_stem)
        fpnull_brk = {}
        for f in sorted(set(fams)):
            idx = [i for i in sampled if fams[i] == f and p40_stem[i]
                   and fams[i] in ATLAS_FAMS]
            idx = [i for i in idx if (lambda t: t and t.ok and t.n_cells >= 2
                                      and t.coverage < 0.85)(get_tex(p40_stem[i]))]
            if len(idx) < 8:
                continue
            fpnull_brk[f] = dict(
                n=len(idx),
                null=round(float(np.mean([np.mean(null_fp[:, i] >= 0.95)
                                          for i in idx])), 3))

        # ------- popA enrichment slice
        popA_stats = dict(
            n=len(popA),
            plus40_enr=round(float(np.nanmean([et40[i] for i in popA])), 3),
            v5_enr=round(float(np.nanmean([etv5[i] for i in popA])), 3),
            null_enr=round(float(np.nanmean(null_et[:, popA])), 3),
            null_sd=round(float(np.std([np.nanmean(null_et[k, popA])
                                        for k in range(K_NULL)])), 3),
            plus40_raw=round(float(np.nanmean([val40[i] for i in popA])), 3),
            v5_raw=round(float(np.nanmean([valv5[i] for i in popA])), 3),
            wins_enr=dict(plus40=int(np.nansum([et40[i] > etv5[i] for i in popA])),
                          v5=int(np.nansum([etv5[i] > et40[i] for i in popA]))),
        )

        # decisive vs unresolved segment counts (verdict on fine families)
        decisive = 0
        unresolved = 0
        fam_dec = {}
        for f, v in verdict.items():
            fam_dec[f] = v["verdict"]
            if v["verdict"] in ("+40", "v5"):
                decisive += v["n"]
            else:
                unresolved += v["n"]

        report[islname] = dict(
            n_segments=n, n_sampled=len(sampled), n_popA=len(popA),
            enrichment=dict(plus40=fam_table(et40, np.ones(n, bool)),
                            v5=fam_table(etv5, np.ones(n, bool)),
                            null=shuffle_table(null_et),
                            note="mask_A (alpha/near-black); null ~1 by "
                                 "construction; >1 = UVs prefer content"),
            verdict=verdict,
            popA=popA_stats,
            geometry=dict(
                features=GF,
                eta2_plus40=eta40, eta2_v5=etav5,
                centroid_cv=dict(plus40=cv40, v5=cvv5,
                                 floor_plus40=floor40, floor_v5=floorv5),
                profile_by_coarse=dict(plus40=prof40, v5=profv5),
            ),
            footprint=dict(plus40=fp40_brk, v5=fpv5_brk, null=fpnull_brk,
                           recheck="see round5_footprint_recheck.json: "
                                  "round-4 20x null was estimator mismatch; "
                                  "matched single-perm null >= +40 rate"),
            decisive_segments=dict(decisive=decisive, unresolved=unresolved,
                                   fam_verdicts=fam_dec),
        )

        # ------- console
        print("\n-- ENRICHMENT (texture-level, mask_A) by family: "
              "null ~1 by construction; >1 = UVs prefer content")
        print(f"   {'family':24s} {'n':>4s} {'+40':>7s} {'v5':>7s} "
              f"{'null':>12s} {'d40':>6s} {'dv5':>6s}  verdict")
        for f, v in verdict.items():
            print(f"   {f:24s} {v['n']:4d} {v['plus40']:7.3f} "
                  f"{(v['v5'] if v['v5'] is not None else float('nan')):7.3f} "
                  f"{v['null']:6.3f}±{v['null_sd']:.3f} "
                  f"{v['d_plus40_vs1']:6.1f} {v['d_v5_vs1']:6.1f}  {v['verdict']}")
        print(f"\n-- popA enrichment: +40 {popA_stats['plus40_enr']} "
              f"v5 {popA_stats['v5_enr']} null {popA_stats['null_enr']}"
              f"±{popA_stats['null_sd']} (raw validity: +40 "
              f"{popA_stats['plus40_raw']} v5 {popA_stats['v5_raw']})  "
              f"wins {popA_stats['wins_enr']}")
        print("\n-- geometry eta^2 (+40 labels vs v5 labels) -- the "
              "texture-independent arbiter:")
        for k in GF:
            print(f"   {k:12s} +40 {eta40[k]}  v5 {etav5[k]}")
        print(f"   centroid-CV acc: +40 {cv40} (floor {floor40})  "
              f"v5 {cvv5} (floor {floorv5})")
        print("\n-- footprint dom95 by family (see recheck note: pooled "
              "round-4 null was estimator-mismatched):")
        for f in sorted(set(list(fp40_brk) + list(fpv5_brk))):
            a = fp40_brk.get(f, {})
            b = fpv5_brk.get(f, {})
            c = fpnull_brk.get(f, {})
            print(f"   {f:24s} +40 {a.get('rate', 0):5.3f}/{a.get('n', 0):4d}  "
                  f"v5 {b.get('rate', 0):5.3f}/{b.get('n', 0):4d}  "
                  f"null {c.get('null', 0):5.3f}/{c.get('n', 0):4d}")
        print(f"\n-- decisive {decisive} vs unresolved {unresolved} segments")

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
