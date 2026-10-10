#!/usr/bin/env python3
"""Session 16 — +36 field probe (0..3772, near-unique per segment).

Hypotheses:
  H_grid: +36 = order of segment in the bih 100x100 grid cells
          (rank correlation between +36 and grid-cell visit order)
  H_stream: +36 = batch/leaf index (monotone with dataOff stream order)
  H_build: +36 = per-building id (segments of one building share +36)
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island  # noqa: E402

ZONE = "/home/z/my-project/work/zone"


def segs_meta(island):
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        out.append(dict(id36=struct.unpack_from("<I", ld, off + 36)[0],
                        dataOff=data_off,
                        centroid=None))
    segs = parse_island(island)
    assert len(segs) == len(out)
    for m, s in zip(out, segs):
        m["centroid"] = s["pos"].mean(0)
    return out


def main():
    for island in ("GothamCity", "GothamCity_Island2"):
        meta = segs_meta(island)
        id36 = np.array([m["id36"] for m in meta])
        print(f"\n===== {island}: n={len(meta)} id36 range {id36.min()}..{id36.max()} "
              f"distinct={len(set(id36.tolist()))}")
        # duplicates?
        c = collections.Counter(id36.tolist())
        dups = sum(v - 1 for v in c.values() if v > 1)
        print(f"  duplicate ids: {dups} (near-unique = {len(set(id36.tolist()))} distinct)")

        # H_stream: correlation with dataOff order
        off = np.array([m["dataOff"] for m in meta])
        r_stream = np.corrcoef(np.argsort(np.argsort(off)).astype(float),
                               np.argsort(np.argsort(id36)).astype(float))[0, 1]
        print(f"  Spearman(id36, dataOff stream order) = {r_stream:+.4f}")

        # H_grid: bih grid cell order
        si = open(f"{ZONE}/{island}/stream_info.bin", "rb").read()
        bbox = struct.unpack_from("<6f", si, 0)
        # session 15: bih stores (x,z,y) permuted; stream_info bbox order?
        # try both; bbox = min/max triplets
        lo = np.array(bbox[:3])
        hi = np.array(bbox[3:])
        # stream_info bbox appears to be (x, y, z) extents; bih grid is x,y
        # (top-down). Build 100x100 cell ids for centroids, both axis orders.
        cents = np.array([m["centroid"] for m in meta])
        for axes in ((0, 1), (0, 2)):
            gx = np.clip(((cents[:, axes[0]] - lo[axes[0]]) /
                          max(hi[axes[0]] - lo[axes[0]], 1e-6) * 100).astype(int), 0, 99)
            gy = np.clip(((cents[:, axes[1]] - lo[axes[1]]) /
                          max(hi[axes[1]] - lo[axes[1]], 1e-6) * 100).astype(int), 0, 99)
            cell = gx * 100 + gy
            r = np.corrcoef(np.argsort(np.argsort(cell)).astype(float),
                            np.argsort(np.argsort(id36)).astype(float))[0, 1]
            print(f"  axes {axes}: Spearman(id36, cell visit order) = {r:+.4f}")
        # H_build: do segments sharing id36 share small spatial radius?
        by_id = collections.defaultdict(list)
        for m in meta:
            by_id[m["id36"]].append(m["centroid"])
        radii = []
        for i, pts in by_id.items():
            if len(pts) >= 3:
                pts = np.array(pts)
                radii.append(np.linalg.norm(pts.max(0) - pts.min(0)))
        if radii:
            print(f"  per-id spatial bbox diag: median {np.median(radii):.1f}u, "
                  f"p90 {np.percentile(radii, 90):.1f}u (n_ids={len(radii)})")


if __name__ == "__main__":
    main()
