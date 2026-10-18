#!/usr/bin/env python3
"""S36 T5 pycounts: comparable lvc counts (records + strings) per island."""
import sys, json, glob, os
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
out = {}
for p in sorted(glob.glob('/tmp/my-project/work/data/*.lvc')):
    name = os.path.basename(p)
    try:
        res = lvc_pure.parse(p, tab, templates, None)
        out[name] = {'nrec': len(res.get('records', [])), 'nstrings': len(res.get('strings', []))}
        if not out[name]['nrec']:
            # lvc_pure may not return 'records' — derive from census totals
            out[name]['nrec'] = sum(len(v) for v in res['census'].values()) if 'census' in res else 0
    except Exception as e:
        out[name] = {'error': str(e)[:100]}
    print(name, out[name])
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t5_pycounts.json', 'w'), indent=1)
