#!/usr/bin/env python3
"""S62 T1 step 1: analyze which reader specs are incomplete and which templates they block."""
import json, sys
from collections import Counter

RE = '/tmp/my-project/work/TDKR-Game/extraction/re/session61'
specs = json.load(open(f'{RE}/s61_reader_specs.json'))
walk = json.load(open(f'{RE}/s61_t1_walk2.json'))
parse = json.load(open(f'{RE}/s61_t1_parse.json'))

PRIMS = {'i', 'c', 'f', 'STR', 'h', 'I', 'C', 's', 'u16', 'u32'}

def is_bad(tok):
    if isinstance(tok, list):
        return True  # nested loop/conditional shape
    return tok not in PRIMS

bad_specs = {}
for cid, s in specs.items():
    bad = [t for t in s['spec'] if is_bad(t)]
    if bad:
        bad_specs[cid] = (s.get('sym', '?'), s['reader'], Counter(
            t if isinstance(t, str) else json.dumps(t)[:40] for t in bad))

print('total specs:', len(specs))
print('specs with unresolved/nested tokens:', len(bad_specs))
for cid, (sym, rd, cnt) in sorted(bad_specs.items(), key=lambda x: -sum(x[1][2].values())):
    print(f'  {cid} {sym[:58]:58s} {rd} {dict(cnt)}')

# walk structure
print()
for ruleset, res in walk.items():
    if isinstance(res, dict):
        keys = {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()}
        print(ruleset, '->', keys)
