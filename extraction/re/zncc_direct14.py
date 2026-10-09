#!/usr/bin/env python3
"""Ground-truth ZNCC at the record placement — direct windowed Pearson
correlation, NO FFT, NO correlation-index convention.

ZNCC(d) defined as: take the window W = support of the SKY density placed at
d; correlate street density S[W] with sky density K[W] (Pearson r over the
window).  This is the quantity 'ZNCC at placement d' without any ambiguity.

Computed for: record placement (shipped), identity (local-0), v13, and the
sweep's global-argmax displacement (+635,+158) — in one consistent frame.
"""
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import load_unit_game, rasterize_tris_xy, SKY_UNITS

TRUE = np.array([-730.0, -1250.0, 0.0])
OLD = np.array([-141.69, -681.15, 0.114])
CELL = 2.0


def build():
    street = [p for i in range(9)
              for p in load_unit_game(f"street_island1_{i:02d}")]
    sky = [p for u in SKY_UNITS for p in load_unit_game(u)]  # shipped=record
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    mgn = 200.0
    origin = np.minimum(sv.min(0), lv.min(0)) - mgn
    shape = (int(np.ceil((max(sv[:, 1].max(), lv[:, 1].max()) - origin[1] + mgn) / CELL)),
             int(np.ceil((max(sv[:, 0].max(), lv[:, 0].max()) - origin[0] + mgn) / CELL)))
    S = np.zeros(shape, np.float64)
    ix = np.round((sv[:, 0] - origin[0]) / CELL).astype(int)
    iy = np.round((sv[:, 1] - origin[1]) / CELL).astype(int)
    np.add.at(S, (iy, ix), 1.0)
    S = gaussian_filter(S, 1.5)
    K0, _ = rasterize_tris_xy(sky, origin, shape, CELL)   # at record
    K0 = gaussian_filter(K0.astype(np.float64), 1.5)
    return S, K0


def window_zncc(S, K, dxy):
    """shift K by dxy (units, world +x/+y) and Pearson-correlate in the
    overlap of K's dilated support with the grid."""
    dy = int(round(dxy[1] / CELL)); dx = int(round(dxy[0] / CELL))
    H, W = K.shape
    Ks = np.zeros_like(K)
    ry0, ry1 = max(0, dy), min(H, H + dy)
    rx0, rx1 = max(0, dx), min(W, W + dx)
    if ry1 <= ry0 or rx1 <= rx0:
        return None
    Ks[ry0:ry1, rx0:rx1] = K[ry0 - dy:ry1 - dy, rx0 - dx:rx1 - dx]
    m = Ks > 0
    if m.sum() < 100:
        return None
    a, b = S[m], Ks[m]
    if a.std() < 1e-9 or b.std() < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def main():
    S, K0 = build()
    print(f"grid {S.shape}, sky support cells {(K0 > 0).sum():,}")
    cands = [
        ("record (shipped, d=0)", (0.0, 0.0)),
        ("identity (d=+TRUE)", (float(TRUE[0]), float(TRUE[1]))),
        ("v13 (d=+OLD-TRUE)", (float(OLD[0] - TRUE[0]), float(OLD[1] - TRUE[1]))),
        ("sweep argmax (+635,+158)", (635.0, 158.0)),
        ("+20,+20", (20.0, 20.0)),
        ("-20,-20", (-20.0, -20.0)),
        ("+40,+45 (raw argmax win60)", (40.0, 45.0)),
    ]
    for nm, d in cands:
        print(f"  {nm:30s} direct windowed ZNCC "
              f"{window_zncc(S, K0, d):+.4f}")

    # also: ZNCC over the FULL GRID window (not just sky support) at record
    a, b = S.ravel(), K0.ravel()
    print(f"\n  full-grid-window Pearson(S,K) @record: "
          f"{np.corrcoef(a, b)[0, 1]:+.4f}")

    # per-axis sharpness of the direct metric
    print("\n  direct ZNCC vs |d| profile (diagonal):")
    for r in (0, 2, 5, 10, 20, 40, 60, 100):
        v = window_zncc(S, K0, (float(r), float(r)))
        print(f"    d=({r:+4d},{r:+4d})  {v:+.4f}")


if __name__ == "__main__":
    main()
