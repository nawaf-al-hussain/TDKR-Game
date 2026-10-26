#!/usr/bin/env python3
"""S62 T5: CFG tracer for reader functions - execution-order read sequence with loops.
Walks the ARM disasm from the entry following the fall-through path at conditionals,
records CMemoryStream::Read* calls in EXECUTION order, and marks back-edges (loops).
Usage: cfg_trace.py <start_hex> <end_hex>"""
import re, subprocess, sys, collections

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
start = int(sys.argv[1], 16)
end = int(sys.argv[2], 16)
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t5_cfg_%x.txt' % start

dis = subprocess.run(
    ['python3', '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_disasm.py',
     '%x' % start, '%x' % end],
    capture_output=True, text=True).stdout

insns = []   # (addr, text)
for line in dis.splitlines():
    m = re.match(r'^([0-9a-f]{8})\s+(.*)$', line)
    if m:
        insns.append((int(m.group(1), 16), m.group(2).strip()))
byaddr = {a: t for a, t in insns}
order = [a for a, _ in insns]
idx = {a: i for i, a in enumerate(order)}

def target(text):
    m = re.search(r'(bl|b|beq|bne|bhs|blo|bhi|bls|bge|blt|bgt|ble|bal)\s+#?0x([0-9a-f]+)', text)
    return int(m.group(2), 16) if m else None

def is_read(text):
    return 'CMemoryStream::Read' in text

def read_kind(text):
    if 'ReadString' in text: return 'STR'
    if 'ReadInt' in text: return 'i'
    if 'ReadFloat' in text: return 'f'
    if 'ReadByte' in text: return 'c'
    if 'ReadShort' in text: return 's'
    return 'READ?'

# straight-line trace with a visited set; conditionals: follow fall-through first,
# but record the branch edge so loops (back-edges) get reported
seq = []      # list of items: ('read', kind, addr) | ('loopback', target, addr) | ('call', sym, addr)
visited = set()
cur = start
steps = 0
while cur in byaddr and steps < 20000:
    steps += 1
    if cur in visited:
        seq.append(('visited', cur, None))
        break
    visited.add(cur)
    t = byaddr[cur]
    if is_read(t):
        seq.append(('read', read_kind(t), cur))
    elif 'bl ' in t and '->' in t:
        sym = t.split('->')[-1].strip()
        if 'CMemoryStream' not in sym and 'operator' not in sym and 'basic_string' not in sym \
           and 'vector<' not in sym and 'throw' not in sym:
            seq.append(('call', sym[:70], cur))
    tgt = target(t)
    is_cond = re.match(r'^(b(eq|ne|hs|lo|hi|ls|ge|lt|gt|le|al))', t) is not None
    is_uncond = t.startswith('b ') or t.startswith('b#') or t.startswith('b.')
    nxt = None
    if is_uncond and tgt is not None and not t.startswith('bl '):
        nxt = tgt
        if tgt <= cur:
            seq.append(('loopback-to-%x' % tgt, cur, None))
    elif is_cond:
        if tgt is not None and tgt <= cur:
            seq.append(('LOOPBACK-if-taken->%x' % tgt, cur, None))
        nxt = order[idx[cur] + 1] if idx[cur] + 1 < len(order) else None
    else:
        nxt = order[idx[cur] + 1] if idx[cur] + 1 < len(order) else None
    if nxt is None:
        seq.append(('end', cur, None))
        break
    cur = nxt

with open(OUT, 'w') as f:
    for item in seq:
        f.write(repr(item) + '\n')
reads = [x for x in seq if x[0] == 'read']
loops = [x for x in seq if x[0].startswith('LOOPBACK') or x[0].startswith('loopback')]
print('trace steps', steps, 'reads', len(reads), 'loops', len(loops), '->', OUT)
for item in seq:
    if item[0] == 'read':
        print('%08x  READ %s' % (item[2], item[1]))
    elif item[0].startswith('LOOPBACK'):
        print('        %s @%08x' % (item[0], item[1]))
    elif item[0] == 'call':
        print('        call %s' % item[1])
    elif item[0] in ('visited', 'end'):
        print('        <%s>' % item[0])
