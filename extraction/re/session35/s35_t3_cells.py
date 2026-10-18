#!/usr/bin/env python3
"""S35 T3d: full Gotham cell decode @0x5a4e6 (LE u16 x7 + char) +
validation battery (symmetry, shared-edge, ground) with nulls."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
db = np.frombuffer(d, np.uint8)
N = len(d)
GS = 0x5a4e6
nrec = (N - GS) // 16
print(f'cells: {nrec} (tail {N - GS - nrec*16} B zero pad)')

recs = np.frombuffer(d, '<u2', count=nrec * 8, offset=GS).reshape(nrec, 8).astype(np.int64)
a, b, c, e0, e1, e2, fl = (recs[:, i] for i in range(7))
idx14 = (GS + np.arange(nrec) * 16 + 14).astype(np.int64)
ch = db[idx14].astype(np.int64)
hi = db[idx14 + 1].astype(np.int64)
print(f'char: {ch.min()}..{ch.max()} uniq {len(np.unique(ch))}; byte15: uniq {sorted(set(hi.tolist()))[:10]}')
print(f'flags f6: {fl.min()}..{fl.max()} uniq {len(np.unique(fl))} top {sorted(np.unique(fl))[:8]}...')

NV = 30824 // 3  # 10274
soup = np.frombuffer(d, '>f4', count=NV * 3, offset=2).astype(np.float64)
V = soup.reshape(NV, 3)
print(f'vertices {NV}: x {V[:,0].min():.1f}..{V[:,0].max():.1f} y {V[:,1].min():.1f}..{V[:,1].max():.1f} '
      f'z {V[:,2].min():.2f}..{V[:,2].max():.2f} med {np.median(V[:,2]):.2f}')

vmax = int(max(a.max(), b.max(), c.max()))
print(f'max vertex id in cells: {vmax} (NV-1 = {NV-1})')
inr = ((a < NV) & (b < NV) & (c < NV)).mean()
print(f'cell verts < NV: {inr:.4f}')
emax = int(max(e0.max(), e1.max(), e2.max()))
print(f'max neighbour id: {emax} (nrec-1 = {nrec-1}); ffff count: '
      f'{(e0==65535).sum()+(e1==65535).sum()+(e2==65535).sum()} of {3*nrec}')

P0, P1, P2 = V[np.clip(a, 0, NV-1)], V[np.clip(b, 0, NV-1)], V[np.clip(c, 0, NV-1)]
cr = np.cross(P1 - P0, P2 - P0)
area = np.linalg.norm(cr, axis=1) / 2
okm = (a < NV) & (b < NV) & (c < NV)
print(f'tri area (valid cells): median {np.median(area[okm]):.1f} m2 p95 {np.quantile(area[okm], 0.95):.1f} '
      f'degenerate {(area[okm] < 1e-4).sum()}')

# symmetry + shared-edge
def nbs(k):
    return (e0[k], e1[k], e2[k])

sym = sh2 = tot = 0
for k in range(nrec):
    ks = {a[k], b[k], c[k]}
    for nb in nbs(k):
        if 0 <= nb < nrec:
            tot += 1
            if k in nbs(nb):
                sym += 1
            if len(ks & {a[nb], b[nb], c[nb]}) == 2:
                sh2 += 1
print(f'\nneighbour symmetry: {sym}/{tot} = {sym/tot:.4f}')
print(f'shared-2-vertex:    {sh2}/{tot} = {sh2/tot:.4f}')

rng = np.random.default_rng(7)
perm = rng.permutation(nrec)
sym_n = sh2_n = 0
for k in range(30000):
    nb = perm[k]
    if k in nbs(nb):
        sym_n += 1
    if len({a[k], b[k], c[k]} & {a[nb], b[nb], c[nb]}) == 2:
        sh2_n += 1
print(f'NULL shuffled-cell "neighbours": symmetry {sym_n}/30000 = {sym_n/30000:.4f}; '
      f'shared-2-vertex {sh2_n}/30000 = {sh2_n/30000:.4f}')

# connectivity: giant component
import sys
sys.setrecursionlimit(10000)
parent = list(range(nrec))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
for k in range(nrec):
    for nb in nbs(k):
        if 0 <= nb < nrec:
            ra, rb = find(k), find(nb)
            if ra != rb:
                parent[ra] = rb
from collections import Counter
comp = Counter(find(k) for k in range(nrec))
sizes = sorted(comp.values(), reverse=True)
print(f'\ncomponents: {len(comp)}; largest {sizes[0]} ({sizes[0]/nrec*100:.1f}%), next {sizes[1:5]}')

np.save('/home/z/my-project/scripts/s35_t3_cells_V.npy', V)
np.save('/home/z/my-project/scripts/s35_t3_cells_recs.npy', recs)
print('saved')
