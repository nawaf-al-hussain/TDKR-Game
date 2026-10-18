#!/usr/bin/env python3
"""S36 T1a: resolve CSimpleNavMeshGrid vtables -> Load (slot 2) implementations."""
import capstone, struct

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

def rd32(v):
    fo = v2f(v)
    if fo is None: return None
    return struct.unpack_from('<I', d, fo)[0]

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

def disasm(va, n_bytes, label=''):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')

# ctor @0x3fe404 stores vtable ptr as first word — find it
print('--- CSimpleNavMeshGrid ctor @0x3fe404 ---')
disasm(0x3fe404, 0x60)
print('--- class2 ctor @0x3fe390 ---')
disasm(0x3fe390, 0x74)
