#!/usr/bin/env python3
"""S36 T1a: resolve grid vtables and dump slots -> find Load."""
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
    return struct.unpack_from('<I', d, fo)[0] if fo is not None else None

# ctor1: ldr r1,[pc,#0x30] @0x3fe404 -> lit @0x3fe43c ; r1 = 0x3fe410 + lit; vt = r1+8
lit1 = rd32(0x3fe43c)
vt1 = 0x3fe410 + lit1 + 8
# ctor2: ldr r3,[pc,#0xc] @0x3fe390 -> lit @0x3fe3a4 ; r3 = 0x3fe398 + lit; vt = r3+8
lit2 = rd32(0x3fe3a4)
vt2 = 0x3fe398 + lit2 + 8
print(f'vt1 (CSimpleNavMeshGrid) = 0x{vt1:x}  (lit 0x{lit1:x})')
print(f'vt2 (class B)           = 0x{vt2:x}  (lit 0x{lit2:x})')

for name, vt in (('GRID-A', vt1), ('GRID-B', vt2)):
    print(f'--- {name} vtable @0x{vt:x} ---')
    for i in range(8):
        v = rd32(vt + 4 * i)
        print(f'  slot {i}: 0x{v:08x}')

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
def disasm(va, n, label=''):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    for ins in md.disasm(d[fo:fo + n], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')

import json
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
for name, vt in (('GRID-A', vt1), ('GRID-B', vt2)):
    for i in range(8):
        v = rd32(vt + 4 * i)
        s = syms.get(hex(v))
        if s: print(f'{name} slot{i} 0x{v:08x} = {s[1] if len(s)>1 else s}')
