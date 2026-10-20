#!/usr/bin/env python3
"""S40 T4: per-binding test of the six locomotion state->clip bindings.

The rig is IN-PLACE (root xy_rate ~ 0 for all bat loco clips) — root travel
cannot discriminate; use FK gait metrics per clip: foot ranges (lf_rng/rf_rng),
gait periodicity (lf_ac/rf_ac autocorrelation), thigh periodicity (lth_ac),
vertical motion (zr).

Name-keyed expectations (one-sided):
  Idle            -> minimal foot motion (low lf_rng)
  Idle_to_Walk    -> gait present but smaller than run transitions
  Walk            -> periodic gait (high lf_ac), moderate foot range
  Walk_to_Run     -> periodic gait, larger foot range than walk
  Run             -> strong periodicity, largest foot range
  Run_to_Idle     -> gait present, decaying (between walk and idle)
Null per binding: rank of the bound clip within ALL bat_* clips (shuffled
binding = random clip), one-sided in the expected direction.
"""
import json
import numpy as np

SIG = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t3_signatures.json'))['rows']
sig = {r['name']: r for r in SIG}
bat = [r for r in SIG if r['name'].startswith('_') and 'bat' in r['name']]
print(f'bat clips with signatures: {len(bat)}')

BINDINGS = [
    # (state, clip, source, expected-direction on (lf_rng, lf_ac), note)
    ('Idle',         '_001_idle_stand', 'embedded', 'min-lf_rng'),
    ('Idle_to_Walk', '_559_bat_idle_to_walk', 'gol', 'mid lf_rng, gait rising'),
    ('Walk',         '_007_walk', 'embedded', 'periodic, mid lf_rng'),
    ('Walk_to_Run',  '_564_bat_walk_to_run', 'gol', 'periodic, > walk lf_rng'),
    ('Run',          '_008_run', 'embedded', 'max periodicity + lf_rng'),
    ('Run_to_Idle',  '_562_bat_run_to_idle', 'gol', 'gait decaying'),
]

feats = np.array([[r.get('lf_rng', 0) or 0, r.get('rf_rng', 0) or 0,
                   r.get('lf_ac', 0) or 0, r.get('rf_ac', 0) or 0,
                   r.get('lth_ac', 0) or 0, r.get('zr', 0) or 0] for r in bat])
names = [r['name'] for r in bat]
print('null distribution (bat clips): lf_rng p10/50/90 =',
      np.percentile(feats[:, 0], [10, 50, 90]).round(3),
      'lf_ac p10/50/90 =', np.percentile(feats[:, 2], [10, 50, 90]).round(3),
      'zr p10/50/90 =', np.percentile(feats[:, 5], [10, 50, 90]).round(3))

EXPECT = {  # one-sided metric, direction
    'Idle':         ('lf_rng', 'low'),
    'Idle_to_Walk': ('lf_rng', 'mid'),
    'Walk':         ('lf_ac', 'high'),
    'Walk_to_Run':  ('lf_ac', 'high'),
    'Run':          ('lf_rng', 'high'),
    'Run_to_Idle':  ('lf_rng', 'mid'),
}
COL = {'lf_rng': 0, 'rf_rng': 1, 'lf_ac': 2, 'rf_ac': 3, 'lth_ac': 4, 'zr': 5}

results = {}
for state, clip, src, note in BINDINGS:
    r = sig.get(clip)
    if r is None:
        print(f'{state:14s} -> {clip:28s} : NO SIGNATURE (embedded GLB clip, not in gol sig table)')
        results[state] = {'clip': clip, 'src': src, 'sig': None}
        continue
    col, direction = EXPECT[state]
    v = r.get(col, 0) or 0
    arr = feats[:, COL[col]]
    rank_lo = (arr < v).sum() / len(arr)   # fraction of nulls below
    if direction == 'low':
        p = rank_lo
    elif direction == 'high':
        p = 1 - (arr <= v).sum() / len(arr)
    else:  # mid: two-sided distance from median rank 0.5 — report only
        p = None
    zr = r.get('zr', 0)
    print(f'{state:14s} -> {clip:28s} {src:8s} {col}={v:.4f} ({direction}) '
          f'rank={rank_lo:.3f} {"p=" + format(p, ".3f") if p is not None else "mid"} zr={zr:.4f} '
          f'lf_ac={r.get("lf_ac", 0):.3f} rf_rng={r.get("rf_rng", 0):.4f}')
    results[state] = {'clip': clip, 'src': src, col: v, 'direction': direction,
                      'rank_below': float(rank_lo), 'p_extreme': None if p is None else float(p),
                      'zr': float(zr), 'lf_ac': float(r.get('lf_ac', 0) or 0),
                      'lf_rng': float(r.get('lf_rng', 0) or 0), 'rf_rng': float(r.get('rf_rng', 0) or 0)}

json.dump(results, open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t4_bindings.json', 'w'), indent=1)
print('\nnote: embedded GLB clips (_001/_007/_008) have no gol signatures — their FK'
      ' gait metrics come from the browser page (s39 FK parity).')
