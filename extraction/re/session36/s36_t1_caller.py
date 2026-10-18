#!/usr/bin/env python3
"""S36 T1e: disassemble around the Create caller 0x48afe4 (function context)."""
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

syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
bn = syms['by_name']
# find enclosing function name for 0x48afe4
cands = [(v, k) for k, v in bn.items() if isinstance(v, list) and abs(v[0] - 0x48afe4) < 0x2000]
for v, k in sorted(cands)[:12]:
    print(hex(v), k)
print()
disasm(0x48af00, 0x180, 'around Create caller')
