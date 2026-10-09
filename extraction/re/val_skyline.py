#!/usr/bin/env python3
"""Skyline placement validation — external-Claude review tests 1/4/5.

Test 1  translation sweep ±60 XY (FFT cross-correlation of street-vertex
        occupancy vs filled skyline footprint mask) + rotation sweep ±5 deg.
        A single sharp peak at d = (-141.69, -681.15) confirms the decode.
Test 4  explicit per-mesh centroid correspondence: FP1/FP2/FP3 vs
        GC_island1_LongDist, Roads bbox identity, LOW unit vs LongDist.
        (FP4 does not exist in the data — see survey output.)
Test 5  island1 (placed) vs island2 (identity) top-down overlap check.

All math in GAME coords (Z-up, right-handed): glTF (x,y,z) -> game (x,-z,y).
Skyline local frame = placed game coords minus ISLAND_WORLD_OFFSET['island1'].

Correlation identity used for the sweep (per axis, Hs/Ws = sky mask shape):
    C = fftconvolve(street, sky[::-1,::-1], 'full')
    C[iy, ix] = Σ street[n] · sky[n - d]   with d = (iy-(Hs-1), ix-(Ws-1))
i.e. d is the world-space translation of the skyline from its local-0
placement; the shipped placement corresponds to d = ISLAND_WORLD_OFFSET.
"""
import json
import os
import struct

import numpy as np
from scipy.signal import fftconvolve

MODELS = "/home/z/my-project/work/TDKR-Game/gh-pages/models"
OUT = "/home/z/my-project/work/valout"
OFFSET = np.array([-141.69, -681.15, 0.114], np.float64)
CELL = 1.0

# ---------------------------------------------------------------- GLB loader

def load_glb_prims_full_named(path, only_name=None):
    """-> list of (name, pos(N,3) f32 gltf-space, idx(M,) int64 or None);
    with only_name, restrict to the mesh whose node/mesh name matches."""
    with open(path, "rb") as f:
        data = f.read()
    assert data[:4] == b"glTF", path
    clen, ctype = struct.unpack_from("<II", data, 12)
    assert ctype == 0x4E4F534A
    j = json.loads(data[20:20 + clen])
    bin_off = 20 + clen
    blen, btype = struct.unpack_from("<II", data, bin_off)
    assert btype == 0x004E4942
    bin_chunk = data[bin_off + 8: bin_off + 8 + blen]

    def acc(ai):
        a = j["accessors"][ai]
        ncomp = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
        ct = {5126: np.float32, 5125: np.uint32, 5123: np.int16,
              5121: np.uint8}[a["componentType"]]
        bv = j["bufferViews"][a["bufferView"]]
        base = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(bin_chunk, dtype=ct, count=a["count"] * ncomp,
                            offset=base)
        return arr.reshape(a["count"], ncomp) if ncomp > 1 else arr

    out = []
    for node in j.get("nodes", []):
        if "mesh" not in node:
            continue
        mesh = j["meshes"][node["mesh"]]
        names = {node.get("name", ""), mesh.get("name", "")}
        if only_name is not None and only_name not in names:
            continue
        for prim in mesh["primitives"]:
            if "POSITION" not in prim.get("attributes", {}):
                continue
            pos = acc(prim["attributes"]["POSITION"]).astype(np.float64).copy()
            idx = acc(prim["indices"]).astype(np.int64).copy() \
                if "indices" in prim else None
            out.append((next(n for n in names if n), pos, idx))
    return out


def load_glb_prims_full(path):
    return load_glb_prims_full_named(path, None)


def to_game(p_gltf):
    """glTF (x,y,z) -> game (x,-z,y)  [inverse of exporter (x,z,-y)]."""
    g = np.empty_like(p_gltf)
    g[:, 0] = p_gltf[:, 0]
    g[:, 1] = -p_gltf[:, 2]
    g[:, 2] = p_gltf[:, 1]
    return g


def load_unit_game(stem, offset=None):
    """GLB -> list of dicts {name, game(N,3) in GAME coords minus offset,
    idx}. Falls back to city_low.glb for the *_LOW units that ship there."""
    path = os.path.join(MODELS, stem + ".glb")
    only = None
    if not os.path.exists(path):
        path = os.path.join(MODELS, "city_low.glb")
        only = stem
    out = []
    for name, pos, idx in load_glb_prims_full_named(path, only):
        g = to_game(pos)
        if offset is not None:
            g = g - offset
        out.append(dict(name=name, game=g, idx=idx))
    return out


# ---------------------------------------------------------------- rasterizer

def rasterize_tris_xy(prims, origin, shape, cell=CELL):
    """Fill triangles (game XY) into a boolean grid. Vertical (XY-degenerate)
    triangles vanish naturally — roofs carry the footprint area."""
    from PIL import Image, ImageDraw
    s = 1.0 / cell
    img = Image.new("1", (shape[1], shape[0]), 0)
    dr = ImageDraw.Draw(img)
    ntri = 0
    for p in prims:
        v = p["game"]
        idx = p["idx"]
        ts = idx.reshape(-1, 3) if idx is not None \
            else np.arange(len(v), dtype=np.int64).reshape(-1, 3)
        xy = np.empty((len(v), 2))
        xy[:, 0] = (v[:, 0] - origin[0]) * s
        xy[:, 1] = (v[:, 1] - origin[1]) * s
        xy = xy.tolist()
        for t in ts:
            a, b, c = xy[t[0]], xy[t[1]], xy[t[2]]
            if abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])) < 1e-9:
                continue
            dr.polygon([a, b, c], fill=1)
            ntri += 1
    return np.asarray(img, dtype=bool), ntri


def vert_occupancy(prims, origin, shape, cell=CELL):
    m = np.zeros(shape, bool)
    for p in prims:
        v = p["game"]
        ix = np.round((v[:, 0] - origin[0]) / cell).astype(np.int64)
        iy = np.round((v[:, 1] - origin[1]) / cell).astype(np.int64)
        ok = (ix >= 0) & (ix < shape[1]) & (iy >= 0) & (iy < shape[0])
        m[iy[ok], ix[ok]] = True
    return m


# ------------------------------------------------------------------- Test 4

def test4():
    print("=" * 72)
    print("TEST 4 — per-mesh centroid correspondence in the shared local frame")
    print("=" * 72)
    longd = load_unit_game("GC_island1_LongDist", OFFSET)
    fp1 = load_unit_game("GC_LongDist_Island1_FP1", OFFSET)
    fp2 = load_unit_game("GC_LongDist_Island1_FP2", OFFSET)
    fp3 = load_unit_game("GC_LongDist_Island1_FP3", OFFSET)
    roads = load_unit_game("GC_LongDist_Island1_Roads", OFFSET)
    low = load_unit_game("GC_island1_LongDist_LOW", OFFSET)
    print(f"GC_island1_LongDist: {len(longd)} meshes (the 54 footprints)")

    L = np.array([p["game"].mean(0) for p in longd])

    def match(name, prims):
        C = np.array([p["game"].mean(0) for p in prims])
        errs = []
        for c in C:
            d = np.linalg.norm(L[:, :2] - c[None, :2], axis=1)
            errs.append(d[int(d.argmin())])
        errs = np.array(errs)
        print(f"  {name:30s} {len(prims):2d} meshes -> nearest-LongDist "
              f"centroid XY err: mean {errs.mean():6.3f}  max {errs.max():6.3f}"
              f"  all<1.0u: {bool((errs < 1.0).all())}")
        return errs

    match("GC_LongDist_Island1_FP1", fp1)
    match("GC_LongDist_Island1_FP2", fp2)
    match("GC_LongDist_Island1_FP3", fp3)
    match("GC_island1_LongDist_LOW", low)

    def bbox(prims):
        v = np.vstack([p["game"] for p in prims])
        return v.min(0), v.max(0)

    lm0, lm1 = bbox(longd)
    rm0, rm1 = bbox(roads)
    print(f"  GC_LongDist_Island1_Roads (9 meshes, merged strips — different")
    print(f"  mesh structure, bbox test instead of centroids):")
    print(f"    min-corner |diff| XYZ = {np.abs(lm0-rm0).round(3)}")
    print(f"    max-corner |diff| XYZ = {np.abs(lm1-rm1).round(3)}")
    rv = np.vstack([p["game"] for p in roads])
    inside = bool(((rv >= lm0 - 0.5) & (rv <= lm1 + 0.5)).all())
    print(f"    every Roads vertex inside LongDist bbox(+/-0.5): {inside}")

    def distinct(prims):
        C = np.array([p["game"].mean(0) for p in prims])
        pairs = [int(np.linalg.norm(L[:, :2] - c[None, :2], axis=1).argmin())
                 for c in C]
        return len(set(pairs)) == len(pairs)

    print(f"  FP1/FP2/FP3 map to distinct LongDist meshes: "
          f"{distinct(fp1)}/{distinct(fp2)}/{distinct(fp3)}")


# ------------------------------------------------------------------- Test 1

SKY_UNITS = ["GC_island1_LongDist", "GC_LongDist_Island1_FP1",
             "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
             "GC_LongDist_Island1_Roads"]


def test1():
    print("=" * 72)
    print("TEST 1 — translation sweep ±60 XY + rotation ±5° (FFT overlap)")
    print("=" * 72)
    street = []
    for i in range(9):
        street += load_unit_game(f"street_island1_{i:02d}")
    sv = np.vstack([p["game"] for p in street])
    print(f"street island1: {len(sv)} verts, world XY bbox "
          f"{sv[:, :2].min(0).round(1)} .. {sv[:, :2].max(0).round(1)}")

    sky = []
    for u in SKY_UNITS:
        sky += load_unit_game(u, OFFSET)      # placed; subtract -> local
    for p in sky:
        p["game"] = p["game"] - OFFSET        # now LOCAL game coords
    lv = np.vstack([p["game"] for p in sky])
    print(f"skyline island1: {len(sky)} meshes, local XY bbox "
          f"{lv[:, :2].min(0).round(1)} .. {lv[:, :2].max(0).round(1)}")

    # grid: union of street-world and sky-local bboxes + margin
    allv = np.vstack([sv[:, :2], lv[:, :2]])
    mgn = 6.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max() - allv[:, 1].min() + 2*mgn) / CELL)),
             int(np.ceil((allv[:, 0].max() - allv[:, 0].min() + 2*mgn) / CELL)))
    print(f"grid {shape} @ {CELL}u  origin {origin.round(1)}")

    street_m = vert_occupancy(street, origin, shape, CELL)
    print(f"street occupancy {street_m.mean()*100:.2f}% of cells")
    sky_m, ntri = rasterize_tris_xy(sky, origin, shape, CELL)
    print(f"skyline filled footprint: {ntri} tris -> {sky_m.sum()} cells")
    np.save(os.path.join(OUT, "street_m.npy"), street_m)
    np.save(os.path.join(OUT, "sky_m.npy"), sky_m)
    np.save(os.path.join(OUT, "origin.npy"), origin)

    C = fftconvolve(street_m.astype(np.float32),
                    sky_m[::-1, ::-1].astype(np.float32), mode="full")
    Hs, Ws = sky_m.shape
    np.save(os.path.join(OUT, "corr_full.npy"), C)

    def val_at(dxw, dyw):
        """intersection cells for world translation (dxw,dyw)."""
        dxc = int(round(dxw / CELL)); dyc = int(round(dyw / CELL))
        return float(C[dyc + Hs - 1, dxc + Ws - 1])

    ex, ey = float(OFFSET[0]), float(OFFSET[1])
    pk = val_at(ex, ey)
    print(f"\nintersection(±cells) at d=OFFSET ({ex:.2f},{ey:.2f}): {pk:,.0f}")
    print("\nX-slice (d=(ex+dx, ey)):")
    print(f"{'dx':>5} {'cells':>12} {'%peak':>7}")
    row = {}
    for dx in [-60, -40, -20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20, 40, 60]:
        v = val_at(ex + dx, ey)
        row[dx] = v
        print(f"{dx:5d} {v:12,.0f} {100*v/pk:6.1f}%")
    print("Y-slice (d=(ex, ey+dy)):")
    col = {}
    for dy in [-60, -40, -20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20, 40, 60]:
        v = val_at(ex, ey + dy)
        col[dy] = v
        print(f"{dy:5d} {v:12,.0f} {100*v/pk:6.1f}%")

    # half-max widths along each axis (nearest crossing)
    def width(dct):
        ks = sorted(dct)
        for a, b in zip(ks, ks[1:]):
            if dct[a] >= pk/2 >= dct[b] or dct[b] >= pk/2 >= dct[a]:
                lo, hi = sorted((a, b))
                if dct[hi] > dct[lo]:
                    lo, hi = hi, lo
                if dct[lo] == dct[hi]:
                    return float(lo)
                t = (dct[lo] - pk/2) / (dct[lo] - dct[hi])
                return lo + t * (hi - lo)
        return None
    wx_p = width({k: val_at(ex + k, ey) for k in range(0, 121)})
    wx_n = width({-k: val_at(ex - k, ey) for k in range(0, 121)})
    wy_p = width({k: val_at(ex, ey + k) for k in range(0, 121)})
    wy_n = width({-k: val_at(ex, ey - k) for k in range(0, 121)})
    print(f"\nhalf-max width X: -{wx_n} .. +{wx_p}   Y: -{wy_n} .. +{wy_p}")

    # exact-grid argmax inside OFFSET±60 window
    i0 = int(round(ey / CELL)) + Hs - 1
    j0 = int(round(ex / CELL)) + Ws - 1
    win = C[i0-60:i0+61, j0-60:j0+61]
    kk = np.unravel_index(np.argmax(win), win.shape)
    peak_d = ((kk[1] - 60) * CELL + ex, (kk[0] - 60) * CELL + ey)
    print(f"argmax within ±60 window: d = ({peak_d[0]:.1f}, {peak_d[1]:.1f}) "
          f"cells (quantized to {CELL}u grid; expected "
          f"({ex:.1f},{ey:.1f}))")

    # ---------------- rotation sweep: world = R(θ)·local + OFFSET
    print("\nrotation sweep (peak intersection re-optimized over ±6u):")
    rot_res = {}
    for th in [-5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 4, 5]:
        R = np.array([[np.cos(np.deg2rad(th)), -np.sin(np.deg2rad(th))],
                      [np.sin(np.deg2rad(th)), np.cos(np.deg2rad(th))]])
        sky_r = []
        for p in sky:
            q = p.copy()
            g = p["game"].copy()
            g[:, :2] = g[:, :2] @ R.T
            q["game"] = g
            sky_r.append(q)
        sm, _ = rasterize_tris_xy(sky_r, origin, shape, CELL)
        Cr = fftconvolve(street_m.astype(np.float32),
                         sm[::-1, ::-1].astype(np.float32), mode="full")
        best = 0.0; bd = None
        for ddy in range(-6, 7):
            for ddx in range(-6, 7):
                v = Cr[i0+ddy, j0+ddx]
                if v > best:
                    best = v; bd = (ddx, ddy)
        rot_res[th] = (float(best), bd)
        print(f"  θ={th:5.1f}°  peak {best:12,.0f} ({100*best/pk:6.2f}% of "
              f"θ=0)  at d={bd}")
    np.save(os.path.join(OUT, "corr_full.npy"), C)

    # ---------------- plots
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.font_manager as fm
    for fp in ("/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            fm.fontManager.addfont(fp)
        except Exception:
            pass
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Noto Sans SC"]
    plt.rcParams["axes.unicode_minus"] = False

    # 2D heatmap around the peak (±60u)
    win2 = C[i0-60:i0+61, j0-60:j0+61]
    fig, ax = plt.subplots(figsize=(8, 6.5), constrained_layout=True)
    ext = [ex-60, ex+60, ey-60, ey+60]
    im = ax.imshow(win2, origin="lower", extent=ext, cmap="inferno",
                   aspect="equal")
    ax.plot(ex, ey, "c+", ms=14, mew=2, label="decoded offset (-141.69, -681.15)")
    ax.plot(0, 0, "w+", ms=10, mew=2, label="zero offset")
    fig.colorbar(im, ax=ax, label="overlap cells (street verts × skyline footprint)")
    ax.set_xlabel("world offset X (units)"); ax.set_ylabel("world offset Y (units)")
    ax.set_title("Island-1 skyline placement — overlap vs translation\n"
                 "single sharp peak = decode confirmed")
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(os.path.join(OUT, "test1_sweep_heatmap.png"), dpi=150)
    plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    dxs = np.arange(-60, 61)
    axs[0].plot(dxs, [val_at(ex + d, ey) for d in dxs], lw=1.5)
    axs[0].axvline(0, color="c", ls="--", lw=1)
    axs[0].set_title("X slice at d_y = -681.15")
    axs[0].set_xlabel("ΔX from decoded offset (units)")
    axs[1].plot(dxs, [val_at(ex, ey + d) for d in dxs], lw=1.5)
    axs[1].axvline(0, color="c", ls="--", lw=1)
    axs[1].set_title("Y slice at d_x = -141.69")
    axs[1].set_xlabel("ΔY from decoded offset (units)")
    for a in axs:
        a.set_ylabel("overlap cells")
    fig.suptitle("Overlap vs offset — slices through the peak")
    fig.savefig(os.path.join(OUT, "test1_slices.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)
    ths = sorted(rot_res)
    vals = [100*rot_res[t][0]/pk for t in ths]
    ax.plot(ths, vals, "o-")
    ax.axvline(0, color="c", ls="--", lw=1, label="decoded rot = 0")
    ax.set_xlabel("rotation θ (deg)"); ax.set_ylabel("peak overlap, % of θ=0")
    ax.set_title("Rotation sweep ±5° (translation re-optimized ±6u)")
    ax.legend()
    fig.savefig(os.path.join(OUT, "test1_rotation.png"), dpi=150)
    plt.close(fig)

    summary = dict(
        peak_cells=pk,
        expected=(ex, ey),
        argmax_quantized=[round(peak_d[0], 1), round(peak_d[1], 1)],
        half_width_x=[None if wx_n is None else round(-wx_n, 1),
                      None if wx_p is None else round(wx_p, 1)],
        half_width_y=[None if wy_n is None else round(-wy_n, 1),
                      None if wy_p is None else round(wy_p, 1)],
        x_slice={str(k): row[k] for k in row},
        y_slice={str(k): col[k] for k in col},
        rotation={str(t): dict(cells=rot_res[t][0], at=rot_res[t][1])
                  for t in rot_res},
        street_verts=int(len(sv)), sky_tris_rasterized=int(ntri),
    )
    with open(os.path.join(OUT, "test1_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("saved plots + test1_summary.json")


# ------------------------------------------------------------------- Test 5

def test5():
    print("=" * 72)
    print("TEST 5 — island1 (placed) vs island2 (identity) overlap")
    print("=" * 72)
    i1 = []
    for u in SKY_UNITS:
        i1 += load_unit_game(u, OFFSET)
    i2stems = ["GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
               "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
               "GC_LongDist_Island2_Roads"]
    i2 = []
    for u in i2stems:
        i2 += load_unit_game(u, np.zeros(3))   # identity

    def bb(prims):
        v = np.vstack([p["game"] for p in prims])[:, :2]
        return v.min(0), v.max(0)

    a0, a1 = bb(i1); b0, b1 = bb(i2)
    print(f"island1 placed XY bbox: {a0.round(1)} .. {a1.round(1)}")
    print(f"island2 identity XY bbox: {b0.round(1)} .. {b1.round(1)}")
    ox = max(0.0, min(a1[0], b1[0]) - max(a0[0], b0[0]))
    oy = max(0.0, min(a1[1], b1[1]) - max(a0[1], b0[1]))
    print(f"bbox intersection: {ox:.1f} x {oy:.1f} = {ox*oy:,.0f} units²"
          f"  (island1 area {(a1[0]-a0[0])*(a1[1]-a0[1]):,.0f}, "
          f"island2 {(b1[0]-b0[0])*(b1[1]-b0[1]):,.0f})")

    # filled-mask overlap (the real test, not just bboxes)
    allv = np.vstack([np.vstack([p["game"] for p in i1])[:, :2],
                      np.vstack([p["game"] for p in i2])[:, :2]])
    mgn = 6.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
             int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
    m1, _ = rasterize_tris_xy(i1, origin, shape, CELL)
    m2, _ = rasterize_tris_xy(i2, origin, shape, CELL)
    inter = float((m1 & m2).sum())
    print(f"filled-footprint overlap: {inter:,.0f} cells of "
          f"{m1.sum():,.0f} (i1) / {m2.sum():,.0f} (i2) "
          f"-> {100*inter/max(1, min(m1.sum(), m2.sum())):.2f}% of smaller")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 9), constrained_layout=True)
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle(a0, a1[0]-a0[0], a1[1]-a0[1], fc="royalblue",
                           alpha=.25, ec="royalblue", label="island1 placed bbox"))
    ax.add_patch(Rectangle(b0, b1[0]-b0[0], b1[1]-b0[1], fc="orange",
                           alpha=.25, ec="orange", label="island2 identity bbox"))
    v1 = np.vstack([p["game"] for p in i1])
    v2 = np.vstack([p["game"] for p in i2])
    ax.scatter(v1[::7, 0], v1[::7, 1], s=.3, c="navy", alpha=.5)
    ax.scatter(v2[::7, 0], v2[::7, 1], s=.3, c="darkorange", alpha=.5)
    sv = []
    for i in range(9):
        sv += load_unit_game(f"street_island1_{i:02d}")
    w = np.vstack([p["game"] for p in sv])
    ax.scatter(w[::23, 0], w[::23, 1], s=.2, c="green", alpha=.3,
               label="street island1")
    ax.set_aspect("equal")
    ax.legend(loc="upper right", markerscale=40)
    ax.set_title("Top-down (game XY): island1 skyline vs island2 skyline\n"
                 "two islands must sit side by side, not stacked")
    ax.set_xlabel("X (units)"); ax.set_ylabel("Y (units)")
    fig.savefig(os.path.join(OUT, "test5_islands.png"), dpi=140)
    plt.close(fig)
    print("saved test5_islands.png")
    return dict(bbox_inter=ox*oy, cells_inter=inter,
                i1_cells=int(m1.sum()), i2_cells=int(m2.sum()))


if __name__ == "__main__":
    test4()
    test1()
    test5()
