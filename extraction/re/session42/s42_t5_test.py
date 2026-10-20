#!/usr/bin/env python3
"""S42 T5: per-object trigger-volume test via SPATIAL JOIN.
907 generic-object records ([bool][i32 objId][pos3,rot3,scale3]) captured from
the EXISTING walk token trees (s41's objId+TRS blocker solved without new
emulation). Join: objects whose TRS position lies within trigger pos +- (half +
pad). Test: |trigger.half| vs |object.scale|/2 correlation; NULL: same-scale-class
shuffled pairing (object's scale quantized to a class, pairing shuffled within
class). >=100 pairs -> validated; else 'unvalidated, engine-derived only'."""
import json
import numpy as np

trigs = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))

def scan(tokens, out):
    if not isinstance(tokens, list):
        return
    for i in range(len(tokens) - 10):
        a = tokens[i]; b = tokens[i + 1]
        if (isinstance(a, list) and a and a[0] == 'B' and isinstance(b, list) and b and b[0] == 'i'):
            run = tokens[i + 2:i + 11]
            if all(isinstance(t, list) and t and t[0] == 'f' for t in run):
                out.append((b, run))
    for t in tokens:
        if isinstance(t, list):
            scan(t, out)

recs = []
for f in ['/tmp/my-project/work/s26_v2_GothamCity_toks.json',
          '/tmp/my-project/work/s26_v2_GothamCity_Island2_toks.json']:
    toks = json.load(open(f))
    for t in toks:
        out = []
        scan(t[1] if isinstance(t, list) and len(t) > 1 else t, out)
        for b, run in out:
            recs.append({'walk_id': t[0], 'objId': b[3],
                         'pos': np.array(run[0:3], float) if False else np.array([r[3] for r in run[0:3]], float),
                         'scale': np.array([r[3] for r in run[6:9]], float)})
P = np.array([r['pos'] for r in recs])
S = np.array([r['scale'] for r in recs])
print(f"objects: {len(recs)}; pos range {P.min(0).round(1)} .. {P.max(0).round(1)}")

TP = np.array([t['pos'] for t in trigs])
TH = np.array([t['half'] for t in trigs], float)
TROT = np.array([t['rot'] for t in trigs], float)
rot_small = np.abs(TROT).max() < 1e-6
print(f"triggers: {len(trigs)}; axis-aligned (rot~0): {bool(rot_small)}; half median {np.median(TH, 0)}")

# spatial join (axis-aligned; triggers with small rot treated as AABB, else skip rot)
pad = 0.25
pairs = []
for ti, t in enumerate(trigs):
    d = np.abs(P - TP[ti])
    inside = (d <= TH[ti] + pad).all(1)
    for oi in np.nonzero(inside)[0]:
        pairs.append({'trig_i': ti, 'trig_id': t['id'], 'obj_i': int(oi), 'objId': recs[oi]['objId'],
                      'd': d[oi].tolist()})
n_trig_with = len(set(p['trig_i'] for p in pairs))
print(f"pairs (object inside trigger box +{pad} pad): {len(pairs)} across {n_trig_with} triggers")

# per-object test: |half| vs scale/2 for the NEAREST object per trigger
import collections
nearest = {}
for p in pairs:
    di = max(p['d'])
    if p['trig_i'] not in nearest or di < nearest[p['trig_i']][0]:
        nearest[p['trig_i']] = (di, p['obj_i'])
xs, ys, cls = [], [], []
for ti, (di, oi) in nearest.items():
    hs = float(np.prod(TH[ti]) ** (1 / 3))
    sc = float(np.prod(S[oi]) ** (1 / 3)) / 2
    if hs > 0 and sc > 0:
        xs.append(hs); ys.append(sc)
        cls.append(int(round(np.log2(max(sc, 1e-3)))))   # size class = log2 bucket
    # (xs/ys kept as lists; converted below)
n = len(xs)
print(f"testable pairs (nearest object per trigger): {n}")
if n >= 10:
    xs = np.array(xs, float); ys = np.array(ys, float)
    r = np.corrcoef(np.log(xs), np.log(ys))[0, 1]
    print(f"corr(log half_geom, log scale/2) = {r:.4f}  (n={n})")
    # null: shuffled pairing WITHIN size class
    rng = np.random.RandomState(7)
    bycls = collections.defaultdict(list)
    for i, c in enumerate(cls):
        bycls[c].append(i)
    nulls = []
    for _ in range(200):
        ys2 = ys.copy()
        for c, idxs in bycls.items():
            if len(idxs) > 1:
                ia = np.array(idxs)
                perm = rng.permutation(ia)
                ys2[ia] = ys[perm]
        nulls.append(np.corrcoef(np.log(xs), np.log(ys2))[0, 1])
    nl = np.array(nulls)
    print(f"same-size-class NULL: mean {nl.mean():.4f} std {nl.std():.4f} p95 {np.percentile(nl, 95):.4f}")
    print(f"real r {r:.4f} vs null p95 {np.percentile(nl, 95):.4f} -> "
          f"{'DISCRIMINATES' if r > np.percentile(nl, 95) else 'does NOT discriminate'}")
else:
    print("pairs < 100: keep 'unvalidated, engine-derived only'")

json.dump({'n_objects': len(recs), 'n_pairs_raw': len(pairs), 'n_testable': n,
           'pairs_sample': pairs[:50]}, open('/home/z/my-project/scripts/s42_t5_pairs.json', 'w'), default=str)
print('saved')
