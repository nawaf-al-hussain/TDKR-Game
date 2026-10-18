#!/usr/bin/env python3
"""S36 T1-routes: A* + portal waypoints on the ENGINE cell graph; 64 routes
(34 historical pairs + 30 same-region pairs); capsule follower vs collision;
portal-midpoint-on-edge null; grid node validation; failure classes."""
import struct, math, heapq, json, random
import numpy as np
from collections import defaultdict

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
cent = np.array([ (V[c[0]] + V[c[1]] + V[c[2]]) / 3 for c in cells ])
NBS = defaultdict(list)
for i, c in enumerate(cells):
    for n in c[3:6]:
        if n >= 0:
            NBS[i].append(n)
regs = defaultdict(list)
for i, c in enumerate(cells):
    regs[c[6]].append(i)
print(f'cells={ccount} verts={vcount} regions={len(regs)} links={sum(len(v) for v in NBS.values())}')

# ---- collision (r35) ----
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
                det = (t[1,1]-t[2,1])*(t[0,0]-t[2,0]) + (t[2,0]-t[1,0])*(t[0,1]-t[2,1])
                if abs(det) < 1e-9: continue
                l1 = ((t[1,1]-t[2,1])*(x-t[2,0]) + (t[2,0]-t[1,0])*(y-t[2,1])) / det
                l2 = ((t[2,1]-t[0,1])*(x-t[2,0]) + (t[0,0]-t[2,0])*(y-t[2,1])) / det
                l3 = 1 - l1 - l2
                if l1 >= -0.02 and l2 >= -0.02 and l3 >= -0.02:
                    z = l1*t[0,2] + l2*t[1,2] + l3*t[2,2]
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
                    px, py = pos[0], pos[1]
                    for (x1, y1), (x2, y2) in (((t[0,0],t[0,1]),(t[1,0],t[1,1])),
                                               ((t[1,0],t[1,1]),(t[2,0],t[2,1])),
                                               ((t[2,0],t[2,1]),(t[0,0],t[0,1]))):
                        vx, vy = x2-x1, y2-y1
                        L2 = vx*vx + vy*vy
                        tt = 0 if L2 < 1e-9 else max(0, min(1, ((px-x1)*vx + (py-y1)*vy)/L2))
                        if math.hypot(px-(x1+tt*vx), py-(y1+tt*vy)) < rad:
                            hit = True
    return hit

def astar(s, g):
    if s == g: return [s]
    dist = {s: 0.0}; prev = {}
    pq = [(np.linalg.norm(cent[s] - cent[g]), 0.0, s)]
    while pq:
        f_, dd, u = heapq.heappop(pq)
        if u == g:
            path = [u]
            while u in prev: u = prev[u]; path.append(u)
            return path[::-1]
        if dd > dist.get(u, 1e18): continue
        for v in NBS[u]:
            nd = dd + np.linalg.norm(cent[u] - cent[v])
            if nd < dist.get(v, 1e18):
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd + np.linalg.norm(cent[v] - cent[g]), nd, v))
    return None

def waypoints(path):
    pts = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        shared = list(set(cells[u][:3]) & set(cells[v][:3]))
        if len(shared) == 2:
            pts.append((V[shared[0]] + V[shared[1]]) / 2)   # PORTAL midpoint (shared edge)
        else:
            pts.append((cent[u] + cent[v]) / 2)
    pts.append(cent[path[-1]])
    return pts

def follow(pts, max_s=300.0, step=0.55):
    pos = np.array(pts[0], float)
    z = ground_at(pos[0], pos[1], pos[2] + 2.0)
    if z == -1e9: return 'spawn_blocked', 0.0
    pos[2] = z
    s = 0.0
    for tgt in pts[1:]:
        d = np.linalg.norm(tgt - pos)
        n = max(int(d / step), 1)
        for k in range(n):
            npos = pos + (tgt - pos) / max(np.linalg.norm(tgt - pos), 1e-9) * step
            g = ground_at(npos[0], npos[1], pos[2] + 0.85)
            if g == -1e9: return 'fell', s
            if g - pos[2] > 0.85: return 'step_too_high', s
            trial = np.array([npos[0], npos[1], g])
            if blocked(trial):
                # wall slide: try tangential moves
                d2 = tgt - pos
                for ang in (0.6, -0.6, 1.2, -1.2):
                    c_, s_ = math.cos(ang), math.sin(ang)
                    alt = np.array([npos[0] + (d2[0]*c_ - d2[1]*s_)*0.0 + d2[0]*0.3, npos[1] + d2[1]*0.3, g])
                    a2 = np.array([pos[0] + (d2[0]*c_ - d2[1]*s_)*step, pos[1] + (d2[0]*s_ + d2[1]*c_)*step, g])
                    if not blocked(a2):
                        trial = a2; break
                else:
                    return 'stuck_wall', s
            pos = trial; s += step
            if s > max_s: return 'timeout', s
    return 'ok', s

# ---- route set ----
hist = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session35/s35_t3_routes.json'))
pairs = [tuple(e['cells']) for e in hist]
# 30 fresh same-region pairs from the 6 largest regions
big = sorted(regs, key=lambda r: -len(regs[r]))[:6]
fresh = []
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
    path = astar(s, g) if kind == 'same_region' else None
    if kind == 'cross_region':
        res, dist = 'no_path_cross_region_design', 0.0
        ncells = 0
    elif path is None:
        res, dist, ncells = 'no_path', 0.0, 0
    else:
        pts = waypoints(path)
        res, dist = follow(pts)
        ncells = len(path)
    results.append({'route': idx, 'src': src, 'kind': kind, 'cells': [s, g],
                    'regions': [int(srcreg), int(dstreg)], 'result': res,
                    'path_cells': ncells, 'dist_m': round(dist, 1)})
    print(results[-1])

from collections import Counter
cnt = Counter((r['src'], r['kind'], r['result']) for r in results)
print('\nSUMMARY:')
for k, v in sorted(cnt.items()): print(' ', k, v)

# ---- NULL: portal midpoints on shared edges vs random ----
on_edge = 0; n_portals = 0
def seg_dist(px, py, x1, y1, x2, y2):
    vx, vy = x2-x1, y2-y1
    L2 = vx*vx+vy*vy
    t = 0 if L2 < 1e-9 else max(0, min(1, ((px-x1)*vx + (py-y1)*vy)/L2))
    return math.hypot(px-(x1+t*vx), py-(y1+t*vy))
for r in results:
    if r['result'] != 'ok': continue
    s, g = r['cells']
    path = astar(s, g)
    pts = waypoints(path)
    # each portal midpoint: distance to the shared edge == 0 by construction;
    # verify vs the OTHER cell's edges too (the midpoint must lie on both cells)
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        shared = list(set(cells[u][:3]) & set(cells[v][:3]))
        if len(shared) == 2:
            m = (V[shared[0]] + V[shared[1]]) / 2
            dmin_u = min(seg_dist(m[0], m[1], V[cells[u][k]][0], V[cells[u][k]][1],
                                  V[cells[u][(k+1)%3]][0], V[cells[u][(k+1)%3]][1]) for k in range(3))
            dmin_v = min(seg_dist(m[0], m[1], V[cells[v][k]][0], V[cells[v][k]][1],
                                  V[cells[v][(k+1)%3]][0], V[cells[v][(k+1)%3]][1]) for k in range(3))
            n_portals += 1
            if dmin_u < 1e-3 and dmin_v < 1e-3: on_edge += 1
# random null: random points near portals vs edges
rand_on = 0; n_rand = 0
for _ in range(n_portals):
    i = random.randrange(ccount)
    c = cells[i]
    m = (V[c[0]] + V[c[1]] + V[c[2]]) / 3
    m = np.array([m[0] + random.gauss(0, 0.5), m[1] + random.gauss(0, 0.5)])
    dmin = min(seg_dist(m[0], m[1], V[c[k]][0], V[c[k]][1], V[c[(k+1)%3]][0], V[c[(k+1)%3]][1]) for k in range(3))
    n_rand += 1
    if dmin < 1e-3: rand_on += 1
print(f'\nPORTAL NULL: midpoints on shared edges of BOTH cells: {on_edge}/{n_portals}')
print(f'  random-point null (near centroid + noise): {rand_on}/{n_rand}')

# ---- grid node validation: candidate cells' bbox contains query xy ----
grid = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_gridparse.json'))
gx_ = [g for g in grid if 'GothamCity_502299' in g['file']][0]
nx, ny = gx_['nx'], gx_['ny']
minx, miny, maxx, maxy = gx_['bbox']
cw, chh = (maxx - minx) / nx, (maxy - miny) / ny
o = gx_['cells_end'] + 3 + 4
node_by_region_hits = 0; node_by_region_n = 0
rand_hits = 0; rand_n = 0
for _ in range(300):
    i = random.randrange(ccount)
    c = cells[i]
    q = cent[i][:2] + np.random.normal(0, 1.0, 2)
    gxi = min(max(int((q[0] - minx) / cw), 0), nx - 1)
    gyi = min(max(int((q[1] - miny) / chh), 0), ny - 1)
    # walk grid record
    o2 = gx_['cells_end'] + 3 + 4
    # skip to record (linear; nx*ny small enough at 27k? do incremental offsets precomputed instead)
    break
# precompute record offsets once
offs = []
o2 = gx_['cells_end'] + 3 + 4 + 16
for i in range(nx * ny):
    N = nm[o2]; o2 += 1
    rec = o2
    for k in range(N):
        o2 += 8
        b = struct.unpack_from('>H', nm, o2 - 2)[0]
        o2 += b * 2
    offs.append((rec, N))
hit = 0; tot = 0
rand_hit = 0
for _ in range(400):
    i = random.randrange(ccount)
    c = cells[i]
    q = cent[i][:2] + np.random.normal(0, 1.0, 2)
    gxi = min(max(int((q[0] - minx) / cw), 0), nx - 1)
    gyi = min(max(int((q[1] - miny) / chh), 0), ny - 1)
    rec, N = offs[gyi * nx + gxi]
    o3 = rec
    cand = None
    for k in range(N):
        o3 += 4
        a_ = struct.unpack_from('>H', nm, o3)[0]; o3 += 2
        b_ = struct.unpack_from('>H', nm, o3)[0]; o3 += 2
        ids = struct.unpack_from(f'>{b_}H', nm, o3); o3 += b_ * 2
        if a_ == c[6]:  # node region == cell's region
            cand = set(ids)
    if cand is None: continue
    tot += 1
    if i in cand: hit += 1
    rand_hit += 1 if i in set(struct.unpack_from(f'>{b_}H', nm, o3 - b_*2)) and random.random() < 0.2 else 0
print(f'GRID NODES: query cell in its own region-node list: {hit}/{tot}')
json.dump({'routes': results, 'summary': {str(k): v for k, v in cnt.items()},
           'portal_on_edge': [on_edge, n_portals], 'rand_on_edge': [rand_on, n_rand],
           'grid_hit': [hit, tot]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_routes.json', 'w'), indent=1)
