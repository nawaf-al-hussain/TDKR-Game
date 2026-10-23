#!/usr/bin/env python3
"""s54 T1 step 8: brute-force pc-rel vtable computation over the WHOLE GCT range.
For each literal word L at P in [GCT, GCT+SIZE]: candidate add-site A = VT - 8 - L.
Check word@A == add rd, pc, rm  (0xE08Fxxxx with Rd==Rm) or sub variant (0xE24Fxxxx).
Report for CComponentGlide vptr 0xbd8998 and dump that case's disassembly + class id.
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

GCT, SIZE = 0x368ac0, 0x36b7c0 - 0x368ac0
VT = 0xbd8998  # CComponentGlide stored vptr (_ZTV+8)

found = []
for P in range(GCT, GCT + SIZE, 4):
    L = struct.unpack_from('<I', data, v2o(P))[0]
    # add rX, pc, rX form: A + 8 + L == VT  -> A = VT - 8 - L
    A = VT - 8 - L
    if GCT <= A < GCT + SIZE:
        w = struct.unpack_from('<I', data, v2o(A))[0]
        if (w & 0x0fff0000) == 0x008f0000:  # add rd, pc, rm-ish
            found.append(('add', P, A, w))
    # ldr rX, [pc, #imm] with the pool entry containing VT directly was ruled out,
    # but also check plain absolute literal (in case some case used one)
    if L == VT:
        found.append(('abs', P, None, None))
for f in found:
    print(f)

if found:
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    kind, P, A, w = found[0]
    lo = min(x for x in (P, A) if x is not None) - 0x80
    hi = max(x for x in (P, A) if x is not None) + 0x40
    print('\ndisasm around the case (from %#x):' % lo)
    # find preceding movw/movt id within 0x200 back
    idval = None
    idaddr = None
    movw = {}
    for a in range(lo - 0x400, lo, 4):
        ww = struct.unpack_from('<I', data, v2o(a))[0]
        if (ww & 0x0fff0000) == 0x03000000:  # movw
            rd = (ww >> 12) & 0xf
            imm = ((ww >> 4) & 0xf000) | (ww & 0xfff)
            movw[rd] = imm
        elif (ww & 0x0fff0000) == 0x03400000:  # movt
            rd = (ww >> 12) & 0xf
            imm = ((ww >> 4) & 0xf000) | (ww & 0xfff)
            if rd in movw:
                idval = (imm << 16) | movw[rd]
                idaddr = a
    print('nearest preceding movw/movt id: %#x @%#x' % (idval, idaddr) if idval else 'no id found before')
    for ins in md.disasm(data[v2o(lo):v2o(hi) - v2o(lo)], lo):
        print('%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
