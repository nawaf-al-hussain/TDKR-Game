#!/usr/bin/env python3
"""S40 T2 final: per-object trigger-volume test with the union position table.

Union table = trigger-class records (440, pos+half, from s36) + the [B][i][9f]
TRS token patterns from the pure-parser dumps (GothamCity + Island2, 907 hits)
+ the 0x14CA79-style scan. Reports script-id resolution coverage and runs the
per-object test with same-size-class nulls at >=100 nulls per real pair.
"""
import json, re, random
import numpy as np
from collections import defaultdict

TRIGS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))
by_id = {t['id']: t for t in TRIGS}

# token-table positions (v2 pure-parser dumps, both islands)
tok_pos = {}
for lvl in ('GothamCity', 'GothamCity_Island2'):
    comps = json.load(open(f'/tmp/my-project/work/s26_v2_{lvl}_comps.json'))
    for entry in comps:
        raw = entry[1]
        pairs = raw if raw and isinstance(raw[0], list) and isinstance(raw[0][0], list) else [raw]
        for pair in pairs:
            if not isinstance(pair, list) or len(pair) < 2: continue
            tk = pair[1]
            for i in range(len(tk) - 10):
                if (tk[i][0] == 'B' and tk[i+1][0] == 'i' and
                        all(tk[i+2+k][0] == 'f' for k in range(9))):
                    oid = tk[i+1][3]
                    trs = [tk[i+2+k][3] for k in range(9)]
                    if isinstance(oid, int) and oid >= 100000:
                        tok_pos.setdefault(oid, {'pos': trs[:3], 'rot': trs[3:6],
                                                 'scale': trs[6:9], 'src': lvl + ':tok'})
                    break

# merge: trigger table wins for owners (has half extents); token entries become
# full members with scale-derived half extents (scale x size 0.5 heuristic is
# NOT engine data -> treat token-only objects as position-only, class 'T')
merged = dict(by_id)
for oid, e in tok_pos.items():
    if oid not in merged:
        merged[oid] = dict(e)

SCRIPTS = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
if isinstance(SCRIPTS, dict):
    SCRIPTS = SCRIPTS['all_scripts']
CALL_RE = re.compile(
    r'\b(?:Enable|Disable|ShowObject|HideObject|EnableShowObject|SpawnObject|'
    r'ObjectGetPosition|SetObjectPos|MoveObject|Activate|Deactivate|'
    r'SetObjectVisible|ActorSetState|KillActor|ActorLookTo|SetActorSpeedWalk|'
    r'SetActorSpeedRun|NPCAttackTarget|NPCGoToPath|NPCSetSniper|NPCSetStance|'
    r'StartEventAtObjectNode|HideOccluder|ShowOccluder)\s*\(\s*(\d{5,})', re.I)
pairs = []
for s in SCRIPTS:
    owner = s.get('obj_id')
    if owner is None: continue
    for m in CALL_RE.finditer(s['script']):
        pairs.append((owner, m.group(1), int(m.group(1))))
ref_ids = {a for _, _, a in pairs}
own_ids = {o for o, _, _ in pairs}
print(f'script pairs: {len(pairs)}; unique callees {len(ref_ids)}; unique owners {len(own_ids)}')
print(f'position table: {len(merged)} ids (triggers {len(by_id)}, token-only {len(tok_pos)})')
print(f'callee ids resolving: {len(ref_ids & set(merged))}/{len(ref_ids)}')
print(f'owner ids resolving:  {len(own_ids & set(merged))}/{len(own_ids)}')

# the volume test needs objects with half extents -> trigger-class only
def dn(p, t):
    hx, hy, hz = t['half']
    if hz > 100: hz = 10.0
    return max(abs(p[0]-t['pos'][0])/max(hx,1e-6), abs(p[1]-t['pos'][1])/max(hy,1e-6),
               abs(p[2]-t['pos'][2])/max(hz,1e-6))

seen = set(); real_pairs = []
for o, f, a in pairs:
    if (o, a) in seen: continue
    seen.add((o, a))
    if o in by_id and a in by_id:
        real_pairs.append((o, a))
print(f'real pairs (both trigger-class): {len(real_pairs)}')

smalls = [t for t in TRIGS if max(t.get('scale', [1,1,1])) < 10]
larges = [t for t in TRIGS if max(t.get('scale', [1,1,1])) >= 10]
small_ids = {t['id'] for t in smalls}
def cls(tid): return 'S' if tid in small_ids else 'L'

rng = random.Random(381)
real_dn = []; null_dn = []; ranks = []; inside = 0
pool = {'S': smalls, 'L': larges}
for (o, a) in real_pairs:
    T, O = by_id[o], by_id[a]
    cl = cls(o) if cls(o) == cls(a) else None
    if cl is None: continue
    d_real = dn(O['pos'], T)
    real_dn.append(d_real); 
    if d_real <= 1: inside += 1
    others = [t for t in pool[cl] if t['id'] != o and t['id'] != a]
    samp = rng.sample(others, min(100, len(others)))
    ds = [dn(O['pos'], t) for t in samp]
    null_dn.extend(ds)
    ranks.append((np.sum(np.array(ds) < d_real) + 1) / (len(ds) + 1))

ra = np.array(real_dn); na = np.array(null_dn)
res = {
 'position_table_size': len(merged), 'trigger_table': len(by_id), 'token_only': len(tok_pos),
 'callee_resolved': int(len(ref_ids & set(merged))), 'callee_total': int(len(ref_ids)),
 'owner_resolved': int(len(own_ids & set(merged))), 'owner_total': int(len(own_ids)),
 'real_pairs_both_trigger': len(real_pairs),
 'classified_pairs': len(ra), 'null_samples': len(na),
 'real_inside_rate': float((ra <= 1).mean()) if len(ra) else None,
 'null_inside_rate': float((na <= 1).mean()),
 'real_dn_median': float(np.median(ra)) if len(ra) else None,
 'null_dn_median': float(np.median(na)),
 'rank_median': float(np.median(ranks)) if ranks else None,
 'rank_mean': float(np.mean(ranks)) if ranks else None,
}
print(json.dumps({k: v for k, v in res.items()}, indent=1))
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t2_result.json', 'w'), indent=1)
