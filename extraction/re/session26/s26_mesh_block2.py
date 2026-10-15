#!/usr/bin/env python3
"""T2: decode the 5 stream sub-descriptors + data + hunt the index buffer."""
import struct, array

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BLOCK = 0x4a58
DATA = BLOCK + 0xf8
DLEN = u32(BLOCK + 0x68)          # 0x1c5bc at block+0x68?
print(f'block {BLOCK:#x}, data @ {DATA:#x}, checking len word @+0x68: '
      f'{u32(BLOCK + 0x68):#x}')

print('\nblock bytes 0..0xf8:')
for o in range(0, 0xf8, 16):
    row = [f'{u32(BLOCK + o + k):08x}' for k in range(0, 16, 4)]
    print(f'  {o:02x}: {" ".join(row)}')

# 5 sub-descriptors at 0x4c, 0x64, 0x7c, 0x94, 0xac (0x18 B each)
print('\nsub-descriptors:')
for i, off in enumerate((0x4c, 0x64, 0x7c, 0x94, 0xac)):
    words = [u32(BLOCK + off + 4 * k) for k in range(6)]
    print(f'  [{i}] @{off:#x}: {words}')
    half = [f'{words[0]:08x} {words[1]:08x}', f32(BLOCK + off) if 0 else '']

# data head: floats + ints
print('\ndata head floats (first 12):')
print('  ', [round(f32(DATA + 4 * k), 4) for k in range(12)])
print('data head as u32 (first 24):')
print('  ', [hex(u32(DATA + 4 * k)) for k in range(24)])

# find where floats end / structure changes: scan the first 0x400 bytes
print('\nfloat-validity map of first 160 words (f = plausible float):')
marks = []
for k in range(160):
    v = u32(DATA + 4 * k)
    fv = struct.unpack('<f', struct.pack('<I', v))[0]
    plausible = (0.0 <= abs(fv) < 1e6) and (v == 0 or abs(fv) > 1e-7)
    marks.append('f' if plausible and v not in (0,) else ('0' if v == 0 else '.'))
for i in range(0, 160, 32):
    print(f'  {i * 4:04x}: {"".join(marks[i:i+32])}')

# index buffer hunt after the data
END = DATA + 0x1c5bc
print(f'\npost-data @ {END:#x}:')
print(' ', d[END:END + 64].hex())
for start in range(END, END + 0x400, 2):
    a = array.array('H')
    a.frombytes(d[start:start + 64])
    if len(a) == 32 and max(a) < 1500 and sum(1 for x in a if x > 0) > 8:
        print(f'u16 candidate @ {start:#x}: {list(a[:16])}')
        break
