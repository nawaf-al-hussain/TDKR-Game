#!/usr/bin/env python3
"""S62 T1 step 1: per-template fail-cause census (canonical-walker variant).
Uses the s61 walker2 functions verbatim (exec of its pre-main source) so results are
bit-identical to s61_t1_walk2.json RAW; only the record loop is re-implemented to
record WHICH component reader failed and WHY per template.
Output: s62_t1_blockers.json"""
import struct, json, collections

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E_raw, INC_raw = build(SPECS_RAW)

blockers = collections.defaultdict(lambda: {'sym': '', 'reader': '', 'templates': 0,
                                            'names': [], 'causes': collections.Counter()})
cause_totals = collections.Counter()
na = exact = bounds = fail = 0
tails = collections.Counter()

for oid, name, comps, flags, payload in recs:
    if not comps:
        na += 1
        continue
    p = 0
    end = len(payload)
    try:
        for cid in comps:
            key = '0x%08x' % cid
            spec = E_raw.get(key)
            if spec is None:
                b = blockers[key]
                b['sym'] = 'NOCASE'
                b['templates'] += 1
                b['names'].append(name)
                b['causes']['nocase'] += 1
                raise ValueError('nocase')
            try:
                p = walk_spec(spec, payload, p, end)
            except (OOB, ValueError) as e:
                src = SPECS_RAW.get(cid) or SPECS_RAW.get(key) or {}
                b = blockers[key]
                b['sym'] = src.get('sym', '?')
                b['reader'] = src.get('reader', '?')
                b['templates'] += 1
                b['names'].append(name)
                kind = 'call' if (isinstance(e, ValueError) and 'call' in str(e)) else (
                    'OOB' if isinstance(e, OOB) else 'err')
                b['causes'][kind] += 1
                e.cid = key
                raise
    except (OOB, ValueError) as e:
        fail += 1
        cause_totals[getattr(e, 'cid', 'nocase')] += 1
        continue
    if p == end:
        exact += 1
    else:
        bounds += 1
        tails['tail:%d' % (end - p)] += 1

print(f'exact {exact} bounds {bounds} (={exact+bounds}) fail {fail} na {na} / {len(recs)}')
print()
print('=== templates blocked per reader (sorted by template count) ===')
for key, b in sorted(blockers.items(), key=lambda x: -x[1]['templates']):
    print(f"{key} {b['reader']:>9s} T={b['templates']:3d} {dict(b['causes'])} {b['sym'][:52]}")
print()
print('cause totals:', dict(cause_totals.most_common(25)))
print('tail histogram:', dict(tails.most_common(15)))

out = {}
for key, b in blockers.items():
    out[key] = {'sym': b['sym'], 'reader': b['reader'], 'templates': b['templates'],
                'names': b['names'][:40], 'causes': dict(b['causes'])}
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_blockers.json', 'w'), indent=1)
print('saved s62_t1_blockers.json')
