#!/usr/bin/env python3
"""S62 T1 step 2: apply the hand-derived BeastObjectComponentGlobal spec [i,i,STR]
and re-walk every template containing 0x59a8390c; report per-template status and
sample the decoded string values (semantic check)."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E, INC = build(SPECS_RAW)
E['0x59a8390c'] = flatten(['i', 'i', 'STR'])   # ENGINE-DERIVED (0x2e1fb0 disasm)

BEAST = 0x59a8390c
stat = {'exact': 0, 'bounds': 0, 'fail': 0}
samples = []
tail_hist = {}
for oid, name, comps, flags, payload in recs:
    if BEAST not in comps:
        continue
    p = 0; end = len(payload); ok = True
    try:
        for cid in comps:
            key = '0x%08x' % cid
            p = walk_spec(E[key], payload, p, end)
    except Exception as e:
        ok = False
        stat['fail'] += 1
        samples.append((name, 'FAIL ' + type(e).__name__ + ' ' + str(e)[:40], len(payload)))
        continue
    if p == end:
        stat['exact'] += 1
        # decode the beast string: last 12 bytes = i,i,STRidx
        i1, i2, sidx = struct.unpack_from('>iii', payload, end - 12)
        sv = strings[sidx] if 0 <= sidx < len(strings) else '<oob>'
        samples.append((name, f'EXACT i1={i1} i2={i2} str={sv!r}', len(payload)))
    else:
        stat['bounds'] += 1
        tail_hist[end - p] = tail_hist.get(end - p, 0) + 1
        samples.append((name, f'BOUNDS tail={end-p}', len(payload)))

print('templates containing 0x59a8390c:', sum(stat.values()), stat)
print('tail histogram:', tail_hist)
print()
for name, desc, ln in samples[:14]:
    print(f'  {name:44s} len={ln:4d} {desc}')
