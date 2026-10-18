#!/usr/bin/env python3
"""S32 T3g: A* waypoint routes + capsule controller (wall slide, step-up,
slope limit) + failure classification."""
import json, struct, sys, collections, math, heapq, time
import numpy as np

D = np.load('/tmp/s32_t3_grid.npz', allow_pickle=True)
Z, FL, SL, valid, WALKABLE, STEP_OK = (D['Z'], D['FL'], D['SL'], D['valid'],
                                       D['WALKABLE'], D['STEP_OK'])
spawns = D['spawns']
gx0, gy0, GSTEP = -1500.0, -1400.0, 2.0
nx, ny = Z.shape
print(f'grid {nx}x{ny}, walkable {WALKABLE.sum()}')

# --- soup + ray (rebuild lightweight) ---
SOUP = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'
dd = open(SOUP, 'rb').read()
ntri, nobj = struct.unpack_from('<II', dd, 4)
name_len = struct.unpack_from('<I', dd, 12)[0]
pos0 = 16 + name_len + nobj * 48
rec = struct.calcsize('<H9fB')
raw = np.frombuffer(dd, dtype=np.uint8, offset=pos0).reshape(ntri, rec)
vtx = raw[:, 2:38].copy().view(np.float32).reshape(ntri, 3, 3).astype(np.float64)
TRI_FLAGS = raw[:, 38]
v0 = vtx[:, 0]
E1 = vtx[:, 1] - vtx[:, 0]
E2 = vtx[:, 2] - vtx[:, 0]
NRM = np.cross(E1, E2)
NN = np.linalg.norm(NRM, axis=1, keepdims=True)
NRM = NRM / np.where(NN > 1e-12, NN, 1)

CELL = 16.0
cx0, cy0 = vtx[:, :, 0].min(), vtx[:, :, 1].min()
gx = ((vtx[:, :, 0] - cx0) // CELL).astype(np.int32)
gy = ((vtx[:, :, 1] - cy0) // CELL).astype(np.int32)
bucket = collections.defaultdict(list)
for i in range(len(vtx)):
    for a in range(gx[i].min(), gx[i].max() + 1):
        for b in range(gy[i].min(), gy[i].max() + 1):
            bucket[(a, b)].append(i)
bucket = {k: np.array(v) for k, v in bucket.items()}


def ray(o, dr, tmax):
    """single ray; returns (t, tri_idx) or (inf, -1)"""
    a, b = cell_of(o[0], o[1])
    a2, b2 = cell_of(o[0] + dr[0] * tmax, o[1] + dr[1] * tmax)
    cands = {(a, b)}
    steps = max(abs(a2 - a), abs(b2 - b))
    for s2 in range(1, steps + 1):
        t0 = s2 / steps
        cands.add((int((o[0] + dr[0] * tmax * t0 - cx0) // CELL),
                   int((o[1] + dr[1] * tmax * t0 - cy0) // CELL)))
    idxs = [bucket[c] for c in cands if c in bucket]
    if not idxs:
        return np.inf, -1
    idx = np.concatenate(idxs)
    e1i, e2i = E1[idx], E2[idx]
    pv = np.cross(dr, e2i)
    det = (e1i * pv).sum(1)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
    tv = o[None, :] - v0[idx]
    u = (tv * pv).sum(1) * inv
    qv = np.cross(tv, e1i)
    v = (np.repeat(dr[None, :], len(idx), 0) * qv).sum(1) * inv
    t = (e2i * qv).sum(1) * inv
    hit = ok & (u >= -1e-6) & (u <= 1 + 1e-6) & (v >= -1e-6) & \
        (u + v <= 1 + 1e-6) & (t > 1e-4) & (t < tmax)
    if not hit.any():
        return np.inf, -1
    k = int(np.argmin(np.where(hit, t, np.inf)))
    return float(t[k]), int(idx[k])


def cell_of(x, y):
    return (int((x - cx0) // CELL), int((y - cy0) // CELL))


def to_cell(x, y):
    return (int(round((x - gx0) / GSTEP)), int(round((y - gy0) / GSTEP)))


# --- A* on walkable grid ---
def astar(s, t):
    def h(c):
        return math.hypot(c[0] - t[0], c[1] - t[1])
    pq = [(h(s), 0.0, s)]
    came = {s: None}
    g = {s: 0.0}
    while pq:
        _, gc, cur = heapq.heappop(pq)
        if cur == t:
            break
        if gc > g.get(cur, 1e18) + 1e-9:
            continue
        i, j = cur
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                nb = (i + di, j + dj)
                if not (0 <= nb[0] < nx and 0 <= nb[1] < ny):
                    continue
                if not WALKABLE[nb]:
                    continue
                if abs(di) + abs(dj) == 2:
                    if not (WALKABLE[(i + di, j)] and WALKABLE[(i, j + dj)]):
                        continue
                    if not (STEP_OK[i, j, 0 if di > 0 else 1] and
                            STEP_OK[i, j, 2 if dj > 0 else 3]):
                        continue
                else:
                    if not STEP_OK[i, j, {(1, 0): 0, (-1, 0): 1,
                                          (0, 1): 2, (0, -1): 3}[(di, dj)]]:
                        continue
                w = math.hypot(di, dj) * GSTEP
                ng = gc + w
                if ng < g.get(nb, 1e18) - 1e-9:
                    g[nb] = ng
                    came[nb] = cur
                    heapq.heappush(pq, (ng + h(nb), ng, nb))
    if t not in came:
        return None
    path = [t]
    while came[path[-1]] is not None:
        path.append(came[path[-1]])
    path.reverse()
    return path


# --- spawn selection ---
good_spawns = []
for s in spawns:
    c = to_cell(s[0], s[1])
    if 0 <= c[0] < nx and 0 <= c[1] < ny and WALKABLE[c]:
        good_spawns.append((s, c))
print(f'spawns on walkable ground: {len(good_spawns)}/{len(spawns)}')

# 12 deterministic pairs, spatially spread
rng = np.random.default_rng(22)
idx = rng.permutation(len(good_spawns))
routes = []
used = set()
for a in idx:
    if len(routes) >= 30:
        break
    if int(a) in used:
        continue
    # partner = farthest unused spawn
    best, bd = None, -1
    sa, ca = good_spawns[int(a)]
    for b in idx:
        ib = int(b)
        if ib in used or ib == int(a):
            continue
        sb, cb = good_spawns[ib]
        dd2 = math.hypot(sa[0] - sb[0], sa[1] - sb[1])
        if dd2 > bd:
            bd, best = dd2, ib
    if best is None:
        continue
    used.add(int(a))
    used.add(best)
    routes.append((int(a), best))
print(f'routes: {len(routes)}')

# --- capsule controller ---
R = 0.4
SLOPE_LIM = 50.0
STEP_LIM = 0.55
DT = 1 / 30


def walk(route_cells, start_pos, target_pos):
    """simulate; returns (outcome, dist_walked, sim_s, detail)"""
    p = np.array([start_pos[0], start_pos[1], start_pos[2] + 0.1])
    wps = [(gx0 + c[0] * GSTEP, gy0 + c[1] * GSTEP) for c in route_cells]
    wps.append((target_pos[0], target_pos[1]))
    wi = 0
    dist = 0.0
    t = 0.0
    stuck = 0.0
    events = collections.Counter()
    p_saved = p.copy()
    t_saved = 0.0
    while t < 240:
        tx, ty = wps[wi]
        dx, dy = tx - p[0], ty - p[1]
        dh = math.hypot(dx, dy)
        if dh < 2.0:
            wi += 1
            if wi >= len(wps):
                return 'ok', dist, t, dict(events)
            continue
        dirv = np.array([dx / dh, dy / dh, 0.0])
        # obstacle rays: knee + chest
        blocked = False
        wall_n = None
        for hz in (0.3, 1.2):
            o = p + np.array([0, 0, hz])
            tt, ii = ray(o, dirv, R + 0.35)
            if ii >= 0:
                blocked = True
                n3 = NRM[ii]
                nh = np.array([n3[0], n3[1], 0.0])
                nl = np.linalg.norm(nh)
                if nl > 0.2:
                    wall_n = nh / nl
                break
        moved = False
        if not blocked:
            moved = True
        else:
            # try step-up
            probe = p + dirv * 0.5 + np.array([0, 0, 0.7])
            tz, ti = ray(np.array([probe[0], probe[1], probe[2] + 0.5]),
                         np.array([0, 0, -1.0]), 3.0)
            if ti >= 0:
                ledge = probe[2] + 0.5 - tz
                if ledge - p[2] <= STEP_LIM and ledge > p[2] - 0.05:
                    p[2] = ledge + 0.02
                    moved = True
                    events['step_up'] += 1
                else:
                    events['step_too_high'] += 1
            if not moved and wall_n is not None:
                slide = dirv - (dirv @ wall_n) * wall_n
                sn = np.linalg.norm(slide)
                base = slide / sn if sn > 0.1 else \
                    np.array([-wall_n[1], wall_n[0], 0.0])
                # steer around the wall tangent
                for ang in (0.0, 0.785, -0.785, 1.571, -1.571):
                    ca_, sa_ = math.cos(ang), math.sin(ang)
                    dv = np.array([base[0]*ca_ - base[1]*sa_,
                                   base[0]*sa_ + base[1]*ca_, 0.0])
                    o2 = p + np.array([0, 0, 0.5])
                    t2, i2 = ray(o2, dv, R + 0.35)
                    if i2 < 0:
                        dirv = dv
                        moved = True
                        events['slide' if ang == 0 else 'steer'] += 1
                        break
                if not moved:
                    events['wall'] += 1
        if t - t_saved > 3.0:
            if np.linalg.norm(p - p_saved) < 0.8:
                events['oscillation'] += 1
                return 'stuck', dist, t, dict(events)
            p_saved = p.copy()
            t_saved = t
        if moved:
            step = 4.0 * DT
            np_ = p + dirv * step
            # ground under new pos
            tz, ti = ray(np.array([np_[0], np_[1], p[2] + 1.2]),
                         np.array([0, 0, -1.0]), 60.0)
            if ti < 0:
                events['fell'] += 1
                return 'fell', dist, t, dict(events)
            gz = p[2] + 1.2 - tz
            if gz > p[2] + STEP_LIM + 0.2:
                # wall ahead higher than step: blocked
                events['wall'] += 1
            elif p[2] - gz > 3.0:
                p[:] = np_
                p[2] -= 3.0 * DT          # falling
                dist += step
            else:
                p[:2] = np_[:2]
                p[2] = gz
                dist += step
            # slope check on landed tri
            sl = math.degrees(math.acos(min(1.0, abs(NRM[ti][2]))))
            if sl > SLOPE_LIM:
                events['steep'] += 1
            stuck = 0.0
        else:
            stuck += DT
            if stuck > 3.0:
                return 'stuck', dist, t, dict(events)
        t += DT
    return 'timeout', dist, t, dict(events)


t0 = time.time()
results = []
for k, (ia, ib) in enumerate(routes):
    sa, ca = good_spawns[ia]
    sb, cb = good_spawns[ib]
    path = astar(ca, cb)
    if path is None:
        results.append(dict(route=k, outcome='no_path',
                            start=sa[:3].tolist(), end=sb[:3].tolist(),
                            straight=math.hypot(sa[0] - sb[0], sa[1] - sb[1])))
        continue
    oc, distw, simt, ev = walk(path, sa[:3], sb[:3])
    results.append(dict(route=k, outcome=oc, waypoints=len(path),
                        walked_m=round(distw, 1), sim_s=round(simt, 1),
                        straight_m=round(math.hypot(sa[0] - sb[0],
                                                    sa[1] - sb[1]), 1),
                        events=ev,
                        start=sa[:3].tolist(), end=sb[:3].tolist()))
    print(f'route {k}: {oc} after {distw:.0f} m ({len(path)} wps, '
          f'{simt:.0f}s sim) {ev} [{time.time()-t0:.0f}s]')
json.dump(results, open('/home/z/my-project/download/s32_t3_routes.json',
                        'w'), indent=1)
oc = collections.Counter(r['outcome'] for r in results)
print('\nOUTCOMES:', dict(oc))
print('wrote s32_t3_routes.json')
