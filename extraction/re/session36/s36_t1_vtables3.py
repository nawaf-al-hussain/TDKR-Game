#!/usr/bin/env python3
"""S36 T1a2: correct vtables (ARM pc = addr+8), dump, disasm both Load impls."""
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

def rd32(v):
    fo = v2f(v)
    return struct.unpack_from('<I', d, fo)[0] if fo is not None else None

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

def disasm(va, n, label=''):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    for ins in md.disasm(d[fo:fo + n], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')

# GRID-A: add r1,pc,r1 @0x3fe410 -> pc=0x3fe418; +8 at 0x3fe418
vtA = 0x3fe418 + rd32(0x3fe43c) + 8
# GRID-B: add r3,pc,r3 @0x3fe3b0 -> pc=0x3fe3b8; +8
vtB = 0x3fe3b8 + rd32(0x3fe3bc) + 8
print(f'vptrA=0x{vtA:x}  vptrB=0x{vtB:x}')
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
for name, vt in (('A:SimpleNavMeshGrid', vtA), ('B:SimpleNavMeshQuadtree', vtB)):
    print(f'--- {name} vtable entries (at vptr) ---')
    for i in range(6):
        v = rd32(vt + 4 * i)
        s = syms.get(hex(v))
        print(f'  +{4*i:02x}: 0x{v:08x} {s[1] if s and len(s)>1 else ""}')
print()
disasm(0x3fe3e8, 0x20, 'CSimpleNavMeshQuadtree::Load')
disasm(0x3fe79c, 0x2e4, 'CSimpleNavMeshGrid::Load')
