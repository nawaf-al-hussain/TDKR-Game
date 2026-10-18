#!/usr/bin/env python3
"""S36 T2-link: identify which component class feeds CTriggerShapeAABB:
compare raw-60 (729ec572) records vs BuiltinBox (1923007858) per object."""
import sys, json, struct
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab, templates, None)
d, strings = res['data'], res['strings']

cens = res['census']
for key in ('729ec572', '1923007858', '938977454'):
    lst = cens.get(key, [])
    print(f'class {key}: {len(lst)} records')

# raw-60 records: dump bytes 0x10..0x20 as floats for the first 10
raws = []
for rid, off, sz in cens.get('729ec572', []):
    o = int(off, 16)
    raws.append(d[o:o + 60])
if raws:
    print('raw-60 sample floats @+0x10..:', )
    for r in raws[:6]:
        w = struct.unpack_from('<3f', r, 0x10)
        print('  ', [round(x, 2) for x in w], '| bytes:', r[:8].hex())
    allf = np.array([struct.unpack_from('<15f', r, 0) for r in raws])
    print('raw-60 @0x10 float pcts (3 cols):')
    for c in range(3):
        print('  col', c, np.percentile(allf[:, 4 + c], [5, 50, 95]).round(2))
