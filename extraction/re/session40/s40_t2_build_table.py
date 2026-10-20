#!/usr/bin/env python3
"""S40 T2: build the objId -> position table from the pure parser's component
tokens (CComponentBase::Load pattern [bool][i32 objId][9 floats TRS]),
report resolution coverage for script-referenced ids."""
import json, re
import numpy as np

def scan(level):
    toks = json.load(open(f'/tmp/my-project/work/s26_v2_{level}_toks.json'))
    comps = json.load(open(f'/tmp/my-project/work/s26_v2_{level}_comps.json'))
    # comps: [compId, [[tag, classId], tokens]]  (tokens = same as toks[compId-1][1])
    pat_rows = []
    class_hist = {}
    for entry in comps:
        cid = entry[0]
        raw = entry[1]
        # normalize: raw is either [pair] or a list of pairs; pair = [tag+id, tokens]
        pairs = raw if raw and isinstance(raw[0], list) and isinstance(raw[0][0], list) else [raw]
        for pair in pairs:
            if not isinstance(pair, list) or len(pair) < 2:
                continue
            cls, tk = pair[0], pair[1]
            for i in range(len(tk) - 10):
                if (tk[i][0] == 'B' and tk[i+1][0] == 'i' and
                        all(tk[i+2+k][0] == 'f' for k in range(9))):
                    objid = tk[i+1][3]
                    trs = [tk[i+2+k][3] for k in range(9)]
                    pat_rows.append((cid, cls, objid, trs))
                    class_hist[(cls[0], cls[1])] = class_hist.get((cls[0], cls[1]), 0) + 1
    print(f'{level}: components {len(comps)}, [B][i][9f] pattern hits: {len(pat_rows)}')
    print('  by class:', sorted(class_hist.items(), key=lambda kv: -kv[1])[:8])
    ids = np.array([r[2] for r in pat_rows if isinstance(r[2], int)])
    if len(ids):
        print(f'  objid range: {ids.min()}..{ids.max()}, unique {len(set(ids.tolist()))}')
        big = (ids >= 100000).mean()
        print(f'  frac >= 100000: {big:.3f}')
    # position sanity: p95 of |x|,|y|
    P = np.array([r[3][:3] for r in pat_rows if isinstance(r[2], int)], float)
    if len(P):
        print('  |x| p50/p95:', np.percentile(np.abs(P[:, 0]), [50, 95]).round(1),
              '|y| p50/p95:', np.percentile(np.abs(P[:, 1]), [50, 95]).round(1),
              '|z| p50/p95:', np.percentile(np.abs(P[:, 2]), [50, 95]).round(1))
    return pat_rows

rows_g = scan('GothamCity')
rows_i = scan('GothamCity_Island2')

# script-referenced ids
SCRIPTS = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
if isinstance(SCRIPTS, dict):
    SCRIPTS = SCRIPTS['all_scripts']
CALL_RE = re.compile(
    r'\b(?:Enable|Disable|ShowObject|HideObject|EnableShowObject|SpawnObject|'
    r'ObjectGetPosition|SetObjectPos|MoveObject|Activate|Deactivate|'
    r'SetObjectVisible|ActorSetState|KillActor|ActorLookTo|SetActorSpeedWalk|'
    r'SetActorSpeedRun|NPCAttackTarget|NPCGoToPath|NPCSetSniper|NPCSetStance|'
    r'StartEventAtObjectNode|HideOccluder|ShowOccluder)\s*\(\s*(\d{5,})', re.I)
ref_ids = set()
owners = set()
for s in SCRIPTS:
    if s.get('obj_id') is not None:
        owners.add(s['obj_id'])
    for m in CALL_RE.finditer(s['script']):
        ref_ids.add(int(m.group(1)))
print(f'\nscripts: {len(SCRIPTS)}, owner ids: {len(owners)}, callee-referenced ids: {len(ref_ids)}')
table_ids = {r[2] for r in rows_g + rows_i if isinstance(r[2], int)}
print('unique ids in token table:', len(table_ids))
print('callee ids resolving in token table:', len(ref_ids & table_ids), '/', len(ref_ids))
print('owner ids resolving in token table:', len(owners & table_ids), '/', len(owners))
json.dump({'n_pattern_hits': len(rows_g) + len(rows_i),
           'unique_ids': len(table_ids),
           'callee_resolved': len(ref_ids & table_ids), 'callee_total': len(ref_ids),
           'owner_resolved': len(owners & table_ids), 'owner_total': len(owners)},
          open('/home/z/my-project/scripts/s40_t2_cov.json', 'w'), indent=1)
