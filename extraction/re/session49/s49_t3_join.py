#!/usr/bin/env python3
"""s49 T3: reconcile 389-vs-0 and rerun the s46 region-preserving test on the
CENSUS-RID join (component census rid == owning template record id — the same
owner-rid semantics s33 used; s47's offset-join and byte-pattern searches used
different definitions). Volumes: half = 0.5*size*scale at the owner TRS."""
import json, re, sys, bisect
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

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse(LVC, tab, templates, None)
d, strings = res['data'], res['strings']

# owner TRS per C_BASE record id
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

# census-rid join: BuiltinBox components whose owning record ALSO has a trigger
boxes_by_rid = collections.defaultdict(list) if False else {}
import collections
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
print('BuiltinBox components:', sum(len(v) for v in boxes_by_rid.values()),
      'owners:', len(boxes_by_rid))
print('trigger components:', len(trig_rids))
print('CENSUS-RID join (owner has both BuiltinBox and trigger):', len(joined_rid))
# tid histogram of the joined owners
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
tids = collections.Counter(hex(tid_of.get(r, -1)) for r in joined_rid)
print('joined owner tids:', dict(tids))

# volumes through the join that works
def owner_trs(f9):
    pos = np.array(f9[0:3])
    scale = np.array(f9[6:9]) if any(abs(x-1.0) > 1e-9 for x in f9[6:9]) else np.ones(3)
    return pos, scale

# volumes from the TRIGGER's own f9 (the 0x264b record carries trigger TRS itself;
# the C_BASE is a separate record — trig & cbase = 0 — so s33's trs_pos(rid) path
# never applied here; the trigger f9 = [pos3, rot3, scale3] per the s24/s33 reads)
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
    scale = np.array(f9[6:9]) if any(abs(x-1.0) > 1e-9 for x in f9[6:9]) else np.ones(3)
    sx, sy, sz2 = boxes_by_rid[rid][0]
    volumes[i0] = {'pos': pos, 'half': 0.5*np.array([sx, sy, sz2])*scale,
                   'yaw': f9[5], 'rid': rid}
print('volumes:', len(volumes))
szs = np.array([np.prod(v['half'])*8 for v in volumes.values()])
print('volume size percentiles (5/50/95):', np.percentile(szs, [5, 50, 95]).round(2))

# Lua pairing (same as s47/s46 design)
luas = json.load(open(LUAS))
objs = {o[1]: owner_trs(o[2])[0] for o in
        ((rid, i0, f9) for rid, (i0, f9) in owners.items())}
pairs = []
for L in luas:
    T = volumes.get(L['objId'])
    if T is None:
        continue
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    Tp = np.array(T['pos'])
    H = float(np.max(T['half']))
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        dd = float(np.linalg.norm(p-Tp))
        pairs.append({'t': L['objId'], 'o': i, 'd': dd, 'H': H,
                      'tregion': (int(Tp[0]//CELL), int(Tp[1]//CELL)),
                      'oregion': (int(p[0]//CELL), int(p[1]//CELL)),
                      'tpos': Tp.tolist(), 'opos': p.tolist()})
# robustness: drop the top-5% largest volumes (garbage extents)
import copy
pairs_all = pairs
Hs = [p['H'] for p in pairs_all]
hcut = float(np.percentile(Hs, 95))
pairs = [p for p in pairs_all if p['H'] <= hcut]
print('Lua pairs (H<=%.1f): %d of %d' % (hcut, len(pairs), len(pairs_all)))
if pairs:
    dd = np.array([p['d'] for p in pairs])
    print('real distance median:', round(float(np.median(dd)), 1),
          'inside 2H+1:', sum(1 for p in pairs if p['d'] <= 2*p['H']+1), '/', len(pairs))

def auc(a, b):
    n = len(a)*len(b)
    gt = sum(1 for x in a for y in b if x < y)
    eq = sum(1 for x in a for y in b if x == y)
    return (gt + 0.5*eq)/n

if len(pairs) >= 100:
    rng = np.random.default_rng(49)
    dd = np.array([p['d'] for p in pairs])
    tr = [p['tregion'] for p in pairs]
    orr = [p['oregion'] for p in pairs]
    tpos = np.array([p['tpos'] for p in pairs])
    opos = np.array([p['opos'] for p in pairs])
    # null A: triggers swapped within the object's region
    nullA = []
    for it in range(200):
        ds = []
        for i in range(len(pairs)):
            cand = [j for j in range(len(pairs)) if tr[j] == orr[i]]
            if not cand:
                continue
            j = cand[rng.integers(len(cand))]
            ds.append(np.linalg.norm(tpos[j]-opos[i]))
        nullA.append(float(np.median(ds)))
    # null B: objects swapped within the trigger's region
    nullB = []
    for it in range(200):
        ds = []
        for i in range(len(pairs)):
            cand = [j for j in range(len(pairs)) if orr[j] == tr[i]]
            if not cand:
                continue
            j = cand[rng.integers(len(cand))]
            ds.append(np.linalg.norm(tpos[i]-opos[j]))
        nullB.append(float(np.median(ds)))
    real_med = float(np.median(dd))
    nA = np.array(nullA); nB = np.array(nullB)
    aucA = auc([real_med], nA.tolist())
    aucB = auc([real_med], nB.tolist())
    zA = (real_med-nA.mean())/max(nA.std(ddof=1), 1e-9)
    zB = (real_med-nB.mean())/max(nB.std(ddof=1), 1e-9)
    frac_in = float(np.mean([p['d'] <= 2*p['H']+1 for p in pairs]))
    print('region-preserving test: real median %.1f | nullA %.1f+/-%.1f (z %.2f) | '
          'nullB %.1f+/-%.1f (z %.2f) | frac inside %.3f' %
          (real_med, nA.mean(), nA.std(), zA, nB.mean(), nB.std(), zB, frac_in))
    out = {'joined_rid': len(joined_rid), 'volumes': len(volumes), 'pairs': len(pairs),
           'real_median': real_med, 'nullA_mean': float(nA.mean()),
           'nullA_std': float(nA.std()), 'zA': float(zA),
           'nullB_mean': float(nB.mean()), 'nullB_std': float(nB.std()), 'zB': float(zB),
           'frac_inside': frac_in}
else:
    out = {'joined_rid': len(joined_rid), 'volumes': len(volumes), 'pairs': len(pairs),
           'verdict': 'insufficient pairs'}
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t3_test.json', 'w'), indent=1)
print('saved s49_t3_test.json')
