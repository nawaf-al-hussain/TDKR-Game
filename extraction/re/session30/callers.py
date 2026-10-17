#!/usr/bin/env python3
"""Find all BL callers of a function (and movw/movt pool refs)."""
import struct, sys
sys.path.insert(0, '/home/z/my-project/scripts/s30')
from disarm import DATA, SEGS
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

target = int(sys.argv[1], 16)
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
callers = []
for v, o, fs, ms in SEGS:
    code = DATA[o:o + fs]
    for ins in md.disasm(code, v):
        if ins.mnemonic == 'bl':
            try:
                t = int(ins.op_str.lstrip('#'), 16)
            except Exception:
                continue
            if t == target:
                callers.append(ins.address)
print(f'callers of 0x{target:x}: {[hex(c) for c in callers]}')
