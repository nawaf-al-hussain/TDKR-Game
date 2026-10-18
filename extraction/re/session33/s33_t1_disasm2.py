#!/usr/bin/env python3
"""S33 T1: disasm helpers of CAnimationBlock ctor."""
import capstone, struct, json

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * 32
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz, p_memsz))

def v2f(v):
    for vaddr, off, filesz, memsz in segs:
        if vaddr <= v < vaddr + filesz:
            return off + (v - vaddr)
    return None

def disasm(va, n_bytes, label, mode=capstone.CS_MODE_ARM, maxn=300):
    fo = v2f(va)
    if fo is None:
        print(f'{label}: vaddr 0x{va:x} not mapped'); return
    md = capstone.Cs(capstone.CS_ARCH_ARM, mode)
    print(f'\n===== {label} @0x{va:x} =====')
    n = 0
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        n += 1
        if n > maxn: break

disasm(0x756b68, 0x400, 'sub_756b68 (called from ctor)', maxn=250)
disasm(0x78e53c, 0x300, 'sub_78e53c (track build?)', maxn=200)
