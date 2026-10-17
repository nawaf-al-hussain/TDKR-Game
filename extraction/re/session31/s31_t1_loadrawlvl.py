#!/usr/bin/env python3
"""S31 T1: disassemble CLevel::LoadRawLvl @0x489100..0x48957c and identify
the record-loop bound register (r16 claim: loop bound = stream size)."""
import struct, bisect, json, sys

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    h = d[e_phoff + i * e_phentsize: e_phoff + (i + 1) * e_phentsize]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIIII', h, 0)
    if p_type == 1:
        segs.append((p_vaddr, p_filesz, p_offset))


def v2f(va):
    for a, s, o in segs:
        if a <= va < a + s:
            return o + (va - a)


START, END = 0x489100, 0x48957c
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False
code = d[v2f(START): v2f(START) + (END - START)]
out = []
for ins in md.disasm(code, START):
    line = f'{ins.address:#08x}  {ins.mnemonic:<8s} {ins.op_str}'
    out.append(line)
txt = '\n'.join(out)
print(txt)
open('/home/z/my-project/scripts/loadrawlvl_disasm.txt', 'w').write(txt)
