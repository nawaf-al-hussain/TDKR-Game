#!/usr/bin/env python3
"""S62 T1: diff s61 reader assignment vs corrected id2reader map."""
import json

specs = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
newmap = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_id2reader.json'))

norm = {}
for k, v in specs.items():
    nk = '0x%08x' % int(k, 16)
    norm[nk] = v

mismatch = []
checked = 0
for cid, c in newmap.items():
    nk = '0x%08x' % int(cid)  # decimal-string keys from int json dump
    if nk not in norm:
        continue
    checked += 1
    old_r = norm[nk]['reader']
    if int(old_r, 16) != int(c['load'], 16):
        mismatch.append((nk, norm[nk]['sym'], old_r, c['load_sym'], c['load']))

print(f's61 specs: {len(norm)}, corrected map: {len(newmap)}, checked: {checked}, reader mismatches: {len(mismatch)}')
for cid, oldsym, oldr, newsym, newr in sorted(mismatch):
    print(f'  {cid}\n    s61: {oldsym[:58]} @ {oldr}\n    s62: {newsym[:58]} @ {newr}')
