#!/usr/bin/env python3
"""T1 (round 13) — diffuse-channel test of the engine chain.

Engine (proven by Unicorn emulation, session 22):
    Coord0 (diffuse)  = w3_raw * s109.xy + s121.xy,  GL_REPEAT
    Coord1 (lightmap) = w4_raw * s133.xy + s145.xy,  GL_REPEAT
where (s109, s121) = pairs[slot(attr1)] = pairs[desc_index(attr1)] (scale first).

v17 shipped:
    uv0 (diffuse)  = w4 dequant (opposite word, no transform)   [export_zone16 uv_of]
    uv1 (lightmap) = frac(w3_deq * s121 + s145)                 [wrong slots, wrong word]

Tests here (diffuse channel only; the high-power test):
  E. Enrichment  : observed non-empty-texel rate / uniform-random rate on the
                   SAME diffuse texture, mask_A = alpha<64 | near-black(lum<20).
                   Per family + per material; permuted-parameter null (K=100).
  C. Atlas-cell containment : fraction of segments whose per-tile fractional
                   UV footprint lies inside ONE connected content cell of the
                   diffuse texture. Engine vs v17 vs permuted null.
  N. Counts      : materials with diffuse scale != 1 (x65535 not 1.0),
                   segments on them, per island; per-class (N,K) census.
  D. Texel density: texels per world metre under engine Coord0 vs v17
                   (worked example: 512px GC_T_Concrete_02 / m97 island 1).
"""
import json
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re/session22")
import batch_parser  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
PNG = "/home/z/my-project/work/TDKR_assets/textures_png"
ISLANDS = ("GothamCity", "GothamCity_Island2")
DEQ = 1.0 / 65535.0
NEAR_BLACK_LUM = 20.0
ALPHA_EMPTY = 64.0
rng = np.random.default_rng(20231013)

_tex_cache = {}


def stem(s):
    if not s or s == "UNBOUND":
        return None
    s = str(s)
    low = s.lower()
    for ext in (".tga", ".png", ".jpg"):
        if low.endswith(ext):
            return s[:-len(ext)]
    return s


def find_png(name):
    import os
    for a in ("l_gothamcity_tex", "commons_tex"):
        for ext in (".png", ".tga.png", ".jpg.png"):
            p = f"{PNG}/{a}/{name}{ext}"
            if os.path.exists(p):
                return p
    return None


def tex_mask(name):
    """-> (mask_A [H,W] bool True=empty, W, H). mask_A = alpha<64 | near-black."""
    if name in _tex_cache:
        return _tex_cache[name]
    p = find_png(name)
    if p is None:
        _tex_cache[name] = None
        return None
    im = Image.open(p).convert("RGBA")
    arr = np.asarray(im, np.uint8)
    a = arr[:, :, 3].astype(np.float32)
    rgb = arr[:, :, :3].astype(np.float32)
    lum = rgb.max(axis=2)  # max-channel luminance proxy
    mask_A = (a < ALPHA_EMPTY) | (lum < NEAR_BLACK_LUM)
    out = (mask_A, im.size[0], im.size[1])
    _tex_cache[name] = out
    return out


def tex_components(name):
    """-> (label [H,W] int32, n_labels) of the CONTENT mask (8-connected),
    or None if texture missing."""
    tm = tex_mask(name)
    if tm is None:
        return None
    mask_A, W, H = tm
    content = ~mask_A
    try:
        from scipy import ndimage
        lab, n = ndimage.label(content, structure=np.ones((3, 3), bool))
        return lab, n, W, H
    except ImportError:
        return None


def family_of(diffuse_name, mat_name):
    d = (diffuse_name or "").lower()
    mn = (mat_name or "").lower()
    if "billboard" in d or "billboard" in mn:
        return "billboards"
    if "props_street" in d or "props_street" in mn:
        return "props_street"
    if "rooftop" in d or "rooftop" in mn:
        return "rooftop"
    if "road" in d or "asphalt" in d or "crossing" in d or "concrete" in d:
        return "roads"
    if "sidewalk" in d or "pavement" in d or "park" in d or "grass" in d \
       or "sand" in d or "dirt" in d:
        return "ground"
    if "window" in d or "facade" in d or "building" in d or "office" in d \
       or "wall" in d or "brick" in d or "shop" in d or "store" in d:
        return "buildings"
    if "vegetation" in d or "tree" in d or "hedge" in d:
        return "vegetation"
    if "fence" in d or "barrier" in d or "traffic" in d or "sign" in d \
       or "lamp" in d or "light" in d:
        return "street_furniture"
    return "other"


def island_segments(islname):
    """(m40, w3, w4, pos) per segment, mirroring export_zone.parse_island order."""
    lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if not stride:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        w3 = words[:, 3].copy() if stride >= 16 else None
        w4 = words[:, 4].copy() if stride >= 20 else None
        pos = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, stride // 4)[:, :3]
        out.append(dict(m40=m40, w3=w3, w4=w4, pos=pos))
    return out


def sample_rate(u, v, mask_A, W, H):
    """fraction of samples NOT in mask_A (repeat wrap; gl v-flip)."""
    px = np.floor(np.mod(u, 1.0) * W).astype(np.int64) % W
    py = np.floor(np.mod(1.0 - v, 1.0) * H).astype(np.int64) % H
    inside = mask_A[py, px]
    return float(1.0 - inside.mean())


def engine_uv(w3, sc, of):
    u16 = (w3 & 0xFFFF).astype(np.float64)
    v16 = (w3 >> 16).astype(np.float64)
    return u16 * sc[0] + of[0], v16 * sc[1] + of[1]


def v17_uv(w4):
    return (w4 & 0xFFFF).astype(np.float64) * DEQ, \
           (w4 >> 16).astype(np.float64) * DEQ


def per_tile_rects(u, v, max_tiles=64):
    """Group wrapped uv samples by integer tile; per-tile fractional rect.
    Returns list of (u0, v0, u1, v1)."""
    tu = np.floor(u).astype(np.int64)
    tv = np.floor(v).astype(np.int64)
    fu = u - tu
    fv = v - tv
    keys = {}
    for a, b, c, d in zip(tu, tv, fu, fv):
        k = (int(a), int(b))
        r = keys.get(k)
        if r is None:
            keys[k] = [c, d, c, d]
        else:
            if c < r[0]:
                r[0] = c
            if d < r[1]:
                r[1] = d
            if c > r[2]:
                r[2] = c
            if d > r[3]:
                r[3] = d
    if len(keys) > max_tiles:
        return None
    return list(keys.values())


def rect_in_one_cell(rect, lab, n_lab, W, H, grid=24, content_min=0.9,
                     dom_min=0.95):
    """A fractional rect lies in one atlas cell if >=content_min of its
    interior samples are content and >=dom_min of those share one label."""
    u0, v0, u1, v1 = rect
    if u1 - u0 <= 0 or v1 - v0 <= 0:
        return False
    us = np.linspace(u0, u1, grid)
    vs = np.linspace(v0, v1, grid)
    uu, vv = np.meshgrid(us, vs)
    px = np.floor(uu * W).astype(np.int64) % W
    py = np.floor((1.0 - vv) * H).astype(np.int64) % H
    labs = lab[py, px]
    tot = labs.size
    n_content = int((labs > 0).sum())
    if n_content / tot < content_min:
        return False
    vals, cnts = np.unique(labs[labs > 0], return_counts=True)
    return float(cnts.max()) / tot >= dom_min


def main():
    result = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        recs = batch_parser.parse_island(islname)
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = island_segments(islname)
        bymat = {}
        for si, s in enumerate(segs):
            bymat.setdefault(s["m40"], []).append(si)

        # ---------- N. counts + classes ----------
        cls_seg = {}
        scale_ne1_mats = []
        diff_mats = []
        for m, rec in enumerate(recs):
            cls = (rec["n"], rec["K"])
            nseg = len(bymat.get(m, []))
            cls_seg[cls] = cls_seg.get(cls, 0) + nseg
            d = stem(rows[m].get("DiffuseMap")) if m < len(rows) else None
            if d and m in bymat:
                diff_mats.append(m)
                i0 = next((i for i, dd in enumerate(rec["descs"])
                           if dd["attr"] == 1), None)
                if i0 is not None:
                    sc = rec["pairs"][i0][0]
                    su = round(sc[0] * 65535.0, 2)
                    sv = round(sc[1] * 65535.0, 2)
                    if abs(su - 1.0) > 0.05 or abs(sv - 1.0) > 0.05:
                        scale_ne1_mats.append(m)
        seg_on_ne1 = sum(len(bymat[m]) for m in scale_ne1_mats)
        print(f"materials w/ diffuse+segments: {len(diff_mats)}; "
              f"diffuse scale != 1: {len(scale_ne1_mats)}; "
              f"segments on those: {seg_on_ne1}")
        print(f"segment (N,K) census: "
              f"{dict(sorted(((str(k), v) for k, v in cls_seg.items()), key=str))}")
        result.setdefault(islname, {})["counts"] = dict(
            diffuse_mats=len(diff_mats),
            scale_ne1_mats=len(scale_ne1_mats),
            scale_ne1_mat_ids=scale_ne1_mats[:40],
            segments_on_scale_ne1=seg_on_ne1,
            segment_classes={str(k): v for k, v in cls_seg.items()})

        # ---------- per-material uv data (engine + v17) ----------
        mat_uv = {}
        for m in diff_mats:
            rec = recs[m]
            d = stem(rows[m].get("DiffuseMap"))
            tm = tex_mask(d)
            if tm is None:
                continue
            i0 = next((i for i, dd in enumerate(rec["descs"])
                       if dd["attr"] == 1), None)
            w3s = [segs[si]["w3"] for si in bymat[m] if segs[si]["w3"] is not None]
            w4s = [segs[si]["w4"] for si in bymat[m] if segs[si]["w4"] is not None]
            if not w3s or not w4s or i0 is None:
                continue
            w3 = np.concatenate(w3s)
            w4 = np.concatenate(w4s)
            sc, of = rec["pairs"][i0]
            eu, ev = engine_uv(w3, sc, of)
            vu, vv = v17_uv(w4)
            mat_uv[m] = dict(diff=d, engine=(eu, ev), v17=(vu, vv),
                             sc=sc, of=of, segs=list(bymat[m]))

        # ---------- E. enrichment ----------
        def enrichment(mode, matmap=None):
            """pooled per-family + overall observed/uniform rates."""
            fam_num, fam_den = {}, {}
            per_mat = {}
            for m, mu in mat_uv.items():
                mm = matmap.get(m, m) if matmap else m
                src = mat_uv[mm] if (matmap and mm in mat_uv) else mu
                if mode in ("engine", "engine_from"):
                    u, v = src["engine"]
                elif mode == "v17":
                    u, v = mu["v17"]
                mask_A, W, H = tex_mask(mu["diff"])
                r = sample_rate(u, v, mask_A, W, H)
                unif = float(1.0 - mask_A.mean())
                fam = family_of(mu["diff"], rows[m].get("name"))
                per_mat[m] = dict(obs=r, unif=unif,
                                  enr=(r / unif if unif > 0 else None))
                fam_num[fam] = fam_num.get(fam, 0.0) + r * len(u)
                fam_den[fam] = fam_den.get(fam, 0.0) + unif * len(u)
            fam_enr = {f: (fam_num[f] / fam_den[f] if fam_den[f] else None)
                       for f in fam_num}
            return fam_enr, per_mat

        fam_eng, per_eng = enrichment("engine")
        fam_v17, per_v17 = enrichment("v17")

        # null: permute engine params across materials (K=100)
        mats = list(mat_uv)
        NS = 100
        eng_null_fixed = None  # sanity: own-param enrichment must equal observed
        null_fam = {}
        for pi in range(NS):
            perm = rng.permutation(len(mats))
            matmap = {mats[i]: mats[perm[i]] for i in range(len(mats))}
            fam_n, _ = enrichment("engine", matmap=matmap)
            for f, e in fam_n.items():
                if e is not None:
                    null_fam.setdefault(f, []).append(e)
        print("\n-- E. diffuse enrichment (obs/uniform, pooled per family)")
        print(f"   {'family':18s} {'engine':>8s} {'v17':>8s} "
              f"{'null':>14s} {'z_eng':>7s} {'z_v17':>7s} n_mats")
        erows = {}
        for f in sorted(set(fam_eng) | set(fam_v17)):
            e1, e2 = fam_eng.get(f), fam_v17.get(f)
            nl = null_fam.get(f, [])
            if len(nl) > 1 and np.std(nl) > 0:
                mu_, sd_ = float(np.mean(nl)), float(np.std(nl))
                z1 = (e1 - mu_) / sd_ if e1 is not None else None
                z2 = (e2 - mu_) / sd_ if e2 is not None else None
                nline = f"{mu_:7.3f}+/-{sd_:5.3f}"
            else:
                mu_ = float(np.mean(nl)) if nl else float("nan")
                z1 = z2 = None
                nline = f"{mu_:7.3f}+/-0.000" if nl else "            -"
            nm = sum(1 for m in mats
                     if family_of(mat_uv[m]["diff"], rows[m].get("name")) == f)
            print(f"   {f:18s} "
                  f"{(e1 if e1 is not None else float('nan')):8.3f} "
                  f"{(e2 if e2 is not None else float('nan')):8.3f} "
                  f"{nline:>14s} "
                  f"{('%7.2f' % z1) if z1 is not None else '     nc'} "
                  f"{('%7.2f' % z2) if z2 is not None else '     nc'} {nm}")
            erows[f] = dict(engine=e1, v17=e2, null=(mu_ if nl else None),
                            null_sd=(float(np.std(nl)) if nl else None),
                            z_engine=z1, z_v17=z2, n_materials=nm)
        result.setdefault(islname, {})["enrichment"] = erows
        result[islname]["enrichment_per_material"] = {
            m: per_eng[m] for m in per_eng}

        # ---------- C. atlas-cell containment (per segment) ----------
        lab_cache = {}
        print("\n-- C. atlas-cell containment per segment")
        cell = dict(engine=[], v17=[])
        rect_stats = dict(engine_area=[], v17_area=[], engine_tiles=[])
        seg_fam_engine = {}
        for m, mu in mat_uv.items():
            lab3 = tex_components(mu["diff"])
            if lab3 is None:
                continue
            lab, n_lab, W, H = lab3
            mask_A, W, H = tex_mask(mu["diff"])
            fam = family_of(mu["diff"], rows[m].get("name"))
            for si in mu["segs"]:
                s = segs[si]
                if s["w3"] is None or s["w4"] is None:
                    continue
                # engine: per-tile fractional rects
                i0 = next((i for i, dd in enumerate(recs[m]["descs"])
                           if dd["attr"] == 1), None)
                sc, of = recs[m]["pairs"][i0]
                eu, ev = engine_uv(s["w3"], sc, of)
                rects = per_tile_rects(eu, ev)
                if rects is not None and len(rects) >= 1:
                    ok = all(rect_in_one_cell(r, lab, n_lab, W, H)
                             for r in rects)
                    cell["engine"].append((ok, fam, m, si))
                    seg_fam_engine[si] = fam
                    for r in rects[:8]:
                        rect_stats["engine_area"].append(
                            max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1]))
                    rect_stats["engine_tiles"].append(len(rects))
                # v17: single rect (dequant, already in [0,1))
                vu, vv = v17_uv(s["w4"])
                rv = (float(vu.min()), float(vv.min()),
                      float(vu.max()), float(vv.max()))
                ok2 = rect_in_one_cell(rv, lab, n_lab, W, H)
                cell["v17"].append((ok2, fam, m, si))
                rect_stats["v17_area"].append(
                    max(0.0, rv[2] - rv[0]) * max(0.0, rv[3] - rv[1]))
        for mode in ("engine", "v17"):
            arr = cell[mode]
            if not arr:
                continue
            oks = [a for a, *_ in arr]
            print(f"   {mode:7s}: {sum(oks)}/{len(oks)} = "
                  f"{sum(oks)/len(oks):.3f} segments in one cell")
        print(f"   rect area: engine median {np.median(rect_stats['engine_area']):.4f} "
              f"p90 {np.percentile(rect_stats['engine_area'], 90):.4f} | "
              f"v17 median {np.median(rect_stats['v17_area']):.4f} "
              f"p90 {np.percentile(rect_stats['v17_area'], 90):.4f}")
        print(f"   engine tiles/segment: median "
              f"{np.median(rect_stats['engine_tiles']):.0f} "
              f"p90 {np.percentile(rect_stats['engine_tiles'], 90):.0f}")
        # null: permuted params, engine pipeline
        NS3 = 40
        null_cell = []
        mats2 = [m for m in mats
                 if tex_components(mat_uv[m]["diff"]) is not None]
        pairpool = {}
        for m in mats2:
            i0 = next((i for i, dd in enumerate(recs[m]["descs"])
                       if dd["attr"] == 1), None)
            pairpool[m] = recs[m]["pairs"][i0]
        for pi in range(NS3):
            perm = rng.permutation(len(mats2))
            pmap = {mats2[i]: pairpool[mats2[perm[i]]] for i in range(len(mats2))}
            oks = tot = 0
            for m in mats2:
                lab, n_lab, W, H = tex_components(mat_uv[m]["diff"])
                sc, of = pmap[m]
                for si in mat_uv[m]["segs"]:
                    s = segs[si]
                    if s["w3"] is None:
                        continue
                    eu, ev = engine_uv(s["w3"], sc, of)
                    rects = per_tile_rects(eu, ev)
                    if rects is None:
                        continue
                    tot += 1
                    if all(rect_in_one_cell(r, lab, n_lab, W, H) for r in rects):
                        oks += 1
            if tot:
                null_cell.append(oks / tot)
        if len(null_cell) > 1 and np.std(null_cell) > 0:
            mu_, sd_ = float(np.mean(null_cell)), float(np.std(null_cell))
            obs_eng = (sum(a for a, *_ in cell["engine"]) / len(cell["engine"])
                       if cell["engine"] else None)
            z = (obs_eng - mu_) / sd_ if obs_eng is not None else None
            print(f"   engine null: {mu_:.3f}+/-{sd_:.3f} "
                  f"(z={'nc' if z is None else round(z, 2)})")
        else:
            mu_, sd_, z = (float(np.mean(null_cell)) if null_cell else None,
                           0.0, None)
            print(f"   engine null: {mu_}+/-0.0 z=not computable")
        result.setdefault(islname, {})["cell_containment"] = dict(
            engine=dict(ok=sum(a for a, *_ in cell["engine"]),
                        tot=len(cell["engine"])),
            v17=dict(ok=sum(a for a, *_ in cell["v17"]),
                     tot=len(cell["v17"])),
            rect_area_median_engine=float(np.median(rect_stats["engine_area"])),
            rect_area_median_v17=float(np.median(rect_stats["v17_area"])),
            engine_tiles_median=float(np.median(rect_stats["engine_tiles"])),
            null=(mu_, sd_, z))

        # ---------- D. texel density ----------
        print("\n-- D. texel density (texels per world metre)")
        dens = dict(engine={}, v17={})
        for m, mu in mat_uv.items():
            mask_A, W, H = tex_mask(mu["diff"])
            i0 = next((i for i, dd in enumerate(recs[m]["descs"])
                       if dd["attr"] == 1), None)
            sc, of = recs[m]["pairs"][i0]
            for si in mu["segs"]:
                s = segs[si]
                if s["w3"] is None or s["w4"] is None:
                    continue
                pos = s["pos"]
                wx = float(np.ptp(pos[:, 0]))
                wz = float(np.ptp(pos[:, 2]))
                wspan = max(wx, wz, 1e-6)
                eu, ev = engine_uv(s["w3"], sc, of)
                vu, vv = v17_uv(s["w4"])
                de = (float(np.ptp(eu)) * W) / wspan
                dv = (float(vu.max() - vu.min()) * W) / wspan
                fam = family_of(mu["diff"], rows[m].get("name"))
                dens["engine"].setdefault(fam, []).append(de)
                dens["v17"].setdefault(fam, []).append(dv)
        for fam in sorted(set(dens["engine"]) | set(dens["v17"])):
            e = dens["engine"].get(fam, [])
            v = dens["v17"].get(fam, [])
            print(f"   {fam:18s}: engine median {np.median(e):9.1f} "
                  f"texel-u/m  (n={len(e)})   v17 median {np.median(v):9.1f} "
                  f"(n={len(v)})")
        result.setdefault(islname, {})["density"] = {
            fam: dict(engine_median=float(np.median(v)) if len(v) else None,
                      v17_median=float(np.median(dens["v17"][fam]))
                      if len(dens["v17"].get(fam, [])) else None,
                      n=len(v))
            for fam, v in dens["engine"].items()}

    class NpEnc(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, np.floating):
                return float(o)
            return super().default(o)

    json.dump(result, open("/home/z/my-project/work/t1_diffuse_results.json",
                           "w"), indent=1, cls=NpEnc)
    print("\nwrote /home/z/my-project/work/t1_diffuse_results.json")


if __name__ == "__main__":
    main()
