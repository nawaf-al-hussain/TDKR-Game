#!/usr/bin/env python3
"""S30 T4 numbers (v2): grid-bucketed probe rays — no OOM."""
import json, struct, collections
import numpy as np

BIN = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'
d = open(BIN, 'rb').read()
assert d[:4] == b'TCS1'
ntri, nobj = struct.unpack_from('<II', d, 4)
name_len = struct.unpack_from('<I', d, 12)[0]
nameblob = d[16:16+name_len]
pos = 16 + name_len
for _ in range(nobj):
    noff, nlen, oid, ntri_o = struct.unpack_from('<IHHI', d, pos); pos += 12
    pos += 36
rec = struct.calcsize('<H9fB')
raw = np.frombuffer(d, dtype=np.uint8, offset=pos).reshape(ntri, rec)
vtx = raw[:, 2:38].copy().view(np.float32).reshape(ntri, 3, 3).astype(np.float64)
flags = raw[:, 38]

print(f'soup: {ntri} triangles, {nobj} objects')
print(f'bbox: min {vtx.reshape(-1,3).min(0).round(1)} max {vtx.reshape(-1,3).max(0).round(1)}')
u, c = np.unique(flags, return_counts=True)
print('material-flag histogram:', {int(a): int(b) for a, b in zip(u, c)})

# spatial buckets on (x, y), 20 m cells
CELL = 20.0
cx0, cy0 = vtx[:, :, 0].min(), vtx[:, :, 1].min()
gx_ = ((vtx[:, :, 0] - cx0) // CELL).astype(np.int32)
gy_ = ((vtx[:, :, 1] - cy0) // CELL).astype(np.int32)
gx_min = gx_.min(1); gx_max = gx_.max(1)
gy_min = gy_.min(1); gy_max = gy_.max(1)
bucket = collections.defaultdict(list)
for i in range(ntri):
    for a in range(gx_min[i], gx_max[i]+1):
        for b in range(gy_min[i], gy_max[i]+1):
            bucket[(a, b)].append(i)
bucket = {k: np.array(v) for k, v in bucket.items()}
print('buckets:', len(bucket))

v0, e1, e2 = vtx[:, 0], vtx[:, 1] - vtx[:, 0], vtx[:, 2] - vtx[:, 0]

def hit_down(O):
    """ray (x,y,z)->(x,y,-inf): returns t (positive down-distance) or inf"""
    out = np.full(len(O), np.inf)
    dirv = np.array([0.0, 0.0, -1.0])
    for j, o in enumerate(O):
        key = (int((o[0]-cx0)//CELL), int((o[1]-cy0)//CELL))
        idx = bucket.get(key)
        if idx is None or len(idx) == 0:
            continue
        v0i = v0[idx]; e1i = e1[idx]; e2i = e2[idx]
        h = np.cross(dirv, e2i)
        a = (e1i * h).sum(1)
        ok = np.abs(a) > 1e-12
        f = np.where(ok, 1.0/np.where(ok, a, 1), 0.0)
        s = o - v0i
        uu = f * (s * h).sum(1)
        q = np.cross(s[:, None, :], e1i)[:, 0, :] if False else np.cross(s, e1i)
        vv = f * (q * dirv).sum(1)
        t = f * (q * e2i).sum(1)
        hit = ok & (uu >= 0) & (vv >= 0) & (uu + vv <= 1) & (t > 0)
        if hit.any():
            out[j] = t[hit].min()
    return out

# 100 m street grid at the spawn centroid
import re
gcj = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_data.js').read()
i = gcj.find('spawns":[')
depth = 0; j = gcj.find('[', i)
for k2 in range(j, len(gcj)):
    if gcj[k2] == '[': depth += 1
    elif gcj[k2] == ']':
        depth -= 1
        if depth == 0: break
spawns = json.loads(gcj[j:k2+1])
S = np.array([s['pos'] for s in spawns])
scx, scy = np.median(S[:, 0]), np.median(S[:, 1])
print(f'spawn centroid ({scx:.0f}, {scy:.0f}); spawns {len(S)}')
xs = np.linspace(scx-50, scx+50, 21)
ys = np.linspace(scy-50, scy+50, 21)
gx, gy = np.meshgrid(xs, ys)
origins = np.stack([gx.ravel(), gy.ravel(), np.full(gx.size, 20.0)], 1)
tmin = hit_down(origins)
hit = tmin < 22.0
print(f'probe rays 21x21 (100 m grid): {len(origins)}, ground found: '
      f'{int(hit.sum())} ({100*hit.mean():.1f}%)   [r19 visual-GLB: 42.9%]')
gz = 20.0 - tmin
print(f'ground z median {np.median(gz[hit]):.2f}, range [{gz[hit].min():.2f}, {gz[hit].max():.2f}]')
miss = [(round(float(x),1), round(float(y),1)) for x, y, h in
        zip(origins[:,0], origins[:,1], ~hit) if h]
print(f'failures ({len(miss)}):', miss[:10])

# material histogram under the player path = under probes
hit_idx = []
for j, o in enumerate(origins):
    if tmin[j] >= 22: continue
    key = (int((o[0]-cx0)//CELL), int((o[1]-cy0)//CELL))
    idx = bucket.get(key)
    if idx is None: continue
    v0i = v0[idx]; e1i = e1[idx]; e2i = e2[idx]
    dirv = np.array([0.0, 0.0, -1.0])
    h = np.cross(dirv, e2i)
    a = (e1i * h).sum(1)
    ok = np.abs(a) > 1e-12
    f = np.where(ok, 1.0/np.where(ok, a, 1), 0.0)
    s = o - v0i
    uu = f * (s * h).sum(1)
    q = np.cross(s, e1i)
    vv = f * (q * dirv).sum(1)
    t = f * (q * e2i).sum(1)
    hitm = ok & (uu >= 0) & (vv >= 0) & (uu + vv <= 1) & (t > 0)
    if hitm.any():
        tt = np.where(hitm, t, np.inf)
        hit_idx.append(idx[tt.argmin()])
u2, c2 = np.unique(flags[hit_idx], return_counts=True)
print('material-flag histogram under probes:',
      {int(a): int(b) for a, b in zip(u2, c2)})

# spawn validation
O2 = np.stack([S[:, 0], S[:, 1], S[:, 2] + 2.0], 1)
t2 = hit_down(O2)
on = t2 <= 3.0
print(f'spawn ground check: {int(on.sum())}/{len(O2)} spawns have ground within 3 m '
      f'({100*on.mean():.1f}%)')
