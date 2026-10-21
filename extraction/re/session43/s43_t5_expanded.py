#!/usr/bin/env python3
"""s43 T5: EXPANDED trigger-volume test — all TRS-bearing records (loose scan,
8064 vs s42's 907) spatially joined against ALL 440 triggers; >=100 testable
triggers gate; |half| vs |scale|/2 correlation with same-size-class shuffled null."""
import json
import numpy as np

objs = json.load(open('/tmp/s43_t5_objs.json'))
trigs = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))
print(f'objects: {len(objs)}  triggers: {len(trigs)}')

P = np.array([o['pos'] for o in objs])
S = np.array([o['scale'] for o in objs])
TP = np.array([t['pos'] for t in trigs])
TH = np.array([t['half'] for t in trigs], float)

pad = 0.25
# brute-force spatial join (440 x 8064 = 3.5M checks, vectorized per trigger)
pairs = []
for ti in range(len(trigs)):
    lo = TP[ti] - TH[ti] - pad
    hi = TP[ti] + TH[ti] + pad
    m = np.all((P >= lo) & (P <= hi), axis=1)
    for oi in np.nonzero(m)[0]:
        pairs.append((ti, int(oi)))
print(f'pairs: {len(pairs)} across {len(set(p[0] for p in pairs))} triggers')

# trigger testable = has >=1 pair; the correlation test uses per-(trigger,object)
testable = sorted(set(p[0] for p in pairs))
print(f'testable triggers: {len(testable)} (gate >= 100)')

x = np.array([float(np.abs(TH[ti]).mean()) for ti, oi in pairs])
y = np.array([float(np.abs(S[oi]).mean()) / 2 for ti, oi in pairs])
# correlation in log space (sizes span decades)
lx, ly = np.log10(x + 1e-3), np.log10(y + 1e-3)
if len(x) > 2 and lx.std() > 0 and ly.std() > 0:
    r = float(np.corrcoef(lx, ly)[0, 1])
else:
    r = float('nan')
print(f'pairs={len(x)} log-log corr |half| vs |scale|/2: {r:.4f}')

# same-size-class shuffled null: quantize object scale into classes, shuffle pairing within class
qs = np.round(np.log10(y + 1e-3) * 4).astype(int)  # size classes
classes = {}
for i, c in enumerate(qs):
    classes.setdefault(int(c), []).append(i)
rng = np.random.default_rng(11)
nulls = []
for _ in range(400):
    yp = y.copy()
    for c, idxs in classes.items():
        if len(idxs) > 1:
            yp[idxs] = y[rng.permutation(idxs)]
    if lx.std() > 0 and yp.std() > 0:
        nulls.append(float(np.corrcoef(lx, yp)[0, 1]))
nulls = np.array(nulls)
print(f'null: mean {nulls.mean():.4f} p95 {np.percentile(nulls, 95):.4f} max {nulls.max():.4f}')
print(f'real r {r:.4f} vs null p95 {np.percentile(nulls, 95):.4f} -> '
      f'{"DISCRIMINATES" if r > np.percentile(nulls, 95) else "does NOT discriminate"}')
out = dict(objects=len(objs), triggers=len(trigs), pairs=len(pairs), testable_triggers=len(testable),
           corr=r, null_mean=float(nulls.mean()), null_p95=float(np.percentile(nulls, 95)),
           null_max=float(nulls.max()), verdict=(r > float(np.percentile(nulls, 95))))
json.dump(out, open('/home/z/my-project/scripts/s43_t5_result.json', 'w'), indent=1)
