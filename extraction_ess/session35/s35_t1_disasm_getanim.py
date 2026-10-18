#!/usr/bin/env python3
"""S35 T1a: disassemble CColladaDatabase::getAnimation @0x7badfc,
getAnimationSegment @0x7bb770, CAnimationBlock ctor @0x755834.
Goal: derive the clip->segment mapping from the engine, not index order."""
import capstone, struct, json

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
    return None

md_arm = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
md_thumb = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)

def disasm(va, n_bytes, label, thumb=False):
    fo = v2f(va)
    if fo is None:
        print(f'{label}: vaddr 0x{va:x} not mapped'); return []
    md = md_thumb if thumb else md_arm
    print(f'\n===== {label} @0x{va:x} (file 0x{fo:x}) =====')
    out = []
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        out.append((ins.address, ins.mnemonic, ins.op_str))
    return out

disasm(0x7badfc, 0x180, 'CColladaDatabase::getAnimation(name, chType, chType)')
disasm(0x7bb770, 0x200, 'CColladaDatabase::getAnimationSegment(int)')
disasm(0x755834, 0x300, 'CAnimationBlock ctor(db, clip, int)')
