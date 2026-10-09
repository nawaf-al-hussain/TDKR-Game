#!/usr/bin/env python3
"""Sharp placement metric: zero-normalized cross-correlation (ZNCC) of
density maps (street vertex density vs skyline roof-area density) over a
+/-320u translation window, for all four island/street combos."""
import sys
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter

sys.path.insert(0, "/home/z/my-project/scripts")
from val_skyline import load_unit_game, vert_occupancy, rasterize_tris_xy

OLD = np.array([-141.69, -681.15, 0.114])
TRUE = np.array([-730.0, -1250.0, 0.0])
CELL = 2.0
U1 = ["GC_island1_LongDist", "GC_LongDist_Island1_FP1",
      "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
      "GC_LongDist_Island1_Roads"]
U2 = ["GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
      "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
      "GC_LongDist_Island2_Roads"]


def zncc_map(street, sky):
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    mgn = 340.0
    origin = allv.min(0) - mgn
    shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
             int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
    # street density
    sd = np.zeros(shape, np.float32)
    for p in street:
        v = p["game"]
        ix = np.round((v[:, 0]-origin[0])/CELL).astype(int)
        iy = np.round((v[:, 1]-origin[1])/CELL).astype(int)
        ok = (ix >= 0) & (ix < shape[1]) & (iy >= 0) & (iy < shape[0])
        np.add.at(sd, (iy[ok], ix[ok]), 1.0)
    sd = gaussian_filter(sd, 1.5)
    # skyline roof-area density (filled)
    km, _ = rasterize_tris_xy(sky, origin, shape, CELL)
    kd = gaussian_filter(km.astype(np.float32), 1.5)
    # ZNCC via FFT: (A-avgA local)*(B-avgB) / (|A|*|B|)
    ones = np.ones_like(kd)
    n = kd.size
    sA = fftconvolve(sd, ones[::-1, ::-1], mode="full")
    sA2 = fftconvolve(sd**2, ones[::-1, ::-1], mode="full")
    sB = fftconvolve(kd, ones[::-1, ::-1], mode="full")
    sB2 = fftconvolve(kd**2, ones[::-1, ::-1], mode="full")
    sAB = fftconvolve(sd, kd[::-1, ::-1], mode="full")
    Hs, Ws = kd.shape
    N = fftconvolve(ones, ones[::-1, ::-1], mode="full")
    cov = sAB - sA*sB/N
    varA = sA2 - sA**2/N
    varB = sB2 - sB**2/N
    denom = np.sqrt(np.maximum(varA*varB, 1e-9))
    Z = cov/denom
    return Z, origin, shape, Hs, Ws, sd, kd


def report(street, sky_base, tag, deltas):
    Z, origin, shape, Hs, Ws, sd, kd = zncc_map(street, sky_base)
    out = {}
    for name, dxy in deltas.items():
        dxc = int(round(dxy[0]/CELL)); dyc = int(round(dxy[1]/CELL))
        out[name] = float(Z[dyc+Hs-1, dxc+Ws-1])
    k = np.unravel_index(np.argmax(Z), Z.shape)
    dy, dx = (k[0]-(Hs-1))*CELL, (k[1]-(Ws-1))*CELL
    print(f"{tag}")
    for name, v in out.items():
        print(f"    {name:34s} ZNCC {v:+.4f}")
    print(f"    global ZNCC peak {Z[k]:+.4f} @ d=({dx:+.0f},{dy:+.0f})")
    return out


s1 = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
s2 = [p for i in range(12) for p in load_unit_game(f"street_island2_{i:02d}")]
i1 = [p for u in U1 for p in load_unit_game(u, OLD)]
i2 = [p for u in U2 for p in load_unit_game(u, OLD)]

deltas = {
    "identity (d=0)": (0.0, 0.0),
    "record TRS d=(-730,-1250)": (-730.0, -1250.0),
    "v13 OLD d=(-141.69,-681.15)": (float(OLD[0]), float(OLD[1])),

}

print("=" * 74)
print("ZNCC placement test (local frame + translation d)")
print("=" * 74)
report(s1, i1, "island-1 skyline vs street-1:", deltas)
report(s2, i1, "island-1 skyline vs street-2:", deltas)
report(s1, i2, "island-2 skyline vs street-1:", deltas)
report(s2, i2, "island-2 skyline vs street-2:", deltas)
