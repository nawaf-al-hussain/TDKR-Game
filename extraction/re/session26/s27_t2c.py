#!/usr/bin/env python3
"""s27 T2 v3: node-tree (skeleton) parse + packed quaternion tests +
bbox cleanup."""
import struct
import math

BDAE = '/home/z/my-project/work/data/batman.bdae'
d = open(BDAE, 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
i32 = lambda o: struct.unpack_from('<i', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

DATA = 0x4ac4
NV = 1449
IDX = 0x210bc
idx = [u16(IDX + 2 * k) for k in range(5430)]

# ---------- A. node tree: find the structure around the 4x4 matrices
# single matrices with [0,0,0,1] bottom row at 0x30d88 etc. Dump around one.
o = 0x30d88
print('=== bytes around first matrix @0x30d88 (u32 view) ===')
for a in range(o - 0x40, o + 0x50, 16):
    print(f'  {a:06x}: ' + ' '.join(f'{u32(a + k):08x}' for k in range(0, 16, 4)))
print('  as floats:', ' '.join(f'{f32(a + k):+9.4f}'
                               for k in range(0, 16, 4)))

# node header candidate: scan backwards for name-pointer pattern.
# find ALL 4x4 matrices with [0,0,0,1] bottom
mats = []
o = 0x30000
while o < len(d) - 64:
    last = [f32(o + 48 + 4 * c) for c in range(4)]
    if abs(last[0]) < 1e-5 and abs(last[1]) < 1e-5 \
            and abs(last[2]) < 1e-5 and abs(last[3] - 1) < 1e-5:
        rows_ok = all(abs(f32(o + r * 16 + 4 * c)) < 1e6
                      for r in range(3) for c in range(4))
        if rows_ok:
            mats.append(o)
            o += 64
            continue
    o += 4
print(f'\ntotal [0,0,0,1]-bottom matrices: {len(mats)}')

# stride between consecutive matrices -> node size
from collections import Counter
gaps = Counter(b - a for a, b in zip(mats, mats[1:]) if 0 < b - a < 512)
print('most common gaps:', gaps.most_common(6))

# ---------- B. dump a full node region and try to read names
def cstr_at(off):
    e = d.index(b'\0', off)
    return d[off:e].decode('latin1')

# names near 0xa5c..0xb59: BATMAN-mesh @0xa5c, Bip01 @0xb59 — name pool?
print('\nname-pool region 0xa00..0xb80:')
print(' ', d[0xa00:0xb80])
