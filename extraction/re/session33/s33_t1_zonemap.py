#!/usr/bin/env python3
"""S33 T1: exhaustive zone map 0x53200..0x70000 (idle_stand channels)."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
N = len(d) // 4
u32all = np.frombuffer(d[:N * 4], np.uint32)
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

LO, HI = 0x53200, 0x70000
w0, w1 = LO // 4, HI // 4
seg = u32all[w0:w1]
asc = (seg[1:] > seg[:-1]) & (seg[1:] < 2_000_000) & (seg[:-1] < 2_000_000)
idx = np.flatnonzero(np.diff(np.concatenate(([0], asc.view(np.int8), [0]))))
truns = [(w0 + int(idx[k]), w0 + int(idx[k + 1])) for k in range(0, len(idx), 2)
         if idx[k + 1] - idx[k] >= 10]

# quat runs
f32all = np.frombuffer(d[:N * 4], np.float32)
qg = f32all[LO // 16 * 4: HI // 16 * 4].reshape(-1, 4)
with np.errstate(invalid='ignore'):
    nrm = np.sqrt((qg.astype(np.float64) ** 2).sum(1))
ok = np.isfinite(nrm) & (np.abs(nrm - 1) < 2e-3)
qidx = np.flatnonzero(np.diff(np.concatenate(([0], ok.view(np.int8), [0]))))
qruns = [((LO // 16) * 16 + int(qidx[k]) * 16, int(qidx[k + 1] - qidx[k]))
         for k in range(0, len(qidx), 2) if qidx[k + 1] - qidx[k] >= 6]

events = ([(a * 4, b - a + 1, 'TICK', int(u32all[a]), int(u32all[b])) for a, b in truns]
          + [(a, n, 'QUAT', None, None) for a, n in qruns])
events.sort()
print(f'zone 0x{LO:x}..0x{HI:x}: {len(truns)} tick runs, {len(qruns)} quat runs')
prev_end = LO
for off, n, kind, lo, hi in events:
    gap = off - prev_end
    print(f'  0x{off:06x} {kind:4s} n={n:3d} {"[%d..%d]" % (lo, hi) if lo is not None else "":14s}'
          f' gap_before={gap}')
    prev_end = off + (n * 4 if kind == 'TICK' else n * 16)

print('\nfirst tick run values @0x%x:' % (truns[0][0] * 4))
a, b = truns[0]
print([int(x) for x in u32all[a:a + 12]], '...',
      [int(x) for x in u32all[b - 3:b + 1]])
deltas = np.diff(u32all[a:b + 1])
import collections
print('delta hist:', dict(collections.Counter(deltas.tolist())))
