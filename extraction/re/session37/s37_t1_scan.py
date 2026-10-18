#!/usr/bin/env python3
"""S37 T1a: corrected whole-binary scans for the region-pair table writers.

Targets:
  - globals 0xc16e48 / 0xc16e4c / 0xc16e54 (unnamed statics near
    CNavMeshNova::m_cellsIdsBuff @0xc16e60)
  - stores to nova+0x5c / nova+0x60 (CanReachCellFrom pair table)
Scans (corrected encodings, whole .text):
  1. MOVW/MOVT pairs materialising the global addresses
  2. literal-pool words equal to the global addresses
  3. str imm 0x5c/0x60 (word) whole text, grouped by function
  4. strd imm spanning 0x5c
Disassembles: CanReachCellFrom, CNavMeshNova::Init, FindClosestCellInRegion
(head), SearchPortalPath (head).
"""
import struct, json, sys, bisect
import capstone
from collections import defaultdict

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _pa, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1 and p_filesz:
        segs.append((p_vaddr, p_offset, p_filesz, p_memsz))

def v2f(v):
    for vaddr, off, filesz, memsz in segs:
        if vaddr <= v < vaddr + max(filesz, memsz):
            return off + (v - vaddr)
    return None

text_lo, text_hi = 0x8000, 0x400000
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
symaddrs = sorted((int(k, 16), str(v[0])) for k, v in syms.items())
_symkeys = [x[0] for x in symaddrs]

def who(a):
    i = bisect.bisect_right(_symkeys, a) - 1
    return symaddrs[i] if i >= 0 else (0, '?')

GLOBALS = [0xc16e48, 0xc16e4c, 0xc16e54, 0xc16e60]

print('=== 1. MOVW/MOVT materialising globals (corrected opcode mask) ===')
movw = {}
for vaddr, off, filesz, memsz in segs:
    if vaddr >= text_hi or vaddr + filesz <= text_lo:
        continue
    blob = d[off:off + filesz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        op = (w >> 20) & 0xFF
        if op in (0x30, 0x34) and ((w >> 28) != 0xF):
            imm16 = (((w >> 16) & 0xF) << 12) | (w & 0xFFF)
            if op == 0x30:
                movw[vaddr + i] = (((w >> 12) & 0xF), imm16)

targets = set()
for a, (rd, imm) in movw.items():
    if imm in (0x6e48, 0x6e4c, 0x6e54, 0x6e60):
        for da in range(a + 4, a + 40, 4):
            f = v2f(da)
            if f is None:
                break
            w = struct.unpack_from('<I', d, f)[0]
            if ((w >> 20) & 0xFF) == 0x34:
                full = ((((((w >> 16) & 0xF) << 12) | (w & 0xFFF)) << 16) | imm)
                if full in GLOBALS:
                    targets.add((a, full, rd))
for a, full, rd in sorted(targets):
    print(f'  MOVW 0x{a:08x} r{rd} = 0x{full:08x}  in {who(a)[1][:60]}')
print(f'  total: {len(targets)} sites')

print('=== 2. literal-pool words == globals ===')
pool = 0
for vaddr, off, filesz, memsz in segs:
    blob = d[off:off + filesz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        if w in GLOBALS and text_lo <= vaddr + i < text_hi:
            print(f'  pool@0x{vaddr + i:08x} = 0x{w:08x}')
            pool += 1
print(f'  total: {pool} pool entries')

print('=== 3. str imm 0x5c/0x60 whole text ===')
hits = defaultdict(list)
for vaddr, off, filesz, memsz in segs:
    blob = d[off:off + filesz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        a = vaddr + i
        if not (text_lo <= a < text_hi):
            continue
        imm = w & 0xFFF
        if (w & 0x0FF00000) == 0x05800000 and imm in (0x5C, 0x60):
            hits[imm].append((a, (w >> 16) & 0xF, (w >> 12) & 0xF))
        if (w & 0x0FE00F10) == 0x01400000 and ((w >> 20) & 1) == 0 and ((w >> 7) & 0xF) == 0xC:
            imm2 = ((w >> 4) & 0xF0) | (w & 0xF)
            if imm2 in (0x58, 0x5C, 0x60):
                hits[('strd', imm2)].append((a, (w >> 16) & 0xF, (w >> 12) & 0xF))
for k, lst in hits.items():
    print(f'  key={k}: {len(lst)} sites')
funcs = defaultdict(list)
for k, lst in hits.items():
    for a, rn, rt in lst:
        fn, nm_ = who(a)
        funcs[(fn, nm_)].append((a, k))
print('  containing functions (navmesh range or >=4 sites):')
for (fn, nm_), lst in sorted(funcs.items()):
    if 0x1c0000 <= fn <= 0x210000 or len(lst) >= 4:
        print(f'    fn 0x{fn:08x} {nm_[:70]}: {len(lst)} sites; first=0x{lst[0][0]:08x} key={lst[0][1]}')

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

def disasm(lo, hi, title):
    print(f'=== {title} 0x{lo:08x}-0x{hi:08x} ===')
    f = v2f(lo)
    code = d[f:f + (hi - lo)]
    for ins in md.disasm(code, lo):
        print(f'  0x{ins.address:08x}  {ins.mnemonic:8s} {ins.op_str}')

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'disasm'):
        disasm(0x1d2c28, 0x1d2cd0, 'CNavMeshNova::CanReachCellFrom')
        disasm(0x1d20e4, 0x1d2170, 'CNavMeshNova::Init')
        disasm(0x1d2550, 0x1d2610, 'FindClosestCellInRegion (head)')
        disasm(0x1d44b0, 0x1d4550, 'SearchPortalPath (head)')
