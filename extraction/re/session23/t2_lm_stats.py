#!/usr/bin/env python3
"""T2 — numeric lightmap statistics, v17 chain vs engine chain.

For every lm-bound street segment (Diffuse + LightMap + TexCoord1 present):
  v17 chain   : uv1 = frac(w3_deq * s121 + s145)          (what v17 ships)
  engine chain: uv1 = (w4_u16 * s133.xy + s145.xy) mod 1  (engine-true)
Sample the island bake page at those uvs (v-flip like the viewer) and report
mean / std / near-black fraction of sampled luminance, pooled per family and
per island. No browser needed.
"""
import json
import os
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re/session22")
sys.path.insert(0, "/home/z/my-project/scripts")
import batch_parser  # noqa
from export_zone16 import stem, m40_and_w3, batch_groups  # noqa
from t1_diffuse import island_segments, family_of  # noqa

RE = "/home/z/my-project/repo/extraction/re"
PNG = "/home/z/my-project/work/TDKR_assets/textures_png"
DEQ = 1.0 / 65535.0

_lmc = {}


def find_lm(name):
    for a in ("l_gothamcity_tex", "commons_tex"):
        for ext in (".png", ".tga.png"):
            p = f"{PNG}/{a}/{name}{ext}"
            if os.path.exists(p):
                return p
    return None


def lm_gray(name):
    if name in _lmc:
        return _lmc[name]
    p = find_lm(name)
    if p is None:
        _lmc[name] = None
        return None
    im = Image.open(p).convert("RGB")
    g = np.asarray(im, np.float32).mean(axis=2)  # H,W luminance
    _lmc[name] = (g, im.size[0], im.size[1])
    return _lmc[name]


def sample_stats(u, v, g, W, H):
    px = np.floor(np.mod(u, 1.0) * W).astype(np.int64) % W
    py = np.floor(np.mod(1.0 - v, 1.0) * H).astype(np.int64) % H
    lum = g[py, px]
    return dict(mean=float(lum.mean()), std=float(lum.std()),
                nearblack=float((lum < 20.0).mean()))


def main():
    out = {}
    for islname in ("GothamCity", "GothamCity_Island2"):
        recs = batch_parser.parse_island(islname)
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        groups = batch_groups(islname)
        segs = island_segments(islname)
        m40w3 = m40_and_w3(islname)
        assert len(segs) == len(m40w3)
        fam_acc = {}
        tot = dict(v17=[0.0, 0.0, 0.0, 0], eng=[0.0, 0.0, 0.0, 0])
        nseg = 0
        for s, (m, w3) in zip(segs, m40w3):
            if w3 is None or s["w4"] is None or m >= len(rows):
                continue
            lm = stem(rows[m].get("LightMap"))
            dif = stem(rows[m].get("DiffuseMap"))
            if not lm:
                continue
            g = lm_gray(lm)
            if g is None:
                continue
            g, W, H = g
            rec = recs[m]
            i1 = next((i for i, dd in enumerate(rec["descs"])
                       if dd["attr"] == 2), None)
            if i1 is None:
                continue
            # v17 chain (what the exporter ships today)
            a, dd = groups[m] if m < len(groups) else ((0, 0, 0), (0, 0, 0))
            cu = (w3 & 0xFFFF).astype(np.float64) * DEQ
            cv = (w3 >> 16).astype(np.float64) * DEQ
            u17 = np.mod(cu * a[0] + dd[0], 1.0)
            v17_ = np.mod(cv * a[1] + dd[1], 1.0)
            # engine chain
            sc1, of1 = rec["pairs"][i1]
            w4 = s["w4"]
            uen = np.mod((w4 & 0xFFFF).astype(np.float64) * sc1[0] + of1[0], 1.0)
            ven = np.mod((w4 >> 16).astype(np.float64) * sc1[1] + of1[1], 1.0)
            s17 = sample_stats(u17, v17_, g, W, H)
            sen = sample_stats(uen, ven, g, W, H)
            fam = family_of(dif, rows[m].get("name")) if dif else "bakealone"
            fa = fam_acc.setdefault(fam, dict(v17=[0.0, 0.0, 0.0, 0],
                                              eng=[0.0, 0.0, 0.0, 0]))
            nv = len(w3)
            for key, st in (("v17", s17), ("eng", sen)):
                acc = fa[key]
                acc[0] += st["mean"] * nv
                acc[1] += st["std"] * nv
                acc[2] += st["nearblack"] * nv
                acc[3] += nv
                t = tot[key]
                t[0] += st["mean"] * nv
                t[1] += st["std"] * nv
                t[2] += st["nearblack"] * nv
                t[3] += nv
            nseg += 1
        print(f"\n### {islname} — lightmap sample stats ({nseg} lm-bound segs)")
        print(f"   {'family':16s} {'v17 mean':>9s} {'eng mean':>9s} "
              f"{'v17 std':>8s} {'eng std':>8s} {'v17 nb':>7s} {'eng nb':>7s} "
              f"{'nvert':>8s}")
        fo = {}
        for fam, fa in sorted(fam_acc.items()):
            r = {}
            for key, lab in (("v17", "v17"), ("eng", "engine")):
                a = fa[key]
                r[lab] = dict(mean=a[0] / a[3], std=a[1] / a[3],
                              nearblack=a[2] / a[3]) if a[3] else None
            print(f"   {fam:16s} {r['v17']['mean']:9.3f} {r['engine']['mean']:9.3f} "
                  f"{r['v17']['std']:8.3f} {r['engine']['std']:8.3f} "
                  f"{r['v17']['nearblack']:7.3f} {r['engine']['nearblack']:7.3f} "
                  f"{fa['v17'][3]:8d}")
            fo[fam] = r
        t = {("v17" if k == "v17" else "engine"):
             dict(mean=v[0] / v[3], std=v[1] / v[3], nearblack=v[2] / v[3],
                  nverts=v[3]) for k, v in tot.items()}
        print(f"   {'TOTAL':16s} {t['v17']['mean']:9.3f} {t['engine']['mean']:9.3f} "
              f"{t['v17']['std']:8.3f} {t['engine']['std']:8.3f} "
              f"{t['v17']['nearblack']:7.3f} {t['engine']['nearblack']:7.3f} "
              f"{t['v17']['nverts']:8d}")
        out[islname] = dict(families=fo, total=t, lm_segments=nseg)
    json.dump(out, open("/home/z/my-project/work/t2_lm_stats.json", "w"),
              indent=1)
    print("\nwrote /home/z/my-project/work/t2_lm_stats.json")


if __name__ == "__main__":
    main()
