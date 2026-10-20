#!/usr/bin/env python3
"""S40 T1b: calibrate the exact ETC1 bit conventions used by texture2ddecoder
(= the reference pool) via synthetic blocks. Positive control for our decoder.

Probe plan:
  P1: diff mode, all mods=1 (+8): check base+delta extraction from bytes 0-2
  P2: single-texel mod field -> map bit index -> (x,y) (row-major vs column-major)
  P3: byte3 bit1 = diff, bit0 = flip (individual mode + flip semantics)
  P4: table1 (bits7-5) vs table2 (bits4-2) assignment to top/bottom half
  P5: 5->8 bit expansion formula
"""
import numpy as np
import texture2ddecoder as t2d

def dec(block8):
    out = t2d.decode_etc1(bytes(block8), 4, 4)
    a = np.frombuffer(out, np.uint8).reshape(4, 4, 4)  # BGRA per texel
    return a[0, 0, 2], a  # first texel R, full array

MODS = [[2, 8, -2, -8], [5, 17, -5, -17], [9, 29, -9, -29], [13, 42, -13, -42]]

def expand5(v): return ((v << 3) | (v >> 2)) & 255

print('P1: diff mode, byte0/1/2 = base<<5|delta')
b = bytes([0xF8, 0x40, 0x00, 0x02, 0x55, 0x55, 0x55, 0x55])  # mods all=01 (+8)
r0, img = dec(b)
# R base 31, d 0 -> paint 31; G base 10 -> paint 10; B 0
print('  texel(0,0) BGRA:', img[0,0][::-1], ' (expect R=31-8+... mod idx1=+8: R=39->clamp? R=31*?') 

print('\nP2: single mod field at bit positions -> which texel changes')
base = bytes([0xF8, 0x40, 0x00, 0x02, 0, 0, 0, 0])  # all mods 00 (+2)
_, img0 = dec(base)
for bitpos in [0, 1, 2, 3, 6, 7, 24, 30]:
    bb = bytearray(base)
    bb[4 + bitpos // 8] |= 1 << (bitpos % 8)   # set bit -> mod field becomes 01 (+8)
    _, img = dec(bytes(bb))
    ys, xs = np.where(np.any(img != img0, axis=2))
    print(f'  bit {bitpos:2d}: changed texels (x,y):', [(int(x), int(y)) for y, x in zip(ys, xs)])

print('\nP3: byte3 bit semantics (individual mode, tables 0/0)')
# individual mode: byte3 bit1 = 0. bytes 0-2 = [R1|R2][G1|G2][B1|B2] 4444?
for b3, note in [(0x00, 'diff=0 flip=0'), (0x01, 'flip=1'), (0x02, 'diff=1')]:
    b = bytes([0x12, 0x34, 0x56, b3, 0, 0, 0, 0])
    _, img = dec(b)
    print(f'  byte3={b3:#04x} ({note}) col0:', [tuple(img[y,0][::-1][:3]) for y in range(4)])
    print(f'                  col3:', [tuple(img[y,3][::-1][:3]) for y in range(4)])

print('\nP4: table assignment (diff mode, flip=0: top half uses table?)')
for t1, t2 in [(1, 0), (0, 1), (2, 3)]:
    b3 = (t1 << 5) | (t2 << 2) | 0x02
    b = bytes([0xF8, 0x40, 0x00, b3, 0b01000100, 0b01000100, 0b01000100, 0b01000100])
    # mods: alternating 0(+2)/1(+8)
    _, img = dec(b)
    print(f'  t1={t1} t2={t2}: row0 mods:', [tuple(img[0,x][::-1][:3]) for x in range(4)])
    print(f'               row3 mods:', [tuple(img[3,x][::-1][:3]) for x in range(4)])

print('\nP5: 5->8 expansion (diff mode, mod=00(+2), base from byte0)')
for base5 in [0, 1, 15, 16, 31]:
    b = bytes([((base5 << 5) | 0) & 0xff, 0x40, 0x00, 0x02, 0, 0, 0, 0])
    _, img = dec(b)
    got = img[0,0][2]
    print(f'  base={base5:2d}: out R={got}, spec (b<<3|b>>2)-2*255/31? clamp({base5}+2)*255/31={min(base5+2,31)}')
