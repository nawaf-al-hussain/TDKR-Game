#!/usr/bin/env python3
"""s54 T1 step 14: scan all lvc files for Glider/Glider_Plunge records with the
pure parser, extended by CComponentGlide's read sequence (i + 22f + i) and the
Glider first component's sequence (0xdd583de - derived from its Load code)."""
import json
import struct
import subprocess
import bisect
import importlib.util

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

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

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def count_load_reads(vaddr, max_bytes=0x400):
    """Count ReadInt/ReadFloat/ReadShort/ReadChar/ReadString calls until pop{pc}."""
    off = v2o(vaddr)
    reads = []
    for ins in md.disasm(data[off:off + max_bytes], vaddr):
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                s = sym_of(t)
                if 'ReadInt' in s:
                    reads.append('i')
                elif 'ReadFloat' in s:
                    reads.append('f')
                elif 'ReadShort' in s:
                    reads.append('s')
                elif 'ReadByte' in s or 'ReadChar' in s:
                    reads.append('c')
                elif 'ReadString' in s:
                    reads.append('STR')
                else:
                    reads.append('CALL:' + s.split('(')[0])
            except ValueError:
                pass
        if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            break
    return reads

print('CComponentGlide::Load reads:', count_load_reads(0x3c0938))
# Glider first component 0xdd583de: find its Load. Use the GCT tree map:
# from s54_t1_gct_tree output - not saved; recompute quickly via the tree script logic.
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
import re
idmap = {}
for i, (a, l) in enumerate(insns):
    m = re.match(r'\S+\s+movt\s+r(\d+), #(0x[0-9a-f]+)', l)
    if not m:
        continue
    rd = m.group(1)
    hi = int(m.group(2), 16)
    lo = None
    for j in range(i - 1, max(0, i - 6), -1):
        m2 = re.match(r'\S+\s+movw\s+%s, #(0x[0-9a-f]+)' % ('r' + rd), insns[j][1])
        if m2:
            lo = int(m2.group(1), 16)
            break
    if lo is None or i + 2 >= len(insns):
        continue
    mc = re.match(r'\S+\s+cmp\s+r0,', insns[i + 1][1])
    mb = re.match(r'\S+\s+(beq|bne)\s+#(0x[0-9a-f]+)', insns[i + 2][1])
    if mc and mb and mb.group(1) == 'beq':
        idmap.setdefault((hi << 16) | lo, []).append(int(mb.group(2), 16))

def vtable_of_case(case):
    i = addr2i.get(case)
    if i is None:
        return None
    for j in range(i, min(i + 40, len(insns))):
        a, l = insns[j]
        if 'PC-REL ADD' in l:
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

for cid in (0xdd583de,):
    for case in idmap.get(cid, [])[:1]:
        vt = vtable_of_case(case)
        sym = sym_of(vt) if vt else '?'
        print('class %#x case %#x vt %#x %s' % (cid, case, vt, sym))
        # Load = vptr+0x10 where vptr = vt+8; slots from vt
        o = v2o(vt)
        slots = [struct.unpack_from('<I', data, o + 4 * k)[0] for k in range(8)]
        print('  slots:', [hex(s) for s in slots], [sym_of(s) for s in slots])

# Now the lvc scan with the extended table
GLIDE = '17878559'
spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

table, templates = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')
# extend: CComponentGlide = i + 22f + i ; 0xdd583de class = derived below
table['components'][GLIDE] = [['i', 4]] + [['f', 4]] * 22 + [['i', 4]]

GLIDER_TIDS = (0x2674, 0x4c741)
import os
files = sorted('/tmp/my-project/work/data/' + f for f in os.listdir('/tmp/my-project/work/data')
               if f.endswith('.lvc'))
for path in files:
    try:
        tokens = []
        res = lp.parse(path, table, templates, tokens)
        # find glide-template records
        hits = [(hex(rid), hex(rs), hex(tid), kind) for rid, rs, tid, end, kind in res['records']
                if tid in GLIDER_TIDS]
        # also census glide class reads
        gc = [(hex(rid), hex(cs), n) for rid, cs, n in res['census'].get(GLIDE, [])]
        print(path.split('/')[-1], 'records', len(res['records']), 'complete', res['complete'],
              '| glider recs', hits, '| glide-comp reads', gc)
    except Exception as e:
        print(path.split('/')[-1], 'FAILED:', type(e).__name__, e)
