#!/usr/bin/env python3
"""Session 16 DECISIVE PROBE: render individual segments textured by their
+40 material's DiffuseMap (runtime table) vs the exporter's v5 choice.

If +40's texture shows coherent content under the segment's raw UVs, the
engine binding is right and v5 was self-fulfilling. Renders XY-projected,
UV-sampled triangles per segment into PNG cards.
"""
import json
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, bind_segment, cross_sections, ISLANDS, uv_of  # noqa
from tex_bind import find_png  # noqa

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
OUT = "/home/z/my-project/work/probe16"


def m40_list(island):
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
        ok = False
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    ok = True
                    break
        if not ok:
            continue
        out.append(struct.unpack_from("<I", ld, off + 40)[0])
    return out


def render_segment(seg, tex_name, out_png, px_per_u=8, pad=2):
    png = find_png(tex_name)
    if png is None:
        return False
    tex = Image.open(png).convert("RGB")
    tw, th = tex.size
    tarr = np.asarray(tex, np.uint8)

    p = seg["pos"][:, :2]   # XY top-down
    u, v = uv_of(seg)
    idx = seg["idx"].astype(np.int64)
    tris = idx.reshape(-1, 3)
    # drop degenerate
    good = (tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) & (tris[:, 0] != tris[:, 2])
    tris = tris[good]

    mn = p.min(0) - pad
    mx = p.max(0) + pad
    W = max(int((mx[0] - mn[0]) * px_per_u), 8)
    H = max(int((mx[1] - mn[1]) * px_per_u), 8)
    if W * H > 40e6:
        scale = (40e6 / (W * H)) ** 0.5
        W, H = int(W * scale), int(H * scale)
        px = min(px_per_u, 1)
    img = np.zeros((H, W, 3), np.uint8)
    img[:] = (28, 26, 30)

    # rasterize by barycentric sampling on triangle bboxes
    xy = (p - mn) * (np.array([W / (mx[0] - mn[0]), H / (mx[1] - mn[1])]))
    for t in tris:
        a, b, c = xy[t[0]], xy[t[1]], xy[t[2]]
        x0 = max(int(min(a[0], b[0], c[0])), 0)
        x1 = min(int(max(a[0], b[0], c[0])) + 1, W - 1)
        y0 = max(int(min(a[1], b[1], c[1])), 0)
        y1 = min(int(max(a[1], b[1], c[1])) + 1, H - 1)
        if x1 < x0 or y1 < y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5,
                             np.arange(y0, y1 + 1) + 0.5)
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-9:
            continue
        w0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
        w1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
        w2 = 1 - w0 - w1
        inside = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
        if not inside.any():
            continue
        uu = np.clip(w0 * u[t[0]] + w1 * u[t[1]] + w2 * u[t[2]], 0, 1)
        vv = np.clip(w0 * v[t[0]] + w1 * v[t[1]] + w2 * v[t[2]], 0, 1)
        # game UVs bottom-origin, PVR top-down storage: row = (1-v)
        ti = ((1 - vv) * (th - 1)).astype(np.int32)
        tj = (uu * (tw - 1)).astype(np.int32)
        img[ys[inside].astype(int), xs[inside].astype(int)] = \
            tarr[ti[inside], tj[inside]]
    Image.fromarray(img).save(out_png)
    return True


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    XSECS = {
        "GothamCity_Road_v1_Island_1": cross_sections("GothamCity_Road_v1_Island_1"),
        "GothamCity_Road_v2_Island_1": cross_sections("GothamCity_Road_v2_Island_1"),
        "GothamCity_Road_Island_2": cross_sections("GothamCity_Road_Island_2"),
        "gothamcity_roads_details": cross_sections("gothamcity_roads_details"),
        "GothamCity_Road_Crossings_Island_1": cross_sections("GothamCity_Road_Crossings_Island_1"),
        "GothamCity_Road_Crossings_Island_2": cross_sections("GothamCity_Road_Crossings_Island_2"),
    }
    isl, isl_d = ISLANDS["GothamCity"], ISLANDS["GothamCity"]["isl"]
    xs = {k: v for k, v in XSECS.items() if "Island_1" in k or "details" in k}
    rows = json.load(open(f"{RE}/runtime_mats_GothamCity.json"))
    segs = parse_island("GothamCity")
    m40s = m40_list("GothamCity")
    assert len(segs) == len(m40s)

    # pick segments: from m74 (trunk), m11 (props street), m13 (rooftop),
    # m300 (billboard), plus an exporter-road and an exporter-flat
    picks = []
    seen_m = {}
    for i, (s, m) in enumerate(zip(segs, m40s)):
        seen_m.setdefault(m, []).append(i)
    for m in (74, 11, 13, 300, 90, 178):
        if m in seen_m:
            picks.append(("m%d" % m, seen_m[m][len(seen_m[m]) // 2]))
    # exporter-road example
    for i, s in enumerate(segs):
        tex, _ = bind_segment(s, isl, xs)
        if tex == "GothamCity_Road_v1_Island_1":
            picks.append(("exp_road", i))
            break
    for i, s in enumerate(segs):
        tex, _ = bind_segment(s, isl, xs)
        if tex == "GC_Park_grass":
            picks.append(("exp_grass", i))
            break

    report = []
    for tag, i in picks:
        s = segs[i]
        m = m40s[i]
        rt = rows[m]
        exp_tex, _ = bind_segment(s, isl, xs)
        p = s["pos"]
        info = dict(tag=tag, seg=i, m40=m, rt_dif=rt["DiffuseMap"],
                    rt_lm=rt["LightMap"], rt_tech=rt["technique"],
                    exp=exp_tex,
                    dim=round(float(np.ptp(p[:, :2]).max()), 1),
                    zr=round(float(np.ptp(p[:, 2])), 1),
                    zmean=round(float(p[:, 2].mean()), 1),
                    nverts=int(len(s["pos"])))
        print(info)
        report.append(info)
        if rt["DiffuseMap"]:
            render_segment(s, rt["DiffuseMap"].replace(".tga", ""),
                           f"{OUT}/seg{i}_m{m}_plus40.png")
        if exp_tex:
            render_segment(s, exp_tex, f"{OUT}/seg{i}_m{m}_exp_{exp_tex[:20]}.png")
    json.dump(report, open(f"{OUT}/probe16_report.json", "w"), indent=1)
    print(f"\nrenders in {OUT}")


if __name__ == "__main__":
    main()
