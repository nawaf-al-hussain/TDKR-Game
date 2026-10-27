#!/usr/bin/env python3
"""S63 T4: carrier recompute with the s63 nested StateSet specs + the lvc second-signal scan.
1. Walk every Health(0x0ddcd6c4)/Awareness(0x6754056b) carrier with the s63 engine-true
   specs (the 6 s62-fail carriers now walk), extract health + 16 awareness radii.
2. Compare vs s62 values and the s58/s60 pins (merc 120, vehicles 300).
3. Second-signal scan: raw-byte search for the Health component id in EVERY .lvc
   (instance-level Health would be a second, independent signal for vehicle health 300.0)."""
import struct, json, glob, os

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json'))
NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}

def walk(toks, buf, p, end):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk(t[2], buf, p, end)
                continue
            if len(t) == 1 and t[0] in NAT:
                t = t[0]
            else:
                raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok')
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        p += sz
    return p

HEALTH, AWARE = 0x0ddcd6c4, 0x6754056b
carriers = {}
for oid, name, comps, flags, payload in recs:
    if HEALTH not in comps and AWARE not in comps:
        continue
    p = 0; end = len(payload); ok = True
    off_h = off_a = None
    try:
        for cid in comps:
            s = E.get('0x%08x' % cid)
            if s is None:
                ok = False; break
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
    if off_h is not None:
        entry['health'] = round(struct.unpack_from('>f', payload, off_h)[0], 3)
    if off_a is not None:
        entry['awareness'] = [round(x, 3) for x in struct.unpack_from('>16f', payload, off_a)]
    carriers[name] = entry

n_ok = sum(1 for v in carriers.values() if v['status'] == 'OK')
fails = [k for k, v in carriers.items() if v['status'] == 'FAIL']
print('carriers: %d templates with Health/Awareness; walked OK: %d; FAIL: %s' % (len(carriers), n_ok, fails))

# comparison vs s62
prev = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_carriers62.json'))
agree = disagree = new = 0
details = []
for name, v in carriers.items():
    pv = prev.get(name)
    if v['status'] != 'OK':
        continue
    if pv is None:
        new += 1
        details.append((name, 'NEW', v.get('health')))
        continue
    if pv.get('status') != 'OK':
        new += 1
        details.append((name, 'NEW-was-FAIL', v.get('health')))
        continue
    same_h = v.get('health') == pv.get('health')
    same_a = v.get('awareness') == pv.get('awareness')
    if same_h and same_a:
        agree += 1
    else:
        disagree += 1
        details.append((name, 'DISAGREE', (pv.get('health'), v.get('health'))))
print('vs s62: agree %d, disagree %d, new(now-OK) %d' % (agree, disagree, new))
for d in details[:20]:
    print('  ', d)

# engine-true value families
vals = {}
for name, v in carriers.items():
    if v.get('health') is not None:
        vals.setdefault(v['health'], []).append(name)
print('health distribution:', {k: len(v) for k, v in sorted(vals.items(), key=lambda x: -len(x[1]))[:10]})
veh_ok = [n for n, v in carriers.items() if v.get('health') == 300.0]
print('vehicle-300 carriers OK:', len(veh_ok))

# lvc second-signal scan
pat = struct.pack('>I', HEALTH)
hits = {}
for f in sorted(glob.glob('/tmp/my-project/work/data/*.lvc')):
    b = open(f, 'rb').read()
    n = b.count(pat)
    if n:
        hits[os.path.basename(f)] = n
print('Health id 0x0ddcd6c4 occurrences across ALL .lvc files:', hits if hits else 'ZERO (single-signal CONFIRMED at the instance level)')
json.dump({'carriers': carriers, 'vs_s62': {'agree': agree, 'disagree': disagree, 'new': new, 'details': details},
           'health_dist': {str(k): len(v) for k, v in vals.items()},
           'lvc_health_id_hits': hits},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t4_carriers.json', 'w'), indent=1)
print('saved s63_t4_carriers.json')
