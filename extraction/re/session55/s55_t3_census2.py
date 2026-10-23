#!/usr/bin/env python3
"""s55 T3: Enemy_Grapnel_Target census via lvc spawn records (tid 0x2662 -> census.spawn,
objId field). Counts per level + positions + null control (bogus ids)."""
import importlib.util, os, json, math, random, struct

spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)
table, templates = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')

DATA = '/tmp/my-project/work/data/'
TARGET = 0xaae6a
res = {}
all_spawns = {}
pos_samples = []
for f in sorted(os.listdir(DATA)):
    if not f.endswith('.lvc'):
        continue
    try:
        out = lp.parse(DATA + f, table, templates)
    except (struct.error, AssertionError) as e:
        res[f] = {'error': str(e)[:80]}
        continue
    spawns = out['census'].get('spawn', [])
    complete = (out['data'][out['table_off']:] is not None)
    n_target = 0
    for s in spawns:
        oid = s.get('objId')
        all_spawns.setdefault(oid, []).append(f)
        if oid == TARGET:
            n_target += 1
            if len(pos_samples) < 10:
                pos_samples.append({'file': f, 'pos': s.get('pos'), 'name': s.get('name')})
    res[f] = {'records': out['nrec_hdr'], 'spawns': len(spawns), 'enemy_grapnel_target': n_target,
              'complete_frame': out.get('complete', None)}

print(json.dumps(res, indent=1))
print('\nspawn objId histogram (top 15):')
hist = sorted(((k, len(v)) for k, v in all_spawns.items()), key=lambda kv: -kv[1])
for k, n in hist[:15]:
    print('   ', hex(k) if isinstance(k, int) else k, n, 'in', sorted(set(v for v in all_spawns[k]))[:4])
print('target samples:', json.dumps(pos_samples[:5], indent=1))
json.dump({'per_level': res, 'histogram': [[hex(k) if isinstance(k, int) else k, n] for k, n in hist],
           'target_samples': pos_samples},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t3_target_census.json', 'w'), indent=1)
