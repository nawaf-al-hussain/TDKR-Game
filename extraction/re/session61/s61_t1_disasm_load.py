#!/usr/bin/env python3
"""S61 T1 step 1: disassemble CGameObjectManager::Load (0x365780) and Reload (0x366104).
Focus: the tree/set search near 0x365a50..0x365a90 and the offset-table walk.
Outputs: s61_t1_gom_load.txt (full annotated disasm of Load) + console summary.
"""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

def rd32(v):
    o = v2o(v)
    return struct.unpack_from('<I', data, o)[0] if o is not None else None

nmout = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for line in nmout.splitlines():
    p = line.split()
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
md.detail = False

LOAD = 0x365780
# function bound: next symbol after LOAD
i = bisect.bisect_right(addrs, LOAD)
end = addrs[i] if i < len(addrs) else LOAD + 0x1000
print(f"CGameObjectManager::Load @ {LOAD:#x} .. {end:#x} ({end-LOAD} B) = {dem(sym_of(LOAD)[0])}")

out = []
o = v2o(LOAD)
insns = list(md.disasm(data[o:o + (end - LOAD)], LOAD))
# literal-pool annotation: collect pc-relative loads and resolve
lit = {}
for ins in insns:
    if ins.mnemonic in ('ldr',) and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        pc = ins.address + 8
        lit[ins.address] = (pc + imm, rd32(pc + imm))

for ins in insns:
    line = f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}"
    ann = ''
    if 'bl' in ins.mnemonic and ins.op_str.startswith('#'):
        try:
            t = int(ins.op_str[1:], 0)
            s = sym_of(t)
            ann = f"  ; -> {dem(s[0])}"
        except Exception:
            pass
    elif ins.address in lit:
        va, val = lit[ins.address]
        if val is not None:
            s = sym_of(val)
            ann = f"  ; [{va:#x}] = {val:#x} {dem(s[0])}" if s[0] != '<none>' else f"  ; [{va:#x}] = {val:#x}"
            if val < 0x100000 and val > 0:
                ann += f" ({val})"
    out.append(line + ann)

with open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_gom_load.txt', 'w') as f:
    f.write('\n'.join(out))
print(f"wrote {len(out)} insns")

# print the region of interest verbatim
print("\n=== 0x365a00..0x365b40 (tree/set search region) ===")
for line in out:
    a = int(line[:8], 16)
    if 0x365a00 <= a < 0x365b40:
        print(line)
