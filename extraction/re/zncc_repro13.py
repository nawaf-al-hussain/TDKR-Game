#!/usr/bin/env python3
"""Arbitrate the session-13 ZNCC (+0.66) vs the float64 sweep (+0.08).

Session 13 (zncc13*.py) computed ZNCC in float32 on grids where
sA*sB/N ~ 1e8-1e9 while the true cov ~ O(1).  Float32 carries ~7 significant
digits, so cov = sAB - sA*sB/N is a catastrophic cancellation -> the +0.66
may be pure round-off noise.

This script reconstructs the session-13 frame from the CURRENT (v14) GLBs:
  shipped = local + TRUE, so local_13 = shipped_game - (TRUE - OLD)
  (identical to what load_unit_game(u, OLD) produced pre-patch)
and runs the EXACT zncc13b math at CELL=2, mgn=340, sigma=1.5 in BOTH
dtypes.  If float32 reproduces ~+0.66 and float64 gives ~+0.1, the session-13
number is proven an artifact.
"""
import os
import sys

import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import load_unit_game, rasterize_tris_xy, SKY_UNITS

OLD = np.array([-141.69, -681.15, 0.114])
TRUE = np.array([-730.0, -1250.0, 0.0])
CELL = 2.0


def sky_local_13():
    """Reconstruct session-13 'local' skyline.

    shipped = local + TRUE  (v14 GLBs), and session-13's
    load_unit_game(u, OLD) on pre-patch GLBs (local + OLD) also yields local.
    So local = shipped - TRUE."""
    out = []
    for u in SKY_UNITS:
        for p in load_unit_game(u):          # shipped = local + TRUE
            p["game"] = p["game"] - TRUE
            out.append(p)
    return out


def zncc13(street, sky, dtype):
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    mgn = 340.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max() - allv[:, 1].min() + 2 * mgn) / CELL)),
             int(np.ceil((allv[:, 0].max() - allv[:, 0].min() + 2 * mgn) / CELL)))
    sd = np.zeros(shape, dtype)
    for p in street:
        v = p["game"]
        ix = np.round((v[:, 0] - origin[0]) / CELL).astype(int)
        iy = np.round((v[:, 1] - origin[1]) / CELL).astype(int)
        ok = (ix >= 0) & (ix < shape[1]) & (iy >= 0) & (iy < shape[0])
        np.add.at(sd, (iy[ok], ix[ok]), 1.0)
    sd = gaussian_filter(sd, 1.5)
    km, _ = rasterize_tris_xy(sky, origin, shape, CELL)
    kd = gaussian_filter(km.astype(dtype), 1.5)
    ones = np.ones_like(kd)
    sA = fftconvolve(sd, ones[::-1, ::-1], mode="full")
    sA2 = fftconvolve(sd * sd, ones[::-1, ::-1], mode="full")
    sB = fftconvolve(kd, ones[::-1, ::-1], mode="full")
    sB2 = fftconvolve(kd * kd, ones[::-1, ::-1], mode="full")
    sAB = fftconvolve(sd, kd[::-1, ::-1], mode="full")
    N = fftconvolve(np.ones_like(sd), ones[::-1, ::-1], mode="full")
    Hs, Ws = kd.shape
    cov = sAB - sA * sB / N
    varA = np.maximum(sA2 - sA * sA / N, 1e-6)
    varB = np.maximum(sB2 - sB * sB / N, 1e-6)
    Z = cov / np.sqrt(varA * varB)
    valid = N >= 0.25 * kd.sum()
    Z[~valid] = -2
    out = {}
    for nm, dd in (("identity", (0, 0)), ("record TRS", (-730, -1250)),
                   ("v13 OLD", tuple(OLD[:2]))):
        dxc = int(round(dd[0] / CELL)); dyc = int(round(dd[1] / CELL))
        out[nm] = float(Z[dyc + Hs - 1, dxc + Ws - 1])
    k = np.unravel_index(np.argmax(Z), Z.shape)
    out["_global"] = (float(Z[k]), (k[1] - (Ws - 1)) * CELL,
                      (k[0] - (Hs - 1)) * CELL)
    return out


def main():
    street = [p for i in range(9)
              for p in load_unit_game(f"street_island1_{i:02d}")]
    sky = sky_local_13()
    print("reconstructed session-13 local skyline: "
          f"{len(sky)} meshes, bbox {np.vstack([p['game'] for p in sky])[:, :2].min(0).round(1)}"
          "..")
    for dt in (np.float32, np.float64):
        r = zncc13(street, sky, dt)
        g, gx, gy = r["_global"]
        print(f"\n--- dtype={np.dtype(dt).name} ---")
        for nm in ("identity", "record TRS", "v13 OLD"):
            print(f"  @{nm:11s} ZNCC {r[nm]:+.4f}")
        print(f"  global peak {g:+.4f} @ d=({gx:+.0f},{gy:+.0f})")
    # magnitude context: terms of the cancellation
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    print(f"\nterm magnitude context: street verts {len(sv):,}, "
          f"sky tris rasterized on CELL=2 grid; sA*sB/N is O(1e8)-O(1e9), "
          f"true cov O(1) -> float32 (7 digits) cannot resolve it.")


if __name__ == "__main__":
    main()
