#!/usr/bin/env python3
"""S34 T1: wider search for _008_run data block using tick-window signature
(ticks in [30000..30666]) + full sequential validation, bidirectional."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)
print(f'file size: {N} (0x{N:x})')

T = 0x204bb70
NE = 156
pairs = [(u32a(T + 8*k), u32a(T + 8*k + 4)) for k in range(NE)]
print('first 10 (off,len):', [(hex(a), hex(b)) for a, b in pairs[:10]])
print('sum lens:', hex(sum(l for _, l in pairs)))

# numpy ascending-run scan over whole file, runs >= 8 ticks within [29000..32000]
M = N // 4
ua = np.frombuffer(ad[:M*4], np.uint32).astype(np.int64)
asc = np.zeros(M, bool)
asc[:-1] = (np.diff(ua) > 0) & (ua[1:] < 2_000_000) & (ua[:-1] < 2_000_000)
idx = np.flatnonzero(np.diff(np.concatenate(([0], asc.view(np.int8), [0]))))
runs = [(int(idx[k]), int(idx[k+1])) for k in range(0, len(idx), 2)]
big = [(a, b) for a, b in runs if b - a + 1 >= 8 and 29000 <= int(ua[a]) and int(ua[b]) <= 32000]
print(f'\nruns>=8 in [29000..32000]: {len(big)}')
for a, b in big[:20]:
    print(f'  @0x{a*4:07x}: n={b-a+1} [{int(ua[a])}..{int(ua[b])}]')

# where do they cluster?
if big:
    arr = np.array([a*4 for a, b in big])
    print('cluster min/max: 0x%x..0x%x' % (arr.min(), arr.max()))
