#!/usr/bin/env python3
"""S29 T1: disassemble id-literal sites to find dispatch + GetClassId patterns."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dis(start, n=40, back=0x10):
    out = []
    for ins in md.disasm(data[start - back:start + n * 4], start - back):
        out.append(f'  {ins.address:#x}: {ins.mnemonic} {ins.op_str}')
    return out

for label, addr in [('0xC69A6A7 site', 0x369d58), ('0x2AD64F3D site A (factory)', 0x22453c),
                    ('0x2AD64F3D site B', 0x2e1db0), ('0x2AD64F3D site C', 0x36acd0),
                    ('0x17AC851F site 1', 0x14f3a4)]:
    print(f'===== {label} @ {addr:#x} =====')
    for l in dis(addr, 30):
        print(l)
    print()
