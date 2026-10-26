#!/usr/bin/env python3
"""S61 T1 step 16: DEFINITIVE GCT case census with restart-on-invalid disasm
across the full 0x368ac0..0x36b6ec window (code islands separated by literal pools).
Extract every (cmp-value, beq-target) case; resolve each case's reader vtable.
Outputs s61_t1_cases_full.json"""
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
GCT, GCT_END = 0x368ac0, 0x36b6ec
buf = data[v2o(GCT):v2o(GCT_END)]

# restart-on-invalid full disasm
insns = []
pos = 0
base = GCT
while pos < len(buf):
    got = False
    for ins in md.disasm(buf[pos:pos + 0x8000], base + pos):
        insns.append(ins)
        pos = ins.address - base + ins.size
        got = True
    if not got:
        pos += 2
print(f"instructions decoded: {len(insns)} (window {GCT_END-GCT} B)")

# track regs across islands; collect cmp sites
cur = {}
sites = {}  # val -> {beq, site}
for idx, ins in enumerate(insns):
    m, ops = ins.mnemonic, ins.op_str
    if m == 'movw' and ', #' in ops:
        r, v = ops.split(', #')
        try:
            cur[r] = ['w', int(v, 0)]
        except ValueError:
            pass
    elif m == 'movt' and ', #' in ops:
        r, v = ops.split(', #')
        try:
            iv = int(v, 0)
        except ValueError:
            continue
        if r in cur and cur[r][0] == 'w':
            cur[r] = ['wt', (iv << 16) | cur[r][1]]
    elif m == 'ldr' and '[pc' in ops:
        r = ops.split(',')[0]
        try:
            imm = int(ops.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        pc = ins.address + 8
        oo = v2o(pc + imm)
        if oo is not None:
            cur[r] = ['L', struct.unpack_from('<I', data, oo)[0]]
    elif m == 'cmp':
        parts = [p.strip() for p in ops.split(',')]
        if len(parts) == 2 and parts[1] in cur:
            e = cur[parts[1]]
            val = e[1] if e[0] in ('L', 'wt') else None
            if val is None:
                continue
            # next branches
            t = {}
            j = idx + 1
            while j < len(insns) and insns[j].address < ins.address + 0x1c:
                mj, oj = insns[j].mnemonic, insns[j].op_str
                if mj in ('beq', 'bne', 'ble', 'bgt', 'blt', 'bge') and oj.startswith('#'):
                    t.setdefault(mj, int(oj[1:], 0))
                j += 1
            if 'beq' in t:
                sites.setdefault(val, {'beq': t['beq'], 'site': ins.address})

print(f"distinct compared values with beq: {len(sites)}")

s60 = set(int(k, 0) for k in json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json')))
new = {v: s for v, s in sites.items() if v not in s60}
print(f"known-from-s60: {len(sites) - len(new)}; NEW: {len(new)}")

# resolve each case's reader: follow beq target; expect mov rX,#alloc; bl operator new;
# ldr r3,[pc..]; add r3,pc,r3; add r3,r3,#8; str r3,[r0] (vtable) — OR direct vtable store
def resolve_case(beq):
    o = v2o(beq)
    if o is None:
        return None
    ins = list(md.disasm(data[o:o + 0x40], beq))
    vtbl = None
    for k, i2 in enumerate(ins):
        if i2.mnemonic == 'ldr' and '[pc' in i2.op_str and k + 2 < len(ins):
            try:
                imm = int(i2.op_str.split('#')[1].split(']')[0], 0)
            except Exception:
                continue
            pc = i2.address + 8
            oo = v2o(pc + imm)
            if oo is None:
                continue
            val = struct.unpack_from('<I', data, oo)[0]
            # check the add r3,pc / add r3,#8 vtable pattern
            nxt = [x.op_str for x in ins[k+1:k+3]]
            if any('pc' in s for s in nxt):
                vtbl = val  # pc-relative base; resolved below
        if i2.mnemonic == 'str' and i2.op_str.startswith('r3, [r0]') and vtbl is not None:
            # r3 = pc + val + 8 computed: need the add chain — approximate: find add r3,pc,r3 then add r3,r3,#8
            for k2, i3 in enumerate(ins):
                if i3.mnemonic == 'add' and i3.op_str.startswith('r3, pc, r3'):
                    base_pc = i3.address + 8
                    for i4 in ins[k2+1:k2+3]:
                        if i4.mnemonic == 'add' and i4.op_str == 'r3, r3, #8':
                            return base_pc + val + 8
                    return base_pc + val
            return None
    return None

out = {}
for val, s in sorted(sites.items()):
    vtbl = resolve_case(s['beq'])
    sym = dem(sym_of(vtbl)[0]) if vtbl else None
    reader = None
    if vtbl:
        oo = v2o(vtbl)
        if oo:
            reader = struct.unpack_from('<I', data, oo)[0]  # vtable[0]; template reader = [vptr+0x10] → vtable+8?? per s60: reader = [vptr+0x10] where vptr = vtable+8
    out[hex(val)] = {'beq': hex(s['beq']), 'site': hex(s['site']), 'vtable': hex(vtbl) if vtbl else None,
                     'vtable_sym': sym, 'status': 's60' if val in s60 else 'NEW'}

n_new = sum(1 for v in out.values() if v['status'] == 'NEW')
n_novt = sum(1 for v in out.values() if not v['vtable'])
print(f"\ntotal cases: {len(out)} (NEW {n_new}, no-vtable-resolved {n_novt})")
for v, s in sorted(out.items()):
    if s['status'] == 'NEW':
        print(f"  {v} beq {s['beq']} vtable {s['vtable']} {s['vtable_sym'][:60] if s['vtable_sym'] else ''}")
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_cases_full.json', 'w'), indent=1)
