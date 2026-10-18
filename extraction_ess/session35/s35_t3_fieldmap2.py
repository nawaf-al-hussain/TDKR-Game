#!/usr/bin/env python3
"""S35 T3c: records vs soup interpretation test.
Soup = 10,274 xyz vertices (30,822 floats + 2 pad); records = 67,850 cells
[f0..f6 u16][char]. H1: f0-f2 = vertex indices; H2: f3-f5 = neighbour ids."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
cnt = struct.unpack_from('>H', d, 0)[0]     # 30,824
ROFF = 2 + cnt * 4
nrec = (N - ROFF) // 16
soup = np.frombuffer(d, '>f4', count=cnt, offset=2).astype(np.float64)
print(f'header u16 {cnt}; soup {cnt} floats; last two: {soup[-2:]}, first: {soup[:3]}')
NV = 10274
V = soup[:NV * 3].reshape(NV, 3)
print(f'VERTICES {NV}: x {V[:,0].min():.1f}..{V[:,0].max():.1f} y {V[:,1].min():.1f}..{V[:,1].max():.1f} '
      f'z {V[:,2].min():.2f}..{V[:,2].max():.2f} med z {np.median(V[:,2]):.2f}')

recs = np.frombuffer(d, '>u2', count=nrec * 8, offset=ROFF).reshape(nrec, 8).astype(np.int64)
chars = np.frombuffer(d, 'i1', count=nrec, offset=ROFF + 14)
a, b, c, e0, e1, e2, g = (recs[:, i] for i in range(7))
for nm, col in (('f0', a), ('f1', b), ('f2', c), ('f3', e0), ('f4', e1), ('f5', e2), ('f6', g)):
    print(f'{nm}: min {col.min()} max {col.max()}  <NV: {(col < NV).mean():.4f}  <nrec: {(col < nrec).mean():.4f}')
print(f'char: min {chars.min()} max {chars.max()} distinct {len(np.unique(chars))}')
print('char histogram (top):', dict(zip(*np.unique(chars, return_counts=True))[:2]) if False else
      {int(k): int(v) for k, v in zip(*np.unique(chars, return_counts=True))})

# geometric validation under H1
P0, P1, P2 = V[a], V[b], V[c]
cr = np.cross(P1 - P0, P2 - P0)
area = np.linalg.norm(cr, axis=1) / 2
print(f'\nH1 triangles: area m2 median {np.median(area):.1f} p95 {np.quantile(area, 0.95):.1f} '
      f'degenerate {(area < 1e-4).sum()}/{nrec}')
zz = (P0[:, 2] + P1[:, 2] + P2[:, 2]) / 3
print(f'cell z median {np.median(zz):.2f} (r34 collision-ground median 6.63)')

# neighbour shared-edge geometry under H2
def nbs_of(k):
    return (e0[k], e1[k], e2[k])

sym = 0; tot = 0; sh2 = 0
for k in range(nrec):
    ks = {a[k], b[k], c[k]}
    for nb in nbs_of(k):
        if 0 <= nb < nrec:
            tot += 1
            if k in nbs_of(nb):
                sym += 1
            if len(ks & {a[nb], b[nb], c[nb]}) == 2:
                sh2 += 1
print(f'H2 neighbour symmetry: {sym}/{tot} = {sym/tot:.4f}')
print(f'H2 neighbour shared-2-vertices: {sh2}/{tot} = {sh2/tot:.4f}')

# NULLS
rng = np.random.default_rng(5)
perm = rng.permutation(nrec)
sym_n = 0
for k in range(20000):
    nb = perm[k]
    if k in nbs_of(nb):
        sym_n += 1
print(f'NULL shuffled-neighbour symmetry: {sym_n}/20000 = {sym_n/20000:.4f}')
perm2 = rng.permutation(NV)
sh2_n = 0
for k in range(20000):
    ks = {perm2[a[k]], perm2[b[k]], perm2[c[k]]}
    nb = perm2[k] % nrec
    if len(ks & {a[nb], b[nb], c[nb]}) == 2:
        sh2_n += 1
print(f'NULL permuted-vertex shared-edge: {sh2_n}/20000 = {sh2_n/20000:.4f}')

np.save('/home/z/my-project/scripts/s35_t3_V2.npy', V)
np.save('/home/z/my-project/scripts/s35_t3_recs2.npy', recs)
np.save('/home/z/my-project/scripts/s35_t3_chars2.npy', chars)
print('saved')
