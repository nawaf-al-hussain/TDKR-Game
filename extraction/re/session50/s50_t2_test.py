#!/usr/bin/env python3
"""s50 T2: trigger-volume statistic — sign, meaning, and controls.

STATISTIC (exact): population = Lua-paired (trigger, object) pairs; each pair's
d = |obj_CBASE_TRS_pos - trigger_TRS_pos|. REAL = median(d). NullA: swap the
TRIGGER position across pairs within the object's 500 m region cell; NullB: swap
the OBJECT position within the trigger's region cell; 200 draws each.
z = (real - mean(null medians)) / std(null medians).
SIGN CONVENTION: z < 0 (real distances SMALLER than region-preserving random
pairing) SUPPORTS the ownership model; z ~ 0 = no signal; z > 0 = anti-support.

CONTROLS:
  POS+: synthetic objects sampled uniformly INSIDE their own engine-exact volume
        -> z must be strongly negative (the statistic must move the supportive
        direction for a known-correct pairing).
  NEG1: objects = uniform random over the trigger-position AABB -> z ~ 0.
  NEG2: objects = their real position but paired with a RANDOM OTHER trigger's
        position from the same region (equivalent to the null) -> z ~ 0.

VOLUMES (engine convention, s24/s33 + CTriggerShapeAABB):
  half_xy = 0.5 * BuiltinBox.size_xy * owner_scale_xy ; z-height = size_z * scale_z
  (BuiltinBox size is a FULL size; the trigger AABB halves x/y, z is a height).
  Report half-extent distribution; robust restriction drops the top-5% volumes.
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
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t2_test.json'

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse(LVC, tab, templates, None)
d, strings = res['data'], res['strings']

owners = {}
for rid, off, sz in res['census'].get(C_BASE, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        r.tok('c')
        i0 = r.tok('i')
        f9 = [r.tok('f') for _ in range(9)]
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
        i0 = r.tok('i')
        f9 = [r.tok('f') for _ in range(9)]
    except Exception:
        continue
    trig_f9[rid] = (i0, f9)

volumes = {}
for rid in joined_rid:
    if rid not in trig_f9:
        continue
    i0, f9 = trig_f9[rid]
    pos = np.array(f9[0:3])
    scale = np.array(f9[6:9]) if any(abs(x - 1.0) > 1e-9 for x in f9[6:9]) else np.ones(3)
    sx, sy, sz2 = boxes_by_rid[rid][0]
    volumes[i0] = {'pos': pos,
                   'half_xy': 0.5 * np.array([sx, sy]) * scale[:2],
                   'height': sz2 * scale[2],
                   'rid': rid}
print('volumes (engine-exact):', len(volumes))
Hs_all = np.array([max(v['half_xy'][0], v['half_xy'][1], v['height'] / 2) for v in volumes.values()])
print('half-extent percentiles (50/90/99/max):',
      np.percentile(Hs_all, [50, 90, 99]).round(2), round(float(Hs_all.max()), 1))
volsz = np.array([2 * v['half_xy'][0] * 2 * v['half_xy'][1] * v['height'] for v in volumes.values()])
print('volume size percentiles (50/95/max):', np.percentile(volsz, [50, 95]).round(1), round(float(volsz.max()), 1))

luas = json.load(open(LUAS))
objs = {o[1]: np.array(o[2][0:3]) for o in
        ((rid, i0, f9) for rid, (i0, f9) in owners.items())}
pairs = []
for L in luas:
    T = volumes.get(L['objId'])
    if T is None:
        continue
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    Tp = np.array(T['pos'])
    H = float(max(T['half_xy'][0], T['half_xy'][1], T['height'] / 2))
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        dd = float(np.linalg.norm(p - Tp))
        pairs.append({'t': L['objId'], 'o': i, 'd': dd, 'H': H,
                      'tregion': (int(Tp[0] // CELL), int(Tp[1] // CELL)),
                      'oregion': (int(p[0] // CELL), int(p[1] // CELL)),
                      'tpos': Tp.tolist(), 'opos': p.tolist()})
Hs = [p['H'] for p in pairs]
hcut = float(np.percentile(Hs, 95))
pairs_all = pairs
pairs = [p for p in pairs_all if p['H'] <= hcut]
print('Lua pairs (H<=%.1f): %d of %d' % (hcut, len(pairs), len(pairs_all)))

def run_test(pair_list, label):
    if len(pair_list) < 100:
        return {'label': label, 'verdict': 'insufficient pairs', 'n': len(pair_list)}
    rng = np.random.default_rng(50)
    dd = np.array([p['d'] for p in pair_list])
    tr = [p['tregion'] for p in pair_list]
    orr = [p['oregion'] for p in pair_list]
    tpos = np.array([p['tpos'] for p in pair_list])
    opos = np.array([p['opos'] for p in pair_list])
    by_oreg = collections.defaultdict(list)
    by_treg = collections.defaultdict(list)
    for j in range(len(pair_list)):
        by_oreg[orr[j]].append(j)
        by_treg[tr[j]].append(j)
    nullA, nullB = [], []
    for it in range(200):
        dsA, dsB = [], []
        for i in range(len(pair_list)):
            ca = by_oreg.get(orr[i]) or [i]
            dsA.append(np.linalg.norm(tpos[rng.choice(ca)] - opos[i]))
            cb = by_treg.get(tr[i]) or [i]
            dsB.append(np.linalg.norm(tpos[i] - opos[rng.choice(cb)]))
        nullA.append(float(np.median(dsA)))
        nullB.append(float(np.median(dsB)))
    real = float(np.median(dd))
    nA = np.array(nullA); nB = np.array(nullB)
    zA = (real - nA.mean()) / max(nA.std(ddof=1), 1e-9)
    zB = (real - nB.mean()) / max(nB.std(ddof=1), 1e-9)
    frac_in = float(np.mean([p['d'] <= 2 * p['H'] + 1 for p in pair_list]))
    print('%-16s n=%d real %.1f | nullA %.1f+/-%.1f zA %+.2f | nullB %.1f+/-%.1f zB %+.2f | inside %.3f'
          % (label, len(pair_list), real, nA.mean(), nA.std(), zA, nB.mean(), nB.std(), zB, frac_in))
    return {'label': label, 'n': len(pair_list), 'real_median': real,
            'nullA_mean': float(nA.mean()), 'nullA_std': float(nA.std()), 'zA': float(zA),
            'nullB_mean': float(nB.mean()), 'nullB_std': float(nB.std()), 'zB': float(zB),
            'frac_inside': frac_in}

results = {}
results['real_robust'] = run_test(pairs, 'REAL(robust)')
results['real_all'] = run_test(pairs_all, 'REAL(all)')

# ---- POS+: synthetic objects INSIDE their own volume (engine-exact box, yaw ignored
# for the synthetic draw; the real test's distance is position-to-position anyway)
rng = np.random.default_rng(51)
syn = []
for p in pairs:
    T = volumes[p['t']]
    a = rng.uniform(0, 2 * np.pi)
    rx = rng.uniform(0, 1) * T['half_xy'][0]
    ry = rng.uniform(0, 1) * T['half_xy'][1]
    off = np.array([rx * np.cos(a) - ry * np.sin(a), rx * np.sin(a) + ry * np.cos(a),
                    rng.uniform(-0.5, 0.5) * T['height']])
    q = np.array(T['pos']) + off
    syn.append({'t': p['t'], 'd': float(np.linalg.norm(q - np.array(T['pos']))),
                'H': p['H'],
                'tregion': p['tregion'], 'oregion': (int(q[0] // CELL), int(q[1] // CELL)),
                'tpos': T['pos'], 'opos': q.tolist()})
results['pos_inside'] = run_test(syn, 'POS+ inside')

# ---- NEG1: uniform random objects over the trigger AABB
tp_all = np.array([p['tpos'] for p in pairs])
lo = tp_all.min(axis=0); hi = tp_all.max(axis=0)
neg1 = []
for p in pairs:
    q = np.array([rng.uniform(lo[k], hi[k]) for k in range(2)] + [p['tpos'][2]])
    neg1.append({'t': p['t'], 'd': float(np.linalg.norm(q - np.array(p['tpos']))),
                 'H': p['H'], 'tregion': p['tregion'],
                 'oregion': (int(q[0] // CELL), int(q[1] // CELL)),
                 'tpos': p['tpos'], 'opos': q.tolist()})
results['neg_random_obj'] = run_test(neg1, 'NEG1 random')

# ---- NEG2: real objects, random OTHER trigger position from the same region
neg2 = []
for i, p in enumerate(pairs):
    cand = [j for j in range(len(pairs)) if pairs[j]['tregion'] == p['oregion'] and j != i]
    if not cand:
        cand = [i]
    j = int(rng.choice(cand))
    neg2.append({'t': p['t'], 'd': float(np.linalg.norm(np.array(pairs[j]['tpos']) - np.array(p['opos']))),
                 'H': p['H'], 'tregion': p['tregion'], 'oregion': p['oregion'],
                 'tpos': pairs[j]['tpos'], 'opos': p['opos']})
results['neg_wrong_trigger'] = run_test(neg2, 'NEG2 wrongtrig')

results['volume_stats'] = {
    'half_xy_p50': float(np.percentile([max(v['half_xy']) for v in volumes.values()], 50)),
    'half_xy_p95': float(np.percentile([max(v['half_xy']) for v in volumes.values()], 95)),
    'half_xy_max': float(max(max(v['half_xy']) for v in volumes.values())),
    'height_p95': float(np.percentile([v['height'] for v in volumes.values()], 95)),
    'convention': 'half_xy = 0.5*size_xy*scale_xy; z-height = size_z*scale_z (BuiltinBox size is FULL; CTriggerShapeAABB halves x/y, z as height)'}
json.dump(results, open(OUT, 'w'), indent=1)
print('saved', OUT)
print('SIGN: z<0 supports ownership; POS+ must be z<0; NEG1/NEG2 must be z~0')
