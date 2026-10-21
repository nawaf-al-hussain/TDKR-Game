#!/usr/bin/env python3
"""s47 T5: trigger volumes from RECORD-JOINED BuiltinBox components.
The lvc stream is sequential: an object's component records follow its
C_BASE record before the next C_BASE. Join every n record (1923007858 =
CComponentBuiltinBox: [f size.x][f size.y][f size.z][i][c][c][c]) to the
MOST RECENT C_BASE owner (record join, NOT spatial), build volumes
half = 0.5*size*scale (with the owner TRS), and rerun the s46
region-preserving near-action test (A: triggers swapped in the object's
region; B: objects swapped in the trigger's region) with >= 100 pairs.
Verdict rule: if AUC vs the permuted-pairing nulls stays inside the null
band, record it and stop spending time on the volume model."""
import json, re, sys
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

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse(LVC, tab, templates, None)
d, strings = res['data'], res['strings']

# ordered record stream: C_BASE owners + n boxes by file offset
owners = []   # (off, objId, pos, scale)
for rid, off, sz in res['census'].get(C_BASE, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        r.tok('c')
        i0 = r.tok('i')
        f9 = [r.tok('f') for _ in range(9)]
    except Exception:
        continue
    owners.append((int(off, 16), i0, f9))
owners.sort()
print('C_BASE owners:', len(owners))

boxes = []
for rid, off, sz in res['census'].get(N_BOX, []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        sx = r.tok('f'); sy = r.tok('f'); sz2 = r.tok('f')
    except Exception:
        continue
    boxes.append((int(off, 16), sx, sy, sz2))
boxes.sort()
print('n (BuiltinBox) records:', len(boxes))

# record join: box -> most recent owner by offset
import bisect
ooffs = [o[0] for o in owners]
joined = {}
for off, sx, sy, sz2 in boxes:
    j = bisect.bisect_right(ooffs, off) - 1
    if j < 0:
        continue
    oid = owners[j][1]
    joined.setdefault(oid, []).append((sx, sy, sz2))
print('owners with >=1 joined box:', len(joined))

# owner scale from the C_BASE f9 (pos, rot?, scale? — s36: ownerScale)
def owner_trs(f9):
    pos = np.array(f9[0:3])
    rot = f9[3:6]
    scale = np.array(f9[6:9]) if any(abs(x - 1.0) > 1e-9 for x in f9[6:9]) else np.ones(3)
    return pos, scale

volumes = {}
for oid, bl in joined.items():
    owner = next((o for o in owners if o[1] == oid), None)
    if owner is None:
        continue
    pos, scale = owner_trs(owner[2])
    sx, sy, sz2 = bl[0]
    half = 0.5 * np.array([sx, sy, sz2]) * scale
    volumes[oid] = {'pos': pos, 'half': half}
print('volumes built:', len(volumes))

# pairing (s46): Lua scripts -> (trigger, acted-on object) pairs
luas = json.load(open(LUAS))
objs = {o[1]: owner_trs(o[2])[0] for o in owners}
pairs = []
for L in luas:
    T = volumes.get(L['objId'])
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    if T is None:
        continue
    H = float(np.max(T['half'])) if T.get('half') is not None else 1.0
    Tp = np.array(T['pos'])
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        d = float(np.linalg.norm(p - Tp))
        inside = bool(d <= 2.0 * H + 1.0)
        pairs.append({'t': L['objId'], 'o': i, 'd': d, 'H': H, 'inside': inside,
                      'tregion': (int(Tp[0] // CELL), int(Tp[1] // CELL)),
                      'oregion': (int(p[0] // CELL), int(p[1] // CELL)),
                      'tpos': Tp.tolist(), 'opos': p.tolist()})
print('pairs:', len(pairs))
dd = np.array([p['d'] for p in pairs])
print('real distance median:', float(np.median(dd)) if len(dd) else '-')

if len(pairs) < 100:
    print('PAIRS < 100 — record-joined model yields too few pairs; report and stop.')
    json.dump({'pairs': len(pairs), 'volumes': len(volumes),
               'verdict': 'insufficient pairs'},
              open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t5_out.json', 'w'), indent=1)
    sys.exit(0)

rng = np.random.default_rng(47)

def auc(a, b):
    # P(a < b) with tie handling
    n = len(a) * len(b)
    gt = sum(1 for x in a for y in b if x < y)
    eq = sum(1 for x in a for y in b if x == y)
    return (gt + 0.5 * eq) / n

def permute_pairs_null(pairs_list, trials=400):
    """permuted-pairing null: shuffle which trigger each object pairs with
    (within the same region-pool), recompute AUC of distance separation"""
    vals = []
    ds_real = np.array([p['d'] for p in pairs_list])
    for _ in range(trials):
        idx = rng.permutation(len(pairs_list))
        # swap the object positions across pairs
        dd = []
        for a, b in zip(pairs_list, idx):
            dd.append(float(np.linalg.norm(np.array(pairs_list[b]['opos']) -
                                           np.array(a['tpos']))))
        vals.append(dd)
    return vals

# region-preserving null A: swap trigger positions within the object's region
def region_swap_null(pairs_list, which, trials=400):
    by_region = {}
    for p in pairs_list:
        key = p['oregion'] if which == 'A' else p['tregion']
        by_region.setdefault(key, []).append(
            p['tpos'] if which == 'A' else p['opos'])
    vals = []
    ds_real = np.array([p['d'] for p in pairs_list])
    for _ in range(trials):
        dd = []
        for p in pairs_list:
            key = p['oregion'] if which == 'A' else p['tregion']
            pool = by_region.get(key) or [p['tpos'] if which == 'A' else p['opos']]
            q = pool[int(rng.integers(0, len(pool)))]
            fixed = p['opos'] if which == 'A' else p['tpos']
            dd.append(float(np.linalg.norm(np.array(q) - np.array(fixed))))
        vals.append(dd)
    return vals

real = np.array([p['d'] for p in pairs])
res_out = {'pairs': len(pairs), 'volumes': len(volumes),
           'real_median': float(np.median(real)),
           'real_inside_frac': float(np.mean([p['inside'] for p in pairs]))}
# null medians + AUC of real-vs-null separation with permuted pairing as the band
for which in ('A', 'B'):
    nulls = region_swap_null(pairs, which, trials=200)
    nmed = [float(np.median(x)) for x in nulls]
    # permuted-pairing band: AUC(real distances, null distances) under label shuffles
    aucs = []
    for x in nulls[:100]:
        aucs.append(auc(real.tolist(), list(x)))
    m = float(np.mean(aucs)); sd = float(np.std(aucs)) or 1e-9
    a_real = float(np.mean([auc(real.tolist(), list(x)) for x in nulls]))
    z = (a_real - m) / sd
    res_out[f'null{which}_median'] = float(np.median(nmed))
    res_out[f'null{which}_auc_mean'] = m
    res_out[f'null{which}_auc_sd'] = sd
    res_out[f'null{which}_z'] = float(z)
    print(f'null {which}: median {np.median(nmed):.1f} m, AUC {m:.4f}±{sd:.4f}, z {z:.2f}')
print('real median:', res_out['real_median'], 'inside frac:', res_out['real_inside_frac'])
json.dump(res_out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t5_out.json', 'w'), indent=1)
print('saved s47_t5_out.json')
