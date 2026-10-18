#!/usr/bin/env python3
"""S36 T2-data: extract BuiltinBox (1923007858) sizes + trigger (938977454)
records from GothamCity.lvc; link by GameObject; build data-determined volumes;
validate: triggers vs spawns vs GetDistFromMC-threshold objects vs street nulls."""
import sys, json, struct, math, re, random
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab, templates, None)
d, strings = res['data'], res['strings']
print('lvc parsed, data', len(d), 'B')

# ---- BuiltinBox records: [f size.x][f size.y][f size.z][i][c][c][c] ----
boxes = []
for rid, off, sz in res['census'].get('1923007858', []):
    o = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = o
    try:
        f = [rr.tok('f') for _ in range(3)]
        i0 = rr.tok('i')
        c = [rr.tok('c') for _ in range(3)]
    except Exception:
        continue
    boxes.append({'off': o, 'size': f, 'i': i0, 'c': c})
print(f'BuiltinBox records: {len(boxes)}')
szs = np.array([b['size'] for b in boxes])
print('size.x pct:', np.percentile(szs[:, 0], [5, 25, 50, 75, 95]).round(2))
print('size.y pct:', np.percentile(szs[:, 1], [5, 25, 50, 75, 95]).round(2))
print('size.z pct:', np.percentile(szs[:, 2], [5, 25, 50, 75, 95]).round(2))

# ---- trigger records ----
trigs = []
for rid, off, sz in res['census'].get('938977454', []):
    o = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = o
    try:
        i0 = rr.tok('i')
        f9 = [rr.tok('f') for _ in range(9)]
        i1 = rr.tok('i')
        c0 = rr.tok('c')
        s_ = rr.tok('STR')
        if isinstance(s_, int): s_ = None
    except Exception:
        continue
    trigs.append({'off': o, 'i0': i0, 'pos': f9[:3], 'rot': f9[3:6], 'scale': f9[6:9],
                  'i1': i1, 'c': c0, 'script': s_})
print(f'trigger records: {len(trigs)}')

# ---- linkage: GameObject -> components ----
# census gives per-class record offsets; the lvc object records list components
# by object. Use res['objects'] if available
objs = res.get('objects') or []
print('objects in parse:', len(objs) if objs else 'N/A')
if objs:
    box_by_obj = {}
    trig_by_obj = {}
    for o_ in objs:
        oid = o_.get('id') if isinstance(o_, dict) else None
        comps = o_.get('components', []) if isinstance(o_, dict) else []
        for c in comps:
            cid = c.get('class') if isinstance(c, dict) else None
            rid = c.get('record_off') if isinstance(c, dict) else None
    # generic: index by whatever structure exists
    print('object[0]:', json.dumps(objs[0])[:300] if objs else '')
json.dump({'boxes': boxes[:2000], 'trigs': trigs[:600]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t2_raw.json', 'w'))
