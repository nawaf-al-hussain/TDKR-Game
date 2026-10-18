#!/usr/bin/env python3
"""S34 T3: empirical decode of GothamCity navdata.nm. BE f32 triples from
byte 2; test triangle strides; check z plausibility vs collision ground; find
adjacency section at tail."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
print(f'size {N}')

# BE f32 view from offset 2
M = (N - 2) // 4
fa = np.frombuffer(d[2:2 + M * 4], '>f4')
print(f'{M} BE f32 from offset 2; first 12: {fa[:12]}')
z = fa[2::3]
print(f'z stats (every 3rd): min {z.min():.2f} max {z.max():.2f} mean {z.mean():.2f} '
      f'median {np.median(z):.2f}')
x = fa[0::3]; y = fa[1::3]
print(f'x range {x.min():.1f}..{x.max():.1f}; y range {y.min():.1f}..{y.max():.1f}')
# fraction of NaN/inf
print(f'non-finite: {(~np.isfinite(fa)).sum()}/{M}')

# stride test: how many floats until pattern breaks (non-plausible values)?
plaus = np.isfinite(fa) & (np.abs(fa) < 5000)
# longest prefix of plausible
brk = np.argmax(~plaus) if (~plaus).any() else M
print(f'first implausible float idx: {brk} (byte {2 + 4*brk})')
# runs of plausible
idxp = np.flatnonzero(np.diff(np.concatenate(([0], plaus.view(np.int8), [0]))))
pruns = [(int(idxp[k]), int(idxp[k+1])) for k in range(0, len(idxp), 2)
         if idxp[k+1] - idxp[k] >= 100]
print(f'plausible runs >=100: {len(pruns)}, first 5: '
      f'{[(a, b, b-a) for a, b in pruns[:5]]}')

# z-histogram to identify ground vs structures
hist, edges = np.histogram(z[np.isfinite(z) & (np.abs(z) < 500)], bins=20)
print('\nz histogram (20 bins over [-500,500]):')
for h, e in zip(hist, edges):
    if h: print(f'  z ~ {e:8.1f}: {h}')

# tail bytes: look for the adjacency (small ints) near end
tail = d[-256:]
print(f'\nlast 64 bytes: {tail[-64:].hex()}')
u8 = np.frombuffer(d, np.uint8)
print(f'byte-value histogram head-1k vs tail-1k:')
print('  head:', np.bincount(u8[:1000], minlength=256).nonzero()[0][:20])
print('  tail:', np.bincount(u8[-1000:], minlength=256).nonzero()[0][:30])
