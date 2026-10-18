#!/usr/bin/env python3
"""S34 T3: navmesh ground validation + adjacency + A* + capsule routes.
Ground check: navmesh tri centroid height vs collision ground below (null:
random street points). Routes: >=30 spawn-to-spawn along navmesh polygons,
capsule follow with slide+step, failure classification."""
import struct, math, json, time
import numpy as np

t0 = time.time()

# ---------- collision soup ----------
col = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin', 'rb').read()
dv = col
nTri = struct.unpack_from('<I', dv, 4)[0]
nObj = struct.unpack_from('<I', dv, 8)[0]
p = 12
nameLen = struct.unpack_from('<I', dv, p)[0]; p += 4 + nameLen
p += nObj * 48
CT = np.frombuffer(col[p:p + nTri * 39], np.uint8).reshape(nTri, 39)
cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
cflags = CT[:, 38]
print(f'collision: {nTri} tris, {nObj} objs, loaded {time.time()-t0:.1f}s')
# axis check: which comp is "up" (small positive spread)
for c in range(3):
    v = cpos[:, :, c]
    print(f'  comp{c}: {v.min():.1f}..{v.max():.1f} median {np.median(v):.2f}')

# navmesh tris (from nmfinal run)
tris = np.load('/home/z/my-project/scripts/s34_t3_nm_tris.npy')
print(f'navmesh: {len(tris)} tris')
