#!/usr/bin/env python3
"""S34 T2: locate real mesh headers + index lists (body 1449v, cape 394v,
third 194v). Scan for u16 index runs with max < vertex count; find u32
394/194/1449 declarations; map the zero runs."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
N = len(d)
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
u16 = lambda o: struct.unpack_from('<H', d, o)[0]

# 1) where do the numbers 1449/394/194 appear as u32?
for target in (1449, 394, 194, 5655):
    hits = []
    for o in range(0, min(N, 0x80000) - 4, 4):
        if u32(o) == target:
            hits.append(o)
    print(f'u32 {target}: {len(hits)} hits in head 512KB: '
          f'{[hex(h) for h in hits[:16]]}')

# 2) u16 index-run scan (head 512KB): runs of >=300 u16s all < 1449
M = 0x80000 // 2
ua = np.frombuffer(d[:M * 2], np.uint16).astype(np.int32)
ok = ua < 1449
idx = np.flatnonzero(np.diff(np.concatenate(([0], ok.view(np.int8), [0]))))
runs = [(int(idx[k]), int(idx[k + 1])) for k in range(0, len(idx), 2)
        if idx[k + 1] - idx[k] >= 300]
print(f'\nu16 runs >=300 all<1449 (head 512KB): {len(runs)}')
for a, b in runs[:20]:
    seg = ua[a:b]
    print(f'  @0x{a*2:06x}: len {b-a}, max {int(seg.max())}, '
          f'min {int(seg.min())}')

# 3) zero runs (whole file) — confirm r23's and find any others > 4KB in head 1MB
z = np.frombuffer(d[:0x100000], np.uint8) == 0
idxz = np.flatnonzero(np.diff(np.concatenate(([0], z.view(np.int8), [0]))))
zruns = [(int(idxz[k]), int(idxz[k + 1])) for k in range(0, len(idxz), 2)
         if idxz[k + 1] - idxz[k] >= 4096]
print(f'\nzero runs >=4KB (head 1MB): {len(zruns)}')
for a, b in zruns:
    print(f'  @0x{a:06x}..0x{b:06x}: {b-a} B (= {b-a}//80 = {(b-a)//80} x 80B verts '
          f'+ {b-a-80*((b-a)//80)} pad)')
