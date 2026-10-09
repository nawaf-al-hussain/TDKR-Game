#!/usr/bin/env python3
"""float64 ZNCC, masked; global peak + rotation sweep for island2."""
import sys
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter

sys.path.insert(0, "/home/z/my-project/scripts")
from val_skyline import load_unit_game, rasterize_tris_xy

OLD = np.array([-141.69, -681.15, 0.114])
CELL = 2.0
U1 = ["GC_island1_LongDist", "GC_LongDist_Island1_FP1",
      "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
      "GC_LongDist_Island1_Roads"]
U2 = ["GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
      "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
      "GC_LongDist_Island2_Roads"]


def zncc(street, sky, tag, rot=0.0, cands=(("identity", 0, 0),
                                           ("record", -730, -1250),
                                           ("v13OLD", -141.69, -681.15))):
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    mgn = 340.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
             int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
    sd = np.zeros(shape, np.float64)
    for p in street:
        v = p["game"]
        ix = np.round((v[:, 0]-origin[0])/CELL).astype(int)
        iy = np.round((v[:, 1]-origin[1])/CELL).astype(int)
        ok = (ix >= 0) & (ix < shape[1]) & (iy >= 0) & (iy < shape[0])
        np.add.at(sd, (iy[ok], ix[ok]), 1.0)
    sd = gaussian_filter(sd, 1.5)
    if rot != 0.0:
        th = np.deg2rad(rot)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        sky2 = []
        for p in sky:
            q = dict(p); g = p["game"].copy()
            g[:, :2] = g[:, :2] @ R.T
            q["game"] = g; sky2.append(q)
        sky = sky2
    km, _ = rasterize_tris_xy(sky, origin, shape, CELL)
    kd = gaussian_filter(km.astype(np.float64), 1.5)
    ones = np.ones_like(kd)
    sA = fftconvolve(sd, ones[::-1, ::-1], mode="full")
    sA2 = fftconvolve(sd*sd, ones[::-1, ::-1], mode="full")
    sB = fftconvolve(kd, ones[::-1, ::-1], mode="full")
    sB2 = fftconvolve(kd*kd, ones[::-1, ::-1], mode="full")
    sAB = fftconvolve(sd, kd[::-1, ::-1], mode="full")
    N = fftconvolve(np.ones_like(sd), ones[::-1, ::-1], mode="full")
    Hs, Ws = kd.shape
    cov = sAB - sA*sB/N
    varA = sA2 - sA*sA/N
    varB = sB2 - sB*sB/N
    scaleA = varA.max(); scaleB = varB.max()
    varA = np.maximum(varA, 0.02*scaleA)
    varB = np.maximum(varB, 0.02*scaleB)
    Z = cov/np.sqrt(varA*varB)
    valid = N >= 0.25*kd.sum()
    Z[~valid] = -2
    k = np.unravel_index(np.argmax(Z), Z.shape)
    dy, dx = (k[0]-(Hs-1))*CELL, (k[1]-(Ws-1))*CELL
    line = f"{tag} rot={rot:+5.1f}: peak {Z[k]:+.4f} @ ({dx:+.0f},{dy:+.0f})"
    for nm, ddx, ddy in cands:
        dxc = int(round(ddx/CELL)); dyc = int(round(ddy/CELL))
        line += f"  {nm}={Z[dyc+Hs-1, dxc+Ws-1]:+.4f}"
    print(line)
    return Z[k], dx, dy


s1 = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
s2 = [p for i in range(12) for p in load_unit_game(f"street_island2_{i:02d}")]
i1 = [p for u in U1 for p in load_unit_game(u, OLD)]
i2 = [p for u in U2 for p in load_unit_game(u, OLD)]

print("== fine check island1 ==")
zncc(s1, i1, "i1 vs s1")
print("== island2 rotation sweeps ==")
for rot in (-180, -135, -90, -45, 0, 45, 90, 135, 180):
    zncc(s2, i2, "i2 vs s2", rot)
for rot in (-90, 0, 90, 180):
    zncc(s1, i2, "i2 vs s1", rot)
