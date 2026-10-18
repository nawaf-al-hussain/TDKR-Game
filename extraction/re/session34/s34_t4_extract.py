#!/usr/bin/env python3
"""S34 T4a: extract ALL GothamCity Lua trigger scripts (tid-9803 records:
[i id][f9][i][c][STR script]) + owner TRS. Output: s34_t4_scripts.json"""
import sys, json, struct
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
print(f'records: {len(res["records"])}, census classes: {len(res["census"])}')

out = []
for cid, recs in res['census'].items():
    if not recs or not isinstance(recs[0], tuple) or len(recs[0]) != 3:
        continue
    for rid, off, sz in recs:
        if not (isinstance(off, str) and off.startswith('0x')):
            continue
        off = int(off, 16)
        if sz != 118:   # the uniform trigger record size (r22)
            continue
        rr = lvc_pure.Reader(d, strings)
        rr.p = off
        try:
            i0 = rr.tok('i')
            f9 = [rr.tok('f') for _ in range(9)]
            i1 = rr.tok('i')
            c0 = rr.tok('c')
            s = rr.tok('STR')
        except Exception:
            continue
        if s and 'function' in s:
            out.append(dict(rec_off=off, rec_id=i0, f9=f9, i1=i1, c0=c0,
                            script=s))
print(f'{len(out)} trigger scripts extracted')
json.dump(out, open('/home/z/my-project/scripts/s34_t4_scripts.json', 'w'))
from collections import Counter
# quick census of function names
import re
fns = []
for o in out:
    m = re.search(r'function\s+([A-Za-z0-9_]+)', o['script'])
    if m: fns.append(m.group(1))
print('function name kinds:', Counter(n.rsplit('_', 1)[-1] for n in fns))
print('sample f9[1:4] (pos):', [np.round(o['f9'][1:4], 1).tolist() for o in out[:4]])
