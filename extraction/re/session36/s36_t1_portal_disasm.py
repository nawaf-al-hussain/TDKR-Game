#!/usr/bin/env python3
"""S36 T1b: disassemble CNavMeshNova portal funcs + Init + AppendPath entry."""
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

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

def disasm(va, n, label=''):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    for ins in md.disasm(d[fo:fo + n], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
    print()

import sys
which = sys.argv[1] if len(sys.argv) > 1 else 'small'
if which == 'small':
    disasm(0x1d2c14, 0x14, 'GetNeigh(u16, s8)')
    disasm(0x1d2c28, 0xa8, 'CanReachCellFrom(u16,u16,int)')
    disasm(0x1d2cd0, 0x90, 'GetCellPortalTo(u16,s8,line3d&)')
    disasm(0x1d2d60, 0xd8, 'GetCellsPortal(u16,s8,line3d&)')
    disasm(0x1d2e38, 0x40, 'GetCellsPortal(u16,s8)')
    disasm(0x1d2e78, 0x40, 'IsSamePortal(u16,s8,u16,s8)')
    disasm(0x1d2eb8, 0x58, 'GetPortalId(u16,s8)')
elif which == 'init':
    disasm(0x1d20e4, 0x104, 'CNavMeshNova::Init')
elif which == 'append':
    disasm(0x1d41c4, 0x10c, 'CNavMeshQuery::AppendPath(nova,from,to,bool)')
elif which == 'search':
    disasm(0x1d44b0, 0x300, 'CNavMeshQuery::SearchPortalPath')
elif which == 'append6':
    disasm(0x1d4aa8, 0x200, 'AppendPath(nova,s16,from,to,s16,u32)')
