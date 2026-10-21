#!/usr/bin/env python3
"""s46 T6: trigger-volume near-action test under STRONGER nulls —
A: triggers swapped within the object's 500 m region (region-preserving)
B: objects swapped within the trigger's 500 m region (region-preserving)
plus fraction-inside (2H+1) under each null. Verdict rule: if the real effect
(AUC vs region nulls) drops to the shuffled-null band, mark the volume model
'unvalidated, engine-derived only'."""
import json, re, sys, math
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
LVC = '/tmp/my-project/work/data/GothamCity.lvc'
VOLS = '/tmp/my-project/work/TDKR-Game/extraction/re/session36_t2_volumes.json'
LUAS = '/tmp/my-project/work/t1_lua_GothamCity.json'
CELL = 500.0

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
    objs[i0] = np.array([f9[0], f9[1], f9[2]])
print('C_BASE object positions:', len(objs))

vols = json.load(open(VOLS))
trigs = {v['id']: v for v in vols}
luas = json.load(open(LUAS))

pairs = []
for L in luas:
    T = trigs.get(L['objId'])
    ids = [int(x) for x in re.findall(r'\((\d{4,7})\)', L['script'])]
    ids = [i for i in set(ids) if i != L['objId']]
    if T is None:
        continue
    H = float(np.max(T['half'])) if T.get('half') else 1.0
    Tp = np.array(T['pos'])
    for i in ids:
        p = objs.get(i)
        if p is None:
            continue
        pairs.append(dict(trigger=L['objId'], obj=i, H=H, tp=Tp, op=p))
print('pairs:', len(pairs))

# region = 500 m grid cell on (x, y)
def cell(p):
    return (int(p[0] // CELL), int(p[1] // CELL))

# index triggers / objects by cell
trig_by_cell = {}
for tid, T in trigs.items():
    if T.get('half'):
        trig_by_cell.setdefault(cell(np.array(T['pos'])), []).append(tid)
obj_by_cell = {}
for oid, p in objs.items():
    obj_by_cell.setdefault(cell(p), []).append(oid)

rng = np.random.default_rng(4646)
dr = np.array([float(np.linalg.norm(p['op'] - p['tp'])) for p in pairs])
dA = np.full(len(pairs), np.nan)
dB = np.full(len(pairs), np.nan)
skA = skB = 0
for j, p in enumerate(pairs):
    co = cell(p['op'])
    cands = [t for t in trig_by_cell.get(co, []) if t != p['trigger']]
    if cands:
        t2 = trigs[rng.choice(cands)]
        dA[j] = float(np.linalg.norm(np.array(t2['pos']) - p['op']))
    else:
        skA += 1
    ct = cell(p['tp'])
    cands2 = [o for o in obj_by_cell.get(ct, []) if o != p['obj']]
    if cands2:
        o2 = objs[rng.choice(cands2)]
        dB[j] = float(np.linalg.norm(p['tp'] - o2))
    else:
        skB += 1
okA = ~np.isnan(dA)
okB = ~np.isnan(dB)
print(f'null A (triggers swapped in object region): {okA.sum()} pairs ({skA} skipped: no other trigger in region)')
print(f'null B (objects swapped in trigger region): {okB.sum()} pairs ({skB} skipped)')

def auc(x, y):
    x, y = np.asarray(x), np.asarray(y)
    return float((x[:, None] < y[None, :]).mean())

def paired_auc(x, y):
    return float((np.asarray(x) < np.asarray(y)).mean())

aucA = paired_auc(dr[okA], dA[okA])
aucB = paired_auc(dr[okB], dB[okB])
# shuffled-assignment z (s45 style) for reference
shuf = np.array([auc(rng.permutation(dr), dr * 0 + np.roll(dr, 1) * 0 + dA[okA][:len(dr)] * 0 + dA[okA][rng.permutation(okA.nonzero()[0].size)] if False else dA[okA]) for _ in range(0)])  # placeholder
# simpler: z vs per-pair null via sign test + null median
print(f'\nREAL median d = {np.median(dr):.1f} m')
print(f'null A median = {np.median(dA[okA]):.1f} m  AUC(real<A) = {aucA:.4f}')
print(f'null B median = {np.median(dB[okB]):.1f} m  AUC(real<B) = {aucB:.4f}')
# null-of-null: shuffle the region-assignment of null A values (rotation test)
za = []
zb = []
for _ in range(200):
    pm = rng.permutation(int(okA.sum()))
    za.append(paired_auc(dr[okA][pm], dA[okA]))
    pm2 = rng.permutation(int(okB.sum()))
    zb.append(paired_auc(dr[okB][pm2], dB[okB]))
za = np.array(za)
print(f'paired-AUC null (permuted pairing): A {za.mean():.4f}+/-{za.std():.4f} (p95 {np.percentile(za, 95):.4f}) -> z_A = {(aucA - za.mean()) / max(za.std(), 1e-9):.2f}')
print(f'                                   B {np.mean(zb):.4f}+/-{np.std(zb):.4f} (p95 {np.percentile(zb, 95):.4f}) -> z_B = {(aucB - np.mean(zb)) / max(np.std(zb), 1e-9):.2f}')

inside_real = float((dr < 2 * np.array([p['H'] for p in pairs]) + 1).mean())
inside_A = float((dA[okA] < 2 * np.array([p['H'] for p in np.array(pairs, dtype=object)[okA]]) + 1).mean())
inside_B = float((dB[okB] < 2 * np.array([p['H'] for p in np.array(pairs, dtype=object)[okB]]) + 1).mean())
print(f'\nfraction inside 2H+1: real {inside_real:.3f} | nullA {inside_A:.3f} | nullB {inside_B:.3f}')

aboveA = aucA > np.percentile(za, 95)
aboveB = aucB > np.percentile(zb, 95)
if aboveA and aboveB:
    verdict = 'WEAKLY VALIDATED (survives region-preserving nulls, effect degraded vs s45 size-class null)'
else:
    verdict = 'UNVALIDATED, engine-derived only (effect shrinks to region nulls)'
print('VERDICT:', verdict)
json.dump({'pairs': int(len(pairs)),
           'real_med': float(np.median(dr)),
           'nullA_med': float(np.median(dA[okA])), 'aucA': aucA,
           'nullB_med': float(np.median(dB[okB])), 'aucB': aucB,
           'nullA_shuffle_mean': float(za.mean()), 'nullA_shuffle_std': float(za.std()),
           'nullA_shuffle_p95': float(np.percentile(za, 95)),
           'z_vs_nullA': float((aucA - za.mean()) / max(za.std(), 1e-9)),
           'z_vs_nullB': float((aucB - np.mean(zb)) / max(np.std(zb), 1e-9)),
           'aucA_paired': aucA, 'aucB_paired': aucB,
           'nullA_pair_mean': float(np.mean(za)), 'nullA_pair_std': float(np.std(za)), 'nullA_pair_p95': float(np.percentile(za, 95)),
           'nullB_pair_mean': float(np.mean(zb)), 'nullB_pair_std': float(np.std(zb)), 'nullB_pair_p95': float(np.percentile(zb, 95)),
           'inside_real': inside_real, 'inside_nullA': inside_A, 'inside_nullB': inside_B,
           'skips': {'A': skA, 'B': skB}, 'verdict': verdict},
          open('/home/z/my-project/scripts/s46_t6_nulls.json', 'w'), indent=1)
