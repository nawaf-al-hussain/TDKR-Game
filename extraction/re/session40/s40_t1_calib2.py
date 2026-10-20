#!/usr/bin/env python3
"""S40 T1b calibration round 2: exact field->texel map, channel order,
expansion + mod-value table."""
import numpy as np
import texture2ddecoder as t2d

def dec(block8):
    out = t2d.decode_etc1(bytes(block8), 4, 4)
    return np.frombuffer(out, np.uint8).reshape(4, 4, 4)

# --- channel order: vary byte0 only
base = [0xE0, 0x00, 0x00, 0x02, 0, 0, 0, 0]   # byte0: base 28, d0 (28<<3=224)
img0 = dec(base)
base2 = [0x00, 0xE0, 0x00, 0x02, 0, 0, 0, 0]  # byte1: base 28
img1 = dec(base2)
base3 = [0x00, 0x00, 0xE0, 0x02, 0, 0, 0, 0]  # byte2: base 28
img2 = dec(base3)
print('byte0 block texel(0,0):', img0[0,0], ' (R,G,B,A?)')
print('byte1 block texel(0,0):', img1[0,0])
print('byte2 block texel(0,0):', img2[0,0])

# --- field -> texel map: set field i to 01 (only), diff mode, all bases 0
print('\nfield->texel map (field i = byte 4+i//4, bits 2*(i%%4)..):')
changes = {}
for i in range(16):
    b = [0x02, 0x02, 0x02, 0x02, 0, 0, 0, 0]  # diff mode, bases 0 (byte3=0x02)
    # NOTE byte3=0x02: diff=1. base bytes 0x02: base=0 d=2
    ref = dec(bytes(b))
    b[4 + i // 4] |= 1 << (2 * (i % 4))
    img = dec(bytes(b))
    ys, xs = np.where(np.any(img != ref, axis=2))
    changes[i] = [(int(x), int(y)) for y, x in zip(ys, xs)]
for i in range(16):
    print(f'  field {i:2d}: {changes[i]}')

# --- mod value table: diff mode, base R=10, all fields = v
print('\nmod values (R base 10, byte3=0x02, table1=0):')
for v in range(4):
    b = [(10 << 3) & 0xff, (10 << 3) & 0xff, (10 << 3) & 0xff, 0x02,
         v * 0x55, v * 0x55, v * 0x55, v * 0x55]
    img = dec(bytes(b))
    print(f'  v={v}: texel(0,0)={tuple(img[0,0])} texel(3,3)={tuple(img[3,3])}')

# --- flip semantics: individual mode, distinct per-half tables
print('\nflip test: individual mode (byte3 bit1=0), t1=1(t7-5), t2=2(t4-2):')
b3 = (1 << 5) | (2 << 2) | 0
for flip in [0, 1]:
    b = [0x00, 0x00, 0x00, b3 | flip, 0x00, 0x00, 0x00, 0x00]
    img = dec(bytes(b))
    print(f'  flip={flip}: col0={ [int(img[y,0][0]) for y in range(4)] }')
    print(f'            row0={ [int(img[0,x][0]) for x in range(4)] }')
