#!/usr/bin/env python3
"""S34 T3 FINAL navmesh decode: robust clean-triangle boundary; triangles;
ground validation vs collision with random null; edge adjacency."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
fa = np.frombuffer(d[2:2 + (N - 2) // 4 * 4], '>f4').astype(np.float64)
T = len(fa) // 3
tr = fa[:T * 3].reshape(T, 3)

# city bbox from collision (r21): use generous bounds; z up
def tri_ok(t):
    return (t[:, 2] > -60) & (t[:, 2] < 450) & \
           (np.abs(t[:, 0]) < 2000) & (np.abs(t[:, 1]) < 2000) & \
           np.isfinite(t).all(axis=1)
okv = tri_ok(tr)
# windowed boundary: first index where a 12-tri window has >= 4 bad
badw = np.convolve((~okv).astype(int), np.ones(12, int), 'valid') >= 4
b = int(np.argmax(badw)) if badw.any() else int(okv.sum())
print(f'clean triangle prefix: {b} tris (byte {2 + 4*3*b})')
tris = tr[:b]
V = tris.reshape(-1, 3)
print(f'triangles {b}, vertices {len(V)}')
print(f'x {V[:,0].min():.1f}..{V[:,0].max():.1f}; y {V[:,1].min():.1f}..{V[:,1].max():.1f}; '
      f'z(up) {V[:,2].min():.2f}..{V[:,2].max():.2f} median {np.median(V[:,2]):.2f}')
z_hist, edges = np.histogram(V[:, 2], bins=[-50, 0, 10, 20, 25, 30, 40, 60, 100, 200, 450])
print('z(up) histogram:', dict(zip([f'{e:.0f}' for e in edges[:-1]], z_hist.tolist())))
np.save('/home/z/my-project/scripts/s34_t3_nm_tris.npy', tris)

# ---- ground validation vs collision ----
C = '/home/z/my-project/work/TDKR-Game/extraction/re/session31/gc_collision.bin'
import os
if not os.path.exists(C):
    C = '/tmp/my-project/work/TDKR-Game/extraction/re/session31/gc_collision.bin'
col = open(C, 'rb').read()
ntri = struct.unpack_from('<I', col, 0)[0] if len(col) > 4 else 0
print(f'\ncollision file: {len(col)} B')
# gc_collision.bin format from r21: tri count + tris (floats)? inspect
head = struct.unpack_from('<4I', col, 0)
print('collision head u32s:', head)
