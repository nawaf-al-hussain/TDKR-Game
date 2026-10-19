#!/usr/bin/env python3
"""S39 T5 v2: PROPER permutation test of the state->clip binding table.

For each state class c and its discriminative feature f:
  real mean f(class c bindings)  vs  null = mean f under permuted class labels
  (200 shuffles of the class column over ALL joined bindings with signatures).
A class only 'passes' if its real mean is extreme vs its own permutation null.
Also lists Batman locomotion bindings for the playable-page wiring.
"""
import json
import numpy as np

PAIRS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t4_stateclip_pairs.json'))
SIG = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t3_signatures.json'))['rows']
sig_by_name = {}
for r in SIG:
    sig_by_name.setdefault(r['name'], r)


def classify(state):
    s = state.lower()
    if 'turn' in s or 'rotate' in s:
        return 'turn'
    if any(k in s for k in ('jump', 'leap', 'fall', 'land', 'vault')):
        return 'air'
    if any(k in s for k in ('walk', 'run', 'sprint', 'jog', 'move', 'strafe', 'sneak', 'creep')):
        return 'loco'
    if 'idle' in s:
        return 'idle'
    return None


rows, classes, feats = [], [], []
for p in PAIRS:
    r = sig_by_name.get(p['clip'])
    if r is None or 'xy_rate' not in r or 'zr' not in r or 'yaw_total' not in r:
        continue
    rows.append(r)
    classes.append(classify(p['state']))
    feats.append([r['xy_rate'], r['zr'], abs(r['yaw_total'])])
feats = np.array(feats)
classes = np.array([c if c else 'other' for c in classes])
print(f'joined {len(rows)} bindings with full signatures; class counts:',
      {c: int((classes == c).sum()) for c in set(classes)})

FEAT = {'idle': 0, 'loco': 0, 'turn': 2, 'air': 1}
HIGH = {'idle': False, 'loco': True, 'turn': True, 'air': True}
rng = np.random.default_rng(542)
res = {'joined': len(rows), 'classes': {}}
for c in ['idle', 'loco', 'turn', 'air']:
    fi, hi = FEAT[c], HIGH[c]
    mask = classes == c
    n = int(mask.sum())
    real = float(feats[mask, fi].mean())
    nulls = []
    for _ in range(200):
        perm = rng.permutation(len(rows))
        sel = perm[:n]
        nulls.append(float(feats[sel, fi].mean()))
    # one-sided p: P(null >= real) for HIGH, P(null <= real) else
    if hi:
        p = float(np.mean(np.array(nulls) >= real))
    else:
        p = float(np.mean(np.array(nulls) <= real))
    res['classes'][c] = {'n': n, 'feature': ['xy_rate', 'zr', 'abs_yaw'][fi],
                         'real_mean': round(real, 4),
                         'null_mean': round(float(np.mean(nulls)), 4),
                         'null_p95': round(float(np.percentile(nulls, 95)), 4),
                         'p_value': round(p, 4)}
    print(f"{c:5s} n={n:3d} real {real:9.4f}  null {np.mean(nulls):8.4f} "
          f"(p95 {np.percentile(nulls, 95):8.4f})  p={p:.3f}")

# page wiring candidates: Batman locomotion set
cand = {}
for p in PAIRS:
    st = p['state']
    sl = st.lower()
    if 'bat' not in p['clip'].lower() and 'batman' not in sl:
        continue
    if sl.endswith('idle') or sl == 'idle':
        cand.setdefault('idle', st + ' -> ' + p['clip'])
    if 'walk' in sl and 'to' not in sl:
        cand.setdefault('walk', st + ' -> ' + p['clip'])
    if sl == 'run' or sl.endswith('_run') or sl == 'sprint':
        cand.setdefault('run', st + ' -> ' + p['clip'])
res['page_wiring_candidates'] = cand
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t5_validation.json', 'w'), indent=1)
print('candidates:', json.dumps(cand, indent=1)[:500])
