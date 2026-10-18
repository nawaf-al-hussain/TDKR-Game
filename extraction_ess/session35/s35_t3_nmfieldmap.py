#!/usr/bin/env python3
"""S35 T3a: decode .nm as indexed mesh: header u16 count, BE f32 vertex soup,
67,850 16-B cell records [7 x BE u16 + 1 x char]; establish the field map
(vertex indices, neighbour ids, flags) with geometric validation + nulls."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
cnt = struct.unpack_from('>H', d, 0)[0]
print(f'header BE u16 = {cnt}; soup floats {cnt} = {cnt*4} B; '
      f'records region {N - 2 - cnt*4} B = {(N - 2 - cnt*4)/16} records')

soup = np.frombuffer(d, '>f4', count=cnt, offset=2).astype(np.float64)
V = soup.reshape(-1, 3)
print(f'vertices: {len(V)}')
print(f'x {V[:,0].min():.1f}..{V[:,0].max():.1f}; y {V[:,1].min():.1f}..{V[:,1].max():.1f}; '
      f'z(up) {V[:,2].min():.2f}..{V[:,2].max():.2f} median {np.median(V[:,2]):.2f}')

ROFF = 2 + cnt * 4
nrec = (N - ROFF) // 16
recs = np.frombuffer(d, '>u2', count=nrec * 8, offset=ROFF).reshape(nrec, 8).astype(np.int64)
chars = np.frombuffer(d, 'i1', count=nrec, offset=ROFF + 14)
print(f'records: {nrec}; char field range {chars.min()}..{chars.max()}')

# field hypotheses: [a b c][d e f][g][char] with (a,b,c) = vertex ids, (d,e,f) = neighbours
a, b, c = recs[:, 0], recs[:, 1], recs[:, 2]
dd, e, f = recs[:, 3], recs[:, 4], recs[:, 5]
g = recs[:, 6]
for nm, col in (('f0', a), ('f1', b), ('f2', c), ('f3', dd), ('f4', e), ('f5', f), ('f6', g)):
    print(f'{nm}: min {col.min()} max {col.max()}')

va_ok = ((a < cnt) & (b < cnt) & (c < cnt)).mean()
nb_ok = ((dd < nrec) & (e < nrec) & (f < nrec)).mean()
print(f'f0-f2 < nverts: {va_ok:.4f};  f3-f5 < nrec: {nb_ok:.4f}')

# geometric validation: triangles (V[a], V[b], V[c]) — area, degenerate rate
P0, P1, P2 = V[a], V[b], V[c]
n = np.cross(P1 - P0, P2 - P0)
area2 = np.linalg.norm(n, axis=1) / 2
print(f'triangle area m2: median {np.median(area2):.1f} p95 {np.quantile(area2,0.95):.1f} '
      f'zero-degenerate {(area2 < 1e-6).sum()}/{nrec}')
# edge lengths
e01 = np.linalg.norm(P1 - P0, axis=1); e12 = np.linalg.norm(P2 - P1, axis=1); e20 = np.linalg.norm(P0 - P2, axis=1)
print(f'edge m: med {np.median(np.concatenate([e01,e12,e20])):.1f} p95 {np.quantile(np.concatenate([e01,e12,e20]),0.95):.1f}')

# SHARED-EDGE neighbour geometry: neighbour nb of cell k shares exactly 2 vertex ids
shared = 0; tot = 0
sym_f3 = 0; sym_tot = 0
for k in range(nrec):
    ks = frozenset((a[k], b[k], c[k]))
    for nb in (dd[k], e[k], f[k]):
        if 0 <= nb < nrec:
            tot += 1
            ns = frozenset((a[nb], b[nb], c[nb]))
            if len(ks & ns) == 2:
                shared += 1
            if k in (dd[nb], e[nb], f[nb]):
                sym_f3 += 1
            sym_tot += 1
print(f'shared-2-vertex edges: {shared}/{tot} = {shared/tot:.3f}')
print(f'neighbour symmetry (k lists nb iff nb lists k): {sym_f3}/{sym_tot} = {sym_f3/sym_tot:.3f}')

# NULL: shuffled neighbour assignment symmetry
rng = np.random.default_rng(3)
perm = rng.permutation(nrec)
sym_null = 0
for k in range(20000):
    nb = perm[dd[k]] if k < len(perm) else 0
    if 0 <= nb < nrec and k in (dd[nb], e[nb], f[nb]):
        sym_null += 1
print(f'NULL (shuffled neighbour ids) symmetry: {sym_null}/20000 = {sym_null/20000:.4f}')

np.save('/home/z/my-project/scripts/s35_t3_V.npy', V)
np.save('/home/z/my-project/scripts/s35_t3_recs.npy', recs)
np.save('/home/z/my-project/scripts/s35_t3_chars.npy', chars)
print('saved V, recs, chars')
