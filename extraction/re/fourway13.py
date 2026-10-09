#!/usr/bin/env python3
"""Four-way placement test: {island1, island2} skyline x {identity, record TRS}
vs {street island1, street island2}. The right assignment should light up."""
import sys
import numpy as np
from scipy.signal import fftconvolve

sys.path.insert(0, "/home/z/my-project/scripts")
from val_skyline import (load_unit_game, vert_occupancy, rasterize_tris_xy,
                         SKY_UNITS)

OLD = np.array([-141.69, -681.15, 0.114])
TRUE = np.array([-730.0, -1250.0, 0.0])
CELL = 2.0

U1 = ["GC_island1_LongDist", "GC_LongDist_Island1_FP1",
      "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
      "GC_LongDist_Island1_Roads"]
U2 = ["GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
      "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
      "GC_LongDist_Island2_Roads"]


def local_unit(stems):
    out = []
    for u in stems:
        out += load_unit_game(u, OLD)     # GLB - OLD = local
    return out


def fft_peak(street, sky, tag):
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    allv = np.vstack([sv, lv])
    origin = allv.min(0) - 8
    shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+16)/CELL)),
             int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+16)/CELL)))
    sm = vert_occupancy(street, origin, shape, CELL)
    km, _ = rasterize_tris_xy(sky, origin, shape, CELL)
    C = fftconvolve(sm.astype(np.float32), km[::-1, ::-1].astype(np.float32),
                    mode="full")
    Hs, Ws = km.shape
    k = np.unravel_index(np.argmax(C), C.shape)
    dy, dx = k[0] - (Hs - 1), k[1] - (Ws - 1)
    base = float(np.percentile(C, 99))
    print(f"{tag:44s} peak {C[k]:10,.0f} @ d=({dx*CELL:+8.0f},{dy*CELL:+8.0f})"
          f"  p99={base:8,.0f}")
    return float(C[k])


s1 = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
s2 = [p for i in range(12) for p in load_unit_game(f"street_island2_{i:02d}")]
i1 = local_unit(U1)
i2 = local_unit(U2)

print("== island1 skyline ==")
fft_peak(s1, [dict(p, game=p["game"]) for p in i1], "i1 skyline @identity vs street1")
fft_peak(s1, [dict(p, game=p["game"] + TRUE) for p in i1], "i1 skyline @( -730,-1250) vs street1")
fft_peak(s2, [dict(p, game=p["game"]) for p in i1], "i1 skyline @identity vs street2")
fft_peak(s2, [dict(p, game=p["game"] + TRUE) for p in i1], "i1 skyline @(-730,-1250) vs street2")
print("== island2 skyline ==")
fft_peak(s1, [dict(p, game=p["game"]) for p in i2], "i2 skyline @identity vs street1")
fft_peak(s1, [dict(p, game=p["game"] + TRUE) for p in i2], "i2 skyline @(-730,-1250) vs street1")
fft_peak(s2, [dict(p, game=p["game"]) for p in i2], "i2 skyline @identity vs street2")
fft_peak(s2, [dict(p, game=p["game"] + TRUE) for p in i2], "i2 skyline @(-730,-1250) vs street2")
