#!/usr/bin/env python3
"""S34 T3c: brute-force the adjacency alignment (start, endian, width) and
triangle count; then validate triangle z against the collision ground."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)

# The plausible-float prefix (from offset 2) = 92483 floats. Zero runs are
# valid f32 too. Try T tris x 36 B; then adjacency must start somewhere in
# [2+T*36, 2+T*36+64]. Score candidate starts by triplet validity.
best = []
for T in range(10260, 10290):
    end = 2 + T * 36
    for start in range(end, min(end + 80, N - 600)):
        for dt in ('<u2', '>u2'):
            n = (N - start) // 6
            if n < T * 0.9: continue
            a = np.frombuffer(d[start:start + n * 6], dt).reshape(n, 3).astype(np.int64)
            ok = ((a == 0xFFFF) | (a < T)).all(axis=1)
            frac = ok.mean()
            best.append((frac, T, start, dt, n))
best.sort(reverse=True)
for frac, T, start, dt, n in best[:6]:
    print(f'T={T} start={start} (delta {start - (2 + T*36):+d}) {dt}: '
          f'{frac*100:.2f}% valid, n={n}')

# winner: rebuild
frac, T, start, dt, n = best[0]
a = np.frombuffer(d[start:start + n * 6], dt).reshape(n, 3).astype(np.int64)
ok = ((a == 0xFFFF) | (a < T)).all(axis=1)
print(f'\nfirst invalid triplet idx: {np.argmax(~ok)}, n_valid_prefix '
      f'{np.argmax(~ok) if (~ok).any() else n}')
tris = np.frombuffer(d[2:2 + T * 36], '>f4').reshape(T, 3, 3).astype(np.float64)
print(f'tris {T}: x {tris[...,0].min():.1f}..{tris[...,0].max():.1f}, '
      f'z median {np.median(tris[...,2]):.2f}')
cent = tris.mean(axis=1)
print(f'centroid z: min {cent[:,2].min():.2f} max {cent[:,2].max():.2f} '
      f'median {np.median(cent[:,2]):.2f}')
np.save('/home/z/my-project/scripts/s34_t3_gc_tris.npy', tris)
np.save('/home/z/my-project/scripts/s34_t3_gc_adj.npy', a[:n])
print(f'wrote tris + adjacency ({n} records)')
