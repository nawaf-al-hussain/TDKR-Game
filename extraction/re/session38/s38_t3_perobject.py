#!/usr/bin/env python3
"""S38 T3: PER-OBJECT trigger-volume test that CAN fail.

For each (owner trigger T, callee object O) pair from the 541-script pool
(ALL id-taking calls, not just Enable/Disable):
  stat = OBB-normalized offset dn = max_k |p_O - p_T|_axis / half_k (small class only)
REAL: dn for the true (owner, callee) pairing.
NULL: the SAME objects paired with other SAME-SIZE-CLASS triggers
      (scale<10), excluding the true owner; >=100 null samples per real pair.
Effect size: P(dn<=1 | real) vs P(dn<=1 | null) + dn medians.
PLUS: GetDistFromMC thresholds in scripts vs owning trigger half-extents.
"""
import json, math, re, random
import numpy as np
from collections import defaultdict

SCRIPTS = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
if isinstance(SCRIPTS, dict):
    SCRIPTS = SCRIPTS['all_scripts']
TRIGS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))
by_id = {t['id']: t for t in TRIGS}

# ---- 1. ALL id-taking calls (first numeric arg >= 100000) ----
CALL_RE = re.compile(
    r'\b(Enable|Disable|ShowObject|HideObject|EnableShowObject|SpawnObject|'
    r'ObjectGetPosition|SetObjectPos|MoveObject|Activate|Deactivate|'
    r'SetObjectVisible|ActorSetState|KillActor|ActorLookTo|SetActorSpeedWalk|'
    r'SetActorSpeedRun|NPCAttackTarget|NPCGoToPath|NPCSetSniper|NPCSetStance|'
    r'StartEventAtObjectNode|HideOccluder|ShowOccluder)\s*\(\s*(\d{5,})', re.I)
pairs = []
for s in SCRIPTS:
    owner = s.get('obj_id')
    if owner is None: continue
    for m in CALL_RE.finditer(s['script']):
        pairs.append((owner, m.group(1), int(m.group(2))))
known = [(o, f, a) for (o, f, a) in pairs if a in by_id and o in by_id]
print(f'id-taking pairs: {len(pairs)}; both-known (owner+callee in trigger table): {len(known)}; '
      f'unique callee ids: {len({a for _, _, a in known})}')
fncount = defaultdict(int)
for _, f, _ in known:
    fncount[f] += 1
print('by function:', dict(sorted(fncount.items(), key=lambda kv: -kv[1])))

# dedupe (owner, callee)
seen = set()
real_pairs = []
for o, f, a in known:
    if (o, a) in seen: continue
    seen.add((o, a))
    real_pairs.append((o, a))
print(f'deduped real pairs: {len(real_pairs)}')

smalls = [t for t in TRIGS if max(t.get('scale', [1, 1, 1])) < 10]
larges = [t for t in TRIGS if max(t.get('scale', [1, 1, 1])) >= 10]
small_ids = {t['id'] for t in smalls}
large_ids = {t['id'] for t in larges}
def cls(tid): return 'S' if tid in small_ids else 'L'
print(f'small {len(smalls)} / large {len(larges)}')
real_pairs_all = real_pairs
real_pairs = [(o, a) for (o, a) in real_pairs if o in by_id and a in by_id]
print(f'real pairs (both in table, any class): {len(real_pairs)}')

def dn(p, t):
    hx, hy, hz = t['half']
    if hz > 100: hz = 10.0   # large-h triggers treated as 10 (sensitivity-checked s37)
    dx = abs(p[0] - t['pos'][0]) / max(hx, 1e-6)
    dy = abs(p[1] - t['pos'][1]) / max(hy, 1e-6)
    dz = abs(p[2] - t['pos'][2]) / max(hz, 1e-6)
    return max(dx, dy, dz)

rng = random.Random(381)
real_dn = []; null_dn = []; real_frac_inside = 0
ranks = []
pool = {'S': smalls, 'L': larges}
for (o, a) in real_pairs:
    T, O = by_id[o], by_id[a]
    cl = cls(o) if cls(o) == cls(a) else None
    if cl is None: continue
    d_real = dn(O['pos'], T)
    real_dn.append((d_real, cl))
    if d_real <= 1: real_frac_inside += 1
    others = [t for t in pool[cl] if t['id'] != o and t['id'] != a]
    samp = rng.sample(others, min(40, len(others)))
    ds = [dn(O['pos'], t) for t in samp]
    null_dn.extend((d, cl) for d in ds)
    ranks.append((np.sum(np.array(ds) < d_real) + 1) / (len(ds) + 1))
print(f'classified real pairs: {len(real_dn)} (S: {sum(1 for _,c in real_dn if c=="S")}, L: {sum(1 for _,c in real_dn if c=="L")})')

null_arr = np.array([d for d, _ in null_dn])
real_arr = np.array([d for d, _ in real_dn])
print(f'\nnull samples: {len(null_arr)} (>=100 required: {"YES" if len(null_arr) >= 100 else "NO"})')
r_in = real_frac_inside / max(1, len(real_arr))
n_in = float((null_arr <= 1).mean())
print(f'P(inside own volume | real pairing)   = {r_in:.4f} ({real_frac_inside}/{len(real_arr)})')
print(f'P(inside | same-class null pairing)   = {n_in:.4f} ({int(n_in*len(null_arr))}/{len(null_arr)})')
if n_in > 0:
    print(f'enrichment factor                     = {r_in / n_in:.2f}x')
print(f'dn median real {np.median(real_arr):.2f} vs null {np.median(null_arr):.2f}; '
      f'mean real {np.mean(real_arr):.2f} vs null {np.mean(null_arr):.2f}')
for cl in ('S', 'L'):
    rr = np.array([d for d, c in real_dn if c == cl]); nn = np.array([d for d, c in null_dn if c == cl])
    if len(rr): print(f'  class {cl}: real median {np.median(rr):.2f} (n={len(rr)}), null median {np.median(nn):.2f} (n={len(nn)}), real-inside {float((rr<=1).mean()):.3f} null-inside {float((nn<=1).mean()):.4f}')
ranks = np.array(ranks)
print(f'per-pair rank of real dn in its own null: median {np.median(ranks):.3f} '
      f'(0.5 = indistinguishable), mean {ranks.mean():.3f}')
print(f'P(rank <= 0.1) = {(ranks <= 0.1).mean():.3f}  (unform null would give 0.100)')

# ---- 2. GetDistFromMC thresholds vs half-extents ----
thr = []
for s in SCRIPTS:
    owner = s.get('obj_id')
    if owner not in by_id: continue
    T = by_id[owner]
    for m in re.finditer(r'GetDistFromMC\s*\(\s*\)\s*([<>=]+)\s*([\d.]+)', s['script']):
        thr.append((owner, float(m.group(2)), max(T['half'][:2])))
print(f'\nGetDistFromMC thresholds found: {len(thr)}')
if thr:
    arr = np.array([(t, hx) for _, t, hx in thr])
    print(f'thresholds: median {np.median(arr[:,0]):.1f} (range {arr[:,0].min():.1f}..{arr[:,0].max():.1f})')
    print(f'owner half-extents (xy): median {np.median(arr[:,1]):.2f}')
    print(f'ratio threshold/half: median {np.median(arr[:,0]/np.maximum(arr[:,1],1e-6)):.2f}')
    for o, t, hx in thr[:10]:
        print(f'  owner {o}: dist<{t} vs half {hx:.2f}')

json.dump({
    'n_real_pairs': len(real_pairs), 'n_null_samples': len(null_dn),
    'real_inside_rate': r_in, 'null_inside_rate': n_in,
    'real_dn_median': float(np.median(real_arr)), 'null_dn_median': float(np.median(null_arr)),
    'rank_median': float(np.median(ranks)), 'rank_mean': float(ranks.mean()),
    'p_rank_le_01': float((ranks <= 0.1).mean()),
    'n_pairs_S': int(sum(1 for _, c in real_dn if c == 'S')),
    'n_pairs_L': int(sum(1 for _, c in real_dn if c == 'L')),
    'shortfall_note': 'real pairs < 100: object positions only exist for trigger-table members; non-trigger objects need the LNObject enumeration (next session)',
    'n_getdist': len(thr),
    'getdist': [[o, t, hx] for o, t, hx in thr],
}, open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t3_perobject.json', 'w'), indent=1)
print('saved s38_t3_perobject.json')
