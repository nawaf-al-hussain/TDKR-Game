#!/usr/bin/env python3
"""S29 T1: derive CCinematicComponent grammar from 34 measured island instances."""
import json, struct, collections
TAB = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_readseq.json'
t = json.load(open(TAB))
TID = '397182239'  # 0x17AC851F
spans = t['spans'][TID]
toks = t['span_toks'][TID]
print(f'{len(spans)} instances, total bytes {sum(s[1] for s in spans)}')

def shape(tk):
    return f'{tk[0]}({tk[2]})'

# print instance 0 fully
first_off = str(spans[0][0])
print(f'--- instance @ {first_off} ({spans[0][1]} B) ---')
for tk in toks[first_off]:
    print(f'   {tk[0]:4s} off={tk[1]} sz={tk[2]} val={str(tk[3])[:48]}')

# structural profile of every instance: counts by kind, and the tail pattern
print('\n--- profiles ---')
prof = []
for off, size in spans:
    tkl = toks[str(off)]
    kinds = collections.Counter(x[0] for x in tkl)
    prof.append((off, size, len(tkl), dict(kinds)))
for off, size, n, kinds in prof:
    print(f'  @{off}: {size}B {n} toks {kinds}')
