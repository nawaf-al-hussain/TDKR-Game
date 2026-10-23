#!/usr/bin/env python3
"""s54 T1 step 3: full disassembly sweep of GenerateComponentTemplate @0x368ac0 (ARM).
Extract every class-id constant (movw/movt pairs, cmp immediates, literal pools),
every vtable literal and BL per branch; find CComponentGlide (vptr 0xbd8998).
"""
import struct
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

GCT = 0x368ac0
SIZE = 11600  # ~11.3 KB
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = True

off = v2o(GCT)
code = data[off:off + SIZE]
insns = list(md.disasm(code, GCT))
print('disassembled %d instructions from %#x' % (len(insns), GCT))

# collect movw/movt chains: class ids are built via movw+movt into a reg
movw = {}  # addr -> (rd, imm16)
for ins in insns:
    if ins.mnemonic == 'movw':
        ops = ins.op_str.split(', ')
        rd = ops[0]
        imm = int(ops[1].replace('#', ''), 0)
        movw[ins.address] = (rd, imm)
    elif ins.mnemonic == 'movt':
        ops = ins.op_str.split(', ')
        rd = ops[0]
        imm = int(ops[1].replace('#', ''), 0)
        # find most recent movw to same rd
        for a in reversed(sorted(movw)):
            if a < ins.address and movw[a][0] == rd:
                val = (imm << 16) | movw[a][1]
                if val > 0x10000:
                    print('%#x: movw/movt r -> %#010x' % (a, val))
                break

# literal pools: words inside the function range that look like ids or vtables
print('\nliteral-pool words > 0x10000 (excluding code):')
seen = set()
for a in range(GCT, GCT + SIZE, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    if 0x10000000 <= w <= 0xffffffff and w not in seen:
        seen.add(w)
        print('  %#x: %#x' % (a, w))

# BL targets
print('\nBL targets:')
bls = {}
for ins in insns:
    if ins.mnemonic in ('bl', 'blx'):
        try:
            t = int(ins.op_str.replace('#', ''), 0)
        except ValueError:
            continue
        bls.setdefault(t, []).append(ins.address)
for t, srcs in sorted(bls.items()):
    print('  -> %#x  from %s' % (t, [hex(s) for s in srcs[:4]]))
