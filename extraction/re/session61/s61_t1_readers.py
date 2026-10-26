#!/usr/bin/env python3
"""S61 T1 step 18: extract EVERY GCT case body (both islands, restart-on-invalid):
case body = alloc (mov rX,#n; bl operator new) [+ optional ctor bl] + vtable store
(str r3,[r0] after add r3,pc,r3/add r3,#8) OR vtable-direct; reader = [vtable+0x18].
Output: s61_t1_case_readers.json (id -> reader addr, reader symbol)."""
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
W_LO, W_HI = 0x368ac0, 0x36b6ec
buf = data[v2o(W_LO):v2o(W_HI)]
insns = []
pos = 0
while pos < len(buf):
    got = False
    for ins in md.disasm(buf[pos:pos + 0x8000], W_LO + pos):
        insns.append(ins)
        pos = ins.address - W_LO + ins.size
        got = True
    if not got:
        pos += 2

# register state machine across the whole window (junk-tolerant: pattern-anchored)
# case body pattern A: mov r0,#alloc ; bl new ; [bl ctor] ; ldr r3,[pc] ; add r3,pc,r3 ;
#                      [add r3,#8] ; [strs] ; str r3,[r0] ; (r4=r0) ; b tail
# pattern B (vtable-direct): ldr r5,[pc] ; ... r5 used as vtable base (prologue-loaded)
out = {}
i = 0
n = len(insns)
while i < n:
    ins = insns[i]
    if ins.mnemonic == 'bl' and 'operator new' in dem(sym_of(int(ins.op_str[1:], 0))[0] if ins.op_str.startswith('#') else ''):
        pass
    i += 1

# simpler: scan for 'str r3, [r0]' preceded (within 10) by 'add r3, pc, r3' preceded (within 6) by 'ldr r3, [pc'
# then back-scan for the movw/movt or mov/movt id feeding the cmp whose beq targets this block
vtable_stores = []
for idx, ins in enumerate(insns):
    if ins.mnemonic == 'str' and ins.op_str.split(',')[0].strip() in ('r3', 'r2') and '[r0]' in ins.op_str.replace(' ', ''):
        # look back for add rX, pc, rX
        for back in range(idx - 1, max(idx - 8, -1), -1):
            b = insns[back]
            if b.mnemonic == 'add' and ', pc, ' in b.op_str:
                reg = b.op_str.split(',')[0].strip()
                base_pc = b.address + 8
                # ldr reg,[pc] before that
                for back2 in range(back - 1, max(back - 5, -1), -1):
                    b2 = insns[back2]
                    if b2.mnemonic == 'ldr' and b2.op_str.startswith(reg + ', [pc'):
                        try:
                            imm = int(b2.op_str.split('#')[1].split(']')[0], 0)
                        except Exception:
                            break
                        oo = v2o(b2.address + 8 + imm)
                        if oo is None:
                            break
                        val = struct.unpack_from('<I', data, oo)[0]
                        # optional add reg, reg, #8 after the add pc
                        extra = 0
                        for fwd in range(back + 1, idx):
                            f = insns[fwd]
                            if f.mnemonic == 'add' and f.op_str.startswith(reg + ', ' + reg + ', #'):
                                try:
                                    extra = int(f.op_str.split('#')[1], 0)
                                except ValueError:
                                    pass
                        vtable_stores.append((ins.address, base_pc + val + extra))
                        break
                break

print(f"vtable stores found: {len(vtable_stores)}")
# map each store to the case id: the cmp whose beq jumps to the block start containing it
# build beq-target -> cmp-value map from the full scan (mov/movt AND movw/movt)
cur = {}
id_at = {}
for idx, ins in enumerate(insns):
    m, ops = ins.mnemonic, ins.op_str
    if m in ('movw', 'mov') and ', #' in ops:
        r, v = ops.split(', #')
        try:
            cur[r] = ['lo', int(v, 0)]
        except ValueError:
            pass
    elif m in ('movt',) and ', #' in ops:
        r, v = ops.split(', #')
        try:
            iv = int(v, 0)
        except ValueError:
            continue
        if r in cur and cur[r][0] == 'lo':
            cur[r] = ['hi', (iv << 16) | cur[r][1]]
    elif m == 'ldr' and '[pc' in ops:
        r = ops.split(',')[0]
        try:
            imm = int(ops.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        oo = v2o(ins.address + 8 + imm)
        if oo is not None:
            cur[r] = ['L', struct.unpack_from('<I', data, oo)[0]]
    elif m == 'cmp':
        parts = [p.strip() for p in ops.split(',')]
        if len(parts) == 2 and parts[1] in cur and cur[parts[1]][0] in ('hi', 'L'):
            id_at[ins.address] = cur[parts[1]][1]

# beq -> cmp mapping
beq_map = {}
for idx, ins in enumerate(insns):
    if ins.mnemonic == 'beq' and ins.op_str.startswith('#'):
        t = int(ins.op_str[1:], 0)
        # find the cmp within 6 before
        for back in range(idx - 1, max(idx - 7, -1), -1):
            if insns[back].address in id_at:
                beq_map[t] = id_at[insns[back].address]
                break

# block start for each store = the beq target whose block contains the store
blocks = sorted(beq_map)
result = {}
for store_addr, vt in vtable_stores:
    # candidate beq targets <= store_addr, nearest
    cand = [b for b in blocks if b <= store_addr]
    if not cand:
        continue
    b = cand[-1]
    cid = beq_map[b]
    reader = None
    oo = v2o(vt)
    if oo:
        reader = struct.unpack_from('<I', data, oo + 0x10)[0]
    result[hex(cid)] = {'beq': hex(b), 'vtable': hex(vt),
                        'reader': hex(reader) if reader else None,
                        'reader_sym': dem(sym_of(reader)[0]) if reader else None,
                        'vtable_sym': dem(sym_of(vt)[0]) if vt else None}
print(f"cases with id+vtable+reader: {len(result)}")
named = sum(1 for v in result.values() if v['reader_sym'] and v['reader_sym'] != '<none>')
print(f"reader symbol resolved: {named}")
json.dump(result, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_case_readers.json', 'w'), indent=1)
for k, v in sorted(result.items(), key=lambda kv: int(kv[0], 0))[:200]:
    rs = v['reader_sym'] or '?'
    print(f"  {k} -> {v['reader']} {rs[:70]}")
