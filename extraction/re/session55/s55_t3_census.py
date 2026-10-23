#!/usr/bin/env python3
"""s55 T3: Enemy_Grapnel_Target (gol template 0xaae6a) instance census across all lvc
files via the pure parser; positions of any instances; null control with a bogus id."""
import struct, importlib.util, os, json, random

spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

table, templates = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')
print('template table entries:', len(table) if hasattr(table, '__len__') else '?')
# what does the table look like?
ks = list(table.keys())[:5] if isinstance(table, dict) else None
print('sample keys:', ks)

DATA = '/tmp/my-project/work/data/'
TARGET = 0xaae6a
NULLS = [0xaae6b, 0xaae69, 0x1aae6a]
census = {}
pos_samples = []
files = sorted(f for f in os.listdir(DATA) if f.endswith('.lvc'))
for f in files:
    path = DATA + f
    try:
        recs = lp.parse_lvc(path, table) if hasattr(lp, 'parse_lvc') else None
    except TypeError:
        recs = None
    if recs is None:
        # fall back: introspect module API
        apis = [x for x in dir(lp) if not x.startswith('_')]
        print(f, '-> module API:', apis)
        break
    n_t = sum(1 for r in recs if getattr(r, 'oid', None) == TARGET)
    n_null = {h: sum(1 for r in recs if getattr(r, 'oid', None) == h) for h in NULLS}
    census[f] = {'records': len(recs), 'target': n_t, 'nulls': n_null}
    for r in recs:
        if getattr(r, 'oid', None) == TARGET and len(pos_samples) < 12:
            pos_samples.append({'file': f, 'rec': str(r)[:200]})
print(json.dumps(census, indent=1))
print('samples:', pos_samples[:3])
