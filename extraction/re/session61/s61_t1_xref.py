#!/usr/bin/env python3
"""S61 T1 step 4: xref callers of GOM::Load 0x365780, GOM::Reload 0x366104,
GCT 0x368ac0; and re-check the GCT default path bytes at 0x368bf4."""
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

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

TEXT_LO, TEXT_HI = 0xa5d80, 0xac2190
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

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def find_bl_calls(target):
    """Scan .text for BL instructions targeting `target` (B/BL imm24 encoded)."""
    hits = []
    o = v2o(TEXT_LO)
    buf = data[o:o + (TEXT_HI - TEXT_LO)]
    for ins in md.disasm(buf, TEXT_LO):
        if ins.mnemonic in ('bl', 'b') and ins.op_str.startswith('#'):
            try:
                t = int(ins.op_str[1:], 0)
            except ValueError:
                continue
            if t == target:
                hits.append((ins.address, ins.mnemonic))
    return hits

for name, tgt in (('GOM::Load', 0x365780), ('GOM::Reload', 0x366104), ('GCT', 0x368ac0)):
    hits = find_bl_calls(tgt)
    print(f"=== callers of {name} {tgt:#x}: {len(hits)}")
    for a, m in hits:
        s = sym_of(a)
        print(f"  {a:#x} {m} in {dem(s[0])} +{s[1]:#x}")

# GCT default path check
print("\n=== GCT 0x368ac0..0x368c20 (prologue+first cases+default) ===")
o = v2o(0x368ac0)
for ins in md.disasm(data[o:o + 0x160], 0x368ac0):
    print(f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}")
