#!/usr/bin/env python3
"""s43 T4a: classify the 10 navmesh/soup height disagreements geographically."""
import json, sys
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
from s41_t4_lib import cent, astar, ground_at

# load s42 harness without running its main()
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t4_navmesh.py').read()
src = src.replace("\nmain()\n", "\n")
ns = {'__name__': 's42harness'}
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session42')
exec(compile(src, 's42_t4_navmesh.py', 'exec'), ns)
NavCtx, nm_ground, follow_nm = ns['NavCtx'], ns['nm_ground'], ns['follow_nm']
cellgrid, NM_TRI, CG = ns['cellgrid'], ns['NM_TRI'], ns['CG']

routes40 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t6_routes4.json'))
same = [r for r in routes40['routes'] if r['kind'] == 'same_region'][:40]
rmap = {r['route']: r for r in same}
DISAGREE = [37, 39, 41, 42, 43, 44, 45, 46, 47, 61]

ctx = NavCtx('navmesh')
out = []
for rid in DISAGREE:
    r = rmap[rid]
    p = astar(r['cells'][0], r['cells'][1])
    if p is None:
        out.append({'route': rid, 'error': 'no_path'})
        continue
    pts = [cent[c] for c in p]
    ctx.fails = []
    verdict, dist, slides, endpos = follow_nm(ctx, pts)
    if not ctx.fails:
        out.append({'route': rid, 'verdict': verdict, 'note': 'no fail recorded'})
        continue
    f = ctx.fails[-1]
    x, y, z = f['x'], f['y'], f['z']
    nm_levels = set()
    gx, gy = int(x // CG), int(y // CG)
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            for i in cellgrid.get((gx + dx, gy + dy), ()):
                t = NM_TRI[i]
                if abs(float(t[:, 0].mean()) - x) < 7 and abs(float(t[:, 1].mean()) - y) < 7:
                    nm_levels.add(round(float(t[:, 2].mean()), 2))
    soup_levels = set()
    for zmax in np.arange(-2, 50, 1.0):
        g = ground_at(x, y, float(zmax), walk_only=True)
        if g is not None and g != -1e9:
            soup_levels.add(round(float(g), 2))
    soup_any = set()
    for zmax in np.arange(-2, 50, 1.0):
        g = ground_at(x, y, float(zmax), walk_only=False)
        if g is not None and g != -1e9:
            soup_any.add(round(float(g), 2))
    lv = sorted(nm_levels)
    near = [L for L in lv if abs(L - z) < 3]
    ground_below = any(L < 1.5 for L in soup_levels)
    elevated = z > 4.0
    if elevated and ground_below:
        klass = 'ELEVATED_DECK_OVER_STREET (bridge/overpass/upper plaza)'
    elif elevated and not ground_below:
        klass = 'ELEVATED_WITHOUT_GROUND_BELOW (structure deck / registration)'
    elif not elevated and not soup_levels:
        klass = 'SOUP_HOLE (no walkable soup nearby)'
    else:
        klass = 'GROUND_LEVEL_REGISTRATION'
    out.append({'route': rid, 'why': f['why'], 'x': round(x, 1), 'y': round(y, 1), 'z': round(z, 2),
                'nm_levels_near': sorted(near), 'nm_levels_all': lv[:8],
                'soup_walkable_levels': sorted(soup_levels)[-6:],
                'soup_any_levels': sorted(soup_any)[-6:],
                'class': klass, 'verdict': verdict, 'dist': round(dist, 1)})
    print(rid, klass, f"z={z:.2f} ({x:.0f},{y:.0f})")
json.dump(out, open('/home/z/my-project/scripts/s43_t4_disagree.json', 'w'), indent=1)
print('saved', len(out))
