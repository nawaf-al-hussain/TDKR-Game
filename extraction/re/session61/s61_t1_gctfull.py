#!/usr/bin/env python3
"""S61 T1 step 10: FULL compare-census in GCT 0x368ac0..0x36b6ec including
literal-pool-fed compares (ldr rX,[pc,#imm] ... cmp r0,rX)."""
import struct, subprocess, bisect, json
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

GCT, GCT_END = 0x368ac0, 0x36b6ec
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
o = v2o(GCT)
insns = list(md.disasm(data[o:o + (GCT_END - GCT)], GCT))

# track register values: movw/movt pairs AND pc-relative literal loads
regval = {}
found = {}  # value -> first site
for idx, ins in enumerate(insns):
    m = ins.mnemonic
    ops = ins.op_str
    if m == 'movw' and ', #' in ops:
        r, v = ops.split(', #')
        regval[r] = ('w', int(v, 0), ins.address)
    elif m == 'movt' and ', #' in ops:
        r, v = ops.split(', #')
        if r in regval and regval[r][0] == 'w' and ins.address - regval[r][2] <= 4:
            regval[r] = ('wt', (int(v, 0) << 16) | regval[r][1], ins.address)
    elif m == 'ldr' and '[pc' in ops:
        r = ops.split(',')[0]
        try:
            imm = int(ops.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        pc = ins.address + 8
        va = pc + imm
        oo = v2o(va)
        if oo is not None:
            val = struct.unpack_from('<I', data, oo)[0]
            regval[r] = ('lit', val, ins.address, va)
    elif m in ('cmp', 'cmn'):
        parts = [p.strip() for p in ops.split(',')]
        if len(parts) >= 2:
            r2 = parts[1]
            if r2 in regval:
                e = regval[r2]
                if e[0] in ('wt', 'lit'):
                    found.setdefault(e[1], []).append(ins.address)

s60ids = set(int(k, 0) for k in json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json')))
print(f"compare values found: {len(found)}")
new = {}
for v in sorted(found):
    tag = 's60' if v in s60ids else 'NEW'
    if v not in s60ids:
        new[v] = found[v]
    if v > 0xffff:
        print(f"  {v:#010x} @{[hex(a) for a in found[v]][:2]}  {tag}")
print(f"\nNEW (not in s60 64): {len(new)}")
for v, sites in sorted(new.items()):
    print(f"  {v:#010x} @{[hex(a) for a in sites][:3]}")
json.dump({hex(k): [hex(a) for a in v] for k, v in found.items()},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_gct_allcmp.json', 'w'), indent=1)
