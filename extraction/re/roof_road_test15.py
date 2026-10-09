#!/usr/bin/env python3
"""Task 3: sharper negative test — sweep translation, measure the fraction of
STREET-TIER ROAD vertices falling inside SKYLINE ROOF footprints.

Everything in GAME coords via val_skyline (session-13/14 verified loaders).
Road selection is engine-derived: segment descriptor +40 = material index
(proven this session: range 0..305 < 307) -> materials.bdae sampler chain:
road materials = LightMap is the Roads0 bake page (the road surface is the
bake paint) or DiffuseMap is road-named; trunk material excluded; ground
level |z| < 12.
Roofs: GC_island1_LongDist assembly XY projection (shipped GLB already
world-placed at the record TRS (-730,-1250,0)).
"""
import glob
import json
import os
import struct
import sys

import numpy as np

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import MODELS, load_glb_prims_full_named, to_game  # noqa

ZONE = "/home/z/my-project/work/zone"


def main():
    island = "GothamCity"
    # segment -> material index (descriptor +40)
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    N = struct.unpack_from("<I", lt, 0)[0]
    seg_mat = {}
    for i in range(N):
        off, sz = struct.unpack_from("<2I", lt, 4 + 8 * i)
        seg_mat[i] = struct.unpack_from("<I", ld, off + 40)[0]

    # road materials: LightMap = Roads0 page or DiffuseMap road-named
    db = json.load(open(f"{RE}/mat_tex_{island}.json"))
    road = set()
    for i, m in enumerate(db["mats"]):
        lm = m.get("LightMap") or ""
        dm = m.get("DiffuseMap") or ""
        if ("Roads0" in lm or "road" in dm.lower() or "crossing" in dm.lower()) \
                and "trunk" not in dm.lower():
            road.add(i)
    print(f"road material set ({len(road)}): {sorted(road)}")

    road_v, all_v = [], []
    for f in sorted(glob.glob(f"{MODELS}/street_island1_*.glb")):
        for nm, pos, idx in load_glb_prims_full_named(f, None):
            g = to_game(pos)
            all_v.append(g)
            sid = int(nm.split("_")[1]) if nm.startswith("seg_") else -1
            if seg_mat.get(sid) in road and np.abs(g[:, 2]).max() < 12:
                road_v.append(g)
    road_v = np.concatenate(road_v)
    all_v = np.concatenate(all_v)
    print(f"street verts {len(all_v):,}; road verts {len(road_v):,}")
    print(f"road z {road_v[:,2].min():.2f}..{road_v[:,2].max():.2f}; "
          f"x {road_v[:,0].min():.0f}..{road_v[:,0].max():.0f} "
          f"y {road_v[:,1].min():.0f}..{road_v[:,1].max():.0f}")

    # roofs (assembly, game coords, world-placed)
    rp = []
    for nm, pos, idx in load_glb_prims_full_named(
            f"{MODELS}/GC_island1_LongDist.glb", None):
        rp.append(to_game(pos))
    roofs = np.concatenate(rp)
    print(f"roof verts {len(roofs):,}; "
          f"x {roofs[:,0].min():.0f}..{roofs[:,0].max():.0f} "
          f"y {roofs[:,1].min():.0f}..{roofs[:,1].max():.0f} "
          f"z {roofs[:,2].min():.0f}..{roofs[:,2].max():.0f}")

    # rasterize roof XY
    cell = 2.0
    mn = (np.floor(np.array([roofs[:, 0].min(), roofs[:, 1].min()])
                   / cell).astype(int) - 2)
    mx = (np.ceil(np.array([roofs[:, 0].max(), roofs[:, 1].max()])
                  / cell).astype(int) + 2)
    W = mx - mn
    mask = np.zeros((int(W[1]), int(W[0])), dtype=bool)
    ix = (roofs[:, 0] / cell).astype(int) - mn[0]
    iy = (roofs[:, 1] / cell).astype(int) - mn[1]
    ok = (ix >= 0) & (iy >= 0) & (ix < W[0]) & (iy < W[1])
    mask[iy[ok], ix[ok]] = True
    m2 = mask.copy()
    m2[1:, :] |= mask[:-1, :]
    m2[:-1, :] |= mask[1:, :]
    m2[:, 1:] |= mask[:, :-1]
    m2[:, :-1] |= mask[:, 1:]
    mask = m2
    print(f"roof mask {W[0]}x{W[1]} @ {cell}u fill {mask.mean():.3f}")

    gx = (road_v[:, 0] / cell).astype(int) - mn[0]
    gy = (road_v[:, 1] / cell).astype(int) - mn[1]

    steps = list(range(-30, 31, 1))  # ±60u at 2u steps
    grid = np.full((len(steps), len(steps)), np.nan)
    best = None
    for a, dx in enumerate(steps):
        for b, dy in enumerate(steps):
            xx = gx + dx
            yy = gy + dy
            okk = (xx >= 0) & (yy >= 0) & (xx < W[0]) & (yy < W[1])
            frac = float(mask[yy[okk], xx[okk]].mean()) if okk.any() else 1.0
            grid[a, b] = frac
            if best is None or frac < best[0]:
                best = (frac, dx * cell, dy * cell)
    at_record = grid[30, 30]
    nb = grid[24:37, 24:37]
    print(f"\nfraction road-in-roof @ record (0,0): {at_record:.4f}")
    print(f"global min {best[0]:.4f} at ({best[1]:+.0f},{best[2]:+.0f})")
    print(f"record nb (±12u): min {np.nanmin(nb):.4f} max {np.nanmax(nb):.4f}")
    print(f"landscape: mean {np.nanmean(grid):.4f} "
          f"p10 {np.nanpercentile(grid,10):.4f} "
          f"p90 {np.nanpercentile(grid,90):.4f}")
    json.dump(dict(at_record=float(at_record),
                   global_min=[float(best[0]), float(best[1]), float(best[2])],
                   nb_min=float(np.nanmin(nb)), nb_max=float(np.nanmax(nb)),
                   landscape_mean=float(np.nanmean(grid)),
                   p10=float(np.nanpercentile(grid, 10)),
                   p90=float(np.nanpercentile(grid, 90)),
                   n_road=int(len(road_v)), road_mats=sorted(road)),
              open(f"{RE}/roof_road_test15.json", "w"), indent=1)
    print("saved roof_road_test15.json")


if __name__ == "__main__":
    main()
