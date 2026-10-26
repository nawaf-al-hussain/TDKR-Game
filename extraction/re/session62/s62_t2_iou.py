#!/usr/bin/env python3
"""S62 T2 step 5: numpy cross-check of the page's posed skinned merc.
- skin the file verts with the page's own per-frame boneMatrices
- mean vertex distance vs the page's dumped verts (per clip/frame)
- raster 256x256 with the page's projection -> 64x64 grid -> IoU vs page gridHex
- nulls: rolled-pose (90deg about Z) and Batman-mesh cross
Output: s62_t2_iou.json"""
import struct, json
import numpy as np

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0]) if False else None

cap = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_capture2.json'))
bw = cap['bw']; bmv = cap['bwVerts']; frames = cap['framesMeta'] if 'framesMeta' in cap else cap['frames']
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t3_mercval.py').read()
ns = {}
exec(src.split("if __name__")[0], ns)
skin = ns['read_bdae2']('/tmp/my-project/work/data/Bane_mercenary.bdae')
V = np.array(skin['verts'], dtype=float).reshape(-1, 3)
J = np.array(skin['skinJ'], dtype=int).reshape(-1, 4)
Wt = np.array(skin['skinW'], dtype=float).reshape(-1, 4)
NJV = len(skin['invB'])

# inverse binds used by the page = the s62 literal = inv(BIPED FK); recover from
# boneInverses dump (bisect) or recompute: page bw.boneMats = BM (col-major 16 per bone)
# BM = boneWorld x invB  =>  boneWorld = BM x invB(invB^-1)... simpler: keep BM directly:
# skinned v = sum_k w_k * (BM_k x [v,1])  (bindMatrix = I in the capture)
def mat16_to44(a):
    return np.array(a, dtype=float).reshape(4, 4).T  # column-major -> math

def skin_with(bm_flat):
    M = np.array(bm_flat, dtype=float).reshape(NJV, 4, 4)  # still col-major rows
    M = M.transpose(0, 2, 1)  # -> math (row-major) per bone
    P = np.concatenate([V, np.ones((len(V), 1))], axis=1)   # NV x 4
    out = np.zeros((len(V), 3))
    for k in range(4):
        w = Wt[:, k:k+1]
        idx = J[:, k]
        # batch: for each vertex, M[idx] @ P
        T = np.einsum('nij,nj->ni', M[idx], P)
        out += w * T[:, :3]
    return out

# rest reference = bind verts (restMaxDev 0 proves the chain)
rest = V.copy()
rmnx, rmxx = rest[:, 0].min(), rest[:, 0].max()
rmnz, rmxz = rest[:, 2].min(), rest[:, 2].max()
rsc = min(2.0 / max(1e-6, rmxx - rmnx), 2.0 / max(1e-6, rmxz - rmnz)) * 0.9
SZ, GRID = 256, 64
IDXF = np.array(skin['idx'], dtype=int)
TRIS = IDXF[:(len(IDXF) // 3) * 3].reshape(-1, 3)  # page draws TRIANGLES (partial last dropped)

def raster_grid(verts, pelvis_xy):
    # raster triangles into a 256x256 mask, then downsample to 64x64 (page grid layout)
    img = np.zeros((SZ, SZ), dtype=bool)
    x = (verts[:, 0] - pelvis_xy[0]) * rsc
    z = (verts[:, 2] - pelvis_xy[1]) * rsc
    px = (x * 0.5 + 0.5) * (SZ - 1)
    py = (z * 0.5 + 0.5) * (SZ - 1)
    for t in TRIS:
        xs = px[t]; ys = py[t]
        x0, x1 = int(max(0, xs.min())), int(min(SZ - 1, xs.max()) + 1)
        y0, y1 = int(max(0, ys.min())), int(min(SZ - 1, ys.max()) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        d = (xs[1]-xs[0])*(ys[2]-ys[0]) - (xs[2]-xs[0])*(ys[1]-ys[0])
        if abs(d) < 1e-12:
            continue
        w0 = ((xs[1]-gx)*(ys[2]-gy) - (xs[2]-gx)*(ys[1]-gy)) / d
        w1 = ((xs[2]-gx)*(ys[0]-gy) - (xs[0]-gx)*(ys[2]-gy)) / d
        w2 = 1 - w0 - w1
        m = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
        img[y0:y1, x0:x1] |= m
    occ = img[::-1].reshape(GRID, SZ // GRID, GRID, SZ // GRID).any(axis=(1, 3))
    bits = np.zeros((GRID, GRID // 8), dtype=np.int64)
    for gy in range(GRID):
        for gx in range(GRID // 8):
            b = 0
            for gy2 in range(4):
                for gx2 in range(8):
                    if occ[gy, gx * 8 + gx2]:
                        b |= 1 << (gy2 * 8 + gx2)
            bits[gy, gx] = b
    grid = bits.tolist()
    return grid
    return grid

def grid_to_mask(grid):
    m = np.zeros((GRID, GRID), dtype=bool)
    for gy, row in enumerate(grid):
        for gxi, word in enumerate(row):
            for gx2 in range(8):
                if word >> gx2 & 1:
                    m[gy, gxi * 8 + gx2] = True
    return m

def page_grid_to_mask(hexstr):
    m = np.zeros((GRID, GRID), dtype=bool)
    for gy in range(GRID):
        row = hexstr[gy*(GRID//8)*8:(gy+1)*(GRID//8)*8]
        for gxi in range(GRID // 8):
            word = int(row[gxi*8:(gxi+1)*8], 16)
            for gx2 in range(8):
                if word >> gx2 & 1:
                    m[gy, gxi * 8 + gx2] = True
    return m

def pelvis_xy_from_bm(bm_flat):
    # boneWorld = BM x invB -> pelvis world translation: use boneMatrices of joint 0 with invB
    # easier: skinned pelvis = weighted centroid of joint-0 weights is close; but page used the BONE world.
    # BM_0 x invB_0: invB_0 = the page literal (first 16 floats)
    inv0 = np.array(IBMLIT[0:16], dtype=float).reshape(4, 4).T
    bm0 = mat16_to44(bm_flat[0:16])
    W0 = bm0 @ np.linalg.inv(inv0)
    return W0[0, 3], W0[2, 3]

IBMLIT = json.load(open('/home/z/my-project/scripts/s62_t2_ibm_literal.json'))

def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0

rows = []
null_rolled = []
for key in sorted(bmv.keys()):
    if '@' not in key:
        continue
    clip, frac = key.rsplit('@', 1)
    page_v = np.array(bmv[key], dtype=float).reshape(-1, 3)
    bm = bw['boneMats'][key]
    npv = skin_with(bm)
    dist = float(np.abs(npv - page_v).mean())
    # pelvis: boneMatrices of joint0 x invB -> world
    inv0 = np.array(IBMLIT[0:16], dtype=float).reshape(4, 4).T
    bm0 = mat16_to44(bm[0:16])
    W0 = bm0 @ np.linalg.inv(inv0)   # MW_0 = BM_0 x invB_0^-1
    pxy = (W0[0, 3], W0[2, 3])
    g_np = raster_grid(npv, pxy)
    fr = frames[clip][int(round((float(frac) - 0.25) / 0.25))]
    g_pg = page_grid_to_mask(fr['gridHex'])
    g_npm = grid_to_mask(g_np)
    v = iou(g_npm, g_pg)
    # rolled-pose null: rotate numpy skin 90 deg about Z (vertical) through pelvis
    c, s = np.cos(np.pi / 2), np.sin(np.pi / 2)
    Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    rolled = (npv - [pxy[0], 0, pxy[1]]) @ Rz.T + [pxy[0], 0, pxy[1]]
    g_rl = grid_to_mask(raster_grid(rolled, pxy))
    null_rolled.append(iou(g_rl, g_pg))
    rows.append({'clip': clip, 'frac': frac, 'meanVertDist': round(dist, 4),
                 'iou': round(v, 4), 'litPage': fr['lit'],
                 'litNumpy': int(g_npm.sum()), 'nVerts': len(V)})
    print(f"{clip:26s}@{frac}: dist={dist:.4f} IoU={v:.4f} (page lit {fr['lit']}, numpy lit {g_npm.sum()})")

print('\nrolled-pose null IoUs:', [round(x, 4) for x in null_rolled])
print('mean IoU:', round(float(np.mean([r['iou'] for r in rows])), 4),
      ' mean dist:', round(float(np.mean([r['meanVertDist'] for r in rows])), 4))
json.dump({'rows': rows, 'nullRolled': [round(x, 4) for x in null_rolled]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_iou.json', 'w'), indent=1)
print('saved')
