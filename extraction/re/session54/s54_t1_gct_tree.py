#!/usr/bin/env python3
"""s54 T1 step 11: full GenerateComponentTemplate case map via the linear-sweep disasm.
Walks the binary-search id compares (movw/movt + beq/bne) and pairs each case body's
pc-rel vtable with its id. Identifies class 0x5441a117 (the generic first component)
and 0x110ce1f (CComponentGlide) vtables and Load functions."""
import struct
import re

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

lines = open('/home/z/my-project/scripts/s54_gct_full_disasm.txt').read().splitlines()
insns = []
for l in lines:
    try:
        a = int(l.split()[0], 16)
    except ValueError:
        continue
    insns.append((a, l))
insns.sort()
addr2i = {a: i for i, (a, _) in enumerate(insns)}

# collect compare-compare-branch structures: movw/movt r3, #imm; cmp r0, r3; bne/beq
ids = []  # (addr_of_cmp, id_value, taken_target, fallthrough_next_case)
for i, (a, l) in enumerate(insns):
    m = re.match(r'\S+\s+movt\s+r(\d+), #(0x[0-9a-f]+)', l)
    if not m:
        continue
    rd = m.group(1)
    hi = int(m.group(2), 16)
    # previous movw same reg
    lo = None
    for j in range(i - 1, max(0, i - 6), -1):
        m2 = re.match(r'\S+\s+movw\s+%s, #(0x[0-9a-f]+)' % ('r' + rd), insns[j][1])
        if m2:
            lo = int(m2.group(1), 16)
            break
    if lo is None:
        continue
    # next: cmp r0, rX ; b(beq/bne)
    if i + 2 < len(insns):
        cmpl = insns[i + 1][1]
        brl = insns[i + 2][1]
        mc = re.match(r'\S+\s+cmp\s+r0,', cmpl)
        mb = re.match(r'\S+\s+(beq|bne)\s+#(0x[0-9a-f]+)', brl)
        if mc and mb:
            ids.append((a, (hi << 16) | lo, mb.group(1), int(mb.group(2), 16)))

print('id compares found:', len(ids))

# case bodies: each beq target = case start (or bne fallthrough)
# vtable per case: first pc-rel add after the case start
def pcrel_after(start, limit=0x80):
    i = addr2i.get(start)
    if i is None:
        return None
    for j in range(i, min(i + 40, len(insns))):
        a, l = insns[j]
        if 'PC-REL ADD' in l:
            # find preceding ldr
            rm = l.split(None, 2)[2].split(';')[0].split(',')[2].strip()
            for d in range(1, 12):
                pa = a - d * 4
                pi = addr2i.get(pa)
                if pi is None:
                    continue
                m2 = re.search(r'ldr\s+%s, \[pc, #(0x[0-9a-f]+)\]' % rm, insns[pi][1])
                if m2:
                    imm = int(m2.group(1), 16)
                    base = (pa + 8) & ~3
                    L = struct.unpack_from('<I', data, v2o(base + imm))[0]
                    return a + 8 + L
    return None

# map: id -> vtable (via beq-target case body) ; for bne the case is the fallthrough
idmap = {}
for a, idv, kind, tgt in ids:
    if kind == 'beq':
        vt = pcrel_after(tgt)
        idmap.setdefault(idv, []).append(('beq', hex(tgt), vt))
    else:
        # case continues at a+0xc (after the bne)
        nxt = insns[addr2i[a] + 3][0] if addr2i[a] + 3 < len(insns) else None
        vt = pcrel_after(nxt) if nxt else None
        idmap.setdefault(idv, []).append(('bne', hex(nxt) if nxt else None, vt))

print('\nclass 0x5441a117 entries:')
for e in idmap.get(0x5441a117, []):
    print(' ', e)
print('class 0x110ce1f entries:')
for e in idmap.get(0x110ce1f, []):
    print(' ', e)

# resolve vtable -> Load address (vt+0x10 from the computed vptr = _ZTV+8, so
# pcrel value IS _ZTV base for some cases and _ZTV+8 for others; handle both)
import subprocess
syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3:
        try:
            a = int(pr[0], 16)
        except ValueError:
            continue
        syms.append((a, pr[2]))
syms.sort()
addrs = [a for a, _ in syms]
import bisect
def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

print('\n5441a117 vtable lookup:')
for e in idmap.get(0x5441a117, []):
    vt = e[2]
    if vt:
        print('  computed=%#x %s' % (vt, sym_of(vt)))
        # try vt and vt-8 as _ZTV base; Load = stored_vptr+0x10
        for base in (vt, vt - 8):
            o = v2o(base)
            if o:
                slots = [struct.unpack_from('<I', data, o + 4 * k)[0] for k in range(8)]
                print('    base %#x slots:' % base, [hex(s) for s in slots])
                break
print('\n110ce1f vtable lookup:')
for e in idmap.get(0x110ce1f, []):
    vt = e[2]
    if vt:
        print('  computed=%#x %s' % (vt, sym_of(vt)))
