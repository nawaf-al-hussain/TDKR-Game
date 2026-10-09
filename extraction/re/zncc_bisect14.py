#!/usr/bin/env python3
"""Bisect the zncc13b (+0.66) vs zncc_sweep14 (+0.08..0.12) discrepancy.

Config deltas between the two runs:
  CELL          2.0 (13b)   vs 1.0 (sweep)      [and 2.0 in rot run]
  margin        340  (13b)   vs 40  (sweep)
  variance floor 1e-6 abs (13b) vs 0.02*max rel (sweep)
  valid mask    N>=0.25*kd.sum() in both

Runs zncc13b's exact math with one toggle at a time and prints Z@record.
"""
import os
import sys

import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import load_unit_game, rasterize_tris_xy, SKY_UNITS

TRUE = np.array([-730.0, -1250.0, 0.0])


def build(cell, mgn):
    street = [p for i in range(9)
              for p in load_unit_game(f"street_island1_{i:02d}")]
    sky = [p for u in SKY_UNITS for p in load_unit_game(u)]
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max() - allv[:, 1].min() + 2 * mgn) / cell)),
             int(np.ceil((allv[:, 0].max() - allv[:, 0].min() + 2 * mgn) / cell)))
    S = np.zeros(shape, np.float64)
    ix = np.round((sv[:, 0] - origin[0]) / cell).astype(int)
    iy = np.round((sv[:, 1] - origin[1]) / cell).astype(int)
    np.add.at(S, (iy, ix), 1.0)
    S = gaussian_filter(S, 1.5)
    K, _ = rasterize_tris_xy(sky, origin, shape, cell)
    K = gaussian_filter(K.astype(np.float64), 1.5)
    return S, K


def zrecord(S, K, floor_mode, use_valid):
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
    if floor_mode == "abs":
        varA = np.maximum(varA, 1e-6)
        varB = np.maximum(varB, 1e-6)
    else:
        varA = np.maximum(varA, 0.02 * varA.max())
        varB = np.maximum(varB, 0.02 * varB.max())
    Z = cov / np.sqrt(varA * varB)
    if use_valid:
        Z[N < 0.25 * K.sum()] = -2
    return float(Z[Hs - 1, Ws - 1])   # d=0 == shipped == record placement


def main():
    for cell, mgn in ((2.0, 340.0), (2.0, 40.0), (1.0, 340.0)):
        S, K = build(cell, mgn)
        for fm in ("abs", "rel"):
            z = zrecord(S, K, fm, True)
            print(f"CELL={cell} mgn={mgn:5.0f} floor={fm:3s} "
                  f"valid=on  -> Z@record {z:+.4f}", flush=True)
        del S, K


if __name__ == "__main__":
    main()
