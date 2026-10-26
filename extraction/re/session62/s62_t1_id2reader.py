#!/usr/bin/env python3
"""S62 T1: CORRECT id->vptr->reader extraction from the two GCT islands.
cmp sites: movw/movt pair feeding `cmp` then beq (distant body) or inline body (bne default).
Body scan: from body start, forward to the terminating `b 0x368bfc`; vptr from
`add rX, pc, rY` + preceding literal. Output: s62_t1_id2reader.json (all cases)."""
import struct, subprocess, bisect, json

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
    q = l.split()
    if len(q) == 3:
        try:
            syms.append((int(q[0], 16), q[2]))
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

ISLANDS = ((0x368ac0, 0x369ab8), (0x369ca4, 0x36b658))

def disas_island(lo, hi):
    insns = []
    pc = lo
    o = v2o(lo)
    raw = data[o:o + (hi - lo)]
    while pc < hi:
        got = False
        for ins in md.disasm(raw[pc - lo:], pc):
            insns.append(ins)
            pc = ins.address + 4
            got = True
            if pc >= hi:
                break
        if not got:
            pc += 4  # restart after literal-pool stall
    return insns

all_cases = {}
for lo, hi in ISLANDS:
    insns = disas_island(lo, hi)
    byaddr = {ins.address: ins for ins in insns}
    alist = sorted(byaddr)
    # 1) collect cmp sites: movw/movt pair -> cmp -> beq/bne
    for i, ins in enumerate(insns):
        if ins.mnemonic != 'cmp':
            continue
        cmp_reg = ins.op_str.split(',')[1].strip()
        # search back for movt within 6 instructions
        lo16 = hi16 = None
        for j in range(i - 1, max(0, i - 7), -1):
            m = insns[j]
            if m.mnemonic == 'movt' and m.op_str.split(',')[0].strip() == cmp_reg:
                hi16 = int(m.op_str.split('#')[1], 0)
                for k in range(j - 1, max(0, j - 7), -1):
                    m2 = insns[k]
                    if m2.mnemonic == 'movw' and m2.op_str.split(',')[0] == m.op_str.split(',')[0]:
                        lo16 = int(m2.op_str.split('#')[1], 0)
                        break
                break
        if hi16 is None or lo16 is None:
            continue
        cid = (hi16 << 16) | lo16
        # case target: beq target, or inline body (next insn if next is bne)
        nxt = byaddr.get(ins.address + 4)
        body = None
        if nxt and nxt.mnemonic == 'beq':
            body = int(nxt.op_str[1:], 16)
        elif nxt and nxt.mnemonic == 'bne':
            body = ins.address + 8
        if body is None:
            continue
        # 2) scan body forward to the terminating b 0x368bfc
        vptr = None
        a = body
        for _ in range(60):
            c = byaddr.get(a)
            if c is None:
                break
            if c.mnemonic == 'add' and ', pc, ' in c.op_str:
                dst = c.op_str.split(',')[0]
                for j in range(len(insns) - 1, -1, -1):
                    pass
                # find preceding ldr of dst (scan back in byaddr)
                aa = c.address
                for _ in range(6):
                    aa -= 4
                    d = byaddr.get(aa)
                    if d and d.mnemonic == 'ldr' and d.op_str.startswith(dst + ', [pc'):
                        try:
                            imm = int(d.op_str.split('#')[1].split(']')[0], 0)
                        except Exception:
                            continue
                        pool = ((d.address + 8) & ~3) + imm
                        vo = v2o(pool)
                        val = struct.unpack_from('<I', data, vo)[0]
                        vptr = c.address + 8 + val + 8
                        break
                if vptr:
                    break
            if c.mnemonic == 'b' and c.op_str == '#0x368bfc':
                break
            a += 4
        if vptr is not None:
            w = struct.unpack_from('<I', data, v2o(vptr + 0x10))[0]
            s, off = sym_of(w)
            all_cases[cid] = {'vptr': '0x%08x' % vptr, 'load': '0x%08x' % w,
                              'load_sym': dem(s), 'body': '0x%08x' % body}

print('cases extracted:', len(all_cases))
for cid in sorted(all_cases):
    c = all_cases[cid]
    print(f"{cid:08x} vptr={c['vptr']} load={c['load']} {c['load_sym'][:58]}")
json.dump(all_cases, open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_id2reader.json', 'w'), indent=1)
print('saved')
