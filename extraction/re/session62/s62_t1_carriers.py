#!/usr/bin/env python3
"""S62 T1 step 7: carrier extraction with the corrected engine-true specs.
Walks every template containing Health (0x0ddcd6c4) / Awareness (0x6754056b),
extracts health = Health spec's first float and the 16 Awareness radii,
compares with the s58/s60 calibrated values (from s61_t1_carriers.json + s58 note)."""
import struct, json

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))
# ensure fixed32 StateSet (empirically best; documented residual)
E['0x5441a117'] = ['i'] + ['STR'] * 7
# engine-true rep semantics override
def walk(toks, buf, p, end):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0: continue
                if n > 100000: raise OOB()
                for _ in range(n): p = walk(t[2], buf, p, end)
                continue
            if len(t) == 1 and t[0] in NAT: t = t[0]
            else: raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None: raise ValueError('tok')
        if p + sz > end: raise OOB()
        if t == 'i': last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c': last = buf[p]
        p += sz
    return p

HEALTH, AWARE = 0x0ddcd6c4, 0x6754056b
carriers = {}
for oid, name, comps, flags, payload in recs:
    if HEALTH not in comps and AWARE not in comps:
        continue
    p = 0; end = len(payload); ok = True
    try:
        for cid in comps:
            s = E.get('0x%08x' % cid)
            if s is None: ok = False; break
            if cid == HEALTH:
                off_h = p
            if cid == AWARE:
                off_a = p
            p = walk(s, payload, p, end)
    except Exception:
        ok = False
    if not ok:
        carriers[name] = {'status': 'FAIL'}
        continue
    entry = {'status': 'OK', 'payload_end': p == end}
    if HEALTH in comps:
        f = struct.unpack_from('>f', payload, off_h)[0]
        entry['health'] = round(f, 3)
    if AWARE in comps:
        radii = struct.unpack_from('>16f', payload, off_a)
        entry['awareness'] = [round(x, 3) for x in radii]
    carriers[name] = entry

n_ok = sum(1 for v in carriers.values() if v['status'] == 'OK')
print(f'carriers: {len(carriers)} templates with Health/Awareness; walked OK: {n_ok}')
json.dump(carriers, open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_carriers62.json', 'w'), indent=1)

# compare vs s60 pinned values: NPC merc 120.0 / awareness16 [11,17,...]; vehicles 300.0
s61c = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_carriers.json'))
print('\nsample carriers:')
for name in ('Melee_Enemy_Merc', 'Helicopter', 'Tumbler', 'Police_Car', 'Bane_SUV'):
    v = carriers.get(name)
    s = s61c['values'] if isinstance(s61c, dict) and 'values' in s61c else None
    if v:
        print(f'  {name}: {json.dumps(v)[:120]}')
