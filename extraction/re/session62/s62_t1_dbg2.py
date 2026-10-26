#!/usr/bin/env python3
"""S62 T1 step 6: per-component debug walk with the corrected table."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))
for nk, toks in list(E.items()):
    E[nk] = toks

target = sys.argv[1]
for oid, name, comps, flags, payload in recs:
    if name != target:
        continue
    p = 0; end = len(payload)
    print(f'{name} len={end} comps={[hex(c) for c in comps]}')
    for cid in comps:
        key = '0x%08x' % cid
        spec = E.get(key)
        try:
            np = walk_spec(spec, payload, p, end)
            print(f'  {key} @{p}..{np} (spec flat len {len(spec)})')
            p = np
        except Exception as e:
            print(f'  {key} @{p} FAIL {type(e).__name__} {str(e)[:50]}')
            # hexdump from p to end for manual inspection
            print(f'  bytes from {p}:', payload[p:p+64].hex(' '))
            break
    if p is not None and all(True for _ in [1]):
        pass
    break
