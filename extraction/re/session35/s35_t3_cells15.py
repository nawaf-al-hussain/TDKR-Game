#!/usr/bin/env python3
"""S35 T3e: cells = 15 B packed (7 x BE u16 + char) @0x5a4e6; full decode +
symmetry/shared-edge/area battery with nulls."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
db = np.frombuffer(d, np.uint8)
N = len(d)
GS = 0x5a4e6
region = N - GS
nrec = region // 15
print(f'region {region} B -> {nrec} cells of 15 B (remainder {region - nrec*15})')

recs = np.zeros((nrec, 8), np.int64)
base = GS + np.arange(nrec) * 15
for j in range(7):
    recs[:, j] = db[base + 2 * j].astype(np.int64) * 256 + db[base + 2 * j + 1]
recs[:, 7] = db[base + 14]
a, b, c, e0, e1, e2, fl, ch = (recs[:, i] for i in range(8))
print('first 5 cells:', recs[:5].tolist())
print(f'char: {ch.min()}..{ch.max()} uniq {len(np.unique(ch))} top {dict(zip(*[x.tolist() for x in np.unique(ch, return_counts=True)]))}' if False else
      f'char: {ch.min()}..{ch.max()} uniq {len(np.unique(ch))}')
print(f'flags f6: min {fl.min()} max {fl.max()} uniq {len(np.unique(fl))} '
      f'top: {sorted(np.unique(fl).tolist())[:10]}')

NV = 30905
soup = np.frombuffer(d, '>f4', count=NV * 3, offset=2).astype(np.float64)
V = soup.reshape(NV, 3)
vmax = int(max(a.max(), b.max(), c.max()))
inr = ((a < NV) & (b < NV) & (c < NV)).mean()
print(f'max vertex id {vmax} (NV-1 {NV-1}); verts<NV: {inr:.4f}; ffff nb slots: '
      f'{int((e0==65535).sum()+ (e1==65535).sum()+(e2==65535).sum())}/{3*nrec}')
nmax = int(max(e0[e0 != 65535].max() if (e0 != 65535).any() else 0,
               e1[e1 != 65535].max() if (e1 != 65535).any() else 0,
               e2[e2 != 65535].max() if (e2 != 65535).any() else 0))
print(f'max neighbour id {nmax} (nrec-1 {nrec-1})')

P0, P1, P2 = V[np.clip(a, 0, NV - 1)], V[np.clip(b, 0, NV - 1)], V[np.clip(c, 0, NV - 1)]
cr = np.cross(P1 - P0, P2 - P0)
area = np.linalg.norm(cr, axis=1) / 2
okm = (a < NV) & (b < NV) & (c < NV)
print(f'tri area (valid): median {np.median(area[okm]):.1f} m2 p95 {np.quantile(area[okm], 0.95):.1f} '
      f'degenerate {int((area[okm] < 1e-4).sum())}/{int(okm.sum())}')

# symmetry + shared edge (vectorized-ish loop)
e0s = np.where(e0 == 65535, -1, e0)
e1s = np.where(e1 == 65535, -1, e1)
e2s = np.where(e2 == 65535, -1, e2)
sym = sh2 = tot = 0
VSET = [set() for _ in range(nrec)]
for k in range(nrec):
    VSET[k] = {a[k], b[k], c[k]}
for k in range(nrec):
    for nb in (e0s[k], e1s[k], e2s[k]):
        if nb >= 0:
            tot += 1
            if k in (e0s[nb], e1s[nb], e2s[nb]):
                sym += 1
            if len(VSET[k] & VSET[nb]) == 2:
                sh2 += 1
print(f'\nneighbour symmetry: {sym}/{tot} = {sym/tot:.4f}')
print(f'shared-2-vertex:    {sh2}/{tot} = {sh2/tot:.4f}')

rng = np.random.default_rng(13)
perm = rng.permutation(nrec)
sym_n = sh2_n = 0
for k in range(30000):
    nb = perm[k]
    if k in (e0s[nb], e1s[nb], e2s[nb]):
        sym_n += 1
    if len(VSET[k] & VSET[nb]) == 2:
        sh2_n += 1
print(f'NULL: symmetry {sym_n}/30000 = {sym_n/30000:.4f}; shared-edge {sh2_n}/30000 = {sh2_n/30000:.4f}')

# connectivity
parent = list(range(nrec))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
for k in range(nrec):
    for nb in (e0s[k], e1s[k], e2s[k]):
        if nb >= 0:
            ra, rb = find(k), find(nb)
            if ra != rb:
                parent[ra] = rb
from collections import Counter
comp = Counter(find(k) for k in range(nrec))
sizes = sorted(comp.values(), reverse=True)
print(f'\ncomponents: {len(comp)}; largest {sizes[0]} ({sizes[0]/nrec*100:.1f}%) next {sizes[1:5]}')

np.save('/home/z/my-project/scripts/s35_t3_Vfin.npy', V)
np.save('/home/z/my-project/scripts/s35_t3_recfin.npy', recs)
print('saved')
