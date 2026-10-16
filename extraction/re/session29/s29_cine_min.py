#!/usr/bin/env python3
"""S29 T1b: full dumps of minimal cinematic instances for grammar derivation."""
import json
TAB = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_readseq.json'
t = json.load(open(TAB))
TID = '397182239'
spans = t['spans'][TID]
toks = t['spans_toks'] if False else t['span_toks'][TID]
by_off = {off: size for off, size in spans}

for target in (5952371, 6207329, 5796656):
    key = str(target)
    print(f'===== instance @{target} ({by_off[target]} B) =====')
    for tk in toks[key]:
        print(f'   {tk[0]:4s} +{tk[1]-target:<5d} sz={tk[2]} val={str(tk[3])[:40]}')
