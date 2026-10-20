#!/usr/bin/env python3
"""S41 T4 lib: navmesh + collision + A* + three followers (ghost / ground-only /
full-slide) with blocking-triangle capture. Derived from s40_t6_routes4.py."""
import struct, math, heapq, json
import numpy as np
from collections import defaultdict

random = __import__('random')
random.seed(41)

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

TRI_AREA = np.abs(np.cross(cpos[:, 1] - cpos[:, 0], cpos[:, 2] - cpos[:, 0])).sum(1) / 2
TRI_ZMIN = cpos[:, :, 2].min(1)
TRI_ZMAX = cpos[:, :, 2].max(1)


def ground_at(x, y, zmax, walk_only=True):
    gx, gy = int(np.floor(x / CGRID)), int(np.floor(y / CGRID))
    best = -1e9
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if walk_only and not WALKABLE[i]:
                    continue
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


class Ctx:
    """Collision-mode context: 'full' (s40 wall-slide), 'ground' (ground tris only),
    'ghost' (nothing blocks, no falls). stepignore: skip blockers whose top is
    within stepignore of local ground (steppable props/ledges)."""
    def __init__(self, mode='full', stepignore=None):
        self.mode = mode
        self.stepignore = stepignore
        self.block_hits = defaultdict(int)

    def blocked(self, pos, rad=0.45):
        if self.mode == 'ghost':
            return False
        gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
        gref = None
        if self.stepignore is not None:
            gref = ground_at(pos[0], pos[1], pos[2] + 2.6)
            if gref == -1e9:
                gref = pos[2]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for i in cmap.get((gx + dx, gy + dy), ()):
                    if self.mode == 'ground' and not WALKABLE[i]:
                        continue
                    if WALKABLE[i]:
                        continue
                    t = cpos[i]
                    mz = t[:, 2].mean()
                    if mz < pos[2] - 0.4 or mz > pos[2] + 1.8:
                        continue
                    if self.stepignore is not None and TRI_ZMAX[i] <= gref + self.stepignore:
                        continue
                    px, py = pos[0], pos[1]
                    for (x1, y1), (x2, y2) in (((t[0, 0], t[0, 1]), (t[1, 0], t[1, 1])),
                                               ((t[1, 0], t[1, 1]), (t[2, 0], t[2, 1])),
                                               ((t[2, 0], t[2, 1]), (t[0, 0], t[0, 1]))):
                        vx, vy = x2 - x1, y2 - y1
                        L2 = vx * vx + vy * vy
                        tt = 0 if L2 < 1e-9 else max(0, min(1, ((px - x1) * vx + (py - y1) * vy) / L2))
                        if math.hypot(px - (x1 + tt * vx), py - (y1 + tt * vy)) < rad:
                            self.block_hits[i] += 1
                            return True
        return False


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
        L = np.linalg.norm(v)
        if L < 1e-4:
            continue
        sv = v * min(1.0, mvlen / L)
        sp2 = pos + np.array([sv[0], sv[1], 0.0])
        g2 = ground_at(sp2[0], sp2[1], pos[2] + 2.6)
        if g2 == -1e9 or abs(g2 - pos[2]) > 0.9:
            continue
        sp2[2] = g2
        if ctx.blocked(sp2):
            continue
        return sp2, float(np.linalg.norm(sp2[:2] - pos[:2]))
    return None


def snap_spawn(ctx, pos):
    z = ground_at(pos[0], pos[1], pos[2] + 2.6)
    if z == -1e9:
        return None, 'no_ground'
    trial = np.array([pos[0], pos[1], z])
    if not ctx.blocked(trial):
        return trial, 'ok'
    for r in np.arange(0.25, 2.01, 0.25):
        for a in np.linspace(0, 2 * math.pi, max(int(2 * math.pi * r / 0.25), 8), endpoint=False):
            x, y = pos[0] + r * math.cos(a), pos[1] + r * math.sin(a)
            z = ground_at(x, y, pos[2] + 2.6)
            if z == -1e9:
                continue
            trial = np.array([x, y, z])
            if not ctx.blocked(trial) and abs(z - pos[2]) < 1.5:
                return trial, f'snapped_{r:.2f}m'
    return None, 'all_blocked'


def astar(s, g):
    if s == g:
        return [s]
    dist = {s: 0.0}; prev = {}
    pq = [(float(np.linalg.norm(cent[s] - cent[g])), 0.0, s)]
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
            nd = dd + float(np.linalg.norm(cent[u] - cent[v])) * (1.0 + 2.0 * climb)
            if nd < dist.get(v, 1e18):
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd + float(np.linalg.norm(cent[v] - cent[g])), nd, v))
    return None


def follow(ctx, pts, step=0.5):
    """Wall-slide follower (s40 analytic + continuous substeps)."""
    pos, why = snap_spawn(ctx, pts[0])
    if pos is None:
        return why, 0.0, 0, None
    astar_len = sum(float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1))
    max_s = 2.0 * astar_len + 40.0
    s = 0.0
    stuck = 0
    stall = 0
    slides = 0
    iters = 0
    ITERS_MAX = 40000
    SUB = 0.2
    last_pos = pos.copy()
    for tgt in pts[1:]:
        d = float(np.linalg.norm(tgt - pos))
        n = max(int(d / step), 1)
        for k in range(n):
            dirv = (tgt - pos) / max(float(np.linalg.norm(tgt - pos)), 1e-9)
            remaining = min(step, d)
            guard = 0
            while remaining > 1e-6 and guard < 6:
                iters += 1
                if iters > ITERS_MAX:
                    return 'stuck_wall', s, slides, pos.copy()
                guard += 1
                mvlen = min(SUB, remaining)
                mv = dirv * mvlen
                if ctx.mode == 'ghost':
                    pos = pos + mv   # pure polyline: no ground, no walls, no climbs
                    s += mvlen; remaining -= mvlen
                    continue
                sp = pos + mv
                g = ground_at(sp[0], sp[1], pos[2] + 2.6)
                if g == -1e9:
                    return 'fell', s, slides, pos.copy()
                climb = g - pos[2]
                if climb > 0.9:
                    sl = try_slide(ctx, pos, mv, mvlen)
                    if sl is not None:
                        pos, moved = sl
                        s += moved; remaining -= moved; slides += 1
                        continue
                    return 'step_too_high', s, slides, pos.copy()
                trial = np.array([sp[0], sp[1], g])
                if ctx.blocked(trial):
                    sl = try_slide(ctx, pos, mv, mvlen)
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
                        return 'stuck_wall', s, slides, pos.copy()
                    remaining = 0
                    break
                pos = trial
                s += mvlen
                remaining -= mvlen
        last_pos = pos.copy()
    return 'ok', s, slides, pos.copy()


def classify_tris(idx):
    """Blocking-triangle classification."""
    out = {}
    for i in idx:
        t = cpos[i]
        n = np.cross(t[1] - t[0], t[2] - t[0])
        area = float(np.linalg.norm(n) / 2)
        nz = abs(float(n[2])) / max(float(np.linalg.norm(n)), 1e-9)
        gz = ground_at(float(t[:, 0].mean()), float(t[:, 1].mean()), float(t[:, 2].max()) + 2.6)
        height_above_ground = float(TRI_ZMAX[i] - gz) if gz != -1e9 else None
        if area < 0.05:
            cls = 'degenerate_tiny'
        elif nz > 0.7 and height_above_ground is not None and height_above_ground < 0.55:
            cls = 'low_ledge_horizontal'
        elif nz > 0.7:
            cls = 'horizontal_nonwalkable'
        elif height_above_ground is not None and height_above_ground < 0.55:
            cls = 'prop_below_capsule'
        elif TRI_ZMAX[i] - TRI_ZMIN[i] < 0.3 and max(np.linalg.norm(t[1] - t[0]), np.linalg.norm(t[2] - t[1]), np.linalg.norm(t[2] - t[0])) > 1.0:
            cls = 'thin_geometry'
        else:
            cls = 'wall_other'
        out[i] = {'cls': cls, 'flag': int(cflags[i]), 'area': round(area, 3),
                  'nz': round(nz, 2), 'h_ag': None if height_above_ground is None else round(height_above_ground, 2),
                  'zmax': round(float(TRI_ZMAX[i]), 2)}
    return out
