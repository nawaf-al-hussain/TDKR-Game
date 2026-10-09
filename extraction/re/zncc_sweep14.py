#!/usr/bin/env python3
"""ZNCC translation sweep — external-Claude round-2 check 1.

"Report the ZNCC peak, not one point. Sweep the translation ±100 units
around (-730,-1250) and confirm a single sharp maximum at the record value."

The v14 GLBs are shipped AT the 0x14051 record TRS (-730,-1250,0), so the
shipped skyline coords ARE the record placement; the ZNCC map below is
indexed by additional translation delta d relative to the record.

Method (float64, masked, gaussian-smoothed density — same as session 13):
  street density S  = street vertex counts per 1u cell, smoothed σ=1.5
  skyline density K = filled roof-footprint mask (tris rasterized XY),
                      smoothed σ=1.5
  ZNCC(d) = cov(S, K shifted by d) / sqrt(var_S(window) * var_K(window))
computed for the whole plane via the FFT convolution identity.

Outputs:
  work/valout/zncc14_heatmap.png     ±100u window around the record
  work/valout/zncc14_global.png      whole search plane
  work/valout/zncc14_slices.png      X/Y slices through the peak (±100u)
  work/valout/zncc14_rotation.png    rotation sweep ±5° (translation re-opt)
  extraction/re/zncc_sweep14.json    numbers for the handoff
"""
import json
import os
import sys

import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, maximum_filter

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import (load_unit_game, rasterize_tris_xy, MODELS, OUT,
                         SKY_UNITS)

TRUE = np.array([-730.0, -1250.0, 0.0])   # the 0x14051 record TRS (v14 shipped)
OLD = np.array([-141.69, -681.15, 0.114])  # the wrong v13 offset
CELL = 1.0
SIGMA = 1.5


def density_maps(cell):
    street = [p for i in range(9)
              for p in load_unit_game(f"street_island1_{i:02d}")]
    sky = [p for u in SKY_UNITS for p in load_unit_game(u)]   # shipped = record
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    mgn = 40.0
    origin = np.minimum(sv.min(0), lv.min(0)) - mgn
    shape = (int(np.ceil((max(sv[:, 1].max(), lv[:, 1].max())
                           - origin[1] + mgn) / cell)),
             int(np.ceil((max(sv[:, 0].max(), lv[:, 0].max())
                           - origin[0] + mgn) / cell)))
    # street: vertex-count density
    S = np.zeros(shape, np.float64)
    ix = np.round((sv[:, 0] - origin[0]) / cell).astype(np.int64)
    iy = np.round((sv[:, 1] - origin[1]) / cell).astype(np.int64)
    np.add.at(S, (iy, ix), 1.0)
    S = gaussian_filter(S, SIGMA)
    # skyline: filled roof footprint (placed at record TRS)
    K, ntri = rasterize_tris_xy(sky, origin, shape, cell)
    K = gaussian_filter(K.astype(np.float64), SIGMA)
    return S, K, origin, shape, ntri, sv, lv


def zncc_map(S, K):
    ones = np.ones_like(K)
    sA = fftconvolve(S, ones[::-1, ::-1], mode="full")
    sA2 = fftconvolve(S * S, ones[::-1, ::-1], mode="full")
    sB = fftconvolve(K, ones[::-1, ::-1], mode="full")
    sB2 = fftconvolve(K * K, ones[::-1, ::-1], mode="full")
    sAB = fftconvolve(S, K[::-1, ::-1], mode="full")
    N = fftconvolve(np.ones_like(S), ones[::-1, ::-1], mode="full")
    Hs, Ws = K.shape
    cov = sAB - sA * sB / N
    varA = sA2 - sA * sA / N
    varB = sB2 - sB * sB / N
    # floor the variances (session-13 trick) so flat windows cannot explode
    varA = np.maximum(varA, 0.02 * varA.max())
    varB = np.maximum(varB, 0.02 * varB.max())
    Z = cov / np.sqrt(varA * varB)
    valid = N >= 0.25 * K.sum()
    Z[~valid] = -2.0
    return Z, (Hs - 1, Ws - 1)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("building density maps (CELL=1u) ...")
    S, K, origin, shape, ntri, sv, lv = density_maps(CELL)
    print(f"grid {shape}  street verts {len(sv):,}  sky tris {ntri:,}  "
          f"sky cells {int((K > 0).sum()):,}")
    print("full-plane ZNCC (6 FFT convolutions) ...")
    Z, c0 = zncc_map(S, K)
    i0, j0 = c0                      # index of d = (0,0) = record TRS
    np.save(os.path.join(OUT, "zncc14_Z.npy"), Z.astype(np.float32))

    z_rec = float(Z[i0, j0])
    # candidate offsets for reference
    def z_at(dx, dy):
        ii = int(round(dy / CELL)) + i0
        jj = int(round(dx / CELL)) + j0
        if 0 <= ii < Z.shape[0] and 0 <= jj < Z.shape[1]:
            return float(Z[ii, jj])
        return None

    d_identity = -TRUE[:2]                       # skyline local-0 placement
    d_v13 = OLD[:2] - TRUE[:2]                   # the wrong v13 offset
    z_ident = z_at(*d_identity)
    z_v13 = z_at(*d_v13)

    # global argmax over the valid region
    gz = np.where(Z > -1.9, Z, -9.0)
    gk = np.unravel_index(np.argmax(gz), gz.shape)
    gdx, gdy = (gk[1] - j0) * CELL, (gk[0] - i0) * CELL
    print(f"\nZNCC @ record Δ=(0,0):        {z_rec:+.4f}")
    print(f"ZNCC @ identity Δ=({d_identity[0]:+.0f},{d_identity[1]:+.0f}): "
          f"{z_ident:+.4f}")
    print(f"ZNCC @ v13 Δ=({d_v13[0]:+.1f},{d_v13[1]:+.1f}):        {z_v13:+.4f}")
    print(f"GLOBAL argmax: Δ=({gdx:+.1f},{gdy:+.1f})  Z={gz[gk]:+.4f}  "
          f"({'== record' if abs(gdx) <= 1 and abs(gdy) <= 1 else '≠ record!'})")

    # distinct local maxima (≥15u apart)
    mf = maximum_filter(gz, size=31)
    peaks = (gz == mf) & (gz > -1.9)
    pj = np.argwhere(peaks)
    vals = gz[pj[:, 0], pj[:, 1]]
    order = np.argsort(vals)[::-1]
    top = []
    for k in order:
        iy, ix = pj[k]
        dy, dx = (iy - i0) * CELL, (ix - j0) * CELL
        if any((dx - a[1]) ** 2 + (dy - a[0]) ** 2 < 15 ** 2 for a in top):
            continue
        top.append((dy, dx, float(vals[k])))
        if len(top) >= 8:
            break
    print("\ndistinct local maxima (≥15u apart):")
    for dy, dx, v in top:
        tag = "  <= record" if abs(dx) <= 1 and abs(dy) <= 1 else ""
        print(f"   Δ=({dx:+8.1f},{dy:+8.1f})  Z={v:+.4f}{tag}")

    # sharpness profile through the record
    prof = {}
    for ax in ("X", "Y"):
        row = {}
        for d in (-100, -60, -40, -20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20,
                  40, 60, 100):
            row[d] = z_at(d, 0) if ax == "X" else z_at(0, d)
        prof[ax] = row
    print("\nslices through the record:")
    for ax in ("X", "Y"):
        print(f"  {ax}: " + "  ".join(
            f"{d:+4d}:{prof[ax][d]:+.3f}" for d in sorted(prof[ax])))

    # half-peak radius: largest r where Z(r) still >= z_rec/2? use first drop
    def drop_r(ax, frac):
        tgt = z_rec * frac
        for r in range(1, 121):
            a = z_at(r, 0) if ax == "X" else z_at(0, r)
            b = z_at(-r, 0) if ax == "X" else z_at(0, -r)
            if (a is not None and a < tgt) or (b is not None and b < tgt):
                return r
        return None
    r50x, r50y = drop_r("X", 0.5), drop_r("Y", 0.5)
    print(f"\nfirst crossing of Z < 0.5*Z_peak: X r={r50x}u  Y r={r50y}u")

    # window stats ±100
    win = Z[i0 - 100:i0 + 101, j0 - 100:j0 + 101]
    wk = np.unravel_index(np.argmax(win), win.shape)
    wdx, wdy = (wk[1] - 100) * CELL, (wk[0] - 100) * CELL
    n80 = int((win >= 0.8 * z_rec).sum())
    n50 = int((win >= 0.5 * z_rec).sum())
    print(f"±100u window: argmax Δ=({wdx:+.0f},{wdy:+.0f}) "
          f"Z={win[wk]:+.4f}; cells ≥0.8·peak: {n80} (of {win.size:,}); "
          f"≥0.5·peak: {n50}")

    # ---------------- rotation sweep (CELL=2, translation re-opt ±15u) ----
    print("\nrotation sweep (CELL=2, ZNCC, translation re-optimized ±15u):")
    S2, K2, origin2, shape2, ntri2, _, _ = density_maps(2.0)
    i02, j02 = K2.shape[0] - 1, K2.shape[1] - 1
    ones2 = np.ones_like(K2)
    sA = fftconvolve(S2, ones2[::-1, ::-1], mode="full")
    sA2 = fftconvolve(S2 * S2, ones2[::-1, ::-1], mode="full")
    N = fftconvolve(np.ones_like(S2), ones2[::-1, ::-1], mode="full")
    varA = np.maximum(sA2 - sA * sA / N, 0.02 * (sA2 - sA * sA / N).max())
    rot = {}
    for th in (-5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 4, 5):
        sky = [p for u in SKY_UNITS for p in load_unit_game(u)]
        if th != 0:
            R = np.array([[np.cos(np.deg2rad(th)), -np.sin(np.deg2rad(th))],
                          [np.sin(np.deg2rad(th)), np.cos(np.deg2rad(th))]])
            for p in sky:
                p["game"][:, :2] = p["game"][:, :2] @ R.T
        Kr, _ = rasterize_tris_xy(sky, origin2, shape2, 2.0)
        Kr = gaussian_filter(Kr.astype(np.float64), SIGMA)
        sB = fftconvolve(Kr, ones2[::-1, ::-1], mode="full")
        sB2 = fftconvolve(Kr * Kr, ones2[::-1, ::-1], mode="full")
        sAB = fftconvolve(S2, Kr[::-1, ::-1], mode="full")
        varB = np.maximum(sB2 - sB * sB / N, 0.02 * (sB2 - sB * sB / N).max())
        Zr = (sAB - sA * sB / N) / np.sqrt(varA * varB)
        valid = N >= 0.25 * Kr.sum()
        Zr[~valid] = -2.0
        w = 15 // 2
        wz = Zr[i02 - w:i02 + w + 1, j02 - w:j02 + w + 1]
        kk = np.unravel_index(np.argmax(wz), wz.shape)
        bdx, bdy = (kk[1] - w) * 2, (kk[0] - w) * 2
        rot[th] = dict(at_record=float(Zr[i02, j02]),
                       best=float(wz[kk]), at=(bdx, bdy))
        print(f"  θ={th:+5.1f}°  Z@record={rot[th]['at_record']:+.4f}  "
              f"best(±15u)={rot[th]['best']:+.4f} @Δ=({bdx:+d},{bdy:+d})")

    # ---------------- plots ----------------
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

    # heatmap ±100
    fig, ax = plt.subplots(figsize=(8.5, 7), constrained_layout=True)
    ext = [-100, 100, -100, 100]
    im = ax.imshow(win, origin="lower", extent=ext, cmap="inferno",
                   aspect="equal")
    ax.plot(0, 0, "c+", ms=14, mew=2,
            label="0x14051 record Δ=(0,0)  Z=%+.3f" % z_rec)
    if abs(wdx) > 1 or abs(wdy) > 1:
        ax.plot(wdx, wdy, "r x", ms=10, mew=2,
                label="window argmax (%+.0f,%+.0f)" % (wdx, wdy))
    fig.colorbar(im, ax=ax, label="ZNCC")
    ax.set_xlabel("ΔX from record (units)")
    ax.set_ylabel("ΔY from record (units)")
    ax.set_title("Island-1 skyline — ZNCC vs translation, ±100u around the "
                 "0x14051 record TRS\nstreet vertex density × skyline roof "
                 "footprint, σ=1.5 smoothing")
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(os.path.join(OUT, "zncc14_heatmap.png"), dpi=150)
    plt.close(fig)

    # global map
    fig, ax = plt.subplots(figsize=(9.5, 8), constrained_layout=True)
    zg = np.where(Z > -1.9, Z, np.nan)
    im = ax.imshow(zg, origin="lower", cmap="inferno",
                   extent=[(0 - j0) * CELL, (Z.shape[1] - 1 - j0) * CELL,
                           (0 - i0) * CELL, (Z.shape[0] - 1 - i0) * CELL])
    ax.plot(0, 0, "c+", ms=14, mew=2, label="record")
    ax.plot(gdx, gdy, "r x", ms=10, mew=2,
            label="global argmax (%+.0f,%+.0f)" % (gdx, gdy))
    ax.plot(d_v13[0], d_v13[1], "w2", ms=10, label="v13 (wrong)")
    ax.plot(d_identity[0], d_identity[1], "g2", ms=10, label="identity")
    fig.colorbar(im, ax=ax, label="ZNCC")
    ax.set_xlabel("ΔX (units)"); ax.set_ylabel("ΔY (units)")
    ax.set_title("Full search plane — ZNCC landscape")
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(os.path.join(OUT, "zncc14_global.png"), dpi=140)
    plt.close(fig)

    # slices
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    ds = np.arange(-100, 101)
    axs[0].plot(ds, [z_at(d, 0) for d in ds], lw=1.4)
    axs[0].axvline(0, color="c", ls="--", lw=1)
    axs[0].set_title("X slice (ΔY=0)")
    axs[0].set_xlabel("ΔX (units)")
    axs[1].plot(ds, [z_at(0, d) for d in ds], lw=1.4)
    axs[1].axvline(0, color="c", ls="--", lw=1)
    axs[1].set_title("Y slice (ΔX=0)")
    axs[1].set_xlabel("ΔY (units)")
    for a in axs:
        a.set_ylabel("ZNCC")
    fig.suptitle("ZNCC slices through the record peak")
    fig.savefig(os.path.join(OUT, "zncc14_slices.png"), dpi=150)
    plt.close(fig)

    # rotation curve
    fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)
    ths = sorted(rot)
    ax.plot(ths, [rot[t]["at_record"] for t in ths], "o-",
            label="Z at record translation")
    ax.plot(ths, [rot[t]["best"] for t in ths], "s--",
            label="Z re-optimized ±15u")
    ax.axvline(0, color="c", ls="--", lw=1, label="record rot = 0")
    ax.set_xlabel("rotation θ (deg)"); ax.set_ylabel("ZNCC")
    ax.set_title("Rotation sweep ±5°")
    ax.legend(fontsize=8)
    fig.savefig(os.path.join(OUT, "zncc14_rotation.png"), dpi=150)
    plt.close(fig)

    summary = dict(
        method="masked ZNCC, float64, gaussian σ=1.5 @ 1u cells; "
               "street vertex density vs skyline roof footprint",
        record_trs=[-730.0, -1250.0, 0.0],
        note="ZNCC landscape is a broad ridge; the +0.66 session-13 value "
             "was a framing-dependent window artifact (see "
             "skyline_verify14.json) - RETRACTED. Sharp evidence for the "
             "record TRS = engine record + FP/assembly centroid "
             "correspondence (sub-unit mean vectors).",
        z_at_record=z_rec,
        z_at_identity=z_ident, identity_delta=[float(d_identity[0]),
                                               float(d_identity[1])],
        z_at_v13=z_v13, v13_delta=[float(d_v13[0]), float(d_v13[1])],
        global_argmax=dict(d=[float(gdx), float(gdy)],
                           z=float(gz[gk])),
        window100_argmax=dict(d=[int(wdx), int(wdy)],
                              z=float(win[wk])),
        local_maxima=[dict(dy=float(t[0]), dx=float(t[1]),
                           z=float(t[2])) for t in top],
        slices=prof,
        half_peak_drop_x=r50x, half_peak_drop_y=r50y,
        cells_ge_08=n80, cells_ge_05=n50,
        rotation={str(k): dict(at_record=float(v['at_record']),
                               best=float(v['best']), at=[int(v['at'][0]),
                               int(v['at'][1])])
                  for k, v in rot.items()},
        grid=[int(x) for x in shape], sky_tris=int(ntri),
    )
    with open(os.path.join(RE, "zncc_sweep14.json"), "w") as f:
        json.dump(summary, f, indent=1)
    with open(os.path.join(OUT, "zncc14_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("\nsaved zncc14_*.png + zncc_sweep14.json")


if __name__ == "__main__":
    main()
