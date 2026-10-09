#!/usr/bin/env python3
"""Deep diagnostic: why is there zero overlap at the decoded offset?

1. Reproduce session-12's per-chunk BBOX overlap metric (8/9 chunks, <=28k u²)
2. Direct geometry-level containment test at d=OFFSET
3. Global argmax of the street×skyline correlation map + top peaks
4. Sign/swap variants of the decoded offset
5. Scatter PNG: street verts vs skyline placed at d=OFFSET
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from val_skyline import (load_unit_game, to_game, vert_occupancy, MODELS,
                         OUT, OFFSET, SKY_UNITS)

street_chunks = [load_unit_game(f"street_island1_{i:02d}") for i in range(9)]
street = [p for ch in street_chunks for p in ch]
sky = []
for u in SKY_UNITS:
    sky += load_unit_game(u, OFFSET)
for p in sky:
    p["game"] = p["game"] - OFFSET          # local

print("=" * 72)
print("1) session-12 metric: per-chunk BBOX XY overlap with placed skyline")
print("=" * 72)
sp = [dict(game=p["game"] + OFFSET) for p in sky]   # placed
sv = np.vstack([p["game"] for p in sp])
smin, smax = sv[:, :2].min(0), sv[:, :2].max(0)
print(f"placed skyline bbox: {smin.round(1)} .. {smax.round(1)}")
tot = 0.0
for i, ch in enumerate(street_chunks):
    cv = np.vstack([p["game"] for p in ch])[:, :2]
    c0, c1 = cv.min(0), cv.max(0)
    ox = max(0.0, min(smax[0], c1[0]) - max(smin[0], c0[0]))
    oy = max(0.0, min(smax[1], c1[1]) - max(smin[1], c0[1]))
    tot += ox * oy
    print(f"  chunk {i}: bbox {c0.round(0)}..{c1.round(0)}  "
          f"bbox-overlap {ox*oy:10,.0f} u²")
print(f"  TOTAL bbox overlap: {tot:,.0f} u²")

print()
print("=" * 72)
print("2) direct geometry containment at d=OFFSET")
print("=" * 72)
allv = np.vstack([np.vstack([p["game"] for p in street])[:, :2], sv[:, :2]])
mgn = 6.0
origin = allv.min(0) - mgn
shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn))),
         int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn))))
from val_skyline import rasterize_tris_xy
sky_m, ntri = rasterize_tris_xy(sky, origin, shape)   # local frame
street_m = vert_occupancy(street, origin, shape)
print(f"sky footprint cells {sky_m.sum():,}  street vert cells "
      f"{street_m.sum():,}  grid {shape}")

def inter_cells(dxy):
    """shift sky (local) by d and count overlap with street occupancy"""
    dx, dy = int(round(dxy[0])), int(round(dxy[1]))
    H, W = sky_m.shape
    sm = np.zeros_like(street_m)
    ty0, tx0 = dy, dx
    ry0, ry1 = max(0, ty0), min(sm.shape[0], ty0 + H)
    rx0, rx1 = max(0, tx0), min(sm.shape[1], tx0 + W)
    if ry0 >= ry1 or rx0 >= rx1:
        return 0
    sm[ry0:ry1, rx0:rx1] = sky_m[ry0-ty0:ry1-ty0, rx0-tx0:rx1-tx0]
    return int((street_m & sm).sum())

d = OFFSET[:2]
print(f"direct intersection @ d={d.round(2).tolist()}: {inter_cells(d):,} cells")
print(f"direct intersection @ d=(0,0)  (local==world): {inter_cells((0,0)):,}")

print()
print("=" * 72)
print("3) global argmax of correlation map (full range)")
print("=" * 72)
from scipy.signal import fftconvolve
C = fftconvolve(street_m.astype(np.float32),
                sky_m[::-1, ::-1].astype(np.float32), mode="full")
Hs, Ws = sky_m.shape
np.save(os.path.join(OUT, "corr_global.npy"), C)
flat = C.ravel()
top = np.argpartition(flat, -8)[-8:]
top = top[np.argsort(flat[top])[::-1]]
print(f"{'rank':>4} {'d (world offset)':>28} {'cells':>12}")
seen = []
for r, fidx in enumerate(top):
    iy, ix = np.unravel_index(fidx, C.shape)
    dy, dx = iy - (Hs - 1), ix - (Ws - 1)
    print(f"{r:>4} ({dx:8.1f}, {dy:8.1f})   {flat[fidx]:12,.0f}")

print()
print("=" * 72)
print("4) sign/swap variants of the decoded offset")
print("=" * 72)
ex, ey = float(OFFSET[0]), float(OFFSET[1])
variants = {
    "decoded (-141.69,-681.15)": (ex, ey),
    "+x,+y (141.69,681.15)": (-ex, -ey),
    "(-141.69,+681.15)": (ex, -ey),
    "(+141.69,-681.15)": (-ex, ey),
    "swapped (-681.15,-141.69)": (ey, ex),
    "swapped (-681.15,+141.69)": (ey, -ex),
    "swapped (+681.15,-141.69)": (-ey, ex),
    "swapped (+681.15,+141.69)": (-ey, -ex),
}
for name, (dx, dy) in variants.items():
    print(f"  {name:30s} -> {inter_cells((dx, dy)):12,} cells")

print()
print("=" * 72)
print("5) scatter: street vs skyline at decoded placement")
print("=" * 72)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)
w = np.vstack([p["game"] for p in street])
ax.scatter(w[::17, 0], w[::17, 1], s=.2, c="green", alpha=.35,
           label="street island1 (world)")
ax.scatter(sv[::5, 0], sv[::5, 1], s=.2, c="red", alpha=.5,
           label="skyline placed @ decoded offset")
lv = np.vstack([p["game"] for p in sky])
ax.scatter(lv[::5, 0], lv[::5, 1], s=.2, c="blue", alpha=.35,
           label="skyline LOCAL frame (offset 0)")
ax.set_aspect("equal")
ax.legend(loc="best", markerscale=60)
ax.set_title("street (green) vs skyline placed (red) vs skyline local (blue)")
ax.set_xlabel("game X"); ax.set_ylabel("game Y")
fig.savefig(os.path.join(OUT, "diag_scatter.png"), dpi=130)
plt.close(fig)
print("saved diag_scatter.png")

# where would the skyline need to sit for max overlap? report centroid shift
print()
w_in = w.mean(0); l_in = lv.mean(0)
print(f"street centroid {w_in.round(1)}  skyline local centroid "
      f"{l_in.round(1)}  delta(l-st) {(l_in-w_in).round(1)}")
