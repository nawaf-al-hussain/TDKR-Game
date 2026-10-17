#!/usr/bin/env python3
"""S32 T3f: walkable prototype hardening — capsule controller with wall
sliding + step handling + slope limit; A* waypoint routes between spawns
(traversability graph from ground probes, NOT straight lines); failure
classification with counts."""
import json, struct, sys, collections, math, heapq
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

SOUP = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'


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
    vtx = raw[:, 2:38].copy().view(np.float32).reshape(ntri, 3, 3).astype(
        np.float64)
    flags = raw[:, 38]
    return vtx, flags


vtx, flags = load_soup(SOUP)
print(f'soup: {len(vtx)} tris')

# --- spatial hash for ray queries ---
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
print(f'hash cells: {len(bucket)}')

v0 = vtx[:, 0]
e1 = vtx[:, 1] - vtx[:, 0]
e2 = vtx[:, 2] - vtx[:, 0]
NRM = np.cross(e1, e2)
NN = np.linalg.norm(NRM, axis=1, keepdims=True)
NRM = NRM / np.where(NN > 1e-12, NN, 1)


def cell_of(x, y):
    return (int((x - cx0) // CELL), int((y - cy0) // CELL))


def ray_hits(O, D, tmax=200.0):
    """O (n,3), D (n,3) normalized; returns (t, idx) with inf/-1 miss.
    Moller-Trumbore against cell buckets."""
    n = len(O)
    t_out = np.full(n, np.inf)
    i_out = np.full(n, -1)
    for j in range(n):
        o, dr = O[j], D[j]
        a, b = cell_of(o[0], o[1])
        a2, b2 = cell_of(o[0] + dr[0] * tmax, o[1] + dr[1] * tmax)
        ca, cb = a, b
        cands = set()
        steps = max(abs(a2 - a), abs(b2 - b)) + 1
        for s2 in range(steps):
            t0 = s2 / steps
            ca = int((o[0] + dr[0] * tmax * t0 - cx0) // CELL)
            cb = int((o[1] + dr[1] * tmax * t0 - cy0) // CELL)
            cands.add((ca, cb))
        idxs = []
        for c in cands:
            if c in bucket:
                idxs.append(bucket[c])
        if not idxs:
            continue
        idx = np.concatenate(idxs)
        p = np.repeat(o[None, :], len(idx), 0)
        e1i = e1[idx]
        e2i = e2[idx]
        pv = np.cross(dr, e2i)
        det = (e1i * pv).sum(1)
        ok = np.abs(det) > 1e-12
        inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
        tv = p - v0[idx]
        u = (tv * pv).sum(1) * inv
        qv = np.cross(tv, e1i)
        v = (np.repeat(dr[None, :], len(idx), 0) * qv).sum(1) * inv
        t = (e2i * qv).sum(1) * inv
        hit = ok & (u >= -1e-6) & (u <= 1 + 1e-6) & \
            (v >= -1e-6) & (u + v <= 1 + 1e-6) & (t > 1e-4) & (t < tmax)
        if hit.any():
            k = np.argmin(np.where(hit, t, np.inf))
            t_out[j] = t[k]
            i_out[j] = idx[k]
    return t_out, i_out


DOWN = np.array([0.0, 0.0, -1.0])


def ground(x, y, from_z=80.0, maxd=200.0):
    t, i = ray_hits(np.array([[x, y, from_z]]), DOWN[None, :], maxd)
    if i[0] < 0:
        return None, None
    return from_z - t[0], int(i[0])


# --- walkable graph over a street-area grid ---
print('building walkable grid...')
X0, X1 = -1500, -200
Y0, Y1 = -1400, -200
STEP = 2.0
nx = int((X1 - X0) / STEP)
ny = int((Y1 - Y0) / STEP)
Z = np.full((nx, ny), np.nan)
FL = np.full((nx, ny), -1, np.int16)
SL = np.full((nx, ny), np.nan)
pts = np.array([[X0 + i * STEP, Y0 + j * STEP, 80.0]
                for i in range(nx) for j in range(ny)])
ts, ii = ray_hits(pts, np.repeat(DOWN[None, :], len(pts), 0), 200.0)
zs = 80.0 - ts
found = ii >= 0
Zm = zs.reshape(nx, ny)
Im = ii.reshape(nx, ny)
valid = found.reshape(nx, ny)
Z[valid] = Zm[valid]
FL[valid] = flags[np.clip(Im[valid], 0, len(flags))]
sl = np.degrees(np.arccos(np.clip(np.abs(NRM[np.clip(Im, 0, len(NRM)), 2]),
                                  0, 1)))
SL[valid] = sl.reshape(nx, ny)[valid]
print(f'ground found: {valid.sum()}/{nx*ny} = {100*valid.mean():.1f}%')

WALKABLE = valid & (SL <= 50) & (~np.isin(FL, [9, 10]))  # not Fence/Stop
print(f'walkable cells (slope<=50, not Fence/Stop): {WALKABLE.sum()} '
      f'({100*WALKABLE.sum()/valid.sum():.1f}% of grounded)')

# neighbor step heights
STEP_OK = np.zeros((nx, ny, 4), bool)
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for i in range(nx):
    for j in range(ny):
        if not WALKABLE[i, j]:
            continue
        for k, (di, dj) in enumerate(DIRS):
            i2, j2 = i + di, j + dj
            if 0 <= i2 < nx and 0 <= j2 < ny and WALKABLE[i2, j2]:
                dz = abs((Z[i2, j2] if valid[i2, j2] else 1e9) -
                         (Z[i, j] if valid[i, j] else 1e9))
                STEP_OK[i, j, k] = dz <= 0.55

np.savez('/tmp/s32_t3_grid.npz', Z=Z, FL=FL, SL=SL, valid=valid,
         WALKABLE=WALKABLE, STEP_OK=STEP_OK, spawns=np.zeros((0, 3)))
print('grid cached (spawns loaded separately)')
import json as _json
tab = _json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in
             _json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
sp = res['census']['spawn']
spawns = np.array([[r['pos'][1], r['pos'][2], r['pos'][3]] for r in sp])
print(f'spawn records: {len(spawns)}')
d2 = np.load('/tmp/s32_t3_grid.npz', allow_pickle=True)
np.savez('/tmp/s32_t3_grid.npz', Z=Z, FL=FL, SL=SL, valid=valid,
         WALKABLE=WALKABLE, STEP_OK=STEP_OK, spawns=spawns)
_json.dump(dict(grid=dict(x0=X0, y0=Y0, step=STEP, nx=nx, ny=ny),
                grounded_frac=float(valid.mean()),
                walkable_frac=float(WALKABLE.sum() / max(valid.sum(), 1))),
           open('/tmp/s32_t3_grid.json', 'w'))
print('grid saved with spawns')
