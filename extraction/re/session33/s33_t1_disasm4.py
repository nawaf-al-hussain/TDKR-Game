#!/usr/bin/env python3
"""S33 T1: disasm track builder + sampler accessor readers."""
import capstone, struct

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

def disasm(va, n_bytes, label, mode=capstone.CS_MODE_ARM, maxn=400):
    fo = v2f(va)
    if fo is None:
        print(f'{label}: 0x{va:x} unmapped'); return
    md = capstone.Cs(capstone.CS_ARCH_ARM, mode)
    print(f'===== {label} @0x{va:x} =====')
    n = 0
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        n += 1
        if n > maxn: break

disasm(0x78e53c, 0x260, 'sub_78e53c (element -> track)')
disasm(0x75c088, 0x200, 'CAnimationTrackEx::getValue(accessor, float, void*, bool)')
