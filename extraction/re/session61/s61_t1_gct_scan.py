#!/usr/bin/env python3
"""S61 T1 step 2: (1) exhaustive literal-compare census in GCT 0x368ac0..0x36b6e0
to find case ids the s60 extractor may have missed.
(2) CMemoryStream::ReadString 0x33a0d4 disasm for the gol name format.
Outputs console report.
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
    pt, po, pv, _, ps = struct.unpack_from('<5I', data, p)
    if pt == 1:
        segs.append((pv, po, ps))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

def rd32(v):
    o = v2o(v)
    return struct.unpack_from('<I', data, o)[0] if o is not None else None

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

# ---------- 1) exhaustive GCT literal census ----------
GCT, GCT_END = 0x368ac0, 0x36b6e0
o = v2o(GCT)
insns = list(md.disasm(data[o:o + (GCT_END - GCT)], GCT))
movw = {}   # reg -> (addr, imm16)
lits = {}   # literal -> list of cmp sites
for ins in insns:
    m = ins.mnemonic
    if m == 'movw' and ',' in ins.op_str:
        parts = ins.op_str.split(', ')
        if len(parts) == 2 and parts[1].startswith('#'):
            try:
                movw[parts[0]] = (ins.address, int(parts[1][1:], 0))
            except ValueError:
                pass
    elif m == 'movt' and ',' in ins.op_str:
        parts = ins.op_str.split(', ')
        if len(parts) == 2 and parts[1].startswith('#'):
            reg = parts[0]
            if reg in movw and movw[reg][0] == ins.address - 2:
                val = (int(parts[1][1:], 0) << 16) | movw[reg][1]
                movw[reg] = (ins.address, val)  # completed 32-bit
    elif m in ('cmp', 'cmn'):
        ops = ins.op_str.split(', ')
        for p_ in ops[1:]:
            p_ = p_.strip()
            if p_.startswith('#'):
                try:
                    v = int(p_[1:], 0)
                    lits.setdefault(v & 0xffffffff, []).append(ins.address)
                except ValueError:
                    pass
            elif p_ in movw and movw[p_][0] >= ins.address - 0x40:
                lits.setdefault(movw[p_][1], []).append(ins.address)
# also cmp using regs holding completed movw/movt pairs anywhere earlier
for ins in insns:
    if ins.mnemonic in ('cmp', 'cmn'):
        ops = ins.op_str.split(', ')
        if len(ops) >= 2:
            reg = ops[1].strip()
            for (waddr, wreg), in []:
                pass
# scan all movw/movt completed values in window regardless of distance
vals32 = {}
cur = {}
for ins in insns:
    if ins.mnemonic == 'movw' and ',' in ins.op_str:
        parts = ins.op_str.split(', ')
        if len(parts) == 2 and parts[1].startswith('#'):
            try:
                cur[parts[0]] = [ins.address, int(parts[1][1:], 0), None]
            except ValueError:
                pass
    elif ins.mnemonic == 'movt' and ',' in ins.op_str:
        parts = ins.op_str.split(', ')
        if len(parts) == 2 and parts[1].startswith('#') and parts[0] in cur:
            cur[parts[0]][2] = int(parts[1][1:], 0)
            vals32[(cur[parts[0]][2] << 16) | cur[parts[0]][1]] = cur[parts[0]][0]
    elif ins.mnemonic in ('cmp', 'cmn'):
        ops = ins.op_str.split(', ')
        if len(ops) >= 2 and ops[1].strip() in cur:
            c = cur[ops[1].strip()]
            if c[2] is not None and ins.address - c[0] < 0x100:
                lits.setdefault(((c[2] << 16) | c[1]), []).append(ins.address)

s60 = set(json_keys) if (json_keys := []) else None
import json
s60cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
s60ids = set(int(k, 0) for k in s60cases)

print("=== literal compares in GCT window (movw/movt-fed or imm8) ===")
big = sorted(v for v in lits if v > 0xffff)
for v in big:
    tag = 'IN-s60-64' if v in s60ids else '*** NEW ***'
    print(f"  {v:#010x}  cmp@{[hex(a) for a in lits[v]][:3]}  {tag}")
small = sorted(v for v in lits if v <= 0xffff and v > 0x1000)
print("small-ish literals:", [hex(v) for v in small])

# ---------- 2) ReadString ----------
RS = 0x33a0d4
i = bisect.bisect_right(addrs, RS)
end = addrs[i]
print(f"\n=== CMemoryStream::ReadString {RS:#x}..{end:#x} = {dem(sym_of(RS)[0])}")
o = v2o(RS)
insns = list(md.disasm(data[o:o + (end - RS)], RS))
lit = {}
for ins in insns:
    if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
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
            ann = f"  ; -> {dem(sym_of(t)[0])}"
        except Exception:
            pass
    elif ins.address in lit:
        va, val = lit[ins.address]
        if val is not None:
            ann = f"  ; [{va:#x}] = {val:#x}"
    print(line + ann)
