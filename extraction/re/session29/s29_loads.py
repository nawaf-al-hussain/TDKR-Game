#!/usr/bin/env python3
"""S29 T1: disassemble Load fns 0x2e7430 (0xC69A6A7) and 0x2a0728 (0x2AD64F3D)."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

for label, addr, n in [('Load(0xC69A6A7) @0x2e7430', 0x2e7430, 60),
                       ('neighbor 0x2e73cc', 0x2e73cc, 20),
                       ('Load(0x2AD64F3D) @0x2a0728', 0x2a0728, 60)]:
    print(f'===== {label} =====')
    for ins in list(md.disasm(data[addr:addr + n * 4], addr))[:n]:
        print(f'  {ins.address:#x}: {ins.mnemonic} {ins.op_str}')
    print()
