#!/usr/bin/env python3
"""T2: the stride verdict. Decode the vertex data at stride 40 vs 80 and
compare triangle edge-length coherence using the real index buffer."""
import struct, array, math, random

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BLOCK = 0x4a58
DATA = BLOCK + 0x6c          # floats begin here (bf1b45f1 = -0.6065)
DLEN = u32(BLOCK + 0x68)
END = BLOCK + 0x6c + DLEN
print(f'data {DATA:#x}..{END:#x} ({DLEN} B)')

# index buffer: starts at END; count until non-triangle-ish
idx = array.array('H')
o = END
while o + 2 <= len(d):
    v = u16(o)
    if v > 2000:
        break
    idx.append(v)
    o += 2
print(f'index buffer: {len(idx)} u16 @ {END:#x}, max idx = {max(idx)}')
print('first 30:', list(idx[:30]))
n_tri = len(idx) // 3
print(f'triangles: {n_tri} (rem {len(idx) % 3})')

# find the periodic structure of the vertex data: word classes
words = DLEN // 4
cls = []
for k in range(words):
    v = u32(DATA + 4 * k)
    fv = struct.unpack('<f', struct.pack('<I', v))[0]
    if v == 0:
        cls.append('0')
    elif abs(fv) < 1e6 and (v >> 23) & 0xFF != 0:
        cls.append('f')
    else:
        cls.append('i')
# find period of the 'i'/'0' positions after the header (word 11)
marks = [k for k in range(11, min(words, 400)) if cls[k] in 'i0']
print('non-float word positions (first 40):', marks[:40])
if len(marks) > 3:
    diffs = [marks[i + 1] - marks[i] for i in range(len(marks) - 1)]
    print('diffs:', diffs[:20])
