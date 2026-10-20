#!/usr/bin/env python3
"""S41 T4: ghost vs ground-only vs full collision on the s40 40 same-region
routes; blocking-triangle classification for stuck routes; step-over fix;
rerun >= 40 routes. Null: shuffled spawn->cell assignment."""
import json, sys
import numpy as np
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_t4_lib import (astar, cent, follow, classify_tris, Ctx, cells, regs)

OUT = '/home/z/my-project/scripts/s41_t4_result.json'
routes40 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t6_routes4.json'))
routes = routes40['routes']
same = [r for r in routes if r['kind'] == 'same_region']
print('same-region routes:', len(same), 'of', len(routes))
assert len(same) >= 40


def path_pts(pair):
    p = astar(pair[0], pair[1])
    if p is None:
        return None
    return [cent[c] for c in p]


import os
STAGE = os.environ.get('T4STAGE', '1')
res = {}
if STAGE == '1':
    RESFILE = '/home/z/my-project/scripts/s41_t4_stage1.json'
elif STAGE == '2':
    RESFILE = '/home/z/my-project/scripts/s41_t4_stage2.json'
else:
    RESFILE = '/home/z/my-project/scripts/s41_t4_stage3.json'

# ---- mode runs ----
def run_mode(mode, stepignore=None, limit=None):
    ctx = Ctx(mode, stepignore)
    rows = []
    for r in (same if limit is None else same[:limit]):
        pts = path_pts(r['cells'])
        if pts is None:
            rows.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow(ctx, pts)
        rows.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1),
                     'slides': slides})
    ok = sum(1 for x in rows if x['result'] == 'ok')
    return ctx, rows, ok

import json as _json
if STAGE == '1':
    print('stage1: ghost + ground-only')
    _, rows_ghost, ok_ghost = run_mode('ghost')
    print('ghost ok:', ok_ghost, '/', len(rows_ghost))
    _, rows_ground, ok_ground = run_mode('ground')
    print('ground-only ok:', ok_ground, '/', len(rows_ground))
    _json.dump({'ghost': [ok_ghost, len(rows_ghost)], 'ground': [ok_ground, len(rows_ground)]}, open(RESFILE, 'w'))
elif STAGE == '2':
    print('stage2: full rerun + blockers')
    ctx_full, rows_full, ok_full = run_mode('full')
    print('full ok:', ok_full, '/', len(rows_full))
    stuck_rows = [x for x in rows_full if x['result'] == 'stuck_wall'][:10]
    blockers = {}
    for row in stuck_rows:
        r = next(rr for rr in same if rr['route'] == row['route'])
        pts = path_pts(r['cells'])
        ctx = Ctx('full')
        v, d, sl, endpos = follow(ctx, pts)
        top = sorted(ctx.block_hits.items(), key=lambda kv: -kv[1])[:6]
        cls = classify_tris([i for i, _ in top])
        blockers[f"route{row['route']}"] = {'verdict': v, 'hits': {str(i): n for i, n in top},
                                            'classes': {str(i): cls[i] for i, _ in top}}
    from collections import Counter
    cls_counter = Counter()
    for b in blockers.values():
        for i, c in b['classes'].items():
            cls_counter[c['cls']] += 1
    print('blocker classes:', dict(cls_counter))
    _json.dump({'full_rerun': [ok_full, len(rows_full)], 'rows_full': rows_full,
                'blockers': blockers, 'blocker_class_counts': dict(cls_counter)}, open(RESFILE, 'w'), default=str)
else:
    print('stage3: fix rerun + nulls')
    _, rows_fix, ok_fix = run_mode('full', stepignore=0.55)
    print('fixed ok:', ok_fix, '/', len(rows_fix))
    _, rows_gfix, ok_gfix = run_mode('ground', stepignore=0.55)
    rng = np.random.default_rng(41)
    shuf = [(r['cells'][1], r['cells'][0]) if rng.random() < 0.5 else (r['cells'][0], r['cells'][1]) for r in same]
    ok_null_same = ok_null_cross = 0
    for (a, b) in shuf:
        ra, rb = cells[a][6], cells[b][6]
        pts = astar(a, b)
        if pts is None:
            continue
        if ra == rb:
            ctx = Ctx('full')
            v, d, sl, e = follow(ctx, [cent[c] for c in pts])
            ok_null_same += (v == 'ok')
        else:
            ok_null_cross += 1
    _json.dump({'full_stepignore0.55': [ok_fix, len(rows_fix)], 'ground_stepignore0.55': [ok_gfix, len(rows_gfix)],
                'null_shuffled': {'same_ok': int(ok_null_same), 'cross_rej': int(ok_null_cross)}}, open(RESFILE, 'w'), default=str)
    print('null shuffled dest: same-region ok', ok_null_same)
