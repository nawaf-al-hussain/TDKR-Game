#!/usr/bin/env python3
"""s51 T5: alternative trigger-extent models vs the engine-exact construction.
Sign convention (declared before results): for the median-distance statistic,
z < 0 SUPPORTS ownership (real distances smaller than region-preserving swaps).
For containment, REAL rate must exceed the swap-null rate.
Models:
  A engine-exact (s50): half_xy = 0.5*size_xy*scale, height = size_z*scale_z
  B no-scale:           half_xy = 0.5*size_xy,        height = size_z
  C script-radius:      H = the numeric radius argument in the Lua script
    (StartEventAtObjectNode / GetDistFromMC); an AABB around the trigger position
    with that half-extent (the 'AABB + script radius' model of the brief).
Metric: containment rate (d <= H + 1) for REAL vs 200 region-preserving swap
draws (NullA) -> per-model z of the containment rate; plus the s50 median-z
under each model's robust cut."""
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
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t5_models.json'

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
# script radius extraction: numeric args near StartEventAtObjectNode / GetDistFromMC
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
    H_C = R if R is not None else None
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
print('pairs:', len(pairs), ' with script radius:', sum(1 for p in pairs if p['HC'] is not None))
rc = [p['HC'] for p in pairs if p['HC'] is not None]
if rc:
    print('script radius percentiles 50/90/max:', np.percentile(rc, [50, 90]).round(2), round(max(rc), 1))

def containment_z(pair_list, key, null_draws=200, seed=52):
    rng = np.random.default_rng(seed)
    tpos = np.array([p['tpos'] for p in pair_list])
    opos = np.array([p['opos'] for p in pair_list])
    orr = [p['oregion'] for p in pair_list]
    by_oreg = collections.defaultdict(list)
    for j in range(len(pair_list)):
        by_oreg[orr[j]].append(j)
    real = float(np.mean([p['d'] <= p[key] + 1 for p in pair_list]))
    nulls = []
    for it in range(null_draws):
        cnt = 0
        for i in range(len(pair_list)):
            ca = by_oreg.get(orr[i]) or [i]
            j = rng.choice(ca)
            dd = float(np.linalg.norm(tpos[j] - opos[i]))
            if dd <= pair_list[i][key] + 1:
                cnt += 1
        nulls.append(cnt / len(pair_list))
    nm = np.array(nulls)
    z = (real - nm.mean()) / max(nm.std(ddof=1), 1e-9)
    return {'model': key, 'n': len(pair_list), 'real_rate': round(real, 4),
            'null_rate_mean': round(float(nm.mean()), 4), 'null_rate_std': round(float(nm.std(ddof=1)), 4),
            'z': round(float(z), 2)}

out = {'n_pairs': len(pairs)}
pc = [p for p in pairs if p['HC'] is not None]
for key, label in (('HA', 'A_engine_exact'), ('HB', 'B_no_scale'), ('HC', 'C_script_radius'), ('HD', 'D_volume_or_radius')):
    use = pc if key == 'HC' else pairs
    if len(use) < 30:
        out[label] = {'n': len(use), 'skip': 'insufficient'}
        continue
    out[label] = containment_z(use, key)
    print(label, out[label])
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
