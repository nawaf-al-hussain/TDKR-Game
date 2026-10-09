#!/usr/bin/env python3
"""Scan ARM A32 code for MOVW/MOVT pairs referencing the zone-string region
(0xb40700-0xb40790) to locate the zone-payload parsing functions."""
import struct
import numpy as np

d = open('/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so', 'rb').read()
w = np.frombuffer(d[:0xbbe1ec], '<u4')

def decode_movw(x):
    if (x & 0x0FF00000) != 0x03000000:
        return None
    imm4 = (x >> 16) & 0xF
    imm12 = x & 0xFFF
    return (imm4 << 12) | imm12

def decode_movt(x):
    if (x & 0x0FF00000) != 0x03400000:
        return None
    imm4 = (x >> 16) & 0xF
    imm12 = x & 0xFFF
    return (imm4 << 12) | imm12

# collect movw/movt per register, pair them when within 32 instructions
regs = {}   # reg -> (imm, idx) from movw
hits = []
for i in range(len(w)):
    x = int(w[i])
    rd = (x >> 12) & 0xF
    mvw = decode_movw(x)
    mvt = decode_movt(x)
    if mvw is not None:
        regs[rd] = (mvw, i)
    elif mvt is not None and rd in regs:
        base, j = regs[rd]
        if i - j <= 32:
            addr = (mvt << 16) | base
            if 0xb40600 <= addr <= 0xb40800:
                hits.append((i * 4, addr))
    elif mvw is None and mvt is None:
        pass
print('MOVW/MOVT refs into zone-string region:')
for off, addr in hits:
    print(f'  code 0x{off:08x} -> 0x{addr:x}')
