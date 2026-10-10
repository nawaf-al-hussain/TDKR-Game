#!/usr/bin/env python3
"""Session-18 T3 — discriminate the (scale@121, offset@145) lightmap chain
from alternatives, with nulls, seams, wrap-mode evidence and populations.

Round-5 reviewer prescriptions:
  1. Luminance-structure re-run for ALTERNATIVES:
       scale@133/offset@109, scale@109+offset@145, (121,145) permuted across
       materials, wrap vs no-wrap, identity.
  2. Seam continuity: near-coincident vertices on adjacent segments with
     different materials -- mean |dLM| under the candidate chain vs the same
     pairs under permuted material params.
  3. Wrap mode: sampler records + engine sampler-state setup (GL_REPEAT vs
     CLAMP constants in libKRHP.so) -- do not ship wrap as an assumption if
     a flag exists.
  4. Non-compact LM materials by name (the 32/26, incl. m73) + shared traits.
  5. Park check on the 20 largest LM-bound segments: sampled LM mean/std vs
     page histogram, old chain vs new chain.
  6. Slots 109/133: u16-dequant hypothesis for a vertex attribute (uv0) --
     before calling them placeholders.  Position is f32 (scale 1e-5 would
     collapse it) -- rejected by construction, reported.
  7. Stride-20 building count (no w3 -> flat tint fallback).

Outputs: extraction/re/round5_t3_chain.json + stdout tables.
"""
import collections
import json
import random
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import parse_island, ISLANDS, find_png, strip_to_tris, uv_of
from round4_lm_probe import seg_words, stem_of
from round4_street_evidence import fam40, m40_list

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round5_t3_chain.json"

PAGE_RES = 1024
K_PERM = 12
SEAM_DIST = 0.30   # world units for near-coincident vertices


def slots_of(islname):
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    out = []
    for m in range(M):
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        out.append(dict(s109=struct.unpack_from("<3f", rec, 109),
                        s121=struct.unpack_from("<3f", rec, 121),
                        s133=struct.unpack_from("<3f", rec, 133),
                        s145=struct.unpack_from("<3f", rec, 145)))
    return out


_page_cache = {}


def page_lum(stem):
    if stem not in _page_cache:
        png = find_png(stem)
        if png is None:
            _page_cache[stem] = None
        else:
            im = Image.open(png).convert("L")
            if max(im.size) > PAGE_RES:
                im = im.resize((PAGE_RES, PAGE_RES), Image.BILINEAR)
            g = np.asarray(im, np.float32) / 255.0
            _page_cache[stem] = g
    return _page_cache[stem]


def sample_lum(g, pu, pv):
    h, w = g.shape[:2]
    ti = np.clip(((1.0 - pv) * (h - 1)).astype(np.int32), 0, h - 1)
    tj = np.clip((pu * (w - 1)).astype(np.int32), 0, w - 1)
    return g[ti, tj]


def w3norm(W):
    return ((W & 0xFFFF).astype(np.float32) / 65535.0,
            (W >> 16).astype(np.float32) / 65535.0)


def chain_uv(cu, cv, s, o, wrap=True):
    pu = cu * s[0] + o[0]
    pv = cv * s[1] + o[1]
    if wrap:
        pu %= 1.0
        pv %= 1.0
    else:
        pu = np.clip(pu, 0.0, 1.0)
        pv = np.clip(pv, 0.0, 1.0)
    return pu, pv


def visited_structure(mats, w3_by_m, slots, rows, wrap=True, perm=None,
                      scale_key="s121", off_key="s145"):
    """mean over materials of visited-region luminance std + edge energy."""
    stds, edges, means, inpage = [], [], [], []
    npr = np.random.default_rng(9)
    for m in mats:
        if m not in w3_by_m:
            continue
        W = w3_by_m[m]
        cu, cv = w3norm(W)
        if perm is not None:
            m2 = perm[m]
            s, o = slots[m2][scale_key], slots[m2][off_key]
        else:
            s, o = slots[m][scale_key], slots[m][off_key]
        lmst = stem_of(rows[m].get("LightMap"))
        g = page_lum(lmst)
        if g is None:
            continue
        pu, pv = chain_uv(cu, cv, s, o, wrap=wrap)
        if not wrap:
            inpage.append(float(np.mean((pu >= 0) & (pu <= 1)
                                        & (pv >= 0) & (pv <= 1))))
        take = min(len(pu), 8000)
        sel = npr.choice(len(pu), take, replace=False)
        vals = sample_lum(g, pu[sel], pv[sel])
        stds.append(float(vals.std()))
        means.append(float(vals.mean()))
        gx = vals[1:] - vals[:-1]
        edges.append(float(np.mean(np.abs(gx))) if len(gx) else 0.0)
    return dict(n_mats=len(stds),
                lum_std=round(float(np.mean(stds)), 4) if stds else None,
                lum_std_sd=round(float(np.std(stds)), 4) if stds else None,
                lum_mean=round(float(np.mean(means)), 4) if means else None,
                edge_energy=round(float(np.mean(edges)), 5) if edges else None,
                in_page=round(float(np.mean(inpage)), 4) if inpage else None)


def build_seam_pairs(segs, w3_per_seg, max_pairs=4000):
    """Near-coincident vertex pairs from LM-bound stride-24 segments of
    DIFFERENT materials (both endpoints need per-vertex w3 + material)."""
    from scipy.spatial import cKDTree
    pts, owner, vref = [], [], []
    voff = {}
    for si, W in sorted(w3_per_seg.items()):
        p = segs[si]["pos"]
        voff[si] = sum(len(x) for x in pts)
        pts.append(p)
        owner.append(np.full(len(p), _seg_m40[si], np.int64))
        vref.append(np.full(len(p), si, np.int64))
    if not pts:
        return None
    P = np.concatenate(pts)
    OW = np.concatenate(owner)
    VR = np.concatenate(vref)
    tree = cKDTree(P)
    prs = tree.query_pairs(SEAM_DIST, output_type="ndarray")
    keep = OW[prs[:, 0]] != OW[prs[:, 1]]
    prs = prs[keep]
    if len(prs) > max_pairs:
        sel = np.random.default_rng(3).choice(len(prs), max_pairs, replace=False)
        prs = prs[sel]
    return P, OW, VR, prs, voff


def seam_continuity(pairs, w3_by_m_per_seg, slots, rows, wrap=True,
                    perm=None, scale_key="s121", off_key="s145",
                    same_page_only=False, uv_space=False):
    """mean |LM(v_i)-LM(v_j)| over seam pairs (or pageUV agreement when
    uv_space).  same_page_only restricts to pairs whose materials share the
    same LightMap page (cross-page seams differ even under correct params)."""
    P, OW, VR, prs, voff = pairs
    diffs = []
    for i, j in prs:
        si, sj = int(VR[i]), int(VR[j])
        mi, mj = _seg_m40[si], _seg_m40[sj]
        if same_page_only:
            pi = stem_of(rows[mi].get("LightMap"))
            pj = stem_of(rows[mj].get("LightMap"))
            if pi != pj:
                continue
        li = _vertex_lm(si, i - voff[si], w3_by_m_per_seg, slots, rows,
                        wrap, perm, scale_key, off_key, uv_space=uv_space)
        lj = _vertex_lm(sj, j - voff[sj], w3_by_m_per_seg, slots, rows,
                        wrap, perm, scale_key, off_key, uv_space=uv_space)
        if li is None or lj is None:
            continue
        if uv_space:
            # wrap-aware per-component difference
            du = abs(li[0] - lj[0]); dv = abs(li[1] - lj[1])
            diffs.append(min(du, 1.0 - du) + min(dv, 1.0 - dv))
        else:
            diffs.append(abs(float(li) - float(lj)))
    return diffs


_seg_m40 = {}


def _vertex_lm(si, local_v, w3_by_m_per_seg, slots, rows, wrap, perm,
               scale_key, off_key, uv_space=False):
    W = w3_by_m_per_seg.get(si)
    if W is None:
        return None
    W = W[local_v:local_v + 1, 3]   # word 3 = packed Coord1
    m40 = _seg_m40[si]
    if perm is not None:
        m2 = perm[m40]
        s, o = slots[m2][scale_key], slots[m2][off_key]
    else:
        s, o = slots[m40][scale_key], slots[m40][off_key]
    if uv_space:
        cu, cv = w3norm(W)
        return chain_uv(cu, cv, s, o, wrap=wrap)
    lmst = stem_of(rows[m40].get("LightMap"))
    g = page_lum(lmst)
    if g is None:
        return None
    cu, cv = w3norm(W)
    pu, pv = chain_uv(cu, cv, s, o, wrap=wrap)
    return float(sample_lum(g, pu, pv)[0])


def main():
    report = {}
    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        slots = slots_of(islname)
        segs = parse_island(islname)
        m40s = m40_list(islname)
        sw = seg_words(islname)
        assert len(sw) == len(segs)
        lm_mats = [m for m in range(len(rows))
                   if rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND"]
        w3_by_m = collections.defaultdict(list)
        stride20 = []
        for si, (m40, W, st) in enumerate(sw):
            _seg_m40[si] = m40
            if W is not None and m40 in lm_mats:
                w3_by_m[m40].append(W[:, 3])   # word 3 = packed Coord1
            if st == 20:
                stride20.append(si)
        w3_by_m = {m: np.concatenate(v) for m, v in w3_by_m.items()}
        # per-segment word arrays for seam test
        w3_per_seg = {si: W for si, (m40, W, st) in enumerate(sw)
                      if W is not None and m40 in lm_mats}

        # ---------------- 1. chain alternatives: visited structure
        chains = {}
        chains["C1_shipped_s121_o145_wrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True)
        chains["C1_clamp_nowrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=False)
        chains["C2_s133_o109_wrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True,
            scale_key="s133", off_key="s109")
        chains["C3_s109_o145_wrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True,
            scale_key="s109", off_key="s145")
        chains["C4_s121_o133_wrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True,
            scale_key="s121", off_key="s133")
        chains["C5_s109_o133_wrap"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True,
            scale_key="s109", off_key="s133")
        chains["C6_identity"] = visited_structure(
            lm_mats, w3_by_m, slots, rows, wrap=True,
            scale_key="s121", off_key="s145") if False else None
        # identity: pageUV = w3 (scale 1, offset 0)
        ident = []
        npr = np.random.default_rng(9)
        for m in lm_mats:
            if m not in w3_by_m:
                continue
            lmst = stem_of(rows[m].get("LightMap"))
            g = page_lum(lmst)
            if g is None:
                continue
            cu, cv = w3norm(w3_by_m[m])
            take = min(len(cu), 8000)
            sel = npr.choice(len(cu), take, replace=False)
            vals = sample_lum(g, cu[sel], cv[sel])
            ident.append(float(vals.std()))
        chains["C6_identity"] = dict(n_mats=len(ident),
                                     lum_std=round(float(np.mean(ident)), 4),
                                     lum_std_sd=round(float(np.std(ident)), 4))
        # permuted (121,145) null
        perm_stds = []
        rng = random.Random(33)
        for k in range(K_PERM):
            keys = list(range(len(rows)))
            perm = {m: rng.choice(keys) for m in lm_mats}
            vs = visited_structure(lm_mats, w3_by_m, slots, rows, wrap=True,
                                   perm=perm)
            if vs["lum_std"] is not None:
                perm_stds.append(vs["lum_std"])
        chains["C7_permuted_(121,145)_null"] = dict(
            k=K_PERM,
            lum_std_mean=round(float(np.mean(perm_stds)), 4),
            lum_std_sd=round(float(np.std(perm_stds)), 4),
            min=round(float(np.min(perm_stds)), 4),
            max=round(float(np.max(perm_stds)), 4))

        print("-- chain alternatives (visited luminance structure):")
        for k, v in chains.items():
            print(f"   {k:32s} {v}")

        # ---------------- 2. seam continuity
        pairs = build_seam_pairs(segs, w3_per_seg)
        seam = {}
        if pairs is not None:
            print(f"   seam pairs (different materials, <{SEAM_DIST}u): "
                  f"{len(pairs[3])}")
            for tag, kw in (("value_all", dict(uv_space=False)),
                            ("value_samepage", dict(uv_space=False,
                                                    same_page_only=True)),
                            ("pageuv_samepage", dict(uv_space=True,
                                                     same_page_only=True))):
                d_auth = seam_continuity(pairs, w3_per_seg, slots, rows, **kw)
                if not d_auth:
                    seam[tag] = dict(n=0)
                    continue
                nulls = []
                for k in range(8):
                    keys = list(range(len(rows)))
                    perm = {m: rng.choice(keys) for m in lm_mats}
                    d = seam_continuity(pairs, w3_per_seg, slots, rows,
                                        perm=perm, **kw)
                    nulls.append(float(np.mean(d)))
                seam[tag] = dict(
                    n=len(d_auth),
                    authored=round(float(np.mean(d_auth)), 4),
                    authored_sd=round(float(np.std(d_auth)), 4),
                    null=round(float(np.mean(nulls)), 4),
                    null_sd=round(float(np.std(nulls)), 4),
                    null_min=round(float(np.min(nulls)), 4))
                print(f"   seam[{tag}] n={seam[tag]['n']}: authored "
                      f"{seam[tag]['authored']} vs permuted-null "
                      f"{seam[tag]['null']}±{seam[tag]['null_sd']} "
                      f"(min {seam[tag]['null_min']})")
        report_seam = seam

        # ---------------- 3. non-compact LM materials (visited extent)
        noncompact = {}
        for m in lm_mats:
            if m not in w3_by_m:
                continue
            cu, cv = w3norm(w3_by_m[m])
            s, o = slots[m]["s121"], slots[m]["s145"]
            pu = (cu * s[0] + o[0]) % 1.0
            pv = (cv * s[1] + o[1]) % 1.0
            # circular extent via sorted gaps
            def circ_extent(x):
                xs = np.sort(x)
                if len(xs) < 2:
                    return 0.0
                gaps = np.diff(xs)
                wrapgap = 1.0 - (xs[-1] - xs[0])
                return float(1.0 - max(gaps.max(), wrapgap))
            eu, ev = circ_extent(pu), circ_extent(pv)
            noncompact[m] = dict(extent_u=round(eu, 3), extent_v=round(ev, 3),
                                 area=round(eu * ev, 3),
                                 n=int(len(pu)),
                                 a121=[round(x, 5) for x in slots[m]["s121"][:2]],
                                 d145=[round(x, 5) for x in slots[m]["s145"][:2]],
                                 technique=rows[m]["technique"][:44],
                                 diffuse=stem_of(rows[m].get("DiffuseMap")),
                                 lm=stem_of(rows[m].get("LightMap")))
        nc_sorted = sorted(noncompact.items(), key=lambda kv: -kv[1]["area"])
        n_big1 = [(m, v) for m, v in nc_sorted if v["area"] > 0.30]
        report_nc = [dict(m=int(m), **v) for m, v in n_big1]
        print(f"-- non-compact LM materials (visited area > 0.30): "
              f"{len(n_big1)} of {len(noncompact)} w3-bearing LM materials")
        for m, v in n_big1[:8]:
            print(f"   m{m:3d} area={v['area']:.2f} dif={v['diffuse']} "
                  f"lm={v['lm']} a121={v['a121']}")

        # ---------------- 4. park check: 20 largest LM-bound segments
        lm_segs = [(si, m40) for si, (m40, W, st) in enumerate(sw)
                   if W is not None and m40 in lm_mats]
        lm_segs.sort(key=lambda t: -len(segs[t[0]]["pos"]))
        park = []
        for si, m40 in lm_segs[:20]:
            W = w3_per_seg[si][:, 3]
            cu, cv = w3norm(W)
            lmst = stem_of(rows[m40].get("LightMap"))
            g = page_lum(lmst)
            if g is None:
                continue
            out = dict(seg=si, m40=m40, nvert=int(len(cu)),
                       lm=lmst,
                       diffuse=stem_of(rows[m40].get("DiffuseMap")))
            # new chain
            s, o = slots[m40]["s121"], slots[m40]["s145"]
            pu, pv = chain_uv(cu, cv, s, o, wrap=True)
            vals = sample_lum(g, pu, pv)
            out["new_mean"] = round(float(vals.mean()), 4)
            out["new_std"] = round(float(vals.std()), 4)
            # old degenerate chain (s109 + o145 -> ~constant d145)
            s2, o2 = slots[m40]["s109"], slots[m40]["s145"]
            pu2, pv2 = chain_uv(cu, cv, s2, o2, wrap=True)
            vals2 = sample_lum(g, pu2, pv2)
            out["old_mean"] = round(float(vals2.mean()), 4)
            out["old_std"] = round(float(vals2.std()), 4)
            out["page_mean"] = round(float(g.mean()), 4)
            out["page_std"] = round(float(g.std()), 4)
            park.append(out)
        print("-- park check (20 largest LM-bound segments):")
        for p in park[:8]:
            print(f"   seg{p['seg']:5d} m{p['m40']:3d} n={p['nvert']:6d} "
                  f"new {p['new_mean']:.3f}±{p['new_std']:.3f}  "
                  f"old {p['old_mean']:.3f}±{p['old_std']:.3f}  "
                  f"page {p['page_mean']:.3f}±{p['page_std']:.3f}  "
                  f"dif={p['diffuse']}")

        # ---------------- 5. slot 109/133 attribute test
        a109 = np.array([slots[m]["s109"][:2] for m in range(len(rows))])
        c133 = np.array([slots[m]["s133"][:2] for m in range(len(rows))])
        tgt = 1.0 / 65535.0
        n109 = int(np.sum(np.abs(a109 - tgt) < 3e-7))
        n133_zero = int(np.sum(c133 == 0.0))
        # uv0 test: does u16*s109 beat u16/65535 on diffuse validity?
        from round5_t2_evidence import get_tex, validity_a
        uv_test = dict(n_s109_eq_dequant=n109,
                       frac=round(n109 / len(rows), 3),
                       n_s133_zero=n133_zero,
                       position_scale_rejected="positions are f32; a 1e-5 "
                       "scale would collapse them (max |pos| < 6000)")
        # sample a few segments: validity of uv0/65535 vs uv0*s109+o133
        diffs = []
        for si in range(0, len(segs), max(1, len(segs) // 40)):
            m40 = m40s[si]
            if rows[m40].get("DiffuseMap") in (None, "UNBOUND"):
                continue
            t = get_tex(stem_of(rows[m40]["DiffuseMap"]))
            if t is None or not t.ok:
                continue
            u16 = segs[si]["uvw"]
            if u16 is None or np.all(u16 == 0xFFFFFFFF):
                continue
            u = (u16 & 0xFFFF).astype(np.float32) / 65535.0
            v = (u16 >> 16).astype(np.float32) / 65535.0
            v0 = validity_a(t, u, v)
            s, o = slots[m40]["s109"][:2], slots[m40]["s133"][:2]
            uu = np.clip(u * 65535.0 * s[0] + o[0], 0, 1)
            vv = np.clip(v * 65535.0 * s[1] + o[1], 0, 1)
            v1 = validity_a(t, uu, vv)
            diffs.append(v1 - v0)
        uv_test["mean_validity_delta_s109_vs_65535"] = \
            round(float(np.mean(diffs)), 5) if diffs else None
        print(f"-- slot109/133: {n109}/{len(rows)} records have "
              f"s109 == 1/65535 (u16 dequant); o133 zeros {n133_zero}; "
              f"uv0-validity delta vs /65535: "
              f"{uv_test['mean_validity_delta_s109_vs_65535']}")

        # ---------------- 6. stride-20 building count
        b20 = [si for si in stride20
               if fam40(stem_of(rows[m40s[si]].get("DiffuseMap"))).startswith("building")]
        b24 = [si for si, (m40, W, st) in enumerate(sw)
               if st == 24 and fam40(stem_of(rows[m40].get("DiffuseMap"))).startswith("building")]
        stride_report = dict(
            stride20_total=len(stride20),
            stride20_building=len(b20),
            stride24_building=len(b24),
            note="stride-20 segments carry no Coord1 -> engine GL constant "
                 "(0,0) -> pageUV = offset only -> flat tint per material")
        print(f"-- stride-20: total {len(stride20)}, building-family "
              f"{len(b20)} (stride-24 buildings {len(b24)})")

        report[islname] = dict(chains=chains, seam=report_seam,
                               noncompact=report_nc,
                               noncompact_count=len(n_big1),
                               w3_lm_materials=len(noncompact),
                               park20=park, slot109_133=uv_test,
                               stride=stride_report)
        _page_cache.clear()

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
