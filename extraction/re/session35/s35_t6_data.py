#!/usr/bin/env python3
"""S35 T6a: extract a playable patch — collision tris near the demo area
(spawn [-140.7,-681.2] .. batcave trigger [-243.5,-691.1]), nearby triggers,
and the walkable-cell grid — as compact JSON for the playable page."""
import struct, json
import numpy as np

col = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin', 'rb').read()
nTri = struct.unpack_from('<I', col, 4)[0]
nObj = struct.unpack_from('<I', col, 8)[0]
p = 12
nameLen = struct.unpack_from('<I', col, p)[0]; p += 4 + nameLen + nObj * 48
CT = np.frombuffer(col[p:p + nTri * 39], np.uint8).reshape(nTri, 39)
cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
cflags = CT[:, 38].astype(np.int32)
WALK = np.isin(cflags, [0, 1, 5, 6])
cent = cpos.mean(axis=1)
# demo area: around [-190, -686] radius 160 m
cx, cy = -190.0, -686.0
R = 160.0
m = (np.abs(cent[:, 0] - cx) < R) & (np.abs(cent[:, 1] - cy) < R)
sel = np.flatnonzero(m)
patch = cpos[sel].reshape(-1, 3)
flags = cflags[sel]
print(f'collision patch: {len(sel)}/{nTri} tris, {len(patch)} verts, '
      f'z {patch[:,2].min():.1f}..{patch[:,2].max():.1f}')

D = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
trigs = []
for t in D['triggers']:
    f = t['f9']
    if abs(f[0] - cx) < R and abs(f[1] - cy) < R:
        trigs.append(dict(id=t['rec_id'], pos=[round(v, 3) for v in f[:3]],
                          rot=[round(v, 2) for v in f[3:6]],
                          scale=[round(v, 3) for v in f[6:9]],
                          fn=t.get('fn'), script=(t.get('script') or '')[:4000],
                          has_script=bool(t.get('script'))))
print(f'nearby triggers: {len(trigs)} ({sum(1 for t in trigs if t["has_script"])} with scripts)')

GD = json.load(open('/home/z/my-project/scripts/s33_gcdata.json'))
spawns = [s for s in GD['spawns'] if abs(s['pos'][0] - cx) < R and abs(s['pos'][1] - cy) < R]
print(f'nearby spawns: {len(spawns)}; first: {spawns[0] if spawns else None}')

out = dict(center=[cx, cy], R=R,
           tris=dict(n=len(sel), flat=[round(float(v), 3) for v in patch.ravel()],
                     flags=flags.tolist()),
           triggers=trigs,
           spawns=[dict(id=s['id'], name=s['name'], pos=[round(v, 3) for v in s['pos']]) for s in spawns[:40]])
json.dump(out, open('/home/z/my-project/scripts/s35_t6_patch.json', 'w'))
print('patch json:', len(json.dumps(out)) // 1024, 'KB')
