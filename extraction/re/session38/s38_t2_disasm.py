#!/usr/bin/env python3
"""S38 T2.4: disassemble the engine PVRTCDecompress (0x746e34) and its thunk
(0x744148) to READ the algorithm: block layout, planes, kernel, mod table."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

SO = '/tmp/my-project/work/libKRHP.so'
import os
if not os.path.exists(SO):
    for cand in ('/tmp/my-project/work/re29/libKRHP.so', '/tmp/my-project/work/apk_lib/libKRHP.so'):
        if os.path.exists(cand): SO = cand; break
d = open(SO, 'rb').read()
print('so size', len(d))
# ELF: find text vaddr->file offset via program headers
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
md.skipdata = True
def dis(va, n=120):
    o = v2o(va)
    code = d[o:o + n * 4]
    out = []
    for ins in md.disasm(code, va):
        out.append(f'{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        if len(out) >= n: break
    return out
import sys
which = int(sys.argv[1]) if len(sys.argv) > 1 else 0
va = int(sys.argv[2], 0x10) if len(sys.argv) > 2 else 0
for l in dis(va, which): print(l)
