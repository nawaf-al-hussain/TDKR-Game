#!/usr/bin/env python3
"""S61 T1 step 15: emulate GCT's compare tree for arbitrary ids.
Walk: at each site decode beq/ble/bgt/bne targets, follow per comparison,
record the path. Test: 0x5441a117 (StateSet), 0x6754056b (Awareness),
0x3ef5108d (DropCollectible), 0x67c82e62 (CVehicleCollision), 0x222567e3, 0x14ca79 (Base)."""
import struct, json
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
byaddr = {ins.address: ins for ins in insns}
addrlist = sorted(byaddr)

# build compare-site table: site -> (value, beq_t, ble_t, bgt_t, bne_t)
sites = {}
cur = {}  # reg -> (lo, hi, movw_addr)
for idx, ins in enumerate(insns):
    m, ops = ins.mnemonic, ins.op_str
    if m == 'movw' and ', #' in ops:
        r, v = ops.split(', #')
        cur[r] = [int(v, 0), None]
    elif m == 'movt' and ', #' in ops:
        r, v = ops.split(', #')
        if r in cur:
            cur[r][1] = int(v, 0)
    elif m == 'ldr' and '[pc' in ops:
        r = ops.split(',')[0]
        try:
            imm = int(ops.split('#')[1].split(']')[0], 0)
        except Exception:
            continue
        pc = ins.address + 8
        oo = v2o(pc + imm)
        if oo is not None:
            val = struct.unpack_from('<I', data, oo)[0]
            cur[r] = ['L', val]  # literal
    elif m in ('cmp',) :
        parts = [p.strip() for p in ops.split(',')]
        if len(parts) == 2 and parts[1] in cur and cur[parts[1]][1] is not None:
            e = cur[parts[1]]
            val = e[1] if e[0] == 'L' else ((e[1] << 16) | (e[0] & 0xffff))
            # gather branch targets in the next few instructions
            t = {'beq': None, 'ble': None, 'bgt': None, 'bne': None, 'blt': None, 'bge': None}
            j = idx + 1
            while j < len(insns) and insns[j].address < ins.address + 0x20:
                mj, oj = insns[j].mnemonic, insns[j].op_str
                if mj in t and oj.startswith('#'):
                    try:
                        t[mj] = int(oj[1:], 0)
                    except ValueError:
                        pass
                if mj == 'b' and oj.startswith('#'):
                    t['b'] = int(oj[1:], 0)
                j += 1
            sites[ins.address] = (val, t)

def walk(x, label):
    a = GCT
    path = []
    sitelist = sorted(sites)
    for _ in range(300):
        # next compare site at or after address a
        site = None
        for sa in sitelist:
            if sa >= a:
                site = sa
                break
        if site is None:
            return ('NO-SITE', a, path)
        val, t = sites[site]
        if x == val:
            path.append((site, f"== {val:#x} -> beq {t['beq']:#x}" if t['beq'] else 'no-beq'))
            return ('CASE', t['beq'], path)
        elif x < val:
            nt = t['ble'] if t['ble'] is not None else t['blt'] if t['blt'] is not None else t['bge']
            which = 'ble/blt'
        else:
            nt = t['bgt'] if t['bgt'] is not None else t['bge'] if t['bge'] is not None else t['blt']
            which = 'bgt/bge'
        path.append((site, f"{x:#x} {('<' if x < val else '>')} {val:#x} -> {which} {hex(nt) if nt else None}"))
        if nt is None:
            # fallthrough to the NEXT compare site (right subtree) or default via bne
            if t.get('bne') is not None:
                path.append((site, f"bne -> {t['bne']:#x}"))
                a = t['bne']
                if a == 0x368bf4:
                    return ('DEFAULT-CRASH', a, path)
                continue
            nxt = [s2 for s2 in sitelist if s2 > site]
            if not nxt:
                return ('END-NO-MATCH', site, path)
            a = nxt[0]
            continue
        a = nt
        if a == 0x368bf4:
            return ('DEFAULT-CRASH', a, path)
        if a is None:
            return ('STUCK', a, path)
    return ('LIMIT', None, path)

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
tests = {
    'Base(cased)': 0x14ca79,
    'new-case': 0x222567e3,
    'StateSet(unk)': 0x5441a117,
    'Awareness(unk)': 0x6754056b,
    'DropCollectible(unk)': 0x3ef5108d,
    'CVehicleCollision(unk)': 0x67c82e62,
    '0x378ded9b(unk)': 0x378ded9b,
    'Motion(unk)': 0x592ce07c,
    'CustomizeActor(unk)': 0x40c6b80a,
}
for label, x in tests.items():
    r = walk(x, label)
    print(f"\n== {label} {x:#x}: {r[0]} -> {hex(r[1]) if r[1] else None}")
    for site, note in r[2][:14]:
        print(f"   {site:#x} {note}")
