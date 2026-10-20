#!/usr/bin/env python3
"""S42 T4: walk ON THE NAVMESH SURFACE (height interpolated from navmesh cell
triangles) with the collision soup used for WALLS ONLY; rerun the s40 40
same-region routes. Failure classification: real curb (soup walkable ground
also steps > 0.9) vs navmesh/soup disagreement (soup walkable is flat).
Controls: ghost + full rerun; null: shuffled destination assignment."""
import json, math, sys
import numpy as np
from collections import defaultdict
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
from s41_t4_lib import (cells, V, cent, NBS, cpos, cflags, WALKABLE, cmap, CGRID,
                        TRI_ZMAX, ground_at, astar, nearest_walls, try_slide, Ctx)

OUT = '/home/z/my-project/scripts/s42_t4_result.json'

# ---- navmesh cell grid: cells are triangles (v0,v1,v2) over V ----
CG = 10.0
cellgrid = defaultdict(list)
for i, c in enumerate(cells):
    xs = [V[c[0]][0], V[c[1]][0], V[c[2]][0]]
    ys = [V[c[0]][1], V[c[1]][1], V[c[2]][1]]
    for dx in range(int(min(xs) // CG), int(max(xs) // CG) + 1):
        for dy in range(int(min(ys) // CG), int(max(ys) // CG) + 1):
            cellgrid[(dx, dy)].append(i)

NM_TRI = np.array([[V[c[0]], V[c[1]], V[c[2]]] for c in cells])  # (nc, 3, 3)


def nm_ground(x, y, zmax):
    """Highest navmesh-surface z at (x,y) with z <= zmax + 0.6; -1e9 if none."""
    gx, gy = int(x // CG), int(y // CG)
    best = -1e9
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cellgrid.get((gx + dx, gy + dy), ()):
                t = NM_TRI[i]
                det = (t[1, 1] - t[2, 1]) * (t[0, 0] - t[2, 0]) + (t[2, 0] - t[1, 0]) * (t[0, 1] - t[2, 1])
                if abs(det) < 1e-12:
                    continue
                l1 = ((t[1, 1] - t[2, 1]) * (x - t[2, 0]) + (t[2, 0] - t[1, 0]) * (y - t[2, 1])) / det
                l2 = ((t[2, 1] - t[0, 1]) * (x - t[2, 0]) + (t[0, 0] - t[2, 0]) * (y - t[2, 1])) / det
                l3 = 1 - l1 - l2
                if l1 >= -0.03 and l2 >= -0.03 and l3 >= -0.03:
                    z = l1 * t[0, 2] + l2 * t[1, 2] + l3 * t[2, 2]
                    if z <= zmax + 0.6 and z > best:
                        best = z
    return best


class NavCtx(Ctx):
    """Navmesh-surface mode: height from the NAVMESH triangles; walls = soup
    non-walkable tris only (same wall set as 'full')."""

    def __init__(self, mode='navmesh'):
        super().__init__(mode=mode)
        self.fails = []          # failure records for classification

    def height(self, x, y, zmax):
        return nm_ground(x, y, zmax)


def snap_spawn_nm(ctx, pos):
    z = nm_ground(pos[0], pos[1], pos[2] + 2.6)
    if z == -1e9:
        return None, 'no_navmesh'
    trial = np.array([pos[0], pos[1], z])
    if not ctx.blocked(trial):
        return trial, 'ok'
    for r in np.arange(0.25, 2.01, 0.25):
        for a in np.linspace(0, 2 * math.pi, max(int(2 * math.pi * r / 0.25), 8), endpoint=False):
            x, y = pos[0] + r * math.cos(a), pos[1] + r * math.sin(a)
            z = nm_ground(x, y, pos[2] + 2.6)
            if z == -1e9:
                continue
            trial = np.array([x, y, z])
            if not ctx.blocked(trial) and abs(z - pos[2]) < 1.5:
                return trial, 'snapped'
    return None, 'all_blocked'


def follow_nm(ctx, pts, step=0.5):
    pos, why = snap_spawn_nm(ctx, pts[0])
    if pos is None:
        return why, 0.0, 0, None
    astar_len = sum(float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1))
    max_s = 2.0 * astar_len + 40.0
    s = 0.0
    stuck = 0
    stall = 0
    slides = 0
    iters = 0
    SUB = 0.2
    for tgt in pts[1:]:
        d = float(np.linalg.norm(tgt - pos))
        n = max(int(d / step), 1)
        for _ in range(n):
            dirv = (tgt - pos) / max(float(np.linalg.norm(tgt - pos)), 1e-9)
            remaining = min(step, d)
            guard = 0
            while remaining > 1e-6 and guard < 6:
                iters += 1
                if iters > 40000:
                    return 'stuck_wall', s, slides, pos.copy()
                guard += 1
                mvlen = min(SUB, remaining)
                dvec = dirv * mvlen
                sp = pos + dvec
                g = nm_ground(sp[0], sp[1], pos[2] + 2.6)
                if g == -1e9:
                    ctx.fails.append({'why': 'fell', 'x': float(sp[0]), 'y': float(sp[1]),
                                      'z': float(pos[2])})
                    return 'fell', s, slides, pos.copy()
                climb = g - pos[2]
                if climb > 0.9:
                    sl = try_slide(ctx, pos, dvec, mvlen)
                    if sl is not None:
                        pos, moved = sl
                        s += moved
                        remaining -= moved
                        slides += 1
                        continue
                    ctx.fails.append({'why': 'step_too_high', 'x': float(sp[0]), 'y': float(sp[1]),
                                      'z': float(pos[2]), 'climb': float(climb)})
                    return 'step_too_high', s, slides, pos.copy()
                trial = np.array([sp[0], sp[1], g])
                if ctx.blocked(trial):
                    sl = try_slide(ctx, pos, dvec, mvlen)
                    if sl is not None:
                        pos, moved = sl
                        s += moved
                        if moved < 0.02:
                            stall += 1
                        else:
                            stall = 0
                        if stall >= 3:
                            return 'stuck_wall', s, slides, pos.copy()
                        remaining -= max(moved, 0.02)
                        slides += 1
                        stuck = 0
                        continue
                    stuck += 1
                    if stuck > 6:
                        ctx.fails.append({'why': 'stuck_wall', 'x': float(pos[0]), 'y': float(pos[1]),
                                          'z': float(pos[2])})
                        return 'stuck_wall', s, slides, pos.copy()
                    remaining = 0
                    break
                pos = trial
                s += mvlen
                remaining -= mvlen
    return 'ok', s, slides, pos.copy()


def main():
    routes40 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t6_routes4.json'))
    routes = routes40['routes']
    same = [r for r in routes if r['kind'] == 'same_region'][:40]
    print('routes:', len(same))

    def path_pts(pair):
        p = astar(pair[0], pair[1])
        return None if p is None else [cent[c] for c in p]

    res = {'modes': {}}

    # ---- navmesh-surface run (the new instrument) ----
    ctx = NavCtx('navmesh')
    rows = []
    for r in same:
        pts = path_pts(r['cells'])
        if pts is None:
            rows.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow_nm(ctx, pts)
        rows.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1), 'slides': slides,
                     'fail': ctx.fails[-1] if verdict in ('fell', 'step_too_high', 'stuck_wall') and ctx.fails else None})
    ok = sum(1 for x in rows if x['result'] == 'ok')
    res['modes']['navmesh'] = {'ok': ok, 'rows': rows}

    # ---- failure classification: real curb vs navmesh/soup disagreement ----
    cls = []
    for row in rows:
        f = row.get('fail')
        if not f:
            continue
        nmz = nm_ground(f['x'], f['y'], f['z'] + 2.6)
        walk_g = ground_at(f['x'], f['y'], f['z'] + 2.6, walk_only=True)
        any_g = ground_at(f['x'], f['y'], f['z'] + 2.6, walk_only=False)
        cls.append({'route': row['route'], 'why': f['why'],
                    'nm_z': None if nmz == -1e9 else round(nmz, 2),
                    'soup_walkable_z': None if walk_g == -1e9 else round(walk_g, 2),
                    'soup_any_z': None if any_g == -1e9 else round(any_g, 2),
                    'class': ('real_step_soup_agrees' if walk_g != -1e9 and abs(walk_g - f['z']) > 0.9
                              else 'navmesh_soup_disagree' if walk_g != -1e9 and abs(walk_g - f['z']) <= 0.9
                              else 'off_soup')})
    res['failure_classification'] = cls

    # ---- controls: full + ghost reruns (s41 reproduction check) ----
    for mode in ('full', 'ghost'):
        c2 = Ctx(mode)
        rows2 = []
        for r in same:
            pts = path_pts(r['cells'])
            if pts is None:
                rows2.append({'route': r['route'], 'result': 'no_path'})
                continue
            verdict, dist, slides, endpos = __import__('s41_t4_lib').follow(c2, pts)
            rows2.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1)})
        res['modes'][mode] = {'ok': sum(1 for x in rows2 if x['result'] == 'ok'), 'rows': rows2}

    # ---- null: shuffled spawn->cell assignment (pairing shuffle) ----
    rng = np.random.RandomState(42)
    dests = [r['cells'][1] for r in same]
    shuffled = list(dests)
    rng.shuffle(shuffled)
    c3 = NavCtx('navmesh')
    rows3 = []
    for r, dst in zip(same, shuffled):
        pts = path_pts((r['cells'][0], dst))
        if pts is None:
            rows3.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow_nm(c3, pts)
        rows3.append({'route': r['route'], 'result': verdict})
    res['null_shuffled_dest_navmesh'] = {'ok': sum(1 for x in rows3 if x['result'] == 'ok'),
                                         'rows': rows3}

    # ---- variant: navmesh surface + stepignore 0.55 (the s41 steppable fix) ----
    c4 = NavCtx('navmesh')
    c4.stepignore = 0.55
    rows4 = []
    for r in same:
        pts = path_pts(r['cells'])
        if pts is None:
            rows4.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow_nm(c4, pts)
        rows4.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1)})
    res['modes']['navmesh_stepignore055'] = {'ok': sum(1 for x in rows4 if x['result'] == 'ok'),
                                             'rows': rows4}

    json.dump(res, open(OUT, 'w'), indent=1)
    for m, d in res['modes'].items():
        print(f"{m}: ok {d['ok']}/40")
    print('null shuffled-dest navmesh ok:', res['null_shuffled_dest_navmesh']['ok'], '/40')
    print('failure classification:')
    for c in cls:
        print('  ', c)


main()
