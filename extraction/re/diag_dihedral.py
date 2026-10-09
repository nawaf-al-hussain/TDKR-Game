#!/usr/bin/env python3
"""Dihedral + rotation sweep: find the transform that actually aligns the
island-1 skyline local frame with the street-tier world frame.

Candidates (applied to skyline local game XY, then + translation d):
  id, flipY (x,-y), flipX (-x,y), rot180, transpose (y,x), rot90 (y,-x),
  rot270 (-y,x), anti-transpose (-y,-x)
Plus continuous rotation 0..359 deg in 1-deg steps (no mirror).
Metric: street vertex occupancy  vs  filled skyline footprint, FFT
cross-correlation; report global argmax + sharpness.
"""
import os
import sys

import numpy as np
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from val_skyline import (load_unit_game, vert_occupancy, rasterize_tris_xy,
                         OUT, OFFSET, SKY_UNITS)

CELL = 2.0

street = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
sky = []
for u in SKY_UNITS:
    sky += load_unit_game(u, OFFSET)
for p in sky:
    p["game"] = p["game"] - OFFSET

sv = np.vstack([p["game"] for p in street])[:, :2]
lv = np.vstack([p["game"] for p in sky])[:, :2]
allv = np.vstack([sv, lv])
mgn = 8.0
origin = allv.min(0) - mgn
shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
         int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
print(f"grid {shape} @ {CELL}u")
street_m = vert_occupancy(street, origin, shape, CELL)
print(f"street cells {street_m.sum():,}")

def apply_T(prims, T):
    out = []
    for p in prims:
        q = dict(p)
        g = p["game"].copy()
        xy = g[:, :2]
        g[:, 0] = T[0][0]*xy[:, 0] + T[0][1]*xy[:, 1]
        g[:, 1] = T[1][0]*xy[:, 0] + T[1][1]*xy[:, 1]
        q["game"] = g
        out.append(q)
    return out

CANDS = {
    "id        (x, y)":  [[1, 0], [0, 1]],
    "flipY     (x,-y)":  [[1, 0], [0, -1]],
    "flipX    (-x, y)":  [[-1, 0], [0, 1]],
    "rot180  (-x,-y)":  [[-1, 0], [0, -1]],
    "transpose(y, x)":  [[0, 1], [1, 0]],
    "rot90    (y,-x)":  [[0, 1], [-1, 0]],
    "rot270   (-y, x)": [[0, -1], [1, 0]],
    "antiTr   (-y,-x)": [[0, -1], [-1, 0]],
}

results = {}
for name, T in CANDS.items():
    sp = apply_T(sky, T)
    sm, _ = rasterize_tris_xy(sp, origin, shape, CELL)
    C = fftconvolve(street_m.astype(np.float32),
                    sm[::-1, ::-1].astype(np.float32), mode="full")
    Hs, Ws = sm.shape
    k = np.unravel_index(np.argmax(C), C.shape)
    dy, dx = k[0] - (Hs - 1), k[1] - (Ws - 1)
    peak = float(C[k])
    p95 = float(np.percentile(C, 95))
    results[name] = dict(peak=peak, d=(int(dx*CELL), int(dy*CELL)),
                         sharp=peak/max(p95, 1))
    print(f"{name:18s} peak {peak:10,.0f}  d=({dx*CELL:7.0f},{dy*CELL:7.0f})"
          f"  peak/p95 {peak/max(p95,1):7.1f}")

best = max(results, key=lambda k: results[k]["peak"])
print(f"\nBEST (mirror family): {best}  -> {results[best]}")

# ---- continuous rotation sweep (no mirror) ----
print("\nrotation sweep 0..359 deg, 1-deg steps (translation re-optimized "
      "globally per angle):")
best_rot = (None, 0.0, None)
rot_curve = []
for th in range(0, 360, 1):
    c, s = np.cos(np.deg2rad(th)), np.sin(np.deg2rad(th))
    T = [[c, -s], [s, c]]
    sp = apply_T(sky, T)
    sm, _ = rasterize_tris_xy(sp, origin, shape, CELL)
    C = fftconvolve(street_m.astype(np.float32),
                    sm[::-1, ::-1].astype(np.float32), mode="full")
    Hs, Ws = sm.shape
    k = np.unravel_index(np.argmax(C), C.shape)
    dy, dx = k[0] - (Hs - 1), k[1] - (Ws - 1)
    peak = float(C[k])
    rot_curve.append((th, peak, dx*CELL, dy*CELL))
    if peak > best_rot[1]:
        best_rot = (th, peak, (dx*CELL, dy*CELL))
rc = np.array([(a, b) for a, b, _, _ in rot_curve])
top5 = sorted(rot_curve, key=lambda r: -r[1])[:5]
print("top-5 angles:")
for th, peak, dx, dy in top5:
    print(f"  θ={th:3d}°  peak {peak:10,.0f}  d=({dx:.0f},{dy:.0f})")
print(f"best rotation: θ={best_rot[0]}° peak {best_rot[1]:,.0f} "
      f"d={best_rot[2]}")
np.save(os.path.join(OUT, "rot_curve.npy"), rc)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax.plot(rc[:, 0], rc[:, 1], lw=1)
for th, peak, _, _ in top5:
    ax.annotate(f"{th}°", (th, peak), fontsize=8,
                xytext=(0, 6), textcoords="offset points")
ax.set_xlabel("rotation θ (deg)")
ax.set_ylabel("global peak overlap cells")
ax.set_title("skyline→street alignment vs rotation (translation optimized "
             "per angle)")
fig.savefig(os.path.join(OUT, "rot_sweep.png"), dpi=140)
plt.close(fig)
print("saved rot_sweep.png")
