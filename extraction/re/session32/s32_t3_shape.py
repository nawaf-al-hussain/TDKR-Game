#!/usr/bin/env python3
"""S32 T3c: parse the 60-B shape class 1923007858 for trigger owners +
disasm IsObjectInside with venv capstone."""
import sys, json, struct, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}

# trigger rids by tid
trig_rids = [rid for rid, s0, tid, e, k in res['records'] if tid in
             (9803, 9809, 18250)]
print(f'trigger objects: {len(trig_rids)}')
set_trig = set(trig_rids)

# parse class 1923007858 records: 60 B each
shape = []
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    shape.append((rid, off, sz, d[off:off + sz]))
print(f'shape records: {len(shape)}, owner-tid counts:',
      collections.Counter(tid_of.get(r) for r, *_ in shape).most_common(4))
# how many belong to trigger objects?
n_own = sum(1 for r, *_ in shape if r in set_trig)
print(f'shape records owned by trigger objects: {n_own}')
for r, off, sz, raw in shape[:3]:
    print(f'  rid {r} tid {tid_of.get(r)} @0x{off:x}: {raw.hex()}')
    print(f'    f32 view: {struct.unpack_from("<15f", raw, 0)}')
    print(f'    u32 view: {[f"{x:08x}" for x in struct.unpack_from("<15I", raw, 0)]}')
