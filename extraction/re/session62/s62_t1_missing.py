#!/usr/bin/env python3
"""S62 T1 step 4b: complete spec table — s62 map first, s61 fallback for ids the
island scan missed (Health, BeastObjectComponent, ...)."""
import struct, json, collections

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
gol_ids = set()
for oid, name, comps, flags, payload in recs:
    for c in comps:
        gol_ids.add('0x%08x' % c)
print('distinct gol component ids:', len(gol_ids))

specs61 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
plan = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_specplan.json'))
final = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

s61_by_id = {}
for k, v in specs61.items():
    s61_by_id['0x%08x' % int(k, 16)] = v

missing = sorted(gol_ids - set(final.keys()))
print('gol ids missing from the s62 table:', missing)
for m in missing:
    v = s61_by_id.get(m)
    print(f'  {m}: s61 has reader {v["reader"] if v else "NONE"} {v["sym"][:46] if v else ""}')
