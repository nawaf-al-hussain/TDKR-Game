#!/usr/bin/env python3
"""Round-4 LM-chain probe — the honest version of the session-16 chain.

The reviewer's null request exposed that the session-16 "100.0000% in-page"
was the DEGENERATE slot-109 mapping (scale ~1e-5 -> pageUV == d constant,
trivially in-page for any base).  The committed w3_coord1_test16.py with the
REAL-scale slot 121 scores only 40.9% / 36.6% in-page — the rest wraps.

This probe settles the chain with non-degenerate criteria:
  1. Tile-partition test (wrap-aware): tiles [d, d+a] over materials whose
     slot121 is a real scale. Authored tiles should partition the page with
     low mutual overlap; same-size tiles placed uniformly on the TORUS
     collide massively. Same test for slot 109 (expected: degenerate ->
     fails coverage) and slot 133 (control).
  2. Per-material visited-rect coherence on the torus (w3-derived extents).
  3. Visible-structure test: sample the bake page at per-vertex pageUVs;
     report luminance structure (std / edge energy) of the visited region
     vs page background, per candidate chain. Includes the park segment
     probe with printed texel values vs page histogram.

Outputs: extraction/re/round4_lm_probe.json + stdout.
"""
import collections
import json
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, ISLANDS, find_png  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round4_lm_probe.json"


def stem_of(dm):
    if not dm or dm == "UNBOUND":
        return None
    s = dm
    for ext in (".tga", ".png", ".jpg"):
        if s.lower().endswith(ext):
            return s[: -len(ext)]
    return s


def seg_words(island):
    """Same filter order as parse_island; returns (m40, words|None, stride)."""
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
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
        if stride is None:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        out.append((m40, words if stride == 24 else None, stride))
    return out


def torus_interval_overlap(a0, wa, b0, wb):
    """Overlap length of two intervals on a unit circle."""
    shift = (b0 - a0) % 1.0
    def iv(s):
        return max(0.0, min(wa, s + wb) - max(0.0, s))
    return iv(shift) + iv(shift - 1.0)


def tile_collisions(rects):
    """Mean fraction of each tile's area covered by any other (torus)."""
    n = len(rects)
    if n < 2:
        return 0.0
    fr = []
    for i in range(n):
        u0, v0, w, h = rects[i]
        cov = 0.0
        for j in range(n):
            if i == j:
                continue
            b = rects[j]
            ou = torus_interval_overlap(u0, w, b[0], b[2])
            ov = torus_interval_overlap(v0, h, b[1], b[3])
            cov += ou * ov
        fr.append(min(1.0, cov / max(w * h, 1e-12)))
    return float(np.mean(fr))


def main():
    report = {}
    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
        stride_b = struct.unpack_from("<I", d, 0)[0]
        M = (len(d) - 4) // stride_b
        slots = []
        for m in range(M):
            rec = d[4 + stride_b * m: 4 + stride_b * (m + 1)]
            slots.append(dict(s109=struct.unpack_from("<3f", rec, 109),
                              s121=struct.unpack_from("<3f", rec, 121),
                              s133=struct.unpack_from("<3f", rec, 133),
                              s145=struct.unpack_from("<3f", rec, 145)))
        lm_mats = [m for m in range(M)
                   if rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND"]
        sw = seg_words(islname)
        w3_by_m = collections.defaultdict(list)
        for m40, words, st in sw:
            if words is not None and m40 in lm_mats:
                w3_by_m[m40].append(words[:, 3])
        w3_cat = {m: np.concatenate(v) for m, v in w3_by_m.items() if v}

        # classify slot121 as real-scale vs not
        def is_real_scale(a):
            return 0.001 < a[0] <= 1.001 and 0.001 < a[1] <= 1.001
        n_real = sum(1 for m in lm_mats if is_real_scale(slots[m]["s121"]))
        n_real109 = sum(1 for m in lm_mats if is_real_scale(slots[m]["s109"]))
        n_real133 = sum(1 for m in lm_mats if is_real_scale(slots[m]["s133"]))
        print(f"LM materials {len(lm_mats)}; slot121 real-scale: {n_real}, "
              f"slot109: {n_real109}, slot133: {n_real133}")

        # ---------------- tile-partition test (wrap-aware)
        npr = np.random.default_rng(4416)
        part = {}
        for tag, key in (("s121", "s121"), ("s109", "s109"), ("s133", "s133")):
            rects = []
            for m in lm_mats:
                a = slots[m][key]
                dd = slots[m]["s145"]
                if not (0.0 < a[0] and 0.0 < a[1]):
                    continue
                rects.append((dd[0] % 1.0, dd[1] % 1.0, a[0], a[1]))
            if len(rects) < 5:
                part[tag] = dict(n=len(rects), note="too few")
                continue
            arr = np.array([r[2:] for r in rects])
            total_area = float(arr[:, 0].sum() * 0 + (arr[:, 0] * arr[:, 1]).sum())
            coll = tile_collisions(rects)
            nulls = []
            for _ in range(60):
                u0 = npr.uniform(0, 1, len(rects))
                v0 = npr.uniform(0, 1, len(rects))
                rs = [(u0[i], v0[i], rects[i][2], rects[i][3]) for i in range(len(rects))]
                nulls.append(tile_collisions(rs))
            part[tag] = dict(n=len(rects), total_tile_area=round(total_area, 3),
                             authored_coll=round(coll, 4),
                             null_coll=round(float(np.mean(nulls)), 4),
                             null_sd=round(float(np.std(nulls)), 4))
            print(f"  partition[{tag}]: n={len(rects)} tileArea={total_area:.2f} "
                  f"authored {coll*100:.1f}% vs null {np.mean(nulls)*100:.1f}%")
        # also: only materials with real scale AND w3 present
        rects = []
        for m in lm_mats:
            a = slots[m]["s121"]
            dd = slots[m]["s145"]
            if not is_real_scale(a) or m not in w3_cat:
                continue
            rects.append((dd[0] % 1.0, dd[1] % 1.0, a[0], a[1]))
        if len(rects) >= 5:
            coll = tile_collisions(rects)
            nulls = []
            for _ in range(60):
                u0 = npr.uniform(0, 1, len(rects))
                v0 = npr.uniform(0, 1, len(rects))
                nulls.append(tile_collisions([(u0[i], v0[i], rects[i][2],
                                               rects[i][3]) for i in range(len(rects))]))
            part["s121_realscale_w3"] = dict(n=len(rects),
                                             authored_coll=round(coll, 4),
                                             null_coll=round(float(np.mean(nulls)), 4),
                                             null_sd=round(float(np.std(nulls)), 4))
            print(f"  partition[s121 real-scale & w3]: n={len(rects)} authored "
                  f"{coll*100:.1f}% vs null {np.mean(nulls)*100:.1f}%")
        report[islname] = dict(partition=part)

        # ---------------- per-material in-page under (s121, s145) with WRAP
        # visited rect on the torus + pageUV stats per material
        per_mat = {}
        for m in sorted(w3_cat, key=lambda m: -len(w3_cat[m]))[:24]:
            W = w3_cat[m]
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            a = slots[m]["s121"]
            dd = slots[m]["s145"]
            pu = (cu * a[0] + dd[0]) % 1.0
            pv = (cv * a[1] + dd[1]) % 1.0
            take = min(len(pu), 20000)
            selp = np.random.default_rng(7).choice(len(pu), take, replace=False)
            pu, pv = pu[selp], pv[selp]
            # 2D histogram occupancy of visited UVs (64x64)
            H, _, _ = np.histogram2d(pu, pv, bins=32, range=[[0, 1], [0, 1]])
            occ = float((H > 0).sum()) / (32 * 32)
            per_mat[m] = dict(n=int(len(W)), a121=[round(x, 4) for x in a],
                              d145=[round(x, 4) for x in dd],
                              occ_cells=round(occ, 3),
                              lm=stem_of(rows[m].get("LightMap")),
                              dif=stem_of(rows[m].get("DiffuseMap")))
        report[islname]["per_material_occupancy"] = per_mat

        # ---------------- visible-structure test on the bake pages
        # for the top LM materials: sample page at pageUV (wrapped), compare
        # visited-region structure vs whole-page structure
        lm_stems = sorted({stem_of(rows[m].get("LightMap")) for m in lm_mats
                           if stem_of(rows[m].get("LightMap"))})
        page_stats = {}
        for st in lm_stems:
            png = find_png(st)
            if png is None:
                continue
            im = Image.open(png).convert("L")
            if max(im.size) > 1024:
                im = im.resize((1024, 1024), Image.BILINEAR)
            g = np.asarray(im, np.float32) / 255.0
            gx = np.zeros_like(g); gy = np.zeros_like(g)
            gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
            gy[1:-1, :] = g[2:, :] - g[:-2, :]
            page_stats[st] = dict(mean=round(float(g.mean()), 4),
                                  std=round(float(g.std()), 4),
                                  edge=round(float(np.hypot(gx, gy).mean()), 5),
                                  pcts=[round(float(x), 3) for x in
                                        np.percentile(g, [1, 25, 50, 75, 99])])
        report[islname]["page_stats"] = page_stats

        # visited-region structure per candidate chain, top materials
        def visited_structure(scale_key, base="w3"):
            out = {}
            for m in list(w3_cat)[:40]:
                W = w3_cat[m]
                cu = (W & 0xFFFF).astype(np.float32) / 65535.0
                cv = (W >> 16).astype(np.float32) / 65535.0
                a = slots[m][scale_key]
                dd = slots[m]["s145"]
                pu = (cu * a[0] + dd[0]) % 1.0
                pv = (cv * a[1] + dd[1]) % 1.0
                lmst = stem_of(rows[m].get("LightMap"))
                if lmst not in page_stats:
                    continue
                png = find_png(lmst)
                im = Image.open(png).convert("L")
                if max(im.size) > 1024:
                    im = im.resize((1024, 1024), Image.BILINEAR)
                g = np.asarray(im, np.float32) / 255.0
                take = min(len(pu), 8000)
                sel = np.random.default_rng(9).choice(len(pu), take, replace=False)
                ti = np.clip(((1.0 - pv[sel]) * 1023).astype(np.int32), 0, 1023)
                tj = np.clip((pu[sel] * 1023).astype(np.int32), 0, 1023)
                vals = g[ti, tj]
                out[m] = dict(nseg=len(W), lum_std=round(float(vals.std()), 4),
                              lum_mean=round(float(vals.mean()), 4),
                              page_std=page_stats[lmst]["std"],
                              lm=lmst)
            return out

        for tag, key in (("s109", "s109"), ("s121", "s121")):
            vs = visited_structure(key)
            stds = [v["lum_std"] for v in vs.values()]
            report[islname][f"visited_structure_{tag}"] = vs
            if stds:
                print(f"  visited-structure[{tag}]: mean lum-std "
                      f"{np.mean(stds):.4f} over {len(stds)} materials")

        # ---------------- park segment probe (the reviewer's ask)
        park = []
        for m in lm_mats:
            dif = stem_of(rows[m].get("DiffuseMap")) or ""
            if dif.startswith("GC_Park") or dif.startswith("GC_SXC"):
                park.append(m)
        probe = {}
        for m in park[:6]:
            if m not in w3_cat:
                continue
            W = w3_cat[m]
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            lmst = stem_of(rows[m].get("LightMap"))
            if lmst not in page_stats:
                continue
            png = find_png(lmst)
            im = Image.open(png).convert("L")
            full = np.asarray(im, np.float32) / 255.0
            if max(im.size) > 1024:
                im = im.resize((1024, 1024), Image.BILINEAR)
            g = np.asarray(im, np.float32) / 255.0
            for tag, key in (("s109", "s109"), ("s121", "s121")):
                a = slots[m][key]
                dd = slots[m]["s145"]
                pu = (cu * a[0] + dd[0]) % 1.0
                pv = (cv * a[1] + dd[1]) % 1.0
                take = min(len(pu), 6000)
                sel = np.random.default_rng(11).choice(len(pu), take, replace=False)
                ti = np.clip(((1.0 - pv[sel]) * (g.shape[0] - 1)).astype(np.int32), 0, g.shape[0] - 1)
                tj = np.clip((pu[sel] * (g.shape[1] - 1)).astype(np.int32), 0, g.shape[1] - 1)
                vals = g[ti, tj]
                probe[f"m{m}_{tag}"] = dict(
                    n=int(len(W)), lm=lmst, dif=stem_of(rows[m].get("DiffuseMap")),
                    a=[round(x, 5) for x in a], d=[round(x, 4) for x in dd],
                    sampled_mean=round(float(vals.mean()), 4),
                    sampled_std=round(float(vals.std()), 4),
                    sampled_pcts=[round(float(x), 4) for x in np.percentile(vals, [1, 25, 50, 75, 99])],
                    page_mean=round(float(full.mean()), 4),
                    page_pcts=[round(float(x), 4) for x in np.percentile(full, [1, 25, 50, 75, 99])])
        report[islname]["park_probe"] = probe
        for k, v in probe.items():
            print(f"  park-probe {k}: lm={v['lm']} sampled mean {v['sampled_mean']:.4f} "
                  f"std {v['sampled_std']:.4f} pcts {v['sampled_pcts']} | page mean "
                  f"{v['page_mean']:.4f} pcts {v['page_pcts']}")

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
