#!/usr/bin/env python3
"""S36 T1d: xref CNavMeshNova::Create (0x1d17cc) — bl and literal pool refs."""
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

# 1) literal-pool references to 0x1d17cc
target = 0x1d17cc
hits = []
for vaddr, off, filesz in segs:
    blob = d[off:off + filesz]
    tb = struct.pack('<I', target)
    start = 0
    while True:
        i = blob.find(tb, start)
        if i < 0: break
        hits.append(vaddr + i)
        start = i + 4
print('literal refs to 0x1d17cc:', [hex(h) for h in hits])

# 2) bl instructions encoding it
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
# scan text segment for BL (F000F800-ish mask) — approximate: search common encodings
# ARM BL: cond 1011 imm24 ; compute for each hit candidate region around literal refs' functions
def disasm(va, n, label=''):
    fo = v2f(va)
    print(f'===== {label} @0x{va:08x} =====')
    for ins in md.disasm(d[fo:fo + n], va):
        if ins.mnemonic in ('bl', 'b') and hex(target)[2:] in ins.op_str:
            print(f'  0x{ins.address:08x}: {ins.mnemonic} {ins.op_str}')

# check the region around each literal ref (function start guess)
for h in hits:
    print(f'literal @0x{h:08x}')
