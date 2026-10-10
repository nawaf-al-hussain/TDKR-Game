#!/usr/bin/env python3
"""Round-4 before/after: one near-tier building block under three bindings.

  v15   : v5 band-atlas structural binding (dark fallback for buildings)
  v16.0 : +40 diffuse x flat-d lightmap x 2   (what is deployed now)
  v16.1 : +40 diffuse x (w3*s121+s145 wrapped) lightmap x 2

Also renders the LIGHTMAP CHANNEL alone for v16.0 vs v16.1 and a composite
card row.  Output: /home/z/my-project/work/round4_ba/*.png + report json.
"""
import collections
import json
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import (parse_island, bind_segment, cross_sections,  # noqa
                         ISLANDS, uv_of, find_png, strip_to_tris)

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = "/home/z/my-project/work/round4_ba"


def stem_of(dm):
    if not dm or dm == "UNBOUND":
        return None
    s = dm
    for ext in (".tga", ".png", ".jpg"):
        if s.lower().endswith(ext):
            return s[: -len(ext)]
    return s


def m40_w3(island):
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
        if not stride:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        w3 = None
        if stride == 24:
            w3 = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, 6)[:, 3].copy()
        out.append((m40, w3))
    return out


_tex = {}


def tex_rgb(stem):
    if stem not in _tex:
        png = find_png(stem)
        if png is None:
            _tex[stem] = None
        else:
            im = Image.open(png).convert("RGB")
            if max(im.size) > 1024:
                im = im.resize((1024, 1024), Image.BILINEAR)
            a = np.asarray(im, np.float32) / 255.0
            _tex[stem] = (a, im.size[0], im.size[1])
    return _tex[stem]


def sample(tex, u, v):
    a, w, h = tex
    tj = np.clip((u * (w - 1)).astype(np.int32), 0, w - 1)
    ti = np.clip(((1.0 - v) * (h - 1)).astype(np.int32), 0, h - 1)
    return a[ti, tj]


def render_block(segs, binds, box, out_png, px_per_u=3.5, lm_only=False,
                 gain=1.0):
    """binds: list per seg of dict(tex=, lm=, lmuv=(u,v)|None, mode=)."""
    x0, y0, x1, y1 = box
    W = int((x1 - x0) * px_per_u)
    H = int((y1 - y0) * px_per_u)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = (0.02, 0.02, 0.03)
    covered = np.zeros((H, W), bool)
    for s, b in zip(segs, binds):
        # clip test
        p = s["pos"]
        if p[:, 0].max() < x0 or p[:, 0].min() > x1 \
                or p[:, 1].max() < y0 or p[:, 1].min() > y1:
            continue
        tris = np.asarray(strip_to_tris(s["idx"]), np.int64).reshape(-1, 3)
        good = (tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) \
            & (tris[:, 0] != tris[:, 2])
        tris = tris[good]
        if not len(tris):
            continue
        xy = p[:, :2]
        u, v = uv_of(s)
        u = u.astype(np.float32)
        v = v.astype(np.float32)
        lmuv = b.get("lmuv")
        tex = tex_rgb(b["tex"]) if b["tex"] else None
        lmtex = tex_rgb(b["lm"]) if b["lm"] else None
        for t in tris:
            ax, ay = xy[t[0], 0], xy[t[0], 1]
            bx, by = xy[t[1], 0], xy[t[1], 1]
            cx, cy = xy[t[2], 0], xy[t[2], 1]
            gx0 = max(int((min(ax, bx, cx) - x0) * px_per_u), 0)
            gx1 = min(int((max(ax, bx, cx) - x0) * px_per_u) + 1, W - 1)
            gy0 = max(int((min(ay, by, cy) - y0) * px_per_u), 0)
            gy1 = min(int((max(ay, by, cy) - y0) * px_per_u) + 1, H - 1)
            if gx1 < gx0 or gy1 < gy0:
                continue
            xs = np.arange(gx0, gx1 + 1) + 0.5
            ys = np.arange(gy0, gy1 + 1) + 0.5
            PX, PY = np.meshgrid(xs, ys)
            wx = x0 + PX / px_per_u
            wy = y0 + PY / px_per_u
            d = (bx - cx) * (ay - cy) + (cx - ax) * (by - cy)
            if abs(d) < 1e-9:
                continue
            w0 = ((bx - cx) * (wx - cx) + (cx - ax) * (wy - cy)) / d
            w1 = ((cx - ax) * (wx - cx) + (ax - bx) * (wy - cy)) / d
            w2 = 1 - w0 - w1
            inside = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
            if not inside.any():
                continue
            uu = np.clip(w0 * u[t[0]] + w1 * u[t[1]] + w2 * u[t[2]], 0, 1)
            vv = np.clip(w0 * v[t[0]] + w1 * v[t[1]] + w2 * v[t[2]], 0, 1)
            # per-pixel lightmap UV
            if lmuv is not None and hasattr(lmuv[0], "shape") and lmuv[0].ndim:
                lmu = w0 * lmuv[0][t[0]] + w1 * lmuv[0][t[1]] + w2 * lmuv[0][t[2]]
                lmv_ = w0 * lmuv[1][t[0]] + w1 * lmuv[1][t[1]] + w2 * lmuv[1][t[2]]
            elif lmuv is not None:
                lmu = np.full(PX.shape, float(lmuv[0]), np.float32)
                lmv_ = np.full(PX.shape, float(lmuv[1]), np.float32)
            else:
                lmu = lmv_ = None
            if lm_only:
                if lmtex is None or lmu is None:
                    col = np.zeros(PX.shape + (3,), np.float32) \
                        + np.array([0.3, 0.05, 0.05])
                else:
                    col = sample(lmtex, lmu, lmv_).mean(axis=-1, keepdims=True)
                    col = np.repeat(col, 3, axis=-1)
                sub = img[gy0:gy1 + 1, gx0:gx1 + 1]
                sub[inside] = np.clip(col, 0, 1)[inside]
            else:
                if tex is None:
                    col = np.zeros(PX.shape + (3,), np.float32) \
                        + np.array([0.055, 0.07, 0.10])
                else:
                    col = sample(tex, uu, vv)
                if lmtex is not None and lmu is not None:
                    lmvv = sample(lmtex, lmu, lmv_)
                    col = col * lmvv * 2.0
                sub = img[gy0:gy1 + 1, gx0:gx1 + 1]
                sub[inside] = np.clip(col, 0, 1)[inside]
            covered[gy0:gy1 + 1, gx0:gx1 + 1][inside] = True
    Image.fromarray((np.clip(img * gain, 0, 1) * 255).astype(np.uint8)).save(out_png)
    return float(covered.mean())


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    islname = "GothamCity"
    isl = ISLANDS[islname]
    rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride_b = struct.unpack_from("<I", d, 0)[0]
    slots = []
    for m in range((len(d) - 4) // stride_b):
        rec = d[4 + stride_b * m: 4 + stride_b * (m + 1)]
        slots.append((struct.unpack_from("<3f", rec, 121),
                      struct.unpack_from("<3f", rec, 145)))
    segs = parse_island(islname)
    m40w3 = m40_w3(islname)
    assert len(segs) == len(m40w3)

    def building_dif(m):
        st = stem_of(rows[m].get("DiffuseMap")) or ""
        return st.startswith(("GC_Footprint", "GC_footprint", "GC_Residential_BD",
                              "GC_Z1_Shops", "GC_Cath", "GC_SXC_Atlas",
                              "GC_Walls", "GC_CBCE", "GC_DMUS", "GC_Glass",
                              "GC_Park_atlas"))

    # pick the densest 160x160 box of building VERTICES
    cand = [i for i, (m, _) in enumerate(m40w3) if building_dif(m)]
    allxy = np.concatenate([segs[i]["pos"][:, :2] for i in cand])
    xs, ys = allxy[:, 0], allxy[:, 1]
    best, bestc = None, -1
    for gx in np.arange(xs.min(), xs.max(), 80):
        for gy in np.arange(ys.min(), ys.max(), 80):
            c = int(((xs >= gx) & (xs < gx + 160) & (ys >= gy) & (ys < gy + 160)).sum())
            if c > bestc:
                bestc, best = c, (gx, gy)
    x0, y0 = float(best[0]), float(best[1])
    box = (x0, y0, x0 + 160.0, y0 + 160.0)
    idxs = [i for i in cand
            if segs[i]["pos"][:, 0].max() >= box[0]
            and segs[i]["pos"][:, 0].min() <= box[2]
            and segs[i]["pos"][:, 1].max() >= box[1]
            and segs[i]["pos"][:, 1].min() <= box[3]]
    print(f"block box {box}: {len(idxs)} building segments")

    XSECS = {k: cross_sections(k) for k in (
        "GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
        "gothamcity_roads_details", "GothamCity_Road_Crossings_Island_1")}
    block = [segs[i] for i in idxs]

    # v15 binding (v5 structural)
    binds15 = []
    for s in block:
        t, _ = bind_segment(s, isl, XSECS)
        binds15.append(dict(tex=t, lm=None, lmuv=None))
    # v16.0 (+40 dif, flat d LM) and v16.1 (w3*s121+s145 wrapped)
    binds160, binds161, lmonly160, lmonly161 = [], [], [], []
    for i, s in zip(idxs, block):
        m, w3 = m40w3[i]
        row = rows[m]
        tex = stem_of(row.get("DiffuseMap"))
        lm = stem_of(row.get("LightMap"))
        a, dd = slots[m] if m < len(slots) else ((0, 0, 0), (0, 0, 0))
        if w3 is not None and lm:
            cu = (w3 & 0xFFFF).astype(np.float32) / 65535.0
            cv = (w3 >> 16).astype(np.float32) / 65535.0
            # v16.1 chain (scale @121, offset @145), wrapped
            pu = (cu * a[0] + dd[0]) % 1.0
            pv = (cv * a[1] + dd[1]) % 1.0
            uv161 = (pu, pv)
            uv160 = (float(dd[0] % 1.0), float(dd[1] % 1.0))
        else:
            uv161 = None
            uv160 = None
        binds160.append(dict(tex=tex, lm=lm, lmuv=uv160))
        binds161.append(dict(tex=tex, lm=lm, lmuv=uv161))
        lmonly160.append(dict(tex=None, lm=lm, lmuv=uv160))
        lmonly161.append(dict(tex=None, lm=lm, lmuv=uv161))

    tag = f"block_{int(x0)}_{int(y0)}"
    cov = {}
    cov["v15"] = render_block(block, binds15, box, f"{OUT}/{tag}_v15.png")
    cov["v16_flatlm"] = render_block(block, binds160, box, f"{OUT}/{tag}_v16_flatlm.png")
    cov["v16_1_realuv"] = render_block(block, binds161, box, f"{OUT}/{tag}_v16p1_realuv.png")
    render_block(block, lmonly160, box, f"{OUT}/{tag}_lmCHANNEL_v16flat.png",
                 lm_only=True)
    render_block(block, lmonly161, box, f"{OUT}/{tag}_lmCHANNEL_v16p1.png",
                 lm_only=True)
    # legibility variants (x3 gain, labelled)
    render_block(block, binds15, box, f"{OUT}/{tag}_v15_gain3.png", gain=3.0)
    render_block(block, binds160, box, f"{OUT}/{tag}_v16_flatlm_gain3.png", gain=3.0)
    render_block(block, binds161, box, f"{OUT}/{tag}_v16p1_realuv_gain3.png", gain=3.0)
    print("coverage:", {k: round(v, 3) for k, v in cov.items()})

    # side-by-side card (gain3 for legibility; raw files also banked)
    ims = [Image.open(f"{OUT}/{tag}_{n}.png") for n in
           ("v15_gain3", "v16_flatlm_gain3", "v16p1_realuv_gain3")]
    w = sum(im.width for im in ims) + 40
    h = max(im.height for im in ims) + 30
    card = Image.new("RGB", (w, h), (24, 24, 28))
    xo = 10
    for im in ims:
        card.paste(im, (xo, 20))
        xo += im.width + 10
    card.save(f"{OUT}/{tag}_CARD.png")

    # material census of the block
    mats = collections.Counter()
    for i in idxs:
        m, _ = m40w3[i]
        mats[f"m{m}:{stem_of(rows[m].get('DiffuseMap'))}"] += 1
    rep = dict(box=list(box), n_seg=len(idxs), coverage=cov,
               materials=dict(mats.most_common(12)))
    json.dump(rep, open(f"{OUT}/{tag}_report.json", "w"), indent=1)
    print(json.dumps(rep, indent=1)[:900])


if __name__ == "__main__":
    main()
