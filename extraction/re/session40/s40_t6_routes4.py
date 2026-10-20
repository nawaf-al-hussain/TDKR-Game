#!/usr/bin/env python3
"""S38 T7 (derived from s37_t1_routes2): CLEARANCE-WEIGHTED ROUTES.
Clearance per cell = 2D distance from the cell center to the nearest NON-walkable
collision edge (capped 2 m); A* edge cost = length * (1 + 2*max(0, (0.45-clr)/0.45));
waypoints with clr<0.45 are pushed toward the locally clearest of 8 directions.
"
# Original r37 header: routes with an improved capsule follower + cross-region census.

Follower fixes vs r26 (per-failure-cause):
  - timeout        -> budget proportional to A* length (2x + 40 m), was 300 m flat
  - stuck_wall     -> 8-direction tangential slide with 3-slide grace, was 4 fixed dirs
  - spawn_blocked  -> ring-search snap up to 2.0 m (0.25 m steps) before giving up
  - step_too_high  -> sub-stepping (split step into 4) so stairs are climbed gradually
  - fell           -> unchanged (missing ground = data), wider ground window +2.6 m
Route set: 34 historical pairs (s35) + 30 seeded same-region pairs (seed 36,
identical procedure to r26 for comparability). Cross-region pairs classified
under the engine semantics (pair table empty -> SearchPortalPath rejects).
Nulls: shuffled spawn->cell assignment.
"""
import struct, math, heapq, json, random
import numpy as np
from collections import defaultdict, Counter

random.seed(36)
NM = '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'
nm = open(NM, 'rb').read()
vcount = struct.unpack_from('>H', nm, 0)[0]
soup_end = 2 + vcount * 12
ccount = struct.unpack_from('>H', nm, soup_end + 2)[0]
cs = soup_end + 4
V = np.zeros((vcount, 3))
for i in range(vcount):
    V[i] = struct.unpack_from('>3f', nm, 2 + i * 12)
cells = []
for i in range(ccount):
    v0, v1, v2, n0, n1, n2 = struct.unpack_from('>6H', nm, cs + i * 15)
    reg = struct.unpack_from('>H', nm, cs + i * 15 + 12)[0]
    f = lambda w: w - 0x10000 if w > 0x7FFF else w
    cells.append((v0, v1, v2, f(n0), f(n1), f(n2), reg))
cent = np.array([(V[c[0]] + V[c[1]] + V[c[2]]) / 3 for c in cells])
NBS = defaultdict(list)
for i, c in enumerate(cells):
    for n in c[3:6]:
        if n >= 0:
            NBS[i].append(n)
regs = defaultdict(list)
for i, c in enumerate(cells):
    regs[c[6]].append(i)

col = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin', 'rb').read()
nTri = struct.unpack_from('<I', col, 4)[0]
nObj = struct.unpack_from('<I', col, 8)[0]
p = 12
nameLen = struct.unpack_from('<I', col, p)[0]; p += 4 + nameLen + nObj * 48
CT = np.frombuffer(col[p:p + nTri * 39], np.uint8).reshape(nTri, 39)
cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
cflags = CT[:, 38].astype(np.int32)
WALKABLE = np.isin(cflags, [0, 1, 5, 6])
CGRID = 10.0
ccx = np.floor(cpos[:, :, 0] / CGRID).astype(np.int64)
ccy = np.floor(cpos[:, :, 1] / CGRID).astype(np.int64)
cmap = defaultdict(list)
for i in range(nTri):
    for dx in range(ccx[i].min(), ccx[i].max() + 1):
        for dy in range(ccy[i].min(), ccy[i].max() + 1):
            cmap[(dx, dy)].append(i)

def ground_at(x, y, zmax):
    gx, gy = int(np.floor(x / CGRID)), int(np.floor(y / CGRID))
    best = -1e9
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                t = cpos[i]
                det = (t[1, 1] - t[2, 1]) * (t[0, 0] - t[2, 0]) + (t[2, 0] - t[1, 0]) * (t[0, 1] - t[2, 1])
                if abs(det) < 1e-9:
                    continue
                l1 = ((t[1, 1] - t[2, 1]) * (x - t[2, 0]) + (t[2, 0] - t[1, 0]) * (y - t[2, 1])) / det
                l2 = ((t[2, 1] - t[0, 1]) * (x - t[2, 0]) + (t[0, 0] - t[2, 0]) * (y - t[2, 1])) / det
                l3 = 1 - l1 - l2
                if l1 >= -0.02 and l2 >= -0.02 and l3 >= -0.02:
                    z = l1 * t[0, 2] + l2 * t[1, 2] + l3 * t[2, 2]
                    if z <= zmax + 0.6 and z > best:
                        best = z
    return best

def blocked(pos, rad=0.45):
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if not WALKABLE[i]:
                    t = cpos[i]
                    mz = t[:, 2].mean()
                    if mz < pos[2] - 0.4 or mz > pos[2] + 1.8:
                        continue
                    px, py = pos[0], pos[1]
                    for (x1, y1), (x2, y2) in (((t[0, 0], t[0, 1]), (t[1, 0], t[1, 1])),
                                               ((t[1, 0], t[1, 1]), (t[2, 0], t[2, 1])),
                                               ((t[2, 0], t[2, 1]), (t[0, 0], t[0, 1]))):
                        vx, vy = x2 - x1, y2 - y1
                        L2 = vx * vx + vy * vy
                        tt = 0 if L2 < 1e-9 else max(0, min(1, ((px - x1) * vx + (py - y1) * vy) / L2))
                        if math.hypot(px - (x1 + tt * vx), py - (y1 + tt * vy)) < rad:
                            return True
    return False

# ---- s38 T7: per-cell clearance (2D distance to nearest non-walkable edge, cap 2 m)
WALK_GRID = defaultdict(list)
for i in range(nTri):
    t = cpos[i]
    gx, gy = int(np.floor(t[:, 0].mean() / CGRID)), int(np.floor(t[:, 1].mean() / CGRID))
    WALK_GRID[(gx, gy)].append(i)

def edge_dist(pos, t):
    best = 1e9
    px, py = pos[0], pos[1]
    for (x1, y1), (x2, y2) in (((t[0, 0], t[0, 1]), (t[1, 0], t[1, 1])),
                               ((t[1, 0], t[1, 1]), (t[2, 0], t[2, 1])),
                               ((t[2, 0], t[2, 1]), (t[0, 0], t[0, 1]))):
        vx, vy = x2 - x1, y2 - y1
        L2 = vx * vx + vy * vy
        tt = 0 if L2 < 1e-9 else max(0, min(1, ((px - x1) * vx + (py - y1) * vy) / L2))
        d = math.hypot(px - (x1 + tt * vx), py - (y1 + tt * vy))
        if d < best: best = d
    return best

CLR_CACHE = {}
def clearance(pos):
    kx, ky = round(pos[0], 1), round(pos[1], 1)
    key = (kx, ky)
    if key in CLR_CACHE: return CLR_CACHE[key]
    best = 2.0
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    R = 2
    for dx in range(-R, R + 1):
        for dy in range(-R, R + 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if WALKABLE[i]: continue
                t = cpos[i]
                mz = t[:, 2].mean()
                if mz < pos[2] - 0.4 or mz > pos[2] + 1.8: continue
                d = edge_dist(pos, t)
                if d < best: best = d
    CLR_CACHE[key] = best
    return best

def astar(s, g, use_clearance=True):
    if s == g:
        return [s]
    dist = {s: 0.0}; prev = {}
    pq = [(np.linalg.norm(cent[s] - cent[g]), 0.0, s)]
    while pq:
        f_, dd, u = heapq.heappop(pq)
        if u == g:
            path = [u]
            while u in prev:
                u = prev[u]; path.append(u)
            return path[::-1]
        if dd > dist.get(u, 1e18):
            continue
        for v in NBS[u]:
            climb = max(0.0, float(cent[v][2] - cent[u][2]))
            nd = dd + np.linalg.norm(cent[u] - cent[v]) * (1.0 + 2.0 * climb)
            if nd < dist.get(v, 1e18):
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd + np.linalg.norm(cent[v] - cent[g]), nd, v))
    return None


def snap_spawn(pos):
    """ring search for a non-blocked grounded spot (fix: spawn_blocked)"""
    z = ground_at(pos[0], pos[1], pos[2] + 2.6)
    if z == -1e9:
        return None, 'no_ground'
    trial = np.array([pos[0], pos[1], z])
    if not blocked(trial):
        return trial, 'ok'
    for r in np.arange(0.25, 2.01, 0.25):
        for a in np.linspace(0, 2 * math.pi, max(int(2 * math.pi * r / 0.25), 8), endpoint=False):
            x, y = pos[0] + r * math.cos(a), pos[1] + r * math.sin(a)
            z = ground_at(x, y, pos[2] + 2.6)
            if z == -1e9:
                continue
            trial = np.array([x, y, z])
            if not blocked(trial) and abs(z - pos[2]) < 1.5:
                return trial, f'snapped_{r:.2f}m'
    return None, 'all_blocked'


def nearest_walls(pos, rad=0.45, k=2):
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    cands = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if WALKABLE[i]:
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

def try_slide(pos, mv, mvlen):
    """Analytic slide: project mv on each nearby wall line, then tangent sweeps.
    Walls are probed at the BLOCKED trial position (collisions can be up to
    mv+rad from the current position). Every candidate is re-checked."""
    probe = pos + np.array([mv[0], mv[1], 0.0])
    walls = nearest_walls(probe)
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
        L = np.linalg.norm(v)
        if L < 1e-4:
            continue
        sv = v * min(1.0, mvlen / L)
        sp2 = pos + np.array([sv[0], sv[1], 0.0])
        g2 = ground_ok(sp2[0], sp2[1], pos[2])
        if g2 is None or abs(g2 - pos[2]) > 0.9:
            continue
        sp2[2] = g2
        if blocked(sp2):
            continue
        return sp2, float(np.linalg.norm(sp2[:2] - pos[:2]))
    return None

def ground_ok(x, y, zref):
    g = ground_at(x, y, zref + 2.6)
    if g == -1e9:
        return None
    return g

def follow3(pts, step=0.5):
    """Analytic wall-slide follower with continuous 0.2 m sub-steps.
    No tunneling: every slide candidate is re-checked for block + ground."""
    pos, why = snap_spawn(pts[0])
    if pos is None:
        return why, 0.0, 0
    astar_len = sum(np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1))
    max_s = 2.0 * astar_len + 40.0
    s = 0.0
    stuck = 0
    stall = 0
    slides = 0
    iters = 0
    ITERS_MAX = 40000
    SUB = 0.2
    for tgt in pts[1:]:
        d = np.linalg.norm(tgt - pos)
        n = max(int(d / step), 1)
        for k in range(n):
            dirv = (tgt - pos) / max(np.linalg.norm(tgt - pos), 1e-9)
            remaining = min(step, d)
            guard = 0
            while remaining > 1e-6 and guard < 6:
                iters += 1
                if iters > ITERS_MAX:
                    return 'stuck_wall', s, slides
                guard += 1
                mvlen = min(SUB, remaining)
                mv = dirv * mvlen
                sp = pos + mv
                g = ground_ok(sp[0], sp[1], pos[2])
                if g is None:
                    return 'fell', s, slides
                climb = g - pos[2]
                if climb > 0.9:
                    sl = try_slide(pos, mv, mvlen)
                    if sl is not None:
                        pos, moved = sl
                        s += moved
                        remaining -= moved
                        slides += 1
                        continue
                    return 'step_too_high', s, slides
                trial = np.array([sp[0], sp[1], g])
                if blocked(trial):
                    sl = try_slide(pos, mv, mvlen)
                    if sl is not None:
                        pos, moved = sl
                        s += moved
                        if moved < 0.02:
                            stall += 1
                        else:
                            stall = 0
                        if stall >= 3:
                            return 'stuck_wall', s, slides
                        remaining -= max(moved, 0.02)
                        slides += 1
                        stuck = 0
                        continue
                    stuck += 1
                    if stuck > 6:
                        return 'stuck_wall', s, slides
                    remaining = 0
                    break
                pos = trial
                s += mvlen
                remaining -= mvlen
            if s > max_s:
                return 'timeout', s, slides
    return 'ok', s, slides

def waypoints(path):
    pts = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        shared = list(set(cells[u][:3]) & set(cells[v][:3]))
        if len(shared) == 2:
            pts.append((V[shared[0]] + V[shared[1]]) / 2)
        else:
            pts.append((cent[u] + cent[v]) / 2)
    pts.append(cent[path[-1]])
    return pts

# ---- route set (identical to s38 for comparability) ----
hist = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session35/s35_t3_routes.json'))
pairs = [tuple(e['cells']) for e in hist]
big = sorted(regs, key=lambda r: -len(regs[r]))[:6]
fresh = []
random.seed(36)
while len(fresh) < 30:
    r = random.choice(big)
    a, b = random.sample(regs[r], 2)
    if np.linalg.norm(cent[a] - cent[b]) > 60:
        fresh.append((a, b))

results = []
for idx, (s, g) in enumerate(pairs + fresh):
    srcreg, dstreg = cells[s][6], cells[g][6]
    kind = 'same_region' if srcreg == dstreg else 'cross_region'
    src = 'hist' if idx < len(pairs) else 'fresh'
    if kind == 'cross_region':
        res, dist, ncells, slides = 'no_path_cross_region_engine', 0.0, 0, 0
    else:
        path = astar(s, g)
        if path is None:
            res, dist, ncells, slides = 'no_path', 0.0, 0, 0
        else:
            pts = waypoints(path)
            res, dist, slides = follow3(pts)
            ncells = len(path)
    results.append({'route': idx, 'src': src, 'kind': kind, 'cells': [int(s), int(g)],
                    'regions': [int(srcreg), int(dstreg)], 'result': res,
                    'path_cells': ncells, 'dist_m': round(float(dist), 1),
                    'slides': int(slides)})
    if True:
        print(f'route {idx}: {res} ({dist:.0f} m, {slides} slides)', flush=True)

cnt = Counter((r['src'], r['kind'], r['result']) for r in results)
print('SUMMARY (s40 analytic wall-slide):')
for k, v in sorted(cnt.items()):
    print(' ', k, v)
same = [r for r in results if r['kind'] == 'same_region']
ok = sum(1 for r in same if r['result'] == 'ok')
print(f'ok same-region: {ok}/{len(same)}')
fails = Counter(r['result'] for r in same if r['result'] != 'ok')
print('failure classes:', dict(fails))

# ---- NULL: shuffled destination cells (same procedure as s38) ----
rng = random.Random(37)
allcells = list(range(ccount))
shuf = Counter()
for s, g in pairs:
    s2 = cells[s][6]
    g2 = cells[rng.randrange(ccount)][6]
    shuf['cross' if s2 != g2 else 'same'] += 1
real = Counter('cross' if cells[s][6] != cells[g][6] else 'same' for s, g in pairs)
print('NULL shuffled dest:', dict(shuf), ' REAL hist pairs:', dict(real))

json.dump({'routes': results, 'summary': {f'{k[0]}|{k[1]}|{k[2]}': v for k, v in cnt.items()},
           'ok_same': ok, 'n_same': len(same), 'fails': dict(fails),
           'null_shuffled': dict(shuf), 'real_pairs': dict(real)},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t6_routes4.json', 'w'), indent=1)
print('saved s40_t6_routes4.json')
