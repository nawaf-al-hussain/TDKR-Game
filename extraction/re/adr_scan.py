#!/usr/bin/env python3
"""Scan .text for ADR (ADD/SUB Rd, PC, #imm) targeting the zone-string block
0xb40600..0xb40800, and more generally find all functions referencing it."""
import struct
import numpy as np

d = open('/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so', 'rb').read()
w = np.frombuffer(d[0xa5d80:0xc22490], '<u4')
base = 0xa5d80
hits = []
for i in range(len(w)):
    x = int(w[i])
    if (x & 0x0FBF0000) == 0x028F0000:   # ADD Rd, PC, #imm (cond, S=0, opcode=1000)
        imm12 = x & 0xFFF
        rd = (x >> 12) & 0xF
        tgt = (base + i * 4) + 8 + imm12
        if 0xb40600 <= tgt <= 0xb40800:
            hits.append((base + i * 4, tgt, 'add'))
    elif (x & 0x0FBF0000) == 0x024F0000:  # SUB Rd, PC, #imm
        imm12 = x & 0xFFF
        rd = (x >> 12) & 0xF
        tgt = (base + i * 4) + 8 - imm12
        if 0xb40600 <= tgt <= 0xb40800:
            hits.append((base + i * 4, tgt, 'sub'))
print('ADR hits into zone-string block:')
for off, tgt, kind in hits:
    print(f'  code 0x{off:08x} {kind} -> 0x{tgt:x}')
