#!/usr/bin/env python3
"""S36 T1h: disassemble CNavMeshQuery::AppendPath.part @0x1f1234 (planner core)."""
import capstone, struct, sys

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2f(v):
    for vaddr, off, filesz in segs:
        if vaddr <= v < vaddr + filesz:
            return off + (v - vaddr)

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
n = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x2c0
fo = v2f(0x1f1234)
for ins in md.disasm(d[fo:fo + n], 0x1f1234):
    print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
