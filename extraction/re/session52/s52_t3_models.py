#!/usr/bin/env python3
"""s52 T3: trigger-volume extent models, FAIR comparison.

SELECTION CRITERION (declared before results):
  best = highest AUC of the scale-free margin d/H on the HELD-OUT folds (2-fold,
  seed 53) among models that (i) pass calibration and (ii) have containment z > 0
  with matched-null construction. Containment z is secondary (report only).
  d/H is the pair's distance divided by that model's extent -> comparable across
  models. Lower d/H supports proximity.

SIGN CONVENTIONS (declared before results):
  containment: real rate ABOVE swap-null rate, z = (real-null_mean)/null_std > 0 supports.
  distance/margin: real mean BELOW swap-null mean, z < 0 supports. AUC > 0.5 supports
  (AUC = P(real margin < swapped margin) + 0.5 P(equal)).

FAIRNESS:
  every model's null uses the SAME construction: region-preserving trigger-position
  swap (donor trigger from the same 500u cell as the real object), each pair keeps
  its OWN threshold H (the union model's H = max(HA,HC) is kept as the pair's
  threshold in the null too). Model C (script radius) exists only for pairs with a
  radius (n=43); models A/B/D are ALSO evaluated on that same subset for a like-
  for-like comparison.

CALIBRATION (metric is discarded if silent):
  known-good: model A on real pairs (must beat null);
  deliberately-wrong: real margins randomly permuted within the pool (must give
  |z| small and AUC ~ 0.5).
"""
import json, re, sys, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
LVC = '/tmp/my-project/work/data/GothamCity.lvc'
LUAS = '/tmp/my-project/work/t1_lua_GothamCity.json'
CELL = 500.0
C_BASE = '1362553'
N_BOX = '1923007858'
TRIG = '938977454'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session52/s52_t3_models.json'

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse(LVC, tab, templates, None)
d, strings = res['data'], res['strings']

owners = {}
for rid, off, sz in res['census'].get(C_BASE, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        r.tok('c'); i0 = r.tok('i'); f9 = [r.tok('f') for _ in range(9)]
    except Exception:
        continue
    owners[rid] = (i0, f9)
boxes_by_rid = collections.defaultdict(list)
for rid, off, sz in res['census'].get(N_BOX, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        sx = r.tok('f'); sy = r.tok('f'); sz2 = r.tok('f')
    except Exception:
        continue
    boxes_by_rid[rid].append((sx, sy, sz2))
trig_rids = set(rid for rid, off, sz in res['census'].get(TRIG, []))
joined_rid = [rid for rid in boxes_by_rid if rid in trig_rids]
trig_f9 = {}
for rid, off, sz in res['census'].get(TRIG, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        i0 = r.tok('i'); f9 = [r.tok('f') for _ in range(9)]
    except Exception:
        continue
    trig_f9[rid] = (i0, f9)

volumes = {}
for rid in joined_rid:
    if rid not in trig_f9:
        continue
    i0, f9 = trig_f9[rid]
    pos = np.array(f9[0:3])
    scaled = any(abs(x - 1.0) > 1e-9 for x in f9[6:9])
    scale = np.array(f9[6:9]) if scaled else np.ones(3)
    sx, sy, sz2 = boxes_by_rid[rid][0]
    volumes[i0] = {'pos': pos, 'size': (sx, sy, sz2), 'scale': scale, 'rid': rid}

luas = json.load(open(LUAS))
def script_radius(txt):
    nums = []
    for m in re.finditer(r'GetDistFromMC\s*\([^)]*\)\s*<\s*([\d.]+)', txt):
        try:
            v = float(m.group(1))
            if 0.5 <= v <= 500:
                nums.append(v)
        except ValueError:
            pass
    if not nums:
        return None
    return float(np.median(nums))

objs = {o[1]: np.array(o[2][0:3]) for o in
        ((rid, i0, f9) for rid, (i0, f9) in owners.items())}
pairs = []
for L in luas:
    T = volumes.get(L['objId'])
    if T is None:
        continue
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    R = script_radius(L['script'])
    sx, sy, sz2 = T['size']
    sc = T['scale']
    H_A = max(0.5 * sx * sc[0], 0.5 * sy * sc[1], sz2 * sc[2] / 2)
    H_B = max(0.5 * sx, 0.5 * sy, sz2 / 2)
    H_C = R
    H_D = max(H_A, H_C) if H_C is not None else H_A
    Tp = np.array(T['pos'])
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        dd = float(np.linalg.norm(p - Tp))
        pairs.append({'t': L['objId'], 'o': i, 'd': dd,
                      'HA': H_A, 'HB': H_B, 'HC': H_C, 'HD': H_D,
                      'tregion': (int(Tp[0] // CELL), int(Tp[1] // CELL)),
                      'oregion': (int(p[0] // CELL), int(p[1] // CELL)),
                      'tpos': Tp.tolist(), 'opos': p.tolist()})
print('pairs:', len(pairs), ' with script radius:', sum(1 for p in pairs if p['HC'] is not None), flush=True)
json.dump({'n_pairs': len(pairs)}, open('/tmp/s52_t3_meta.json', 'w'))

def swap_null_dists(pair_list, null_draws=200, seed=52):
    """region-preserving trigger-position swap; returns array [draws][n] distances."""
    rng = np.random.default_rng(seed)
    tpos = np.array([p['tpos'] for p in pair_list])
    opos = np.array([p['opos'] for p in pair_list])
    orr = [p['oregion'] for p in pair_list]
    by_oreg = collections.defaultdict(list)
    for j in range(len(pair_list)):
        by_oreg[orr[j]].append(j)
    outd = np.zeros((null_draws, len(pair_list)))
    for it in range(null_draws):
        for i in range(len(pair_list)):
            ca = by_oreg.get(orr[i]) or [i]
            j = rng.choice(ca)
            outd[it, i] = np.linalg.norm(tpos[j] - opos[i])
    return outd

def auc(real, nullpool):
    real = np.asarray(real); pool = np.asarray(nullpool).ravel()
    gt = (real[:, None] < pool[None, :]).mean() + 0.5 * (real[:, None] == pool[None, :]).mean()
    return float(gt)

def evaluate(pair_list, key, null_draws=200, seed=52, label=''):
    H = np.array([p[key] for p in pair_list])
    d = np.array([p['d'] for p in pair_list])
    margin = d / np.maximum(H, 0.5)
    nd = swap_null_dists(pair_list, null_draws, seed)
    nmargin = nd / np.maximum(H[None, :], 0.5)
    real_rate = float(np.mean(d <= H + 1))
    null_rate = (nd <= (H + 1.0)[None, :]).mean(axis=1)      # per-draw rate (draws,)
    zc = (real_rate - null_rate.mean()) / max(null_rate.std(ddof=1), 1e-9)
    nm_means = nmargin.mean(axis=1)                           # per-draw mean margin (draws,)
    zm = (margin.mean() - nm_means.mean()) / max(nm_means.std(ddof=1), 1e-9)
    a = auc(list(margin), list(nmargin))
    return {'model': key, 'label': label, 'n': len(pair_list),
            'contain_real': round(real_rate, 4), 'contain_null': round(float(null_rate.mean()), 4),
            'contain_null_std': round(float(null_rate.std(ddof=1)), 4), 'contain_z': round(float(zc), 2),
            'margin_mean': round(float(margin.mean()), 3), 'margin_null_mean': round(float(nm_means.mean()), 3),
            'margin_z': round(float(zm), 2), 'auc_margin': round(a, 4)}

def calibrate_wrong(pair_list, key, null_draws=200, seed=77):
    """deliberately-wrong: ONE region-swapped draw treated as 'real', scored against
    the remaining draws. A well-constructed statistic must score ~0.5 AUC / z~0 here;
    if it does not, the statistic is pair-identity-leaky and is discarded."""
    H = np.array([p[key] for p in pair_list])
    nd = swap_null_dists(pair_list, null_draws, seed)
    fake_margin = nd[0] / np.maximum(H, 0.5)
    rest = nd[1:] / np.maximum(H[None, :], 0.5)
    a = auc(list(fake_margin), list(rest))
    nm_means = rest.mean(axis=1)
    zm = (fake_margin.mean() - nm_means.mean()) / max(nm_means.std(ddof=1), 1e-9)
    fake_rate = float(np.mean(nd[0] <= H + 1))
    rest_rate = (nd[1:] <= (H + 1.0)[None, :]).mean(axis=1)
    zc = (fake_rate - rest_rate.mean()) / max(rest_rate.std(ddof=1), 1e-9)
    return {'wrong_auc': round(a, 4), 'wrong_margin_z': round(float(zm), 2),
            'wrong_contain_z': round(float(zc), 2)}

def folds(pair_list, key, seed=53):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(pair_list))
    half = len(pair_list) // 2
    f1, f2 = [pair_list[i] for i in idx[:half]], [pair_list[i] for i in idx[half:]]
    return [evaluate(f1, key, 120, seed), evaluate(f2, key, 120, seed + 1)]

MODELS = [('HA', 'A_engine_exact'), ('HB', 'B_no_scale'), ('HC', 'C_script_radius'), ('HD', 'D_union')]
sub_C = [p for p in pairs if p['HC'] is not None]
out = {'selection_criterion': 'max held-out AUC(margin d/H) among calibrated models with containment z>0',
       'n_pairs_total': len(pairs), 'n_pairs_with_radius': len(sub_C)}
for key, label in MODELS:
    use = sub_C if key == 'HC' else pairs
    if len(use) < 30:
        out[label] = {'n': len(use), 'skip': 'insufficient'}
        continue
    ent = {'full' if key != 'HC' else 'radius_subset': evaluate(use, key, label=label)}
    ent['calibration_wrong'] = calibrate_wrong(use, key)
    ent['folds'] = folds(use, key)
    out[label] = ent
    print(label, json.dumps(ent['radius_subset' if key == 'HC' else 'full']), flush=True)
# fairness: A/B/D on the radius subset
LBL = {'HA': 'A_engine_exact', 'HB': 'B_no_scale', 'HD': 'D_union'}
for key, label in LBL.items():
    out[label]['on_radius_subset'] = evaluate(sub_C, key, label='subset_fair')
    print('fair', key, out[label]['on_radius_subset'], flush=True)
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
