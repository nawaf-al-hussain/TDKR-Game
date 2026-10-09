#!/usr/bin/env python3
"""Final validation: skyline placed at the TRUE 0x14051 record TRS
(-730, -1250, 0) vs street tier — FFT overlap sweep (Claude test 1),
plus island2 record from GothamCity_Island2.lvc and the top-down plot."""
import json
import os
import struct
import sys

import numpy as np
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from val_skyline import (load_unit_game, vert_occupancy, rasterize_tris_xy,
                         MODELS, OUT, SKY_UNITS)

CELL = 1.0
TRUE1 = np.array([-730.0, -1250.0, 0.0])

# ---------------- island2 lvc record ----------------
print("=" * 72)
print("island2: scan GothamCity_Island2.lvc for 0x14051 record")
print("=" * 72)
d2 = open("/home/z/my-project/download/TDKR_assets/raw/game_config/"
          "GothamCity_Island2.lvc", "rb").read()
tbl2 = struct.unpack_from(">I", d2, 4)[0]


def parse_strings(d):
    tbl = struct.unpack_from(">I", d, 4)[0]
    pos = tbl
    n = struct.unpack_from(">i", d, pos)[0]
    pos += 4
    out = []
    for i in range(n):
        ln = struct.unpack_from(">i", d, pos)[0]
        pos += 4
        out.append(d[pos:pos + ln].decode("utf-8", "replace"))
        pos += ln
    return out


s2 = parse_strings(d2)
print(f"island2 lvc: {len(s2)} strings")
TRUE2 = None
for tid in (0x14051,):
    pat = struct.pack(">I", tid)
    s = 9
    while True:
        j = d2.find(pat, s, tbl2)
        if j < 0:
            break
        p = j + 4
        b = d2[p]; p += 1
        oid = struct.unpack_from(">i", d2, p)[0]; p += 4
        trs = struct.unpack_from(">9f", d2, p); p += 36
        bl = d2[p:p + 3]; p += 3
        nm = struct.unpack_from(">i", d2, p)[0]; p += 4
        ch = d2[p:p + 4]; p += 4
        nm_s = s2[nm] if 0 <= nm < len(s2) else f"<{nm}>"
        print(f"  0x14051 @{j:#x}: bool={b} objId={oid} TRS="
              f"{[round(v,4) for v in trs]} bools={list(bl)} "
              f"mesh={nm_s!r} chars={ch.hex()}")
        if "island2" in nm_s.lower() and TRUE2 is None:
            TRUE2 = np.array(list(trs[0:3]) + [0.0])
        s = j + 4
    # also 0x14050 reflection records count
if TRUE2 is None:
    TRUE2 = np.zeros(3)

# ---------------- overlap test, island 1 ----------------
print()
print("=" * 72)
print("island1: skyline @ TRUE offset (-730,-1250,0) vs street — FFT sweep")
print("=" * 72)
OLD = np.array([-141.69, -681.15, 0.114])   # the WRONG v13 offset (shipped GLBs)
TRUE1 = np.array([-730.0, -1250.0, 0.0])    # the 0x14051 record TRS
street = [p for i in range(9) for p in load_unit_game(f"street_island1_{i:02d}")]
sky = []
for u in SKY_UNITS:
    sky += load_unit_game(u, OLD)     # subtract the OLD v13 offset -> LOCAL
for p in sky:
    p["game"] = p["game"] + TRUE1     # place at the 0x14051 record TRS
sv = np.vstack([p["game"] for p in street])[:, :2]
lv = np.vstack([p["game"] for p in sky])[:, :2]
print(f"street XY bbox {sv.min(0).round(1)}..{sv.max(0).round(1)}")
print(f"skyline placed XY bbox {lv.min(0).round(1)}..{lv.max(0).round(1)}")

allv = np.vstack([sv, lv])
mgn = 6.0
origin = allv.min(0) - mgn
shape = (int(np.ceil((allv[:, 1].max()-allv[:, 1].min()+2*mgn)/CELL)),
         int(np.ceil((allv[:, 0].max()-allv[:, 0].min()+2*mgn)/CELL)))
street_m = vert_occupancy(street, origin, shape, CELL)
sky_m, ntri = rasterize_tris_xy(sky, origin, shape, CELL)
print(f"street cells {street_m.sum():,}  skyline footprint cells "
      f"{sky_m.sum():,}")
C = fftconvolve(street_m.astype(np.float32),
                sky_m[::-1, ::-1].astype(np.float32), mode="full")
Hs, Ws = sky_m.shape

def val_at(dxw, dyw):
    dxc = int(round(dxw / CELL)); dyc = int(round(dyw / CELL))
    return float(C[dyc + Hs - 1, dxc + Ws - 1])

pk_new = val_at(0.0, 0.0)   # TRUE offset == d0 (sky already placed at TRUE)
pk_old = val_at(*( (OLD - TRUE1)[:2] ))  # old offset relative to TRUE
print(f"\nintersection @ TRUE (d=0):       {pk_new:12,.0f} cells")
print(f"intersection @ OLD v13 offset:   {pk_old:12,.0f} cells")
i0 = int(round(0.0/CELL)) + Hs - 1
j0 = int(round(0.0/CELL)) + Ws - 1
win = C[i0-60:i0+61, j0-60:j0+61]
kk = np.unravel_index(np.argmax(win), win.shape)
print(f"argmax within ±60 of TRUE: d = ({kk[1]-60:+d}, {kk[0]-60:+d}) cells")
print("\nslices around TRUE (d = TRUE + delta):")
for ax, deltas in (("X", [-60,-40,-20,-10,-5,-2,-1,0,1,2,5,10,20,40,60]),):
    row = {}
    for dx in deltas:
        row[dx] = val_at(dx, 0)
    print("  dX:", {k: f"{v:,.0f}" for k, v in row.items()})
col = {}
for dy in [-60,-40,-20,-10,-5,-2,-1,0,1,2,5,10,20,40,60]:
    col[dy] = val_at(0, dy)
print("  dY:", {k: f"{v:,.0f}" for k, v in col.items()})

# sharpness: half-max widths
def width(dct):
    ks = sorted(dct); pk = dct[0]
    for a, b in zip(ks, ks[1:]):
        if (dct[a] >= pk/2 >= dct[b]) or (dct[b] >= pk/2 >= dct[a]):
            return (a, b)
    return None
wx = width({k: val_at(k, 0) for k in range(-120, 121)})
wy = width({k: val_at(0, k) for k in range(-120, 121)})
print(f"half-max drop crossings: X {wx}  Y {wy}")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8.5, 7), constrained_layout=True)
ext = [-60, 60, -60, 60]
im = ax.imshow(win, origin="lower", extent=ext, cmap="inferno",
               aspect="equal")
ax.plot(0, 0, "c+", ms=14, mew=2, label="decoded 0x14051 TRS (-730,-1250)")
fig.colorbar(im, ax=ax, label="overlap cells")
ax.set_xlabel("ΔX (units)"); ax.set_ylabel("ΔY (units)")
ax.set_title("Island-1 skyline @ 0x14051 record — overlap vs offset\n"
             "(CComponentMesh name = gc_island1_longdist.bdae)")
ax.legend(loc="upper left", fontsize=8)
fig.savefig(os.path.join(OUT, "final_sweep_true_offset.png"), dpi=150)
plt.close(fig)

# rotation sweep at TRUE offset
print("\nrotation sweep ±5° at TRUE translation:")
best = (0.0, None)
res = {}
for th in [-5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 4, 5]:
    R = np.array([[np.cos(np.deg2rad(th)), -np.sin(np.deg2rad(th))],
                  [np.sin(np.deg2rad(th)), np.cos(np.deg2rad(th))]])
    sky_r = []
    for p in sky:
        q = dict(p); g = p["game"].copy()
        g[:, :2] = g[:, :2] @ R.T
        q["game"] = g; sky_r.append(q)
    sm, _ = rasterize_tris_xy(sky_r, origin, shape, CELL)
    Cr = fftconvolve(street_m.astype(np.float32),
                     sm[::-1, ::-1].astype(np.float32), mode="full")
    v = float(Cr[i0, j0])
    res[th] = v
    print(f"  θ={th:5.1f}°  overlap {v:12,.0f} ({100*v/max(pk_new,1):6.2f}%)")

# ---------------- top-down plot ----------------
fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)
w = np.vstack([p["game"] for p in street])
ax.scatter(w[::17, 0], w[::17, 1], s=.2, c="green", alpha=.35,
           label="street island1 (world)")
ax.scatter(lv[::5, 0], lv[::5, 1], s=.2, c="red", alpha=.5,
           label="skyline @ 0x14051 TRS (-730,-1250)")
ax.set_aspect("equal")
ax.legend(loc="best", markerscale=60)
ax.set_xlabel("game X"); ax.set_ylabel("game Y")
ax.set_title("Island-1 skyline placed by the lvc 0x14051 LowPolyLongDistance record")
fig.savefig(os.path.join(OUT, "final_overlay_true.png"), dpi=130)
plt.close(fig)

json.dump(dict(true_offset=[-730.0, -1250.0, 0.0],
               peak_true=pk_new, peak_old_v13=pk_old,
               argmax_win60=[int(kk[1]-60), int(kk[0]-60)],
               half_width_x=wx, half_width_y=wy,
               rotation={str(k): v for k, v in res.items()},
               island2_record=None if TRUE2 is None else TRUE2.tolist()),
          open(os.path.join(OUT, "final_validation.json"), "w"), indent=1)
print("\nsaved final_sweep_true_offset.png / final_overlay_true.png / "
      "final_validation.json")
