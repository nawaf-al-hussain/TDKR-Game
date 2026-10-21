#!/usr/bin/env python3
"""S44 T4 part 1: re-run the s42 headline harness modes with PER-ROUTE fails
isolation to confirm the headline counts (navmesh+stepignore 15/40, full 10/40,
ghost 36/40, null 4/40) are unaffected by the s42 shared-ctx.fails bug.

Bug recap (s43): one NavCtx/Ctx per mode, ctx.fails accumulated across routes,
row['fail'] = ctx.fails[-1] -> a route that ends in a stall path that returns
without appending a fail record BORROWS the previous route's record. Verdicts
('ok'/'fell'/...) were always per-route; only the fail attribution was shared.
Here every fail record is tagged with the route id at append time (isolation by
construction), and the counts are recomputed from the per-route verdicts.
"""
import json, math, sys
import numpy as np
from collections import defaultdict
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
import s41_t4_lib as L
from s41_t4_lib import (cells, V, cent, NBS, cpos, cflags, WALKABLE, cmap,
                        TRI_ZMAX, ground_at, astar, Ctx, CGRID)

OUT = '/home/z/my-project/scripts/s44_t4_result.json'

# ---- navmesh cell grid (same as s42_t4_navmesh.py) ----
CG = 10.0
cellgrid = defaultdict(list)
for i, c in enumerate(cells):
    xs = [V[c[0]][0], V[c[1]][0], V[c[2]][0]]
    ys = [V[c[0]][1], V[c[1]][1], V[c[2]][1]]
    for dx in range(int(min(xs) // CG), int(max(xs) // CG) + 1):
        for dy in range(int(min(ys) // CG), int(max(ys) // CG) + 1):
            cellgrid[(dx, dy)].append(i)

NM_TRI = np.array([[V[c[0]], V[c[1]], V[c[2]]] for c in cells])


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
    """navmesh-surface height + soup walls; fails carry route ids (isolation)."""

    def __init__(self, mode='navmesh', stepignore=None):
        super().__init__(mode=mode, stepignore=stepignore)
        self.fails = []
        self.cur_route = None

    def fail(self, why, x, y, z, **extra):
        self.fails.append({'route': self.cur_route, 'why': why,
                           'x': float(x), 'y': float(y), 'z': float(z), **extra})


class IsoNavCtx(NavCtx):
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


def nearest_walls(ctx, pos, rad=0.45, k=2):
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    cands = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if WALKABLE[i]:
                    continue
                if ctx.stepignore is not None:
                    gref = ground_at(pos[0], pos[1], pos[2] + 2.6)
                    if gref == -1e9:
                        gref = pos[2]
                    if TRI_ZMAX[i] <= gref + ctx.stepignore:
                        continue
                t = cpos[i]
                mz = t[:, 2].mean()
                if mz < pos[2] - 0.4 or mz > pos[2] + 1.8:
                    continue
                for (x1, y1), (x2, y2) in (((t[0, 0], t[0, 1]), (t[1, 0], t[1, 1])),
                                           ((t[1, 0], t[1, 1]), (t[2, 0], t[2, 1])),
                                           ((t[2, 0], t[2, 1]), (t[0, 0], t[0, 1]))):
                    vx, vy = x2 - x1, y2 - y1
                    L2 = vx * vx + vy * vy
                    if L2 < 1e-9:
                        continue
                    tt = max(0.0, min(1.0, ((pos[0] - x1) * vx + (pos[1] - y1) * vy) / L2))
                    qx, qy = x1 + tt * vx, y1 + tt * vy
                    d = math.hypot(pos[0] - qx, pos[1] - qy)
                    if d < rad:
                        cands.append((d, (pos[0] - qx) / max(d, 1e-9), (pos[1] - qy) / max(d, 1e-9)))
    cands.sort(key=lambda c: c[0])
    return cands[:k]


def try_slide(ctx, pos, mv, mvlen):
    probe = pos + np.array([mv[0], mv[1], 0.0])
    walls = nearest_walls(ctx, probe)
    if not walls:
        return None
    cands = []
    mvl = float(np.linalg.norm(mv[:2]))
    for wi, (_, nx_, ny_) in enumerate(walls):
        n2 = np.array([nx_, ny_])
        v = mv[:2] - np.dot(mv[:2], n2) * n2
        if np.linalg.norm(v) > 1e-4:
            cands.append(v)
        if wi == 0:
            t2 = np.array([-n2[1], n2[0]])
            for sgn in (1.0, -1.0):
                cands.append(t2 * sgn * mvl)
    if cands and np.linalg.norm(cands[0]) > 1e-4:
        v0 = cands[0] / np.linalg.norm(cands[0])
        for ang in (25, -25, 90, -90):
            a = math.radians(ang)
            ca, sa = math.cos(a), math.sin(a)
            cands.append(np.array([v0[0] * ca - v0[1] * sa, v0[0] * sa + v0[1] * ca]) * mvl)
    for v in cands:
        LL = np.linalg.norm(v)
        if LL < 1e-4:
            continue
        sv = v * min(1.0, mvlen / LL)
        sp2 = pos + np.array([sv[0], sv[1], 0.0])
        g2 = ground_at(sp2[0], sp2[1], pos[2] + 2.6)
        if g2 == -1e9 or abs(g2 - pos[2]) > 0.9:
            continue
        sp2[2] = g2
        if ctx.blocked(sp2):
            continue
        return sp2, float(np.linalg.norm(sp2[:2] - pos[:2]))
    return None


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
                    ctx.fail('stuck_wall_timeout', pos[0], pos[1], pos[2])
                    return 'stuck_wall', s, slides, pos.copy()
                guard += 1
                mvlen = min(SUB, remaining)
                dvec = dirv * mvlen
                sp = pos + dvec
                g = nm_ground(sp[0], sp[1], pos[2] + 2.6)
                if g == -1e9:
                    ctx.fail('fell', sp[0], sp[1], pos[2])
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
                    ctx.fail('step_too_high', sp[0], sp[1], pos[2], climb=float(climb))
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
                            ctx.fail('stuck_wall_stall', pos[0], pos[1], pos[2])
                            return 'stuck_wall', s, slides, pos.copy()
                        remaining -= max(moved, 0.02)
                        slides += 1
                        stuck = 0
                        continue
                    stuck += 1
                    if stuck > 6:
                        ctx.fail('stuck_wall', pos[0], pos[1], pos[2])
                        return 'stuck_wall', s, slides, pos.copy()
                    remaining = 0
                    break
                pos = trial
                s += mvlen
                remaining -= mvlen
    return 'ok', s, slides, pos.copy()


def follow_full(ctx, pts, step=0.5):
    """the s40/s41 'full' follower (ground_at heights + walls + slide)"""
    pos, why = L.snap_spawn(ctx, pts[0])
    if pos is None:
        return why, 0.0, 0, None
    astar_len = sum(float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1))
    max_s = 2.0 * astar_len + 40.0
    s = 0.0
    stuck = 0
    stall = 0
    slides = 0
    iters = 0
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
                    ctx.fail('stuck_wall_timeout', pos[0], pos[1], pos[2])
                    return 'stuck_wall', s, slides, pos.copy()
                guard += 1
                SUB = 0.2
                mvlen = min(SUB, remaining)
                dvec = dirv * mvlen
                sp = pos + dvec
                g = ground_at(sp[0], sp[1], pos[2] + 2.6)
                if g == -1e9:
                    ctx.fail('fell', sp[0], sp[1], pos[2])
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
                    ctx.fail('step_too_high', sp[0], sp[1], pos[2], climb=float(climb))
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
                            ctx.fail('stuck_wall_stall', pos[0], pos[1], pos[2])
                            return 'stuck_wall', s, slides, pos.copy()
                        remaining -= max(moved, 0.02)
                        slides += 1
                        stuck = 0
                        continue
                    stuck += 1
                    if stuck > 6:
                        ctx.fail('stuck_wall', pos[0], pos[1], pos[2])
                        return 'stuck_wall', s, slides, pos.copy()
                    remaining = 0
                    break
                pos = trial
                s += mvlen
                remaining -= mvlen
    return 'ok', s, slides, pos.copy()


def main():
    routes40 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t6_routes4.json'))
    same = [r for r in routes40['routes'] if r['kind'] == 'same_region'][:40]
    print('routes:', len(same))

    def path_pts(pair):
        p = astar(pair[0], pair[1])
        return None if p is None else [cent[c] for c in p]

    res = {'modes': {}, 'per_route_fails': {}}

    # ---- mode: navmesh + stepignore 0.55 (the headline) ----
    ctx = IsoNavCtx('navmesh', stepignore=0.55)
    rows = []
    for r in same:
        ctx.cur_route = r['route']
        pts = path_pts(r['cells'])
        if pts is None:
            rows.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow_nm(ctx, pts)
        rows.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1), 'slides': slides})
    res['modes']['navmesh_stepignore055'] = {'ok': sum(1 for x in rows if x['result'] == 'ok'), 'rows': rows}

    # ---- controls: full + ghost (s41 reproduction; L.follow ghost = pure polyline) ----
    for mode in ('full', 'ghost'):
        c2 = Ctx(mode)
        rows2 = []
        for r in same:
            pts = path_pts(r['cells'])
            if pts is None:
                rows2.append({'route': r['route'], 'result': 'no_path'})
                continue
            verdict, dist, slides, endpos = L.follow(c2, pts)
            rows2.append({'route': r['route'], 'result': verdict, 'dist': round(dist, 1)})
        res['modes'][mode] = {'ok': sum(1 for x in rows2 if x['result'] == 'ok'), 'rows': rows2}

    # ---- null: shuffled destination assignment ----
    rng = np.random.RandomState(42)
    dests = [r['cells'][1] for r in same]
    shuffled = list(dests)
    rng.shuffle(shuffled)
    c3 = IsoNavCtx('navmesh')
    rows3 = []
    for r, dst in zip(same, shuffled):
        c3.cur_route = r['route']
        pts = path_pts((r['cells'][0], dst))
        if pts is None:
            rows3.append({'route': r['route'], 'result': 'no_path'})
            continue
        verdict, dist, slides, endpos = follow_nm(c3, pts)
        rows3.append({'route': r['route'], 'result': verdict})
    res['null_shuffled_dest_navmesh'] = {'ok': sum(1 for x in rows3 if x['result'] == 'ok'), 'rows': rows3}

    # ---- per-route fail records (isolation by construction: route-tagged) ----
    res['per_route_fails'] = {str(f['route']): f for f in
                              (ctx.fails + c3.fails)}

    json.dump(res, open(OUT, 'w'), indent=1)
    for m, d in res['modes'].items():
        print(f"{m}: ok {d['ok']}/40")
    print('null shuffled-dest navmesh ok:', res['null_shuffled_dest_navmesh']['ok'], '/40')
    print('routes with tagged fails:', len(res['per_route_fails']))


main()
