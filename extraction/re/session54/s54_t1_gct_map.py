#!/usr/bin/env python3
"""s54 T1 step 10: map every GCT pc-rel add site to its computed vtable target;
find the CComponentGlide case (target 0xbd8998) and the class id guarding it."""
import struct
import re

data = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

lines = open('/home/z/my-project/scripts/s54_gct_full_disasm.txt').read().splitlines()
idx = {}
for l in lines:
    if not l:
        continue
    try:
        a = int(l.split()[0], 16)
    except ValueError:
        continue
    idx[a] = l

targets = {}
for a, l in sorted(idx.items()):
    if 'PC-REL ADD' not in l:
        continue
    rest = l.split(None, 2)[2]
    rest = rest.split(';')[0]
    parts = [p.strip() for p in rest.split(',')]
    rm = parts[2]
    for d in range(1, 12):
        pa = a - d * 4
        if pa in idx:
            m2 = re.search(r'ldr\s+%s, \[pc, #(0x[0-9a-f]+)\]' % rm, idx[pa])
            if m2:
                imm = int(m2.group(1), 16)
                base = (pa + 8) & ~3
                L = struct.unpack_from('<I', data, v2o(base + imm))[0]
                targets[a] = a + 8 + L
                break

glide = [(a, t) for a, t in targets.items() if t in (0xbd8998, 0xbd8990)]
print('GLIDE case sites:', [(hex(a), hex(t)) for a, t in glide])
ts = sorted(set(targets.values()))
print('distinct targets:', len(ts), 'range', hex(ts[0]), hex(ts[-1]))

if glide:
    a = glide[0][0]
    # find the guarding class id: search back for the nearest movw/movt or cmp
    # with a large constant before the case body
    movw = {}
    idv = None
    ida = None
    for pa in range(a - 0x800, a, 4):
        if pa not in idx:
            continue
        l = idx[pa]
        m = re.match(r'\S+\s+(movw|movt)\s+r(\d+), #(0x[0-9a-f]+)', l)
        if m:
            rd = int(m.group(2))
            imm = int(m.group(3), 16)
            if m.group(1) == 'movw':
                movw[rd] = imm
            else:
                if rd in movw:
                    idv = (imm << 16) | movw[rd]
                    ida = pa
    print('nearest preceding movw/movt full id: %#x @%#x' % (idv, ida) if idv else 'none via movw/movt')
    # dump disasm lines around the case
    lo, hi = a - 0x60, a + 0x50
    print('\ndisasm around case:')
    for pa in range(lo, hi, 4):
        if pa in idx:
            print(idx[pa])
