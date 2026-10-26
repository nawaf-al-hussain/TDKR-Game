#!/usr/bin/env python3
"""S62 T1 step 5: blocker census on the CORRECTED spec table."""
import struct, json, collections

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))
specs61 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
idmap = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_id2reader.json'))
sym_by_reader = {}
for cid, c in idmap.items():
    sym_by_reader['0x%08x' % int(c['load'], 16)] = c['load_sym']

blockers = collections.defaultdict(lambda: {'templates': 0, 'names': [], 'causes': collections.Counter()})
na = exact = bounds = fail = 0
for oid, name, comps, flags, payload in recs:
    if not comps:
        na += 1
        continue
    p = 0; end = len(payload); reason = None
    try:
        for cid in comps:
            key = '0x%08x' % cid
            spec = E.get(key)
            if spec is None:
                reason = f'nocase {key}'; break
            p = walk_spec(spec, payload, p, end)
    except OOB:
        reason = f'OOB after {key}@{p}'
    except ValueError as e:
        reason = f'tok {key}: {str(e)[:30]}'
    except Exception as e:
        reason = f'exc {key}: {str(e)[:30]}'
    if reason:
        # find the cid at fault: re-walk to find which component was active
        q = 0
        for cid in comps:
            key = '0x%08x' % cid
            spec = E.get(key)
            try:
                q = walk_spec(spec, payload, q, end)
            except Exception:
                b = blockers[key]
                b['templates'] += 1
                b['names'].append(name)
                b['causes'][reason.split(' ')[0]] += 1
                break
        fail += 1
        continue
    if p == end:
        exact += 1
    else:
        bounds += 1

print(f'exact {exact} pass {exact+bounds} fail {fail} na {na}')
print()
for key, b in sorted(blockers.items(), key=lambda x: -x[1]['templates']):
    rd = ''
    v = None
    src = [s for s in specs61.values() if '0x%08x' % int(s['reader'], 16) == key]
    print(f"{key} {b['reader'] if 'reader' in b else ''} T={b['templates']:3d} {dict(b['causes'])} "
          f"{(sym_by_reader.get(key) or (src[0]['sym'] if src else '?'))[:52]}")
    print('      ', b['names'][:8])
