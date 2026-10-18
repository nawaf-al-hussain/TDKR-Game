#!/usr/bin/env python3
"""S35 T2c: examine 0x23cc8..0x2b7d8 gap zone for a real 394x80 cape stream;
dense alignment test (layout AND edge simultaneously); record anatomy."""
import struct, math
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', md, o)[0]
u16 = lambda o: struct.unpack_from('<H', md, o)[0]
f32 = lambda o: struct.unpack_from('<f', md, o)[0]

GAP0, GAP1 = 0x23cc8, 0x2b7d8
print(f'gap zone 0x{GAP0:x}..0x{GAP1:x} = {GAP1-GAP0} B; 394x80 = {394*80}')

def rec(o):
    p = struct.unpack_from('<3f', md, o)
    n = struct.unpack_from('<3f', md, o + 12)
    ur, vr = u16(o + 72), u16(o + 76)
    return p, n, (ur, vr)

print('\nfirst 4 records @0x23cc8 (as-if stream):')
for i in range(4):
    p, n, uv = rec(GAP0 + i * 80)
    print(f'  [{i}] pos={tuple(round(x,4) for x in p)} nrm={tuple(round(x,3) for x in n)} uv={uv}')

# dense alignment: base in [GAP0-400, GAP0+400] step 4, require 394 recs fit
def layout_at(base, nv=394):
    ok = 0
    for i in range(nv):
        o = base + i * 80
        if o + 80 > len(md): return 0.0
        p = struct.unpack_from('<3f', md, o)
        n = struct.unpack_from('<3f', md, o + 12)
        if not all(abs(x) < 10 and math.isfinite(x) for x in p): continue
        nl = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        if not (0.7 < nl < 1.3): continue
        ur, vr = u16(o + 72), u16(o + 76)
        if ur >= 16*4096 or vr >= 16*4096: continue
        ok += 1
    return ok / nv

best = []
for base in range(GAP0 - 800, GAP0 + 800, 4):
    ls = layout_at(base)
    if ls > 0.9:
        best.append((round(ls, 3), base))
best.sort(reverse=True)
print(f'\ndense alignment layout>0.9 near gap start: {best[:10]}')

# full-file alignment scan for 394 (layout>=0.99 AND nonzero pos variety)
print('\nfull-file layout>=0.99 scan (394 recs, step 4) — may take a while:')
hits = []
span = 394 * 80
for base in range(0x1000, len(md) - span, 4):
    ls = layout_at(base)
    if ls >= 0.99:
        hits.append(base)
print(f'layout>=0.99 hits: {len(hits)}')
for h in hits[:20]:
    p0 = struct.unpack_from('<3f', md, h)
    V0 = [struct.unpack_from('<3f', md, h + i*80) for i in range(0, 394, 40)]
    zs = sum(1 for V in V0 for x in V if x != 0)
    print(f'  0x{h:x}: nonzero-sample {zs}/15 first-pos {tuple(round(x,4) for x in p0)}')
