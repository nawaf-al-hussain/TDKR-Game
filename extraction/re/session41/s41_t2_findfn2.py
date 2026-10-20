#!/usr/bin/env python3
"""S41 T2: find code xrefs to the modifier-table pool word (0xb88710) and
disassemble the referencing function to derive decompressETC1's signature."""
import struct, sys
import capstone
from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    t, off, va, _, fs, _ = struct.unpack_from('<6I', d, o)
    if t == 1: segs.append((va, off, fs))

def v2o(va):
    for v, o, s in segs:
        if v <= va < v + s: return o + (va - v)
    return None

def o2v(o):
    for v, oo, s in segs:
        if oo <= o < oo + s: return v + (o - oo)
    return None

# table content via proper mapping
to = v2o(0xb88710)
tab = struct.unpack_from('<32i', d, to)
STD = [2,8,-2,-8,5,17,-5,-17,9,29,-9,-29,13,42,-13,-42,
       18,60,-18,-60,24,80,-24,-80,33,106,-33,-106,47,183,-47,-183]
print('table @vaddr 0xb88710 (file 0x%x):' % to, '== standard ETC1:', list(tab) == STD)
for i in range(8): print(f'  row {i}:', tab[i*4:i*4+4])

# pool words containing the table vaddr
needle = struct.pack('<I', 0xb88710)
pool_hits = []
p = 0
while True:
    p = d.find(needle, p)
    if p < 0: break
    v = o2v(p)
    if v is not None: pool_hits.append(v)
    p += 4
print('pool words (vaddr):', [hex(v) for v in pool_hits])

# scan all executable Thumb code for LDR-literal targeting those pools
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = True
ex = [(v, o, s) for (v, o, s) in segs if s > 0x100000]  # big exec segs
targets = set(pool_hits)
sites = []
for (v, o, s) in ex:
    code = d[o:o+s]
    i = 0
    # walk halfwords; detect LDR-literal T1: 01001 Rn(3) Rt(3) imm8 -> 0x48xx..0x4Fxx
    hw = struct.unpack_from('<%dH' % (s//2), code)
    n = len(hw)
    for k in range(n):
        h = hw[k]
        if 0x4800 <= h <= 0x4F7F:  # T1 LDR literal
            imm = (h & 0xff) * 4
            va = v + k*2
            tgt = ((va + 4) & ~3) + imm
            if tgt in targets:
                sites.append((va, h >> 8 & 7, tgt))
print('LDR-literal sites:', [(hex(a), f'r{r}', hex(t)) for a, r, t in sites])

# disassemble around each site (function context: 0x80 back)
for (va, r, tgt) in sites:
    lo = max(0, va - 0x60)
    print(f'\n--- context around {va:08x} ---')
    o2 = v2o(lo)
    code = d[o2:o2 + 0xC0]
    for ins in md.disasm(code, lo):
        mark = ' <== LDR table' if ins.address == va else ''
        print(f'{ins.address:08x}  {ins.mnemonic:8s} {ins.op_str}{mark}')
