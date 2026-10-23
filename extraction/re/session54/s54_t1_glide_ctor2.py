#!/usr/bin/env python3
"""s54 T1 step 2: find CComponentGlide ctor (function storing vptr 0xbd8998),
then BL-caller scan to learn which factory instantiates it."""
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

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

# 1. disasm backward window ending at the literal pool @0x52b54
print('=== window 0x52a40..0x52b58 (before literal pool) ===')
off = v2o(0x52a40)
for ins in md.disasm(data[off:off + (0x52b58 - 0x52a40)], 0x52a40):
    print('%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))

# 2. scan the whole code segment for literal 0xbd8998 references via LDR rX, [pc, #imm]
#    (already know only one pool hit @0x52b54) -> find the function start by scanning
#    backwards for 'push' prologue from 0x52b54
print('\n=== backward prologue scan from 0x52b54 ===')
o = v2o(0x52b54)
start = None
for back in range(0x52b54, 0x51b54, -4):
    oo = v2o(back)
    w = struct.unpack_from('<I', data, oo)[0]
    if (w & 0xffff0000) == 0xe92d0000 or (w & 0xffff0000) == 0xe92d4000:  # push {...}
        start = back
        break
print('prologue candidate:', hex(start) if start else None)
if start:
    print('=== ctor disasm from %s ===' % hex(start))
    for ins in md.disasm(data[v2o(start):v2o(0x52b54)], start):
        print('%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))

# 3. BL-caller scan: find all BLs in code segment targeting the ctor
if start:
    print('\n=== BL callers of %#x ===' % start)
    callers = []
    lo, hi = 0x8000, 0xbbf000
    for a in range(lo, hi, 4):
        w = struct.unpack_from('<I', data, v2o(a))[0]
        if (w & 0x0f000000) == 0x0b000000:  # BL
            imm = w & 0x00ffffff
            if imm & 0x800000:
                imm -= 0x1000000
            target = a + 8 + imm * 4
            if target == start:
                callers.append(a)
    for c in callers:
        print('  BL from %#x' % c)
    print('total callers:', len(callers))
