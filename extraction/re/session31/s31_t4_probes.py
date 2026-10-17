#!/usr/bin/env python3
"""S31 T4: multi-grid ground probes + slope/step stats + continuous-path test.
Grid centers chosen deterministically BEFORE probing: 5 densest spawn buckets
(seeded k-means-free grid count) on GothamCity + island-2 spawn centroid."""
import json, struct, sys, collections, math
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure


def load_soup(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'TCS1'
    ntri, nobj = struct.unpack_from('<II', d, 4)
    name_len = struct.unpack_from('<I', d, 12)[0]
    pos = 16 + name_len
    for _ in range(nobj):
        pos += 48
    rec = struct.calcsize('<H9fB')
    raw = np.frombuffer(d, dtype=np.uint8, offset=pos).reshape(ntri, rec)
    vtx = raw[:, 2:38].copy().view(np.float32).reshape(ntri, 3, 3).astype(np.float64)
    flags = raw[:, 38]
    return vtx, flags


def build_bucket(vtx, CELL=20.0):
    cx0, cy0 = vtx[:, :, 0].min(), vtx[:, :, 1].min()
    gx = ((vtx[:, :, 0] - cx0) // CELL).astype(np.int32)
    gy = ((vtx[:, :, 1] - cy0) // CELL).astype(np.int32)
    bucket = collections.defaultdict(list)
    for i in range(len(vtx)):
        for a in range(gx[i].min(), gx[i].max() + 1):
            for b in range(gy[i].min(), gy[i].max() + 1):
                bucket[(a, b)].append(i)
    bucket = {k: np.array(v) for k, v in bucket.items()}
    return cx0, cy0, CELL, bucket


def make_prober(vtx, bucket, cx0, cy0, CELL):
    v0, e1, e2 = vtx[:, 0], vtx[:, 1] - vtx[:, 0], vtx[:, 2] - vtx[:, 0]
    n = np.cross(e1, e2)
    nn = np.linalg.norm(n, axis=1, keepdims=True)
    n = n / np.where(nn > 1e-12, nn, 1)

    def hit_down(O, maxd=40.0):
        """down-ray; returns (t, tri_idx) arrays with inf/-1 for miss"""
        t_out = np.full(len(O), np.inf)
        i_out = np.full(len(O), -1)
        for j, o in enumerate(O):
            key = (int((o[0]-cx0)//CELL), int((o[1]-cy0)//CELL))
            idx = bucket.get(key)
            if idx is None or len(idx) == 0:
                continue
            v0i, e1i, e2i = v0[idx], e1[idx], e2[idx]
            h = np.cross(np.array([0.0, 0.0, -1.0]), e2i)
            a = (e1i * h).sum(1)
            ok = np.abs(a) > 1e-12
            f = np.where(ok, 1.0/np.where(ok, a, 1), 0.0)
            s = o - v0i
            uu = f * (s * h).sum(1)
            q = np.cross(s, e1i)
            vv = f * (q * np.array([0.0, 0.0, -1.0])).sum(1)
            tt = f * (e2i * q).sum(1)
            hit = ok & (uu >= -1e-9) & (vv >= -1e-9) & (uu + vv <= 1 + 1e-9) \
                & (tt > 0) & (tt < maxd)
            if hit.any():
                k = np.argmin(np.where(hit, tt, np.inf))
                t_out[j] = tt[k]
                i_out[j] = idx[k]
        return t_out, i_out
    return hit_down, n


def grid_stats(hit_down, n, center, tag):
    rng = np.linspace(-50, 50, 21)
    pts = np.array([[center[0] + dx, center[1] + dy, center[2] + 30.0]
                    for dx in rng for dy in rng])
    t, idx = hit_down(pts)
    found = np.isfinite(t)
    frac = found.mean()
    ground = center[2] + 30.0 - t
    slopes = np.array([0.0])
    if found.any():
        slopes = np.degrees(np.arccos(np.clip(np.abs(n[idx[found]][:, 2]), 0, 1)))
    z = np.where(found, ground, np.nan).reshape(21, 21)
    steps = []
    for a in range(21):
        for b in range(21):
            for dz, dy in ((0, 1), (1, 0)):
                if a+dz < 21 and b+dy < 21 and np.isfinite(z[a, b]) \
                   and np.isfinite(z[a+dz, b+dy]):
                    steps.append(abs(z[a+dz, b+dy] - z[a, b]))
    steps = np.array(steps if steps else [0.0])
    print(f'  [{tag}] center ({center[0]:.0f},{center[1]:.0f}): ground '
          f'{found.sum()}/{len(pts)} = {100*frac:.1f}%; slope deg: median '
          f'{np.median(slopes):.1f}, p95 {np.percentile(slopes, 95):.1f}; '
          f'step m: median {np.median(steps):.2f}, p95 {np.percentile(steps, 95):.2f}, '
          f'max {steps.max():.2f}; z range [{np.nanmin(z):.1f},{np.nanmax(z):.1f}]')
    return dict(tag=tag, center=center, frac=float(frac),
                slope_med=float(np.median(slopes)),
                slope_p95=float(np.percentile(slopes, 95)),
                step_med=float(np.median(steps)),
                step_p95=float(np.percentile(steps, 95)),
                step_max=float(steps.max()),
                zmin=float(np.nanmin(z)), zmax=float(np.nanmax(z)))


# ---- spawn positions for blind center selection ----
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
templates = {int(k, 16): v for k, v in json.load(open(
    '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
spawns = []
spec9826 = tab['dedicated']['9826']
for rid, off, tid, end, kind in res['records']:
    if kind == 'ded 0x2662':
        rr = lvc_pure.Reader(d, strings)
        rr.p = off
        tk = []
        rr.tok('i', out=tk)
        lvc_pure.replay(spec9826, rr, tk)
        fs = [t[3] for t in tk if t[0] == 'f']
        if len(fs) >= 3:
            # spawn TRS stores (y, z, x, ...): pos = (f[1], f[0], f[2])
            spawns.append((fs[1], fs[0], fs[2]))
spawns = np.array(spawns)
print(f'spawns: {len(spawns)}')
# 5 densest 200-m buckets (blind selection)
B = 200
cnt = collections.Counter((int(x // B), int(y // B)) for x, y, z in spawns)
top5 = [k for k, _ in cnt.most_common(5)]
centers = []
for a, b in top5:
    sel = spawns[(spawns[:, 0] // B == a) & (spawns[:, 1] // B == b)]
    centers.append(tuple(sel.mean(0)))
print('blind grid centers (5 densest spawn buckets):',
      [(round(c[0]), round(c[1])) for c in centers])

res2 = lvc_pure.parse('/tmp/my-project/work/data/GothamCity_Island2.lvc',
                      tab, templates, None)
d2 = res2['data']
sp2 = []
for rid, off, tid, end, kind in res2['records']:
    if kind == 'ded 0x2662':
        rr = lvc_pure.Reader(d2, strings)
        rr.p = off
        tk = []
        rr.tok('i', out=tk)
        lvc_pure.replay(spec9826, rr, tk)
        fs = [t[3] for t in tk if t[0] == 'f']
        if len(fs) >= 3:
            sp2.append((fs[1], fs[0], fs[2]))
sp2 = np.array(sp2)
i2center = tuple(sp2.mean(0))
print(f'island2 spawns {len(sp2)}, centroid ({i2center[0]:.0f},{i2center[1]:.0f})')

results = []
P = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'
vtx, flags = load_soup(P)
cx0, cy0, CELL, bucket = build_bucket(vtx)
hit_down, nrm = make_prober(vtx, bucket, cx0, cy0, CELL)
print(f'\nGothamCity soup: {len(vtx)} tris')
for i, c in enumerate(centers):
    results.append(grid_stats(hit_down, nrm, (c[0], c[1], c[2]), f'GC-grid{i+1}'))
results.append(grid_stats(hit_down, nrm, (i2center[0], i2center[1], 30.0),
                          'GC@I2-centroid (expect ~0%)'))

P2 = '/tmp/my-project/work/TDKR-Game/extraction/prototype/i2_collision.bin'
vtx2, _ = load_soup(P2)
cx02, cy02, CELL2, bucket2 = build_bucket(vtx2)
hit_down2, nrm2 = make_prober(vtx2, bucket2, cx02, cy02, CELL2)
print(f'\nIsland2 soup: {len(vtx2)} tris')
results.append(grid_stats(hit_down2, nrm2, (i2center[0], i2center[1], i2center[2]),
                          'I2-grid'))

# ---- continuous-path test: 20 random spawn->spawn routes ----
print('\n=== path test (ground-follow march, step limit 0.6 m, fall limit 3 m) ===')
rng = np.random.default_rng(42)
routes = []
fails = {'stuck': 0, 'fell': 0, 'ok': 0}
walk_fracs = []
for r in range(20):
    a, b = spawns[rng.integers(len(spawns))], spawns[rng.integers(len(spawns))]
    L = float(np.linalg.norm(a[:2] - b[:2]))
    if L < 30:
        continue
    steps_n = int(L / 1.0)
    z = a[2]
    walked = 0
    state = 'ok'
    for sN in range(steps_n):
        p = a + (b - a) * (sN / steps_n)
        pt = np.array([[p[0], p[1], z + 2.0]])
        t, idx = hit_down(pt)
        if not np.isfinite(t[0]):
            pt[0, 2] = z + 30
            t, idx = hit_down(pt)
        if not np.isfinite(t[0]):
            state = 'fell'
            break
        gz = z + 2.0 - t[0]
        if gz < z - 3.0:
            state = 'fell'
            break
        if gz > z + 0.6:
            state = 'stuck'
            break
        z = gz
        walked += 1.0
    fails[state] += 1
    walk_fracs.append(walked / L)
    routes.append((state, walked / L))
print(f'  routes: {len(routes)}, states {dict(fails)}')
print(f'  walkable fraction: median {np.median(walk_fracs)*100:.0f}%, '
      f'mean {np.mean(walk_fracs)*100:.0f}%')
allr = results + [dict(path_test=dict(routes=len(routes), **fails,
                    walkable_median=float(np.median(walk_fracs))))]
json.dump(allr, open('/home/z/my-project/download/s31_t4_probes.json', 'w'),
          indent=1)
print('\nwrote /home/z/my-project/download/s31_t4_probes.json')
