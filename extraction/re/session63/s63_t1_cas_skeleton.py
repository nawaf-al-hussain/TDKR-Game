#!/usr/bin/env python3
"""S63 T1: extract the READ-call skeleton + loop structure of CContainerStateAnimation::Load (0x3b45f4..).
Uses the s62_reader dump machinery; walks the linear disasm, lists every CMemoryStream::Read*
call site, every back-edge (loop), and the direct bl calls (nested Load helpers)."""
import struct, subprocess, bisect, sys

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
    return None

nm = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for l in nm.splitlines():
    q = l.split()
    if len(q) == 3:
        try:
            syms.append((int(q[0], 16), q[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

def dem(n):
    return subprocess.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

READS = {}
for a, t in ((0x339510, 'c'), (0x339574, 'c'), (0x3395d8, 'c'), (0x339634, 'c'),
             (0x339690, 'c'), (0x3396ec, 'c'),
             (0x339758, 's'), (0x3397dc, 's'), (0x339868, 's'),
             (0x339914, 'i'), (0x3399d4, 'i'), (0x339ab4, 'i'),
             (0x339b94, 'f'), (0x339c58, 'f'),
             (0x33a0d4, 'STR'), (0x33ab94, 'STR'), (0x33ad74, 'STR'), (0x33a730, 'STRW'), (0x33b01c, 'STRW'),
             (0x33b3d0, '3f'), (0x33b4dc, '2f'), (0x33b6ac, '4f')):
    READS[a] = t

START = 0x3b45f4
i0 = bisect.bisect_right(addrs, START) - 1
END = 0x3b7928
print('CAS::Load %x..%x (%d B)' % (START, END, END - START))

o = v2o(START)
insns = list(md.disasm(data[o:o + (END - START)], START))
print('insns:', len(insns))

# literal pool values
lits = {}
for ins in insns:
    if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        pc = (ins.address + 8) & ~3
        va = pc + imm
        vo = v2o(va)
        vv = struct.unpack_from('<I', data, vo)[0] if vo else None
        lits[ins.address] = vv

events = []
for idx, ins in enumerate(insns):
    m = ins.mnemonic
    if m.startswith('bl') and ins.op_str.startswith('#'):
        try:
            tgt = int(ins.op_str[1:], 16)
        except Exception:
            continue
        if tgt in READS:
            events.append((ins.address, 'READ ' + READS[tgt]))
        elif tgt < START or tgt >= END:
            s, off = sym_of(tgt)
            events.append((ins.address, 'CALL %s+%x' % (dem(s)[:60], off)))
        else:
            s, off = sym_of(tgt)
            events.append((ins.address, 'bl-inner %x (%s)' % (tgt, dem(s)[:44])))
    elif m[0] == 'b' and m != 'bl' and m != 'blx':
        try:
            tgt = int(ins.op_str[1:].replace('#', ''), 16)
        except Exception:
            continue
        if tgt <= ins.address:
            events.append((ins.address, 'LOOPBACK -> %x (dist %d)' % (tgt, ins.address - tgt)))

# compress: only show READ/loop/CALL events
for a, t in events:
    print('%08x  %s' % (a, t))
