#!/usr/bin/env python3
"""S32 T1h: cape mystery block structure + reconstruction test."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

BASE, N = 0x4b5c, 1449
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])

BLK = 0x54d78
LN = 21552

print('=== first 112 u32 of cape block ===')
head = [u32(BLK + 4 * i) for i in range(112)]
print(head)
print('\nas (a,b) pairs:', list(zip(head[0::2], head[1::2])))

# (f32,u32) pair view of whole block
print('\n=== (f32 w, u32 idx) pairs ===')
NP = LN // 8
pairs = [(struct.unpack_from('<f', d, BLK + 8 * k)[0],
          u32(BLK + 8 * k + 4)) for k in range(NP)]
print('first 12:', [(round(w, 3), i) for w, i in pairs[:12]])
print('last 12:', [(round(w, 3), i) for w, i in pairs[-12:]])
idxs = np.array([p[1] for p in pairs])
ws = np.array([p[0] for p in pairs])
print(f'idx range [{idxs.min()}, {idxs.max()}], '
      f'w range [{ws.min():.3f}, {ws.max():.3f}]')

# where do (f32,u32) pairs start being well-formed? check head region:
# first 448 B as u32 = counts? test group structure:
# hypothesis: [ngroups][per group: (count, offset)]... check b monotonic
print('\nb values monotonic?', all(head[i + 3] > head[i + 1]
                                    for i in range(0, 108, 2)))

# hypothesis: head = (count, offset) pairs into the pairs region
# group g: count head[2g], byte offset head[2g+1] (relative to BLK)
# verify: does the pair at offset head[2g+1] start a run of head[2g] pairs?
okg = 0
for g in range(56):
    cnt, off = head[2 * g], head[2 * g + 1]
    if off + cnt * 8 <= LN and off >= 448:
        okg += 1
print(f'(count,offset) pairs with offset>=448: {okg}/56')

# alternative: head = pairs too? (idx=31, w-as-u32=4?) no.

# try: 448-B head = 56 groups of TWO u32: (start_idx, count)?
print('\n=== reconstruction attempt: consecutive (w,idx) runs of len L ===')
# find natural runs: group boundaries where idx jumps non-monotonically
runs = []
s = 0
for k in range(1, NP):
    if idxs[k] < idxs[k - 1] - 4:      # restart
        runs.append((s, k - s))
        s = k
runs.append((s, NP - s))
print(f'{len(runs)} natural runs; len histogram:')
from collections import Counter
print(sorted(Counter(l for _, l in runs).items())[:15])
print('first 10 runs:', runs[:10])

# reconstruct points from runs with sum(w)~1: point = sum w*verts[idx]
rec = []
for s0, l in runs:
    seg = pairs[s0:s0 + l]
    ww = np.array([p[0] for p in seg])
    ii = np.array([p[1] for p in seg], int)
    if len(seg) and ii.max() < N and ww.sum() > 0.5:
        p = (ww[:, None] * verts[ii]).sum(axis=0)
        rec.append((s0, l, p, float(ww.sum())))
print(f'\nreconstructed {len(rec)} points from runs')
if rec:
    P = np.array([r[2] for r in rec])
    print(f'point cloud: x [{P[:,0].min():.2f},{P[:,0].max():.2f}] '
          f'y [{P[:,1].min():.2f},{P[:,1].max():.2f}] '
          f'z [{P[:,2].min():.2f},{P[:,2].max():.2f}]')
    print('sample points:', np.round(P[:6], 3))

# compare with cape bind origins (z 0.16..1.58, x -1.75..1.75)
CAPE = 0x5a210
cape_bind = np.array([np.linalg.inv(np.array(
    struct.unpack_from('<16f', d, CAPE + k * 64),
    np.float64).reshape(4, 4)) for k in range(38)])
org = cape_bind[:, 3, :3]
print('\ncape bind origins for comparison:')
print('  x range', org[:, 0].min(), org[:, 0].max(),
      'y', org[:, 1].min(), org[:, 1].max(),
      'z', org[:, 2].min(), org[:, 2].max())

# CAPE_down companion block @0x6474c: same (w,idx) view?
B2 = 0x6474c
LN2 = 11760
head2 = [u32(B2 + 4 * i) for i in range(48)]
print('\nCAPE_down block head u32s:', head2)
NP2 = LN2 // 8
p2 = [(struct.unpack_from('<f', d, B2 + 8 * k)[0], u32(B2 + 8 * k + 4))
      for k in range(NP2)]
print('first 8 pairs:', [(round(w, 3), i) for w, i in p2[:8]])
print('last 8 pairs:', [(round(w, 3), i) for w, i in p2[-8:]])
