#!/usr/bin/env python3
"""T2: mesh block decode — streams, vertex data, index buffer hunt."""
import struct

BDAE = '/home/z/my-project/work/actors/batman.bdae'
d = open(BDAE, 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

M = 0x4a58
print(f'mesh block @ {M:#x}:')
for o in range(M, M + 0x50, 16):
    row = [f'{u32(o + k):08x}' for k in range(0, 16, 4)]
    print(f'  {o - M:04x}: {" ".join(row)}')

# round-15: header @0x4a68 = [7 u32 sig][1][count 1449][8][5x(off,8)][f8][0][1][data]
H = 0x4a68
count = u32(H + 4 * 9)
print(f'\ncount @+9: {count}')
offs = [(u32(H + 40 + 8 * i), u32(H + 44 + 8 * i)) for i in range(5)]
print('stream descriptors (off, 8):', [(hex(a), hex(b)) for a, b in offs])
print('next words:', [hex(u32(H + 80 + 4 * i)) for i in range(6)])
data_len = u32(H + 100)
print('data_len word @+100:', hex(data_len), data_len)

# the data region: where does it start? scan after the descriptors
# 5x(off,8) at +40..+80; then [f8][0][1][len] = +80..+96; data at +96?
DATA = H + 96
print(f'\nassumed data @ {DATA:#x}, {data_len} B -> ends {DATA + data_len:#x}')
print('first 80 B:', d[DATA:DATA + 80].hex())

# floats at stride 80 / 40?
fl = lambda o: struct.unpack_from('<f', d, o)[0]
print('\nfirst verts as 20 f32 (stride-80 view):')
for v in range(2):
    vals = [round(fl(DATA + v * 80 + 4 * k), 3) for k in range(20)]
    print(f'  v{v}: {vals}')
print('\nfirst verts as 10 f32 (stride-40 view):')
for v in range(3):
    vals = [round(fl(DATA + v * 40 + 4 * k), 3) for k in range(10)]
    print(f'  v{v}: {vals}')

# index buffer hunt: after the data? scan for u16 runs with max < 2000
import array
best = None
for start in range(DATA + data_len, min(DATA + data_len + 0x8000,
                                         len(d) - 2), 4):
    a = array.array('H')
    a.frombytes(d[start:start + 96])
    if len(a) == 48 and max(a) < 1500 and min(a) >= 0:
        # triangle-like: many repeats of small values
        best = (start, a[:12])
        print(f'\nu16 candidate @ {start:#x}: {list(a[:12])} max={max(a)}')
        break
print('post-data bytes:', d[DATA + data_len:DATA + data_len + 64].hex())
