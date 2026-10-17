#!/usr/bin/env python3
"""S32 T1i: cape reconstruction from (w, bodyVertIdx) pairs, take 2."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BASE, N = 0x4b5c, 1449
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])

BLK, LN = 0x54d78, 21552
TAB = 32 * 8                      # 32-entry (count, offset) table
tab = [(u32(BLK + 8 * g), u32(BLK + 8 * g + 4)) for g in range(32)]
print('table (count, offset):', tab)

# chunk g: count c, offset o (bytes, absolute within file? within block?)
# test: absolute-in-file offsets
o0 = tab[0][1]
print(f'tab[0] offset {o0} -> absolute? block+{o0}: u32 = {u32(BLK+o0)}')

# pairs region: try from 256 to LN as (f32, u32)
pairs = [(f32(BLK + 256 + 8 * k), u32(BLK + 256 + 8 * k + 4))
         for k in range((LN - 256) // 8)]
print(f'{len(pairs)} pairs from +256')
# sanity: how many have idx < 1449 and 0<=w<=1
good = [(w, i) for w, i in pairs if 0 <= i < N and -1e-3 <= w <= 1.001]
print(f'good pairs: {len(good)}')
# runs by idx continuity
runs, s = [], 0
for k in range(1, len(good)):
    if good[k][1] < good[k - 1][1] - 4:
        runs.append((s, k - s))
        s = k
runs.append((s, len(good) - s))
print(f'{len(runs)} runs, len hist top:',
      sorted(__import__('collections').Counter(l for _, l in runs).items())
      [:8])
rec = []
for s0, l in runs:
    seg = good[s0:s0 + l]
    ww = np.array([p[0] for p in seg])
    ii = np.array([p[1] for p in seg], int)
    if 0.9 <= ww.sum() <= 1.1:
        rec.append((ww[:, None] * verts[ii]).sum(axis=0))
print(f'reconstructed {len(rec)} pts with sum(w)~1')
if rec:
    P = np.array(rec)
    print(f'bbox x [{P[:,0].min():.2f},{P[:,0].max():.2f}] '
          f'y [{P[:,1].min():.2f},{P[:,1].max():.2f}] '
          f'z [{P[:,2].min():.2f},{P[:,2].max():.2f}]')
    print('first 8 pts:', np.round(P[:8], 3).tolist())

# Where do the referenced body verts live spatially?
ii_all = sorted({i for _, i in good})
sub = verts[ii_all]
print(f'\nreferenced body verts ({len(ii_all)} distinct): bbox '
      f'x [{sub[:,0].min():.2f},{sub[:,0].max():.2f}] '
      f'y [{sub[:,1].min():.2f},{sub[:,1].max():.2f}] '
      f'z [{sub[:,2].min():.2f},{sub[:,2].max():.2f}]')

# compare chunk counts with runs
counts = [c for c, _ in tab]
print(f'\nsum(count) = {sum(counts)}; len(runs) = {len(runs)}; '
      f'chunk count histogram sample {counts[:8]}')
