#!/usr/bin/env python3
"""S60 T3: rest-pose silhouette reference (Python rasterizer) + IoU vs the page grid.
Projection MUST match the page exactly: mesh-local (x,z), sc=min(2/w,2/h)*0.9, centered,
256x256 render -> 64x64 occupancy, grid row 0 = top (max z).
Calibration: (a) the merc's own grid vs itself = 1.0; (b) batman verts rendered with the
merc's grid = IoU must be clearly lower; (c) x-flipped merc grid vs page = must be worse.
"""
import struct, json, numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location('mv', '/tmp/my-project/scripts/s60_t3_mercval.py')

def read_bdae2_min(path):
    # reuse the parser from s60_t3_mercval (exec its top half)
    src = open('/tmp/my-project/scripts/s60_t3_mercval.py').read().split("import re\nD = ")[0]
    ns = {}
    exec(src, ns)
    return ns['read_bdae2'](path)

GRID = 64
SZ = 256

def silhouette_grid(verts, idx, flipx=False):
    x, z = verts[:, 0], verts[:, 2]
    if flipx:
        x = -x
    mnx, mxx, mnz, mxz = x.min(), x.max(), z.min(), z.max()
    sx = 2.0 / max(1e-6, mxx - mnx); sz2 = 2.0 / max(1e-6, mxz - mnz)
    sc = min(sx, sz2) * 0.9
    cx, cz = (mnx + mxx) / 2, (mnz + mxz) / 2
    X = (x - cx) * sc; Z = (z - cz) * sc
    # NDC: px = (X+1)/2*SZ ; py with +up: readPixels flip handled at grid stage
    px = (X + 1) / 2 * SZ
    py = (Z + 1) / 2 * SZ   # z-up maps to py-up
    img = np.zeros((SZ, SZ), dtype=bool)
    tri = idx.reshape(-1, 3)
    for t in tri:
        xs = px[t]; ys = py[t]
        x0, x1 = int(max(0, np.floor(xs.min()))), int(min(SZ - 1, np.ceil(xs.max())))
        y0, y1 = int(max(0, np.floor(ys.min()))), int(min(SZ - 1, np.ceil(ys.max())))
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (xs[1] - xs[0]) * (gy - ys[0]) - (ys[1] - ys[0]) * (gx - xs[0])
        e = (xs[2] - xs[1]) * (gy - ys[1]) - (ys[2] - ys[1]) * (gx - xs[1])
        f = (xs[0] - xs[2]) * (gy - ys[2]) - (ys[0] - ys[2]) * (gx - xs[2])
        inside = ((d >= 0) & (e >= 0) & (f >= 0)) | ((d <= 0) & (e <= 0) & (f <= 0))
        img[y0:y1 + 1, x0:x1 + 1] |= inside
    # grid: row 0 = top (max z) -> flip py rows
    occ = img[::-1].reshape(GRID, SZ // GRID, GRID, SZ // GRID).any(axis=(1, 3))
    # pack like the page: for gy rows, gx groups of 8, 4 sub-rows x 8 bits
    bits = np.zeros((GRID, GRID // 8), dtype=np.uint8)
    for gy in range(GRID):
        for gx in range(GRID // 8):
            b = 0
            for gy2 in range(4):
                for gx2 in range(8):
                    if occ[gy, gx * 8 + gx2]:
                        b |= 1 << (gy2 * 8 + gx2)
            bits[gy, gx] = b
    return bits, (mnx, mxx, mnz, mxz)

def bits_to_occ(bits):
    occ = np.zeros((GRID, GRID), dtype=bool)
    for gy in range(GRID):
        for gx in range(GRID // 8):
            b = bits[gy, gx]
            for gy2 in range(4):
                for gx2 in range(8):
                    if b & (1 << (gy2 * 8 + gx2)):
                        occ[gy, gx * 8 + gx2] = True
    return occ

def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0

mer = read_bdae2_min('/tmp/my-project/work/data/Bane_mercenary.bdae')
bat = read_bdae2_min('/tmp/my-project/work/data/batman.bdae')
mref, mb = silhouette_grid(mer['verts'], mer['idx'])
bref, bb = silhouette_grid(bat['verts'], bat['idx'])
mrefx, _ = silhouette_grid(mer['verts'], mer['idx'], flipx=True)
json.dump({'merc_ref_hex': mref.tobytes().hex(), 'merc_bbox': mb,
           'batman_ref_hex': bref.tobytes().hex()},
          open('/tmp/my-project/scripts/s60_t3_sil_refs.json', 'w'))
print('merc bbox (x,z):', mb, ' batman bbox:', bb)
print('self-IoU (sanity):', iou(bits_to_occ(mref), bits_to_occ(mref)))
print('merc-vs-flippedmerc IoU (orientation sensitivity):', round(iou(bits_to_occ(mref), bits_to_occ(mrefx)), 4))
print('merc-vs-batman IoU (cross null):', round(iou(bits_to_occ(mref), bits_to_occ(bref)), 4))
