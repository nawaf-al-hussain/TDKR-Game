#!/usr/bin/env python3
"""S36 T1: disassemble CNavMeshNova::Create @0x1d17cc fully — find the
portal-zone read sequence after the 15-B cell loop."""
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

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
md.detail = False

def disasm(va, n_bytes, label):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    out = []
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        out.append(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        if ins.address >= va + n_bytes:
            break
    print('\n'.join(out))

if __name__ == '__main__':
    # Create is large; disassemble 0x1d17cc .. ~0x1d2600
    disasm(0x1d17cc, 0x800, 'CNavMeshNova::Create part1')
    disasm(0x1d1c6c, 0x200, 'record loop')
    disasm(0x1d1e6c, 0x900, 'part3 after loop')
