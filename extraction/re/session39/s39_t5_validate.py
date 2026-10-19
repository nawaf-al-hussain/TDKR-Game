#!/usr/bin/env python3
"""S39 T5: validate the 542 state->clip bindings against clip root-motion
signatures, per state class, vs shuffled-binding nulls.

Classes from state-name keywords; expectations:
  idle  -> xy_rate ~ 0, small foot range
  loco  -> horizontal travel + alternating feet (lf_rng, foot AC, gait period)
  turn  -> yaw_total high
  air   -> root z range high
"""
import json, re
import numpy as np

PAIRS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t4_stateclip_pairs.json'))
SIG = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t3_signatures.json'))['rows']
sig_by_name = {}
for r in SIG:
    sig_by_name.setdefault(r['name'], r)

NEEDED = {'idle': ['xy_rate', 'zr'], 'loco': ['xy_rate', 'lf_rng', 'lth_per'],
          'turn': ['yaw_total'], 'air': ['zr']}
joined = []
for p in PAIRS:
    st, cl = p['state'], p['clip']
    r = sig_by_name.get(cl)
    if r is None:
        continue
    if any(k not in r for k in NEEDED['idle'] + NEEDED['loco'] + NEEDED['turn'] + NEEDED['air']):
        continue
    joined.append((st, cl, r))
print(f'bindings {len(PAIRS)}, with signatures {len(joined)} '
      f'({len({c for _, c, _ in joined})} unique clips)')


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


EXPECT = {
    'idle': lambda r: r['xy_rate'] < 0.05 and r['zr'] < 0.15,
    'loco': lambda r: r['xy_rate'] > 0.05 or (r['lf_rng'] > 5 and r['lth_per'] > 0),
    'turn': lambda r: abs(r['yaw_total']) > 20,
    'air': lambda r: r['zr'] > 0.2,
}

cls_sets = {}
for st, cl, row in joined:
    c = classify(st)
    if c:
        cls_sets.setdefault(c, []).append((st, cl, row))

rng = np.random.default_rng(542)
res = {'joined': len(joined), 'classes': {}}
for c, items in sorted(cls_sets.items()):
    ok = [EXPECT[c](row) for _, _, row in items]
    rate = float(np.mean(ok))
    # null: shuffle clip assignments within this class (breaks state-clip pairing)
    clips = [cl for _, cl, _ in items]
    null_rates = []
    for _ in range(200):
        perm = rng.permutation(len(items))
        nr = []
        for i, (st, _, _) in enumerate(items):
            nr.append(EXPECT[c](items[perm[i]][2]))
        null_rates.append(float(np.mean(nr)))
    res['classes'][c] = {
        'n': len(items), 'pass_rate': round(rate, 3),
        'null_pass_rate_mean': round(float(np.mean(null_rates)), 3),
        'null_pass_rate_p95': round(float(np.percentile(null_rates, 95)), 3),
        'fails': [{'state': st, 'clip': cl} for (st, cl, row), o in zip(items, ok) if not o][:20]}
    print(f"{c:5s} n={len(items):3d} pass {rate:.3f} vs null {np.mean(null_rates):.3f} "
          f"(p95 {np.percentile(null_rates, 95):.3f})  fails {sum(1 for x in ok) if False else len(res['classes'][c]['fails'])}")

# example bindings wired into the playable page
want = {}
for p in PAIRS:
    st = p['state'].lower()
    if st in ('idle', 'walk', 'run', 'sprint', 'combat_idle') and p['state'] not in want:
        want[p['state']] = p['clip']
res['page_wiring_candidates'] = want
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t5_validation.json', 'w'), indent=1)
print('candidates:', json.dumps(want)[:400])
