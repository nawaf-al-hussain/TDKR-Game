#!/usr/bin/env python3
"""S61 T1 step 14: (1) disasm BeginRead fully (DICT parse; where does it leave pos?).
(2) locate the raw pointer-word hits for Reload/CreateObject/GCT/ctor/Load with
file-offset + section mapping + relocation info."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

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
        print(f"PT_LOAD va {pv:#x} off {po:#x} filesz {ps:#x}")

# sections
import subprocess as sp
secout = sp.run(['readelf', '-S', '--wide', SO], capture_output=True, text=True).stdout
for line in secout.splitlines():
    if any(k in line for k in ('.got', '.data', '.bss', '.rel.dyn', '.text', '.rodata', '.data.rel.ro')):
        parts = line.split()
        print('SEC:', ' '.join(parts[:7]))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

nm = sp.run(['nm', SO], capture_output=True, text=True).stdout
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
    return sp.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

print("\n=== BeginRead (0x33c8b8..0x33c8f8) ===")
B0 = 0x33c8b8
i = bisect.bisect_right(addrs, 0x33c8d4) - 1
print("BeginRead sym:", dem(sym_of(0x33c8d4 - 0x1c)[0]) if sym_of(0x33c8b8)[0] == '<none>' else dem(sym_of(0x33c8b8)[0]))
o = v2o(B0)
for ins in md.disasm(data[o:o + (0x33c8f8 - B0)], B0):
    print(f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}")

print("\n=== pointer-word hits with mapping ===")
for name, tgt in (('Reload', 0x366104), ('CreateObject', 0x36774c), ('GCT', 0x368ac0),
                  ('ctor', 0x365598), ('Load', 0x365780)):
    needle = struct.pack('<I', tgt)
    start = 0
    print(f"-- {name} {tgt:#x}")
    while True:
        j = data.find(needle, start)
        if j < 0:
            break
        va = None
        for va_, off_, sz_ in segs:
            if off_ <= j < off_ + sz_:
                va = va_ + (j - off_)
                break
        print(f"   file {j:#x} -> va {hex(va) if va is not None else 'UNMAPPED'}")
        start = j + 1
