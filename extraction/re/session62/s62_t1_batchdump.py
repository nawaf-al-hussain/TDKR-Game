#!/usr/bin/env python3
"""S62 T1: batch-dump read sequences for all readers needing derivation.
Prints each reader's stream-read list + loop structure hints (backward branches)."""
import struct, subprocess, bisect, json

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

def func_end(fn):
    i = bisect.bisect_right(addrs, fn) - 1
    return syms[i + 1][0] if i + 1 < len(syms) else fn + 0x1000

READS = {}
for a, t in ((0x339510, 'c'), (0x339574, 'c'), (0x3395d8, 'c'), (0x339634, 'c'),
             (0x339690, 'c'), (0x3396ec, 'c'),
             (0x339758, 's'), (0x3397dc, 's'), (0x339868, 's'),
             (0x339914, 'i'), (0x3399d4, 'i'), (0x339ab4, 'i'),
             (0x339b94, 'f'), (0x339c58, 'f'),
             (0x33a0d4, 'STR'), (0x33ab94, 'STR'), (0x33ad74, 'STR'), (0x33a730, 'STRW'), (0x33b01c, 'STRW'),
             (0x33b3d0, '3f'), (0x33b4dc, '2f'), (0x33b6ac, '4f')):
    READS[a] = t

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

plan = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_specplan.json'))
for nk, (r, sym) in sorted(plan['need_derive'].items()):
    fn = int(r, 16)
    end = min(func_end(fn), fn + 0x1200)
    o = v2o(fn)
    insns = list(md.disasm(data[o:o + (end - fn)], fn))
    items = []
    backedges = set()
    for ins in insns:
        if 'bl' in ins.mnemonic and ins.op_str.startswith('#'):
            tgt = int(ins.op_str[1:], 16)
            if tgt in READS:
                items.append((ins.address, READS[tgt]))
            elif tgt not in (0x206a60, 0x2069fc, 0x206c64) and 'basic_string' not in 'x':
                pass
        if ins.mnemonic == 'ldrb' and '[r' in ins.op_str:
            items.append((ins.address, 'c*'))   # inline byte read
        if ins.mnemonic in ('b', 'bne', 'beq', 'ble', 'blt', 'bgt', 'bge', 'bls', 'bhs', 'blo') and ins.op_str.startswith('#'):
            tgt = int(ins.op_str[1:], 16)
            if tgt < ins.address and tgt > fn:
                backedges.add((tgt, ins.address))
    seq = ' '.join(f'{t}@{a - fn:#x}' for a, t in items)
    loops = ' '.join(f'{t:#x}->{a:#x}' for t, a in sorted(backedges))
    size = end - fn
    print(f'{nk} {r} ({size}B)\n  reads: {seq}\n  loops: {loops}')
