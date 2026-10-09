#!/usr/bin/env python3
"""ZNCC with proper masking: find the precise best translation for
i1-vs-street1 and i2-vs-street2 (and cross terms)."""
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


def zncc(street, sky, tag, topk=5):
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    mgn = 340.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
             int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
    sd = np.zeros(shape, np.float32)
    for p in street:
        v = p["game"]
        ix = np.round((v[:, 0]-origin[0])/CELL).astype(int)
        iy = np.round((v[:, 1]-origin[1])/CELL).astype(int)
        ok = (ix >= 0) & (ix < shape[1]) & (iy >= 0) & (iy < shape[0])
        np.add.at(sd, (iy[ok], ix[ok]), 1.0)
    sd = gaussian_filter(sd, 1.5)
    km, _ = rasterize_tris_xy(sky, origin, shape, CELL)
    kd = gaussian_filter(km.astype(np.float32), 1.5)
    ones = np.ones_like(kd)
    sA = fftconvolve(sd, ones[::-1, ::-1], mode="full")
    sA2 = fftconvolve(sd*sd, ones[::-1, ::-1], mode="full")
    sB = fftconvolve(kd, ones[::-1, ::-1], mode="full")
    sB2 = fftconvolve(kd*kd, ones[::-1, ::-1], mode="full")
    sAB = fftconvolve(sd, kd[::-1, ::-1], mode="full")
    N = fftconvolve(np.ones_like(sd), ones[::-1, ::-1], mode="full")
    Hs, Ws = kd.shape
    cov = sAB - sA*sB/N
    varA = np.maximum(sA2 - sA*sA/N, 1e-6)
    varB = np.maximum(sB2 - sB*sB/N, 1e-6)
    Z = cov/np.sqrt(varA*varB)
    valid = N >= 0.25*kd.sum()          # require substantial overlap
    Z[~valid] = -2
    k = np.unravel_index(np.argmax(Z), Z.shape)
    dy, dx = (k[0]-(Hs-1))*CELL, (k[1]-(Ws-1))*CELL
    print(f"{tag}: peak ZNCC {Z[k]:+.4f} @ d=({dx:+.0f},{dy:+.0f})")
    # report ZNCC at specific candidate d
    for nm, dd in (("identity", (0, 0)), ("record TRS", (-730, -1250)),
                   ("v13 OLD", tuple(OLD[:2]))):
        dxc = int(round(dd[0]/CELL)); dyc = int(round(dd[1]/CELL))
        print(f"    @{nm:11s} ZNCC {Z[dyc+Hs-1, dxc+Ws-1]:+.4f}")
    return (dx, dy), float(Z[k])


s1 = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
s2 = [p for i in range(12) for p in load_unit_game(f"street_island2_{i:02d}")]
i1 = [p for u in U1 for p in load_unit_game(u, OLD)]
i2 = [p for u in U2 for p in load_unit_game(u, OLD)]

pk11 = zncc(s1, i1, "i1 skyline vs street1")
pk12 = zncc(s2, i1, "i1 skyline vs street2")
pk21 = zncc(s1, i2, "i2 skyline vs street1")
pk22 = zncc(s2, i2, "i2 skyline vs street2")
print("\nsummary:")
for (a, b), (d, z) in zip([("i1", "s1"), ("i1", "s2"), ("i2", "s1"),
                           ("i2", "s2")], [pk11, pk12, pk21, pk22]):
    print(f"  {a} vs {b}: ZNCC {z:+.4f} at d=({d[0]:+.0f},{d[1]:+.0f})")
