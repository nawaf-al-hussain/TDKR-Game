#!/usr/bin/env python3
"""S62 T1: reassign s61 byte-sequence specs by READER FUNCTION using the corrected
id2reader map; list readers that still need disasm derivation."""
import json

specs = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
newmap = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_id2reader.json'))

# reader func -> spec (from s61 specs), normalized by int value
by_reader = {}
for k, v in specs.items():
    by_reader[int(v['reader'], 16)] = (v, '0x%08x' % int(k, 16))

need_derive = {}
reassign = {}
for cid, c in newmap.items():
    nk = '0x%08x' % int(cid)
    r = int(c['load'], 16)
    if r in by_reader:
        reassign[nk] = ('0x%08x' % r, by_reader[r][0]['sym'])
    else:
        need_derive[nk] = ('0x%08x' % r, c['load_sym'])

print(f'readers covered by an existing s61 spec: {len(reassign)}')
print(f'readers NEEDING derivation: {len(need_derive)}')
for nk, (r, sym) in sorted(need_derive.items()):
    print(f'  {nk} -> {r} {sym[:58]}')

json.dump({'reassign': reassign, 'need_derive': need_derive},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_specplan.json', 'w'), indent=1)
print('saved plan')
