#!/usr/bin/env python3
"""S35 T2a v2: stride-80 vertex-stream sweep, band-criterion edge score
(0.1mm < len <= 25cm), positive control body @0x4b5c, shuffled-vertex and
random-offset nulls, 394/194 cape sizes."""
import struct
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
NBYTES = len(md)

def read_verts(vert_off, nverts):
    V = np.empty((nverts, 3), np.float32)
    for i in range(nverts):
        V[i] = struct.unpack_from('<3f', md, vert_off + i * 80)
    return V

def read_idx(off, n):
    return np.array([struct.unpack_from('<H', md, off + 2 * i)[0] for i in range(n)], np.int64)

body_idx = read_idx(0x210ba, 5655)
cape_idx = read_idx(0x2b7d8, 2006)

def edge_score(vert_off, nverts, idx, lo=1e-4, hi=0.25):
    V = read_verts(vert_off, nverts)
    if not np.all(np.isfinite(V)):
        return -1.0
    a, b = idx[0::3], idx[1::3]
    m = (a < nverts) & (b < nverts)
    if m.sum() < 10:
        return -1.0
    d = np.linalg.norm(V[a[m]] - V[b[m]], axis=1)
    return float(((d > lo) & (d <= hi)).mean())

print('=== positive control: body 1449 v @0x4b5c ===')
print('body real edge-band score:', round(edge_score(0x4b5c, 1449, body_idx), 4))
rng = np.random.default_rng(1)
perm = rng.permutation(1449)
print('body shuffled-vertex null:', round(edge_score(0x4b5c, 1449, perm[np.clip(body_idx, 0, 1448)]), 4))
print('body at zero-run 0x388a0:', round(edge_score(0x388a0, 1449, body_idx), 4))

print('\n=== sweep 394 v (cape idx, max 393) ===')
span = 394 * 80
best = []
for off in range(0x1000, NBYTES - span, 4):
    s = edge_score(off, 394, cape_idx)
    if s > 0.5:
        best.append((round(s, 3), off))
best.sort(reverse=True)
print(f'candidates >0.5: {len(best)}')
for s, off in best[:10]:
    V = read_verts(off, 394)
    print(f'  0x{off:x}: score {s} bbox {V.min(0).round(2)}..{V.max(0).round(2)}')

print('\n=== random-offset null (394 v) ===')
rng2 = np.random.default_rng(9)
nulls = []
for _ in range(200):
    off = int(rng2.integers(0x1000, NBYTES - span - 4)) & ~3
    sc = edge_score(off, 394, cape_idx)
    if sc >= 0:
        nulls.append(sc)
print(f'null: median {np.median(nulls):.3f} p95 {np.quantile(nulls, 0.95):.3f} max {max(nulls):.3f} (n={len(nulls)})')

print('\n=== sweep 194 v (no index buffer known; smoothness criterion) ===')
def smooth194(off):
    V = read_verts(off, 194)
    if not (np.all(np.isfinite(V)) and np.all(np.abs(V) < 10)):
        return -1.0
    if np.all(V == 0):
        return -1.0
    d = np.linalg.norm(np.diff(V, axis=0), axis=1)
    nz = d[d > 1e-5]
    if len(nz) < 50:
        return -1.0
    return float((nz <= 0.25).mean())

span194 = 194 * 80
best194 = []
for off in range(0x1000, NBYTES - span194, 4):
    s = smooth194(off)
    if s > 0.9:
        best194.append((round(s, 3), off))
best194.sort(reverse=True)
print(f'candidates >0.9: {len(best194)}')
for s, off in best194[:10]:
    V = read_verts(off, 194)
    print(f'  0x{off:x}: score {s} bbox {V.min(0).round(2)}..{V.max(0).round(2)}')
rng3 = np.random.default_rng(11)
n194 = []
for _ in range(200):
    off = int(rng3.integers(0x1000, NBYTES - span194 - 4)) & ~3
    sc = smooth194(off)
    if sc >= 0:
        n194.append(sc)
print(f'null: median {np.median(n194) if n194 else -1:.3f} p95 {np.quantile(n194, 0.95) if n194 else -1:.3f} (n={len(n194)})')

print('\n=== zero-run recheck ===')
for off, nv in ((0x388a0, 1449), (0x5cc24, 394), (0x6901c, 194)):
    V = read_verts(off, nv)
    print(f'  0x{off:x} ({nv}v): all-zero pos = {bool(np.all(V == 0))}')
