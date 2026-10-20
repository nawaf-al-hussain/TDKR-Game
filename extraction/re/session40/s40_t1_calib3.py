#!/usr/bin/env python3
"""S40 T1b calibration round 3: exact color pipeline tables."""
import numpy as np
import texture2ddecoder as t2d

def dec(b8):
    return np.frombuffer(t2d.decode_etc1(bytes(b8), 4, 4), np.uint8).reshape(4, 4, 4)

# out as function of base (diff mode, delta=0, mods=0, table t1=0)
print('base sweep (R channel, texel (0,0), x=0 col -> mod bits from byte5/7=0):')
row = []
for b in range(32):
    img = dec([b << 3 & 0xff, 0, 0, 0x02, 0, 0, 0, 0])
    row.append(int(img[0, 0, 0]))  # R = index0? (byte0 drove c2 in RGBA view; here [R?])
print(row)
# NOTE: img channel order TBD: byte0 varies -> which index? check:
img = dec([0xE0, 0, 0, 0x02, 0, 0, 0, 0])
print('byte0=0xE0 ->', tuple(img[0,0]), ' byte1=0xE0 ->', tuple(dec([0,0xE0,0,0x02,0,0,0,0])[0,0]),
      ' byte2=0xE0 ->', tuple(dec([0,0,0xE0,0x02,0,0,0,0])[0,0]))

# delta sweep at base 10
print('delta sweep (base 10, byte0=0x50|d):')
print([int(dec([(10 << 3 | d) & 0xff, 0, 0, 0x02, 0, 0, 0, 0])[0, 0, 0]) for d in range(8)])
# delta sweep with NEGATIVE delta (base 10, d=7 = -1)
print('delta sweep (base 20 = 0xA0):')
print([int(dec([(20 << 3 | d) & 0xff, 0, 0, 0x02, 0, 0, 0, 0])[0, 0, 0]) for d in range(8)])

# mod value sweep: use x=2 column (mod bits byte4/6) with base 10 R
print('mod sweep at texel (2,0): byte4 bit0=low, byte6 bit0=high:')
for low in range(2):
    for high in range(2):
        b4 = low & 1
        b6 = (high & 1)
        img = dec([(10 << 3) & 0xff, 0, 0, 0x02, b4, 0, b6, 0])
        print(f'  low={low} high={high}: R={int(img[0,2,0])}')

# table selection: t1 (bits 7-5) applies to x<2 (flip=0)? use texel (0,0) and (3,0)
print('table assignment: vary t1 (bits7-5) / t2 (bits4-2), read texels (0,0) and (3,0):')
for t1 in range(4):
    for t2 in range(4):
        b3 = (t1 << 5) | (t2 << 2) | 0x02
        img = dec([(10 << 3) & 0xff, 0, 0, b3, 0, 0, 0, 0])
        print(f'  t1={t1} t2={t2}: (0,0)={int(img[0,0,0])} (3,0)={int(img[0,3,0])} (2,0)={int(img[0,2,0])}')
