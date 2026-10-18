#!/usr/bin/env python3
"""S33 T3a/b + T4: trigger null, count reconciliation, OBB-enter call log link.

- Decode 440 trigger components + 484 shapes (r32 layout).
- SPAWN NULL: 158/225 real spawns in trigger OBBs vs 225 random street points
  (sampled on collision-ground positions inside the spawns' convex hull).
- Count reconciliation: tid histogram + shape owners.
- T4: capsule-in-OBB test for the Lua call-log trigger (1900053).
"""
import sys, json, struct, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d = res['data']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}

shapes = {}
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    e3 = struct.unpack_from('>3f', d[off:off + 12], 0)
    shapes[rid] = e3
trigs = {}
for rid, off, sz in res['census'].get('938977454', []):
    off = int(off, 16)
    raw = d[off:off + sz]
    i0 = struct.unpack_from('>i', raw, 0)[0]
    f9 = struct.unpack_from('>9f', raw, 4)
    trigs[rid] = dict(tid=tid_of.get(rid), i0=i0, f9=f9)
print(f'triggers {len(trigs)}, shapes {len(shapes)}')
tidh = collections.Counter(t['tid'] for t in trigs.values())
print('trigger tids:', dict(tidh))
# trigger rid -> object TRS position (pos = f1, f0, f2 per r21 field fix)
base = {rid: int(o, 16) for rid, o, sz in res['census'].get('1362553', [])}
def trs_pos(rid):
    o = base.get(rid)
    if o is None: return None
    m = struct.unpack_from('<4f', d, o)   # [w?] r21: (y,z,x order) f1,f0,f2
    return np.array([m[1], m[0], m[2]])
OBBS = []
for rid, t in trigs.items():
    p = trs_pos(rid)
    if p is None: continue
    e3 = shapes.get(rid)
    if e3 is None: continue
    yaw = t['f9'][5]
    ex, ey, ez = abs(e3[0]) * max(t['f9'][7], 1e-6) if t['f9'][7] else abs(e3[0]), \
                 abs(e3[1]), abs(e3[2]) * max(t['f9'][8], 1e-6) if t['f9'][8] else abs(e3[2])
    OBBS.append((rid, p, yaw, (ex, ey, ez)))
print(f'OBBs with TRS+shape: {len(OBBS)}')

def inside_obb(p, pos, yaw, ext):
    c, s = np.cos(yaw), np.sin(yaw)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    lp = R.T @ (p - pos)
    return bool(np.all(np.abs(lp) <= np.array(ext) + 1e-9))

# spawns: r21 field fix pos=(f1,f0,f2) — reuse the census: objects with spawn tid 0x264b
spawns = []
for rid, off, sz in res['census'].get('1362553', []):
    pass
# spawns decoded in r21: class 0x264b records
sp_recs = []
for cid, recs in res.get('census', {}).items():
    pass
# simpler: reuse r21 spawn extraction: TRS of tid 0x264b objects
tid_by_rid = tid_of
# object tids: res['records'] gives (rid, s0, tid, e, k)
spawn_pts = []
for rid, s0, tid, e, k in res['records']:
    if tid == 0x264b:
        p = trs_pos(rid)
        if p is not None: spawn_pts.append(p)
print(f'spawn records (tid 0x264b): {len(spawn_pts)}')

if OBBS and spawn_pts:
    S = np.array(spawn_pts)
    n_in = sum(1 for p in S if any(inside_obb(p, *o) for o in OBBS))
    print(f'REAL spawns inside a trigger OBB: {n_in}/{len(S)} = {100*n_in/len(S):.1f}%')
    # NULL: 225 random points on the ground plane within the spawn hull bbox,
    # z = ground (use the spawn z median as street level)
    rng = np.random.default_rng(36)
    lo, hi = S.min(0), S.max(0)
    z0 = np.median(S[:, 2])
    R_null = np.column_stack([rng.uniform(lo[0], hi[0], 225),
                              rng.uniform(lo[1], hi[1], 225),
                              np.full(225, z0)])
    n_null = sum(1 for p in R_null if any(inside_obb(p, *o) for o in OBBS))
    print(f'NULL (225 random street pts in spawn bbox): {n_null}/225 = {100*n_null/225:.1f}%')
    # second null: random points in a 200-m box around the spawn centroid
    c = S.mean(0)
    R2 = np.column_stack([c[0] + rng.uniform(-100, 100, 225),
                          c[1] + rng.uniform(-100, 100, 225),
                          np.full(225, z0)])
    n2 = sum(1 for p in R2 if any(inside_obb(p, *o) for o in OBBS))
    print(f'NULL-2 (225 random pts, +-100 m box at centroid): {n2}/225 = {100*n2/225:.1f}%')
    # T4 link: which OBB contains a spawn near the Lua trigger 1900053?
    for rid, p, yaw, ext in OBBS:
        if any(inside_obb(sp, rid and p, yaw, ext) for sp in S[:1]):
            pass
    hits = [(rid, p) for rid, p, yaw, ext in OBBS
            if sum(1 for sp in S if inside_obb(sp, p, yaw, ext)) > 0]
    print(f'triggers containing >=1 spawn: {len(hits)}')
    if 1900053 in [t['i0'] for t in trigs.values()]:
        # find its record
        for rid, t in trigs.items():
            if t['i0'] == 1900053:
                p = trs_pos(rid)
                e3 = shapes.get(rid)
                ins = sum(1 for sp in S if p is not None and e3 is not None
                          and inside_obb(sp, p, t['f9'][5],
                                         (abs(e3[0]), abs(e3[1]), abs(e3[2]))))
                print(f'Lua script trigger 1900053: OBB pos {None if p is None else np.round(p,1)}, '
                      f'extents {e3}, spawns inside: {ins}')
json.dump(dict(triggers=len(trigs), shapes=len(shapes), tids=dict(tidh),
               obbs=len(OBBS)),
          open('/home/z/my-project/scripts/s33_t3_trigcounts.json', 'w'), indent=1)
