#!/usr/bin/env python3
"""S35 T3h: routes on ENGINE-DECODED navmesh adjacency (31,647 cells,
neighbour ids from the 15-B records) + capsule follower vs collision.
30+ spawn-to-spawn routes; failure classes; compare vs r34 0/34 (derived)
and grid A* 1/30."""
import struct, math, json, time, heapq
import numpy as np
from collections import defaultdict

t0 = time.time()

# ---- navmesh (engine-decoded) ----
F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
db = np.frombuffer(d, np.uint8)
GS = 0x5a4e6
NCELL = 31647
NV = 92715 // 3   # 30905
soup = np.frombuffer(d, '>f4', count=NV * 3, offset=2).astype(np.float64)
V = soup.reshape(NV, 3)
recs = np.zeros((NCELL, 8), np.int64)
base = GS + np.arange(NCELL) * 15
for j in range(7):
    recs[:, j] = db[base + 2 * j].astype(np.int64) * 256 + db[base + 2 * j + 1]
recs[:, 7] = db[base + 14]
a, b, c, e0, e1, e2, fl, ch = (recs[:, i] for i in range(8))
TRI = np.stack([V[a], V[b], V[c]], axis=1)          # (NCELL, 3, 3)
cent = TRI.mean(axis=1)
NBS = [tuple(int(x) for x in (e0[k], e1[k], e2[k]) if x != 65535) for k in range(NCELL)]
deg = np.array([len(n) for n in NBS])
print(f'cells {NCELL}, verts {NV}; degree mean {deg.mean():.2f} zero {(deg==0).sum()} '
      f'({(deg==0).mean()*100:.1f}%)')
print(f'cell z: med {np.median(cent[:,2]):.2f}')

# ---- collision (from r34) ----
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
                x1, y1 = t[0, 0], t[0, 1]; x2, y2 = t[1, 0], t[1, 1]; x3, y3 = t[2, 0], t[2, 1]
                det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
                if abs(det) < 1e-9: continue
                l1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
                l2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
                l3 = 1 - l1 - l2
                if l1 >= -0.02 and l2 >= -0.02 and l3 >= -0.02:
                    z = l1 * t[0, 2] + l2 * t[1, 2] + l3 * t[2, 2]
                    if z <= zmax + 0.6 and z > best: best = z
    return best

def blocked(pos, rad=0.45):
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    hit = False
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if not WALKABLE[i]:
                    t = cpos[i]
                    mz = t[:, 2].mean()
                    if mz < pos[2] - 0.4 or mz > pos[2] + 1.8: continue
                    # 2D point-triangle distance vs capsule radius
                    px, py = pos[0], pos[1]
                    dss = []
                    for (x1, y1), (x2, y2) in (((t[0,0],t[0,1]),(t[1,0],t[1,1])),
                                               ((t[1,0],t[1,1]),(t[2,0],t[2,1])),
                                               ((t[2,0],t[2,1]),(t[0,0],t[0,1]))):
                        vx, vy = x2-x1, y2-y1
                        L2 = vx*vx + vy*vy
                        tt = 0 if L2 < 1e-9 else max(0, min(1, ((px-x1)*vx + (py-y1)*vy)/L2))
                        dss.append(math.hypot(px-(x1+tt*vx), py-(y1+tt*vy)))
                    if min(dss) < rad:
                        hit = True
    return hit

# ---- A* over ENGINE adjacency ----
def astar(s, g):
    if s == g: return [s]
    dist = {s: 0.0}
    prev = {}
    pq = [(np.linalg.norm(cent[s] - cent[g]), 0.0, s)]
    while pq:
        f, dd, u = heapq.heappop(pq)
        if u == g:
            path = [u]
            while u in prev: u = prev[u]; path.append(u)
            return path[::-1]
        if dd > dist.get(u, 1e18): continue
        for v in NBS[u]:
            if not (0 <= v < NCELL): continue
            nd = dd + np.linalg.norm(cent[u] - cent[v])
            if nd < dist.get(v, 1e18):
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd + np.linalg.norm(cent[v] - cent[g]), nd, v))
    return None

# shared-edge midpoints for waypoints (engine cells share 2 vertices)
def waypoints(path):
    pts = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        su = set((a[u], b[u], c[u])); sv = {a[v], b[v], c[v]}
        shared = list(su & sv)
        if len(shared) == 2:
            m = (V[shared[0]] + V[shared[1]]) / 2
            pts.append(m)
        else:
            pts.append((cent[u] + cent[v]) / 2)
    pts.append(cent[path[-1]])
    return pts

# ---- capsule follower (r34 logic) ----
def follow(pts, max_s=240.0, step=0.55):
    pos = np.array(pts[0], float)
    pos[2] = ground_at(pos[0], pos[1], pos[2] + 2.0) + 0.05
    if blocked(pos):
        return 'spawn_blocked', 0.0
    tgt = 1
    walked = 0.0
    while walked < max_s:
        target = np.array(pts[tgt], float)
        d = target - pos
        dh = np.linalg.norm(d[:2])
        if dh < 0.9 and tgt == len(pts) - 1:
            return 'ok', walked
        if dh < 1.2:
            tgt += 1
            if tgt >= len(pts): tgt = len(pts) - 1
            continue
        dir2 = d[:2] / dh
        # ground + step handling
        gz = ground_at(pos[0] + dir2[0]*step, pos[1] + dir2[1]*step, pos[2] + 0.8)
        if gz < -1e8:
            return 'no_ground', walked
        if gz - pos[2] > 0.85:
            return 'step_too_high', walked
        nxt = np.array([pos[0] + dir2[0]*step, pos[1] + dir2[1]*step, gz + 0.05])
        if blocked(nxt):
            # wall slide: try rotated directions
            ok = False
            for ang in (0.5, -0.5, 1.0, -1.0, 1.6, -1.6):
                ca, sa = math.cos(ang), math.sin(ang)
                r2 = np.array([dir2[0]*ca - dir2[1]*sa, dir2[0]*sa + dir2[1]*ca])
                gz2 = ground_at(pos[0] + r2[0]*step, pos[1] + r2[1]*step, pos[2] + 0.8)
                if gz2 < -1e8 or gz2 - pos[2] > 0.85: continue
                n2 = np.array([pos[0] + r2[0]*step, pos[1] + r2[1]*step, gz2 + 0.05])
                if not blocked(n2):
                    nxt = n2; ok = True; break
            if not ok:
                return 'stuck_wall', walked
        pos = nxt
        walked += step
    return 'timeout', walked

# ---- endpoints: r32 spawn pairs + random ground-cell pairs ----
import glob, os
sp = sorted(glob.glob('/tmp/my-project/work/TDKR-Game/extraction/re/session3*/s32_spawns*.json') +
            glob.glob('/tmp/my-project/scripts/s32_spawn*.json'))
spawns = None
for f in sp:
    try:
        j = json.load(open(f))
        if isinstance(j, list) and len(j) > 8:
            spawns = j; print('spawn file:', f); break
    except Exception: pass
pairs = []
if spawns:
    pts = []
    for s in spawns[:80]:
        try:
            if isinstance(s, dict):
                p3 = s.get('pos') or s.get('position')
            else:
                p3 = s
            pts.append(np.array(p3[:3], float))
        except Exception: pass
    rng0 = np.random.default_rng(2)
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            if np.linalg.norm(pts[i][:2] - pts[j][:2]) > 60:
                pairs.append((pts[i], pts[j]))
    rng0.shuffle(pairs)

def nearest_cell(p):
    dd = np.linalg.norm(cent[:, :2] - p[:2], axis=1)
    okz = np.abs(cent[:, 2] - p[2]) < 12
    dd2 = np.where(okz, dd, 1e9)
    return int(np.argmin(dd2))

# random ground-cell pairs to reach >= 32 routes
rng = np.random.default_rng(23)
street = np.flatnonzero((cent[:, 2] > -1) & (cent[:, 2] < 25))
while len(pairs) < 34:
    i, j = rng.choice(street, 2, replace=False)
    if np.linalg.norm(cent[i][:2] - cent[j][:2]) > 80:
        pairs.append((cent[i].copy(), cent[j].copy()))

# ---- run 34 routes ----
rows = []
for i, (pA, pB) in enumerate(pairs[:34]):
    s = nearest_cell(pA); g = nearest_cell(pB)
    path = astar(s, g)
    row = dict(route=i, cells=(s, g))
    if path is None:
        row['result'] = 'no_path'; rows.append(row); print(f"route {i}: no_path"); continue
    pts = waypoints(path)
    res, walked = follow(pts)
    row.update(result=res, walked=round(walked, 1), path_cells=len(path),
               plan_len=round(float(sum(np.linalg.norm(pts[k+1]-pts[k]) for k in range(len(pts)-1))), 1))
    rows.append(row)
    print(f"route {i}: {res} walked {row['walked']} m plan {row['plan_len']} m cells {len(path)}")

res_c = defaultdict(int)
for r in rows:
    res_c[r['result']] += 1
print(f'\nSUMMARY 34 routes on ENGINE adjacency: {dict(res_c)}')
ok = res_c['ok']
print(f'success {ok}/34 = {ok/34*100:.1f}%  (r34 derived-adjacency 0/34; grid A* 1/30)')
json.dump(rows, open('/home/z/my-project/scripts/s35_t3_routes.json', 'w'), default=float)
print(f'elapsed {time.time()-t0:.0f}s')
