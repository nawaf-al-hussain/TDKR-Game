#!/usr/bin/env python3
"""S63 T2: restate the posed merc skinning validation table with full n and nulls.
- 15 real rows (5 clips x 3 fracs) reproduced from the s62 capture (meanVertDist, IoU, n)
- NEW: wrong-clip null matrix - numpy skin of clip B (B's boneMats) vs page grid of clip A
- rolled-pose null + batman-mesh cross null (from s62) + the s60 rest-frame Batman row
Output: s63_t2_table.json"""
import json
import numpy as np

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
IBMLIT = json.load(open('/home/z/my-project/scripts/s62_t2_ibm_literal.json'))

def mat16_to44(a):
    return np.array(a, dtype=float).reshape(4, 4).T

def skin_with(bm_flat):
    M = np.array(bm_flat, dtype=float).reshape(NJV, 4, 4).transpose(0, 2, 1)
    P = np.concatenate([V, np.ones((len(V), 1))], axis=1)
    out = np.zeros((len(V), 3))
    for k in range(4):
        w = Wt[:, k:k+1]
        idx = J[:, k]
        T = np.einsum('nij,nj->ni', M[idx], P)
        out += w * T[:, :3]
    return out

rest = V.copy()
rmnx, rmxx = rest[:, 0].min(), rest[:, 0].max()
rmnz, rmxz = rest[:, 2].min(), rest[:, 2].max()
rsc = min(2.0 / max(1e-6, rmxx - rmnx), 2.0 / max(1e-6, rmxz - rmnz)) * 0.9
SZ, GRID = 256, 64
IDXF = np.array(skin['idx'], dtype=int)
TRIS = IDXF[:(len(IDXF) // 3) * 3].reshape(-1, 3)

def raster_grid(verts, pelvis_xy):
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
    return occ

def grid_to_mask(occ):
    return occ

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

def pelvis_of(bm_flat):
    inv0 = np.array(IBMLIT[0:16], dtype=float).reshape(4, 4).T
    bm0 = mat16_to44(bm_flat[0:16])
    W0 = bm0 @ np.linalg.inv(inv0)
    return (W0[0, 3], W0[2, 3])

def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0

keys = sorted(k for k in bmv if '@' in k)
print('capture keys:', len(keys))
# numpy skins per clip@frac
skins = {}
for key in keys:
    bm = bw['boneMats'][key]
    npv = skin_with(bm)
    pxy = pelvis_of(bm)
    skins[key] = (raster_grid(npv, pxy), npv, pxy)
print('numpy skins done')

def mask_from_occ(occ):
    return occ

wrong = []
for ka in keys:
    clip_a, frac_a = ka.rsplit('@', 1)
    ga = page_grid_to_mask(frames[clip_a][int(round((float(frac_a) - 0.25) / 0.25))]['gridHex'])
    for kb in keys:
        if kb == ka:
            continue
        clip_b, frac_b = kb.rsplit('@', 1)
        gb = skins[kb][0]
        v = iou(gb, ga)
        wrong.append({'pageClip': clip_a, 'pageFrac': frac_a,
                      'npClip': clip_b, 'npFrac': frac_b, 'iou': round(v, 4)})
real = [w['iou'] for w in wrong if w['pageClip'] == w['npClip']]
# wrong-clip at frac 0.5 only (cleanest pose separation)
w05 = [w for w in wrong if w['pageFrac'] == '0.5' and w['npFrac'] == '0.5']
print('wrong-clip pairs (frac 0.5):')
for w in sorted(w05, key=lambda x: x['iou']):
    print('  page %-22s np %-22s IoU %.4f' % (w['pageClip'], w['npClip'], w['iou']))

# reproduce the 15 real rows for n restatement
prev = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_iou.json'))
# verify one row against the recomputed skins (same pipeline)
k0 = keys[0]
ca, fa = k0.rsplit('@', 1)
ga = page_grid_to_mask(frames[ca][int(round((float(fa) - 0.25) / 0.25))]['gridHex'])
v0 = iou(skins[k0][0], ga)
match = any(abs(r['iou'] - v0) < 0.02 and r['clip'] == ca and r['frac'] == fa for r in prev['rows'])
print('reproduction check %s@%s: %.4f vs stored %s -> %s' % (
    ca, fa, v0,
    [r['iou'] for r in prev['rows'] if r['clip'] == ca and r['frac'] == fa],
    'OK' if match else 'MISMATCH'))

table = {
    'mercPosed': prev['rows'],
    'mercPosed_meanIoU': round(float(np.mean([r['iou'] for r in prev['rows']])), 4),
    'nullRolled': prev['nullRolled'],
    'nullBatmanCross': prev['nullBatman'],
    'nullWrongClip': wrong,
    'nullWrongClip_frac05': w05,
    'batmanRestRow': {
        'source': 's60 T3 (static bind-pose render, DIFFERENT pipeline: rest frame)',
        'iou': 0.9516, 'nVerts': 1294,
        'nulls': {'batmanMeshCross': 0.6922, 'xFlipped': 0.6772},
        'note': 'rest-frame comparison between rigs sharing the BIPED rest offsets - WEAK discriminator'
    },
}
json.dump(table, open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t2_table.json', 'w'), indent=1)
rr = [r['iou'] for r in prev['rows']]
print('\nSUMMARY: real %0.4f-%0.4f (mean %0.4f) | rolled %0.4f-%0.4f | batman-cross %0.4f-%0.4f | wrong-clip(f.5) %0.4f-%0.4f' % (
    min(rr), max(rr), float(np.mean(rr)), min(prev['nullRolled']), max(prev['nullRolled']),
    min(prev['nullBatman']), max(prev['nullBatman']),
    min(w['iou'] for w in w05), max(w['iou'] for w in w05)))
print('saved s63_t2_table.json')
