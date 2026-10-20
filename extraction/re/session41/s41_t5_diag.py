#!/usr/bin/env python3
"""S41 T5 (time-boxed diagnostic): characterize the 0x14CA79 id-space mismatch
from the EXISTING engine-walk products (no unicorn rerun within budget).
Quantifies: record counts, token truncation point, id overlap with the
script-id space, and the resulting pair ceiling."""
import json, sys
import numpy as np
from collections import defaultdict

RECS = '/tmp/my-project/work/s26_v2_GothamCity_records.json'
TOKS = '/tmp/my-project/work/s26_v2_GothamCity_toks.json'
TRIGS = '/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'

recs = json.load(open(RECS))
print('walk records:', len(recs))
tids = defaultdict(int)
for r in recs:
    tids[r[2]] += 1
print('top tids:', sorted(tids.items(), key=lambda kv: -kv[1])[:8])
n_generic = sum(c for t, c in tids.items() if t == 0x14CA79 or t == 5304953)
print('0x14CA79 records (5304953):', tids.get(5304953, 0))

# walk ids = engine ids recovered
walk_ids = set(r[0] for r in recs)
print('unique walk ids:', len(walk_ids))

# trigger table ids
trigs = json.load(open(TRIGS))
trig_ids = set(t['id'] for t in trigs)
print('trigger-table ids:', len(trig_ids), ' overlap with walk ids:', len(trig_ids & walk_ids))

# script id space: from the s40 analysis, script ids referenced by the 541
# scripts (callee/owner id pools). Rebuild the referenced-id set from the
# trigger scripts extracted in s33 (picked10/call_log) + the lvc gol table.
# Cheapest sound proxy: the gol.bin state table ids (542 bindings) + trigger
# table ids themselves.
try:
    gol = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/gol_bindings.json'))
    gol_ids = set()
    for b in gol:
        gol_ids.add(b.get('obj')) if isinstance(b, dict) else None
except Exception:
    gol_ids = set()
print('gol ids available:', len(gol_ids))

# token truncation: count [B][i][9f] contiguous runs in the walk toks
toks = json.load(open(TOKS))
print('tok entries:', len(toks))
runs = 0
run_ids = set()
for entry in toks:
    raw = entry[1]
    pairs = raw if raw and isinstance(raw[0], list) and isinstance(raw[0][0], list) else [raw]
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) < 11: continue
        tk = pair[1]
        for i in range(len(tk) - 10):
            if (tk[i][0] == 'B' and tk[i+1][0] == 'i' and
                    all(tk[i+2+k][0] == 'f' for k in range(9))):
                runs += 1
                oid = tk[i+1][3]
                if isinstance(oid, int): run_ids.add(oid)
print('engine-walk [B][i][9f] runs:', runs, 'unique ids:', len(run_ids))
print('walk-run ids that are ALSO trigger-table ids:', len(run_ids & trig_ids))
print('=> pair ceiling (both positioned + id-resolved):',
      len((run_ids | trig_ids) & trig_ids))
