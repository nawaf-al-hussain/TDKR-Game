#!/usr/bin/env python3
"""S62 T1 tool: symbol-bounded ARM disassembler with literal-pool annotation.
Usage: s62_disasm.py <start_hex> <end_hex> [--marks a,b,c]
- ARM mode only (libKRHP text is ARM; Thumb junk)
- ldr rX,[pc,#imm] resolved to the literal value + demangled symbol if pointer
- bl/b targets demangled
- marks: print '=== MARK ===' at the given addresses"""
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
    p = l.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
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

def dump(start, end):
    o = v2o(start)
    if o is None:
        print('vaddr not mapped'); return
    insns = list(md.disasm(data[o:o + (end - start)], start))
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
            lits[ins.address] = (va, vv)
    for ins in insns:
        line = f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}"
        ann = []
        if ins.address in lits:
            va, vv = lits[ins.address]
            s, off = sym_of(vv) if vv else ('?', 0)
            ann.append(f"; [{va:08x}]={vv:08x} {dem(s)}{'+%d' % off if off and s != '<none>' else ''}")
        if ins.mnemonic in ('bl', 'b', 'blx') and ins.op_str.startswith('#'):
            try:
                tgt = int(ins.op_str[1:].split(',')[0], 16) if not ins.op_str.startswith('#0x') else int(ins.op_str[1:], 16)
            except Exception:
                tgt = None
            if tgt is None:
                try:
                    tgt = int(ins.op_str.strip('#'), 0)
                except Exception:
                    tgt = None
            if tgt:
                s, off = sym_of(tgt)
                ann.append(f"; -> {tgt:08x} {dem(s)}")
        print(line + (' ' + ' '.join(ann) if ann else ''))

if __name__ == '__main__':
    a = int(sys.argv[1], 16)
    b = int(sys.argv[2], 16)
    dump(a, b)
