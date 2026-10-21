#!/usr/bin/env python3
"""s45 T3b v2: id bridge + near-trigger action test using saved trigger volumes.

Triggers: extraction/re/session36_t2_volumes.json (440: id, pos, rot, scale, half).
Scripts: /tmp/my-project/work/t1_lua_GothamCity.json (437: off, objId, script).
Object positions: C_BASE census class (c,i,9f,...) from the current parse.
Test: d_real (trigger -> objects its script acts on) vs same-size-class null
(other triggers' centers, |log H ratio| <= ln2), >= 100 pairs, effect = AUC +
medians, calibrated against a shuffled-assignment null (200 reps).
"""
import json, re, sys, math
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
LVC = '/tmp/my-project/work/data/GothamCity.lvc'
VOLS = '/tmp/my-project/work/TDKR-Game/extraction/re/session36_t2_volumes.json'
LUAS = '/tmp/my-project/work/t1_lua_GothamCity.json'

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse(LVC, tab, templates, None)
d, strings = res['data'], res['strings']

objs = {}
for rid, off, sz in res['census'].get('1362553', []):
    r = lvc_pure.Reader(d, strings)
    r.p = int(off, 16)
    try:
        r.tok('c')
        i0 = r.tok('i')
        f9 = [r.tok('f') for _ in range(9)]
    except Exception:
        continue
    objs[i0] = [f9[0], f9[1], f9[2]]
print('C_BASE object positions:', len(objs))

vols = json.load(open(VOLS))
trigs = {v['id']: v for v in vols}
print('triggers:', len(trigs))

luas = json.load(open(LUAS))
cov_self = sum(1 for L in luas if L['objId'] in trigs)
pairs = []
n_refs = n_pos = 0
for L in luas:
    T = trigs.get(L['objId'])
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    n_refs += len(ids)
    if T is None:
        continue
    H = float(np.max(T['half'])) if T.get('half') else 1.0
    Tp = np.array(T['pos'])
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        n_pos += 1
        d_real = float(np.linalg.norm(np.array(p) - Tp))
        # same-size-class null: other triggers with |log H ratio| <= ln2
        dnull = []
        for tid2, T2 in trigs.items():
            if tid2 == L['objId'] or not T2.get('half'):
                continue
            H2 = float(np.max(T2['half']))
            if abs(math.log((H2 if H2 else 1e-6) / (H if H else 1e-6))) <= math.log(2.0):
                dnull.append(float(np.linalg.norm(np.array(p) - np.array(T2['pos']))))
        if dnull:
            pairs.append(dict(trigger=L['objId'], obj=i, H=H,
                              d_real=d_real, d_null_med=float(np.median(dnull)),
                              n_null=len(dnull)))

print(f'scripts {len(luas)}, objId in trigger set {cov_self} ({100*cov_self/len(luas):.0f}%), '
      f'acted refs {n_refs}, with TRS pos {n_pos}')
print(f'pairs: {len(pairs)} (gate >= 100)')
out = {'bridge': dict(scripts=len(luas), script_is_trigger=cov_self, acted_refs=n_refs,
                      acted_with_pos=n_pos, triggers=len(trigs), objs=len(objs)),
       'pairs': len(pairs)}
if pairs:
    dr = np.array([p['d_real'] for p in pairs])
    dn = np.array([p['d_null_med'] for p in pairs])
    auc = float((dr < dn).mean())
    rng = np.random.default_rng(7)
    A = np.array([float((dr[rng.permutation(len(dr))] < dn).mean()) for _ in range(200)])
    out.update(d_real_med=float(np.median(dr)), d_null_med=float(np.median(dn)),
               auc=auc, null_mean=float(A.mean()), null_p95=float(np.percentile(A, 95)),
               above_null=bool(auc > np.percentile(A, 95)),
               sample=sorted(pairs, key=lambda p: p['d_real'])[:10])
    print(f'median d_real {np.median(dr):.1f} m | median d_null {np.median(dn):.1f} m | '
          f'AUC {auc:.3f} vs shuffled null {A.mean():.3f} (p95 {np.percentile(A, 95):.3f}) -> '
          f'{"ABOVE NULL" if auc > np.percentile(A, 95) else "WITHIN NULL"}')
json.dump(out, open('/home/z/my-project/scripts/s45_t3_pairs.json', 'w'), indent=1)
print('saved')
