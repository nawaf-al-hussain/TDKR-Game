#!/usr/bin/env python3
"""S35 T3g: validate section-1 cells (contiguous 15-B from 0x5a4e6):
vertex-pool fit, neighbour symmetry, shared-edge, areas — with nulls."""
import struct
import numpy as np
from collections import Counter

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
db = np.frombuffer(d, np.uint8)
N = len(d)
GS = 0x5a4e6
NV = 30905  # floats in clean soup prefix (92,715 = 3 x 30,905)
soup = np.frombuffer(d, '>f4', count=(NV // 3) * 3, offset=2).astype(np.float64)
NV3 = len(soup)
V = soup.reshape(NV3 // 3, 3)
NV = NV3 // 3
print(f'soup: {NV} floats = {NV} coords?? -> {NV//3} xyz; boundary byte {2+NV*4}')

# determine contiguous valid prefix
nmax = (N - GS) // 15
ncells = 0
for k in range(nmax):
    off = GS + k * 15
    v = struct.unpack_from('>7H', d, off)
    if not all(x < NV for x in v[:3]):
        break
    ncells += 1
print(f'contiguous valid cells: {ncells} (0x{GS:x}..0x{GS + ncells*15:x})')

recs = np.zeros((ncells, 8), np.int64)
base = GS + np.arange(ncells) * 15
for j in range(7):
    recs[:, j] = db[base + 2*j].astype(np.int64) * 256 + db[base + 2*j + 1]
recs[:, 7] = db[base + 14]
a, b, c, e0, e1, e2, fl, ch = (recs[:, i] for i in range(8))
print(f'vertex id max: {max(a.max(), b.max(), c.max())} (NV-1 {NV-1})')
print(f'neighbour id max (non-ffff): {int(max(e0[e0!=65535].max(), e1[e1!=65535].max(), e2[e2!=65535].max()))} '
      f'(ncells-1 {ncells-1})')
oob = int(((e0 >= ncells) & (e0 != 65535)).sum() + ((e1 >= ncells) & (e1 != 65535)).sum()
          + ((e2 >= ncells) & (e2 != 65535)).sum())
print(f'neighbour ids >= ncells (non-ffff): {oob} of {3*ncells}')

P0, P1, P2 = V[a], V[b], V[c]
cr = np.cross(P1 - P0, P2 - P0)
area = np.linalg.norm(cr, axis=1) / 2
print(f'area m2: median {np.median(area):.1f} p95 {np.quantile(area,0.95):.1f} '
      f'degenerate {(area < 1e-4).sum()}')
zz = (P0[:,2] + P1[:,2] + P2[:,2]) / 3
print(f'cell z: median {np.median(zz):.2f} (collision ground median 6.63)')

e0s = np.where(e0 == 65535, -1, e0)
e1s = np.where(e1 == 65535, -1, e1)
e2s = np.where(e2 == 65535, -1, e2)
sym = sh2 = tot = 0
VSET = [frozenset((a[k], b[k], c[k])) for k in range(ncells)]
for k in range(ncells):
    for nb in (e0s[k], e1s[k], e2s[k]):
        if 0 <= nb < ncells:
            tot += 1
            if k in (e0s[nb], e1s[nb], e2s[nb]):
                sym += 1
            if len(VSET[k] & VSET[nb]) == 2:
                sh2 += 1
print(f'\nneighbour symmetry: {sym}/{tot} = {sym/tot:.4f}')
print(f'shared-2-vertex:    {sh2}/{tot} = {sh2/tot:.4f}')

rng = np.random.default_rng(17)
perm = rng.permutation(ncells)
sym_n = sh2_n = 0
for k in range(30000):
    nb = perm[k]
    if k in (e0s[nb], e1s[nb], e2s[nb]):
        sym_n += 1
    if len(VSET[k] & VSET[nb]) == 2:
        sh2_n += 1
print(f'NULL: symmetry {sym_n}/30000 = {sym_n/30000:.4f}; shared-edge {sh2_n}/30000 = {sh2_n/30000:.4f}')

# connectivity
parent = list(range(ncells))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
for k in range(ncells):
    for nb in (e0s[k], e1s[k], e2s[k]):
        if 0 <= nb < ncells:
            ra, rb = find(k), find(nb)
            if ra != rb:
                parent[ra] = rb
comp = Counter(find(k) for k in range(ncells))
sizes = sorted(comp.values(), reverse=True)
print(f'components: {len(comp)}; largest {sizes[0]} ({sizes[0]/ncells*100:.1f}%) next {sizes[1:5]}')

np.save('/home/z/my-project/scripts/s35_t3_Vsec.npy', V)
np.save('/home/z/my-project/scripts/s35_t3_recsec.npy', recs)
print('saved')
