#!/usr/bin/env python3
"""S32 T3i: corrected grid probes (from_z=400), no-step A* recheck,
spawn-in-trigger verification."""
import json, struct, sys, collections, math, heapq
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

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
gxb = ((vtx[:, :, 0] - cx0) // CELL).astype(np.int32)
gyb = ((vtx[:, :, 1] - cy0) // CELL).astype(np.int32)
bucket = collections.defaultdict(list)
for i in range(len(vtx)):
    for a in range(gxb[i].min(), gxb[i].max() + 1):
        for b in range(gyb[i].min(), gyb[i].max() + 1):
            bucket[(a, b)].append(i)
bucket = {k: np.array(v) for k, v in bucket.items()}


def cell_of(x, y):
    return (int((x - cx0) // CELL), int((y - cy0) // CELL))


def ray_batch(O, D, tmax=400.0):
    n = len(O)
    t_out = np.full(n, np.inf)
    i_out = np.full(n, -1)
    for j in range(n):
        o, dr = O[j], D[j]
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
            continue
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
        if hit.any():
            k = int(np.argmin(np.where(hit, t, np.inf)))
            t_out[j] = t[k]
            i_out[j] = idx[k]
    return t_out, i_out


DOWN = np.array([0.0, 0.0, -1.0])

# ---- 1. corrected grid probes (5 grids, 21x21, from z=400) ----
D = np.load('/tmp/s32_t3_grid.npz', allow_pickle=True)
spawns = D['spawns']
buck = collections.Counter()
for s in spawns:
    buck[(int(s[0] // 200), int(s[1] // 200))] += 1
top5 = [b for b, _ in buck.most_common(5)]
grids = []
for k, (bx, by) in enumerate(top5):
    cx, cy = bx * 200 + 100, by * 200 + 100
    xs = np.linspace(cx - 50, cx + 50, 21)
    ys = np.linspace(cy - 50, cy + 50, 21)
    pts = np.array([[x, y, 400.0] for x in xs for y in ys])
    ts, ii = ray_batch(pts, np.repeat(DOWN[None, :], len(pts), 0), 450.0)
    zf = 400.0 - ts
    fl = np.where(ii >= 0, TRI_FLAGS[np.clip(ii, 0, len(TRI_FLAGS))], -1)
    sl = np.where(ii >= 0,
                  np.degrees(np.arccos(np.clip(
                      np.abs(NRM[np.clip(ii, 0, len(ii)), 2]), 0, 1))), -1)
    found = ii >= 0
    fails = collections.Counter()
    holes_xy = []
    G = found.reshape(21, 21)
    for a in range(21):
        for b in range(21):
            if not G[a, b]:
                nb = [G[max(0, a + da):a + da + 1, max(0, b + db):b + db + 1]
                      for da in (-2, -1, 0, 1, 2) for db in (-2, -1, 0, 1, 2)
                      if (da, db) != (0, 0)]
                ng = sum(int(g.sum()) for g in nb if g.size)
                if ng >= 12:
                    fails['missing_data'] += 1
                else:
                    fails['hole'] += 1
                    holes_xy.append([round(float(xs[a]), 1),
                                     round(float(ys[b]), 1)])
            elif sl[a * 21 + b] > 60:
                fails['wall_face'] += 1
            elif fl[a * 21 + b] in (9, 10):
                fails['fence_stop'] += 1
    fr = 100 * found.mean()
    print(f'grid {k} @({cx},{cy}) z400: ground {fr:.1f}%  fails {dict(fails)}')
    grids.append(dict(tag=f'GC-{k}', cx=cx, cy=cy, ground_frac=fr,
                      fails=dict(fails), holes=holes_xy[:40]))

# ---- 2. spawn-in-trigger verification ----
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in
             json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
shapes = {}
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    shapes[rid] = struct.unpack_from('>3f', d, off)
trigs = []
for rid, off, sz in res['census'].get('938977454', []):
    off = int(off, 16)
    f9 = struct.unpack_from('>9f', d, off + 4)
    if rid in shapes:
        trigs.append(dict(rid=rid, pos=f9[0:3], yaw=f9[5], H=f9[6],
                          sx=f9[7], sz=f9[8], e=shapes[rid],
                          tid=tid_of.get(rid)))
n_in = 0
pair_examples = []
for s in spawns:
    for t in trigs:
        e = t['e']
        hx = e[0] * max(t['sx'], 0.01)
        hz = e[2] * max(t['sz'], 0.01)
        hy = e[1]
        dx, dy, dz = s[0] - t['pos'][0], s[1] - t['pos'][1], s[2] - t['pos'][2]
        ca, sa = math.cos(math.radians(t['yaw'])), \
            math.sin(math.radians(t['yaw']))
        lx = ca * dx + sa * dy
        ly = -sa * dx + ca * dy
        if abs(lx) <= hx and abs(ly) <= hz and abs(dz) <= hy:
            n_in += 1
            if len(pair_examples) < 5:
                pair_examples.append(dict(
                    spawn=[round(float(x), 2) for x in s],
                    trig_rid=t['rid'], tid=t['tid'],
                    ext=[round(float(e[0] * t['sx']), 1),
                         round(float(e[1]), 1), round(float(e[2] * t['sz']), 1)],
                    H=round(float(t['H']), 2)))
            break
print(f'\nspawns inside a trigger OBB: {n_in}/{len(spawns)}')
print('examples:', json.dumps(pair_examples[:3], indent=0)[:400])
json.dump(dict(grids=grids, spawn_in_trigger=n_in,
               n_spawns=int(len(spawns)), examples=pair_examples),
          open('/home/z/my-project/download/s32_t3_grids.json', 'w'))
print('wrote s32_t3_grids.json')
