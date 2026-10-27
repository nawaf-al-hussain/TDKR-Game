#!/usr/bin/env python3
"""S63 T1 step 9: rescan CAS::Load including INLINE byte reads (ldrb from stream buffer+cursor).
Pattern: ldr rA,[r4] (buffer base); ldr rB,[r4,#0xc] (cursor); ldrb rC,[rA,rB] -> 1-byte read."""
import struct, subprocess, bisect

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    pt, po, pv, _, ps = struct.unpack_from('<5I', data, p)
    if pt == 1:
        segs.append((pv, po, ps))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

START, END = 0x3b45f4, 0x3b7928
o = v2o(START)
insns = list(md.disasm(data[o:o + (END - START)], START))

READS = {0x339914: 'i', 0x339b94: 'f', 0x33a0d4: 'STR', 0x3399d4: 'i', 0x339ab4: 'i', 0x339c58: 'f'}
events = []
for idx, ins in enumerate(insns):
    if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
        try:
            tgt = int(ins.op_str[1:], 16)
        except Exception:
            continue
        if tgt in READS:
            events.append((ins.address, 'READ ' + READS[tgt]))
    elif ins.mnemonic == 'ldrb' and ', r' in ins.op_str:
        # check provenance: base reg from [r4], offset reg from [r4,#0xc] within last 10
        regs = [r.strip() for r in ins.op_str.rstrip(']').split('[')[1].split(',')]
        if len(regs) != 2:
            continue
        base, off = regs
        okb = oko = False
        for j in range(max(0, idx - 12), idx):
            t = insns[j].mnemonic
            op = insns[j].op_str
            if t == 'ldr' and op.startswith(base + ', [r4]'):
                okb = True
            if t == 'ldr' and op.startswith(off + ', [r4, #0xc]'):
                oko = True
        if okb and oko:
            events.append((ins.address, 'READ c (inline)'))
    elif ins.mnemonic[0] == 'b' and ins.mnemonic not in ('bl', 'blx'):
        try:
            tgt = int(ins.op_str[1:].replace('#', ''), 16)
        except Exception:
            continue
        if tgt <= ins.address:
            events.append((ins.address, 'LOOP -> %x (d%d)' % (tgt, ins.address - tgt)))

for a, t in events:
    print('%08x  %s' % (a, t))
