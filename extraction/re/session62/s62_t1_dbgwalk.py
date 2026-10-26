#!/usr/bin/env python3
"""S62 T1: debug the per-component walk on one template with chosen spec fixes."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E, INC = build(SPECS_RAW)

# fixes under test (command-line selectable)
FIX_CB = '--cb44' in sys.argv      # CBase f x9 (44 B)
FIX_BC = '--bc2str' in sys.argv    # BeastComponent second STR (40 B)
FIX_BG = '--bg' in sys.argv        # BeastGlobal i,i,STR (12 B)
if FIX_CB:
    for k in ('0x0014ca79',):
        E[k] = flatten(['c', 'i'] + ['f'] * 9 + ['c', 'c', 'c'])
if FIX_BC:
    E['0x365cfd67'] = flatten(['f'] * 4 + ['STR'] + ['f'] * 4 + ['STR'])
if FIX_BG:
    E['0x59a8390c'] = flatten(['i', 'i', 'STR'])

target = sys.argv[1] if not sys.argv[1].startswith('--') else None
for oid, name, comps, flags, payload in recs:
    if target and name != target:
        continue
    p = 0; end = len(payload)
    print(f'{name} len={end}')
    for cid in comps:
        key = '0x%08x' % cid
        spec = E.get(key)
        sym = SPECS_RAW.get(key, {}).get('sym', '?')
        try:
            np = walk_spec(spec, payload, p, end)
            print(f'  {key} {sym[:44]:44s} @{p}..{np}')
            p = np
        except Exception as e:
            print(f'  {key} {sym[:44]:44s} @{p} FAIL {type(e).__name__} {str(e)[:40]}')
            p = None
            break
    if p is not None:
        print(f'  END p={p} len={end} -> ' + ('EXACT' if p == end else f'tail {end-p}'))
    if target:
        break
