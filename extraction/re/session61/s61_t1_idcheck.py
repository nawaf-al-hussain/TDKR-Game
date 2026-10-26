#!/usr/bin/env python3
"""S61 T1 step 17: DEFINITIVE per-id case check.
For each of the 120 gol id2 values: scan the GCT window (0x368ac0..0x36b6ec) raw bytes
for movw+movt pairs encoding the id, verify a cmp referencing that register within +/-0x18,
and identify the case body via the beq. Also scan ReloadComponentTemplate window."""
import struct, json, subprocess, bisect
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
md.detail = True

W_LO, W_HI = 0x368ac0, 0x36b6ec
buf = data[v2o(W_LO):v2o(W_HI)]

# pre-decode every aligned word as instruction (even in pools) to find movw/movt
def find_id_cases(x):
    """Return list of (cmp_site, beq_target) for id x."""
    hits = []
    lo = x & 0xffff
    hi = (x >> 16) & 0xffff
    for off in range(0, len(buf) - 8, 2):
        w0 = struct.unpack_from('<I', buf, off)[0]
        if (w0 & 0x0ff00000) != 0x03000000:  # movw
            continue
        imm0 = ((w0 & 0xf0000) >> 4) | (w0 & 0xfff)
        rd = (w0 >> 12) & 0xf
        if imm0 != lo:
            continue
        # movt within next 8 bytes (allow interleaving)
        for d in (4, 8):
            if off + d + 4 > len(buf):
                continue
            w1 = struct.unpack_from('<I', buf, off + d)[0]
            if (w1 & 0x0ff00000) != 0x03400000:
                continue
            imm1 = (((w1 >> 16) & 0xf) << 12) | (w1 & 0xfff)
            rd1 = (w1 >> 12) & 0xf
            if imm1 != hi or rd1 != rd:
                continue
            site = W_LO + off + d + 4
            # look for cmp rd,? or cmp ?,rd within +0x18
            o = v2o(site)
            ins = list(md.disasm(data[o:o + 0x20], site))
            for i2 in ins[:6]:
                if i2.mnemonic == 'cmp' and f'r{rd}' in [p.strip() for p in i2.op_str.split(',')]:
                    # beq within next 5
                    o2 = v2o(i2.address)
                    ins2 = list(md.disasm(data[o2:o2 + 0x20], i2.address))
                    beq = None
                    for i3 in ins2[:5]:
                        if i3.mnemonic == 'beq' and i3.op_str.startswith('#'):
                            beq = int(i3.op_str[1:], 0)
                            break
                    hits.append((i2.address, beq))
                    break
            break
    return hits

d = json.load(open('extraction/re/session61/s61_t1_parse.json'))
allid = sorted(int(v, 0) for v in d['all_id2'])
print(f"gol ids: {len(allid)}")
cased = {}
uncased = []
for x in allid:
    h = find_id_cases(x)
    if h:
        cased[x] = h
    else:
        uncased.append(x)
print(f"CASED (movw/movt+cmp in GCT window): {len(cased)}")
print(f"UNCASED: {len(uncased)} -> {[hex(v) for v in uncased]}")

# resolve case bodies -> vtables
def case_vtable(beq):
    if not beq:
        return None
    o = v2o(beq)
    ins = list(md.disasm(data[o:o + 0x44], beq))
    for k, i2 in enumerate(ins):
        if i2.mnemonic == 'add' and i2.op_str.startswith('r3, pc, r3'):
            base_pc = i2.address + 8
            # preceding ldr r3,[pc,#imm] within 3
            for back in range(k - 1, max(k - 4, -1), -1):
                i3 = ins[back]
                if i3.mnemonic == 'ldr' and i3.op_str.startswith('r3, [pc'):
                    try:
                        imm = int(i3.op_str.split('#')[1].split(']')[0], 0)
                    except Exception:
                        continue
                    val = struct.unpack_from('<I', data, v2o(i3.address + 8 + imm))[0]
                    for i4 in ins[k + 1:k + 3]:
                        if i4.mnemonic == 'add' and i4.op_str == 'r3, r3, #8':
                            return base_pc + val + 8
                    return base_pc + val
        if i2.mnemonic == 'ldr' and i2.op_str.startswith('r5, [pc'):
            pass
    return None

table = {}
for x, h in sorted(cased.items()):
    cmp_site, beq = h[0]
    vt = case_vtable(beq)
    sym = dem(sym_of(vt)[0])[:64] if vt else '?'
    table[hex(x)] = {'cmp': hex(cmp_site), 'beq': hex(beq) if beq else None,
                     'vtable': hex(vt) if vt else None, 'sym': sym}
for x in uncased:
    table[hex(x)] = {'status': 'UNCASED'}
json.dump(table, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_id_cases.json', 'w'), indent=1)
print(f"\nresolved vtables: {sum(1 for v in table.values() if v.get('vtable'))}/{len(cased)}")
for x, h in sorted(cased.items()):
    if len(h) > 1:
        print(f"  {x:#x}: {len(h)} compare sites")
for x in uncased:
    print(f"  uncased: {x:#x}")
