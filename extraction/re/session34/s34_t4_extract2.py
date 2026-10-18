#!/usr/bin/env python3
"""S34 T4a-v2: extract ALL Lua scripts from GothamCity.lvc via the
[u8 length][script bytes] pool at 'function ...' occurrences; join with the
380 trigger records by object id."""
import sys, json, re, struct
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open(TAB))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab,
                     templates, None)
d, strings = res['data'], res['strings']

# 1) all scripts: [len byte][script]
scripts = []
for m in re.finditer(rb'function\s+[A-Za-z_][A-Za-z0-9_]*\s*\(', d):
    start = m.start()
    ln = d[start - 1]
    if ln < 16 or start + ln > len(d): continue
    body = d[start:start + ln]
    # sanity: body should not contain NUL and should end plausibly with 'end'
    if b'\x00' in body: continue
    tail = body.rstrip()
    if not tail.endswith(b'end'): continue
    scripts.append(dict(off=start, len=ln, script=body.decode('latin1')))
# dedup by start
seen = set()
uniq = []
for s in scripts:
    if s['off'] in seen: continue
    seen.add(s['off']); uniq.append(s)
print(f'{len(uniq)} scripts (length-prefixed, ends with end)')

# 2) function names + object ids
for s in uniq:
    m = re.search(r'function\s+([A-Za-z0-9_]+)', s['script'])
    s['fn'] = m.group(1) if m else None
    m2 = re.search(r'Obj(\d+)_', s['fn'] or '')
    s['obj_id'] = int(m2.group(1)) if m2 else None

# 3) trigger records: class 938977454 (54-B: [i][f9][i][c][STR->script])
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
    trigs.append(dict(rec_id=i0, f9=f9, rec_off=o, script=s_ or '',
                      fn=((re.search(r'function\s+([A-Za-z0-9_]+)', s_ or '')).group(1) if s_ and re.search(r'function\s+([A-Za-z0-9_]+)', s_) else None)))
print(f'{len(trigs)} trigger records (54-B class)')

joined = sum(1 for t in trigs if t.get('script'))
print(f'triggers with inline scripts: {joined}/{len(trigs)}')
pool_ids = {s['obj_id'] for s in uniq if s['obj_id'] is not None}
trig_ids = {t['rec_id'] for t in trigs}
orphan = [s for s in uniq if s['obj_id'] not in trig_ids]
print(f'pool scripts not on 54-B triggers: {len(orphan)} (other object types)')

json.dump(dict(triggers=trigs, all_scripts=uniq),
          open('/home/z/my-project/scripts/s34_t4_scripts.json', 'w'))
from collections import Counter
kinds = Counter(s['fn'].rsplit('_', 1)[-1] for s in uniq if s['fn'])
print('function suffix census:', dict(kinds))
