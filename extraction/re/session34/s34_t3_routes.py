#!/usr/bin/env python3
"""S34 T3 main: ground validation (+null), edge adjacency, A*, capsule routes
with failure classification. >=30 routes between spawn-like navmesh points."""
import struct, math, json, time, heapq
import numpy as np

t0 = time.time()

# ---------- load ----------
col = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin', 'rb').read()
nTri = struct.unpack_from('<I', col, 4)[0]
nObj = struct.unpack_from('<I', col, 8)[0]
p = 12
nameLen = struct.unpack_from('<I', col, p)[0]; p += 4 + nameLen + nObj * 48
CT = np.frombuffer(col[p:p + nTri * 39], np.uint8).reshape(nTri, 39)
cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
cflags = CT[:, 38].astype(np.int32)
WALKABLE = np.isin(cflags, [0, 1, 5, 6])   # concrete/wet/metal-ish/solid; excl Fence(9)/Stop(10)
tris = np.load("/home/z/my-project/scripts/s34_t3_nm_tris.npy").reshape(-1, 3, 3)
NT = len(tris)
print(f'collision {nTri} tris ({WALKABLE.sum()} walkable-flag), navmesh {NT} tris')

# ---------- 1. ground validation with shuffled null ----------
# collision ground height under (x,y): grid-hash collision tris by xy
G = 16.0
cx = np.floor(cpos[:, :, 0] / G).astype(np.int64)
cy = np.floor(cpos[:, :, 1] / G).astype(np.int64)
from collections import defaultdict
gmap = defaultdict(list)
for i in range(nTri):
    for dx in range(cx[i].min(), cx[i].max() + 1):
        for dy in range(cy[i].min(), cy[i].max() + 1):
            gmap[(dx, dy)].append(i)
keys = np.array(list(gmap.keys()), dtype=np.int64) if gmap else np.zeros((0, 2))
kset = set(map(tuple, gmap.keys()))

def ground_under(x, y, zref=None):
    """collision surface z at xy; with zref: nearest below-or-close surface"""
    gx, gy = int(np.floor(x / G)), int(np.floor(y / G))
    zs = []
    for cands in (gmap.get((gx, gy)), gmap.get((gx, gy - 1)), gmap.get((gx, gy + 1)),
                  gmap.get((gx - 1, gy)), gmap.get((gx + 1, gy))):
        if not cands: continue
        for i in cands:
            t = cpos[i]
            x1, y1 = t[0, 0], t[0, 1]; x2, y2 = t[1, 0], t[1, 1]; x3, y3 = t[2, 0], t[2, 1]
            det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if abs(det) < 1e-9: continue
            l1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
            l2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
            l3 = 1 - l1 - l2
            if l1 >= -0.02 and l2 >= -0.02 and l3 >= -0.02:
                zs.append(l1 * t[0, 2] + l2 * t[1, 2] + l3 * t[2, 2])
    if not zs: return -1e9
    if zref is None: return max(zs)
    below = [z for z in zs if z <= zref + 1.5]
    return min(below, key=lambda z: abs(z - zref)) if below else max(zs)

cent = tris.mean(axis=1)
d_real = []
for c in cent[::7]:                       # subsample 4,400 centroids
    g = ground_under(c[0], c[1], c[2])
    if g > -1e8:
        d_real.append(abs(c[2] - g))
d_real = np.array(d_real)
rng = np.random.default_rng(5)
d_null = []
zpool = tris[:, :, 2].ravel()
for _ in range(4400):
    c = cent[rng.integers(NT)]
    zsh = zpool[rng.integers(len(zpool))]   # shuffled navmesh height at a real xy
    g = ground_under(c[0], c[1])
    if g > -1e8:
        d_null.append(abs(zsh - g))
d_null = np.array(d_null)
print(f'\nGROUND: navmesh-vs-collision |dz|: n={len(d_real)} median '
      f'{np.median(d_real):.3f} m p95 {np.percentile(d_real, 95):.3f} m '
      f'<0.5m: {(d_real < 0.5).mean()*100:.1f}%')
print(f'NULL (shuffled z at real xy): median {np.median(d_null):.3f} m '
      f'p95 {np.percentile(d_null, 95):.3f} m <0.5m: {(d_null < 0.5).mean()*100:.1f}%')

# ---------- 2. adjacency from shared edges ----------
# DERIVED adjacency v2: edge-point sampling (seams ~1-2 m in the soup).
# Sample every ~2 m along each cell-triangle edge; two cells connect if they
# have sampled points within 1.5 m AND heights compatible.
SH = 2.0
shash = defaultdict(list)
def skey(p):
    return (int(np.floor(p[0] / SH)), int(np.floor(p[1] / SH)))
for i in range(NT):
    t = tris[i]
    for a, b in ((0, 1), (1, 2), (2, 0)):
        va, vb = t[a], t[b]
        L = float(np.linalg.norm(vb - va))
        n = max(2, int(L / SH))
        for k in range(n + 1):
            q = va + (vb - va) * (k / n)
            shash[skey(q)].append((i, q))
adj = [set() for _ in range(NT)]
for i in range(NT):
    t = tris[i]
    seen = set()
    for a, b in ((0, 1), (1, 2), (2, 0)):
        va, vb = t[a], t[b]
        L = float(np.linalg.norm(vb - va))
        n = max(2, int(L / SH))
        for k in range(n + 1):
            q = va + (vb - va) * (k / n)
            gx, gy = skey(q)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for (j, q2) in shash.get((gx + dx, gy + dy), ()):
                        if j == i or j in seen: continue
                        if np.linalg.norm(q - q2) < 1.5 and abs(q[2] - q2[2]) < 2.0:
                            adj[i].add(j); adj[j].add(i); seen.add(j)
deg = np.array([len(a) for a in adj])
print(f'\nadjacency: mean degree {deg.mean():.2f}, isolated {(deg == 0).sum()}')
# connected components
comp = np.full(NT, -1)
nc = 0
for s in range(NT):
    if comp[s] >= 0: continue
    stack = [s]; comp[s] = nc
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if comp[v] < 0:
                comp[v] = nc; stack.append(v)
    nc += 1
sizes = np.bincount(comp)
big = int(sizes.argmax())
print(f'components: {nc}, largest {sizes.max()} tris ({sizes.max()/NT*100:.1f}%), '
      f'next {sorted(sizes)[-2]}')

# ---------- 3. A* over tri graph ----------
def astar(s, g):
    if s == g: return [s]
    cent = tris.mean(axis=1)
    dist = {s: 0.0}
    prev = {}
    pq = [(np.linalg.norm(cent[s] - cent[g]), 0.0, s)]
    while pq:
        f, d, u = heapq.heappop(pq)
        if u == g:
            path = [u]
            while u in prev: u = prev[u]; path.append(u)
            return path[::-1]
        if d > dist.get(u, 1e18): continue
        for v in adj[u]:
            nd = d + np.linalg.norm(cent[u] - cent[v])
            if nd < dist.get(v, 1e18):
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd + np.linalg.norm(cent[v] - cent[g]), nd, v))
    return None

# ---------- 4. capsule follower ----------
CGRID = 10.0
ccx = np.floor(cpos[:, :, 0] / CGRID).astype(np.int64)
ccy = np.floor(cpos[:, :, 1] / CGRID).astype(np.int64)
cmap = defaultdict(list)
for i in range(nTri):
    for dx in range(ccx[i].min(), ccx[i].max() + 1):
        for dy in range(ccy[i].min(), ccy[i].max() + 1):
            cmap[(dx, dy)].append(i)

def tri_hit(p0, p1, tri, rad):
    """segment-vs-triangle approx: distance from segment to tri centroid < rad+tri_size"""
    c = tri.mean(axis=0)
    d = p1 - p0
    L = np.linalg.norm(d)
    if L < 1e-9: return False
    t = np.clip(np.dot(c - p0, d) / (L * L), 0, 1)
    q = p0 + t * d
    return np.linalg.norm(q - c) < rad + np.linalg.norm(tri[0] - c)

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
    """walls: walkable-flag tris intersecting the capsule cylinder (2D dist)"""
    gx, gy = int(np.floor(pos[0] / CGRID)), int(np.floor(pos[1] / CGRID))
    hit = False
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in cmap.get((gx + dx, gy + dy), ()):
                if not WALKABLE[i]: continue
                t = cpos[i]
                zmin, zmax = t[:, 2].min(), t[:, 2].max()
                if zmax < pos[2] + 0.25 or zmin > pos[2] + 1.7: continue
                # 2D point-triangle distance
                px, py = pos[0], pos[1]
                d2 = 1e9
                for k in range(3):
                    a, b2 = t[k], t[(k + 1) % 3]
                    ex, ey = b2[0] - a[0], b2[1] - a[1]
                    L2 = ex * ex + ey * ey
                    tt = 0 if L2 < 1e-9 else max(0, min(1, ((px - a[0]) * ex + (py - a[1]) * ey) / L2))
                    qx, qy = a[0] + tt * ex, a[1] + tt * ey
                    d2 = min(d2, (px - qx) ** 2 + (py - qy) ** 2)
                # inside test
                x1, y1 = t[0, 0], t[0, 1]; x2, y2 = t[1, 0], t[1, 1]; x3, y3 = t[2, 0], t[2, 1]
                det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
                if abs(det) > 1e-9:
                    l1 = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / det
                    l2 = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / det
                    l3 = 1 - l1 - l2
                    if l1 >= 0 and l2 >= 0 and l3 >= 0: d2 = 0.0
                if d2 < rad * rad: return True
    return hit if hit else False

def follow(path_tris, start_pos):
    """drive capsule along triangle-centroid path; returns (outcome, walked, events)"""
    cent = tris.mean(axis=1)
    pos = start_pos.copy()
    events = defaultdict(int)
    walked = 0.0
    wp = 0
    last_progress = 0.0
    steps = 0
    t_start = time.time()
    while wp < len(path_tris) and steps < 24000 and time.time() - t_start < 15:
        target = cent[path_tris[wp]]
        d3 = target - pos
        dh = math.hypot(d3[0], d3[1])
        if dh < 1.2:
            wp += 1; last_progress = walked; continue
        dirv = np.array([d3[0] / dh, d3[1] / dh, 0.0])
        step = 0.5
        # slide: if blocked ahead, rotate direction
        nxt = pos + dirv * step
        if blocked(nxt):
            events['slide'] += 1
            moved = False
            # r22-style tangent steering: persistent ±45/90 with progress memory
            for ang in (0.3, -0.3, 0.7, -0.7, 1.2, -1.2, 1.9, -1.9, 2.6, -2.6):
                ca, sa = math.cos(ang), math.sin(ang)
                r = np.array([dirv[0] * ca - dirv[1] * sa, dirv[0] * sa + dirv[1] * ca, 0])
                if not blocked(pos + r * step):
                    dirv = r; nxt = pos + r * step
                    moved = True
                    break
            if not moved:
                # try step-up
                gz = ground_at(*(pos + dirv * step)[:2], pos[2] + 0.9)
                if gz > -1e8 and 0 <= gz - pos[2] <= 0.55:
                    events['step_up'] += 1
                    pos[2] = gz + 0.05
                    nxt = pos + dirv * step
                else:
                    events['step_too_high'] += 1
                    return ('stuck', walked, dict(events), pos)
        # gravity/ground snap
        gz = ground_at(nxt[0], nxt[1], pos[2] + 0.9)
        if gz > -1e8:
            if gz < pos[2] - 2.5:
                events['fell'] += 1
                return ('fell', walked, dict(events), pos)
            pos[2] = gz + 0.05 if gz > pos[2] - 0.55 else pos[2] - 0.4
        else:
            events['no_ground'] += 1
            return ('fell', walked, dict(events), pos)
        if blocked(nxt):
            events['wall'] += 1
            return ('stuck', walked, dict(events), pos)
        walked += float(np.linalg.norm(nxt - pos))
        pos = nxt
        steps += 1
        if walked - last_progress > 40:
            last_progress = walked
    if wp >= len(path_tris):
        return ('ok', walked, dict(events), pos)
    return ('timeout', walked, dict(events), pos)

# ---------- 5. routes ----------
ground_tris = np.where((comp == big) & (tris[:, 0, 2] < 30) & (tris[:, 1, 2] < 30)
                       & (tris[:, 2, 2] < 30))[0]
print(f'ground-level tris in giant component: {len(ground_tris)}')
rng2 = np.random.default_rng(9)
pick = rng2.choice(ground_tris, 80, replace=False)
routes = []
r32 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session32/s32_t3_routes.json'))
starts = [np.array(r['start']) for r in r32]
# nearest navmesh tri to each r32 start
def nearest_tri(p):
    dd = np.linalg.norm(cent_all - p, axis=1)
    return int(np.argmin(dd))
cent_all = tris.mean(axis=1)
pairs = []
for i in range(len(starts)):
    for j in range(i + 1, len(starts)):
        pairs.append((nearest_tri(starts[i]), nearest_tri(starts[j])))
        if len(pairs) >= 12: break
    if len(pairs) >= 12: break
while len(pairs) < 34:
    a, b2 = rng2.choice(ground_tris, 2, replace=False)
    pa, pb2 = cent_all[a], cent_all[b2]
    if np.linalg.norm(pa - pb2) > 150:
        pairs.append((int(a), int(b2)))
print(f'{len(pairs)} route pairs; running...')
results = []
for k, (a, b2) in enumerate(pairs):
    path = astar(a, b2)
    if path is not None:
        # greedy line-of-sight smoothing: skip waypoints while the straight
        # segment stays on collision ground and unblocked
        sm = [path[0]]
        i = 0
        while i < len(path) - 1:
            j = len(path) - 1
            while j > i + 1:
                pa, pb = cent_all[path[i]], cent_all[path[j]]
                d = pb - pa
                L = np.linalg.norm(d[:2])
                ok = L > 0
                for fr in np.linspace(0.1, 0.9, 9):
                    q = pa + d * fr
                    gz = ground_under(q[0], q[1], q[2])
                    if gz <= -1e8 or abs(gz - q[2]) > 2.5 or blocked(np.array([q[0], q[1], gz + 0.9])):
                        ok = False; break
                if ok: break
                j -= 1
            sm.append(path[j]); i = j
        path = sm
    if path is None:
        results.append(dict(route=k, outcome='no_path', a=int(a), b=int(b2),
                        straight_m=float(np.linalg.norm(cent_all[a] - cent_all[b2]))))
        print(f'  route {k}: no_path', flush=True)
        json.dump(results, open('/home/z/my-project/scripts/s34_t3_routes_out.json', 'w'), indent=1)
        continue
    oc, walked, ev, endpos = follow(path, cent_all[a].copy())
    results.append(dict(route=k, outcome=oc, walked_m=round(walked, 1),
                        straight_m=round(float(np.linalg.norm(cent_all[a] - cent_all[b2])), 1),
                        events=ev, a=int(a), b=int(b2)))
    print(f'  route {k}: {oc} walked {walked:.0f} m ev {ev}', flush=True)
    json.dump(results, open('/home/z/my-project/scripts/s34_t3_routes_out.json', 'w'), indent=1)
json.dump(results, open('/home/z/my-project/scripts/s34_t3_routes_out.json', 'w'), indent=1)
oc = [r['outcome'] for r in results]
from collections import Counter
print('\nOUTCOMES:', dict(Counter(oc)))
print(f'total {time.time()-t0:.0f}s')
