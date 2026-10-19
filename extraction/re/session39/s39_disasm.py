#!/usr/bin/env python3
"""Disassemble PVRTCDecompress regions: the mode-bit branch (0x747bb0),
the opA branch (0x747da8), and the modulation extraction (~0x74744c+)."""
import struct
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    p_type, p_offset, p_vaddr, _, p_filesz, _ = struct.unpack_from('<6I', d, o)
    if p_type == 1: segs.append((p_vaddr, p_offset, p_filesz))


def v2o(va):
    for vaddr, off, sz in segs:
        if vaddr <= va < vaddr + sz: return off + (va - vaddr)
    raise ValueError(hex(va))


md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False


def dis(lo, hi):
    o = v2o(lo)
    code = d[o:o + (hi - lo)]
    out = []
    for i in md.disasm(code, lo):
        out.append(f'{i.address:08x}: {i.mnemonic:8s} {i.op_str}')
    return '\n'.join(out)


if __name__ == '__main__':
    import sys
    lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
    print(dis(lo, hi))
