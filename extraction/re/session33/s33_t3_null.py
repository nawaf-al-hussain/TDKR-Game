#!/usr/bin/env python3
"""S33 T3a/b: spawn-in-trigger NULL + count reconciliation (self-contained)."""
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
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
base = {rid: int(o, 16) for rid, o, sz in res['census'].get('1362553', [])}

def read_trs9(rid):
    if rid not in base: return None
    rr = lvc_pure.Reader(d, strings)
    rr.p = base[rid]
    bt = []
    try:
        rr.tok('c', out=bt); rr.tok('i', out=bt)
        for _ in range(9): rr.tok('f', out=bt)
        rr.tok('c', out=bt); rr.tok('c', out=bt); rr.tok('c', out=bt)
    except Exception:
        return None
    return [t[3] for t in bt if t[0] == 'f']

# shapes (484): BE extents
shapes = {}
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    shapes[rid] = struct.unpack_from('>3f', d[off:off + 12], 0)
# triggers (440)
trigs = {}
for rid, off, sz in res['census'].get('938977454', []):
    off = int(off, 16)
    raw = d[off:off + sz]
    i0 = struct.unpack_from('>i', raw, 0)[0]
    f9 = struct.unpack_from('>9f', raw, 4)
    trigs[rid] = dict(tid=tid_of.get(rid), i0=i0, f9=f9)
tidh = collections.Counter(t['tid'] for t in trigs.values())

# spawns: prototype-embedded (gc_data.js, r29 pipeline from GothamCity.lvc)
GD = json.load(open('/home/z/my-project/scripts/s33_gcdata.json'))
spawn_pts = [np.array(s['pos']) for s in GD['spawns']]
n9826 = len(spawn_pts)
print(f'spawns (prototype gc_data): {n9826}')
S = np.array(spawn_pts)
if len(S) > 5:
    print(f'spawn pos spread: x [{S[:,0].min():.1f},{S[:,0].max():.1f}] '
          f'y [{S[:,1].min():.1f},{S[:,1].max():.1f}] z [{S[:,2].min():.1f},{S[:,2].max():.1f}]')

# OBBs: center = f9[1:4], yaw = f9[5], H = f9[6], scale = f9[7]/f9[8],
# half-extents = shape * scale (r32 formula)
OBBS = []
for rid, t in trigs.items():
    e3 = shapes.get(rid)
    if e3 is None: continue
    f9 = t['f9']
    pos = np.array(f9[1:4])
    yaw = f9[5]
    ex = abs(e3[0]) * max(abs(f9[7]), 1e-6) if abs(f9[7]) > 1e-6 else abs(e3[0])
    ey = abs(e3[1])
    ez = abs(e3[2]) * max(abs(f9[8]), 1e-6) if abs(f9[8]) > 1e-6 else abs(e3[2])
    if min(ex, ey, ez) <= 0 or max(ex, ey, ez) > 3000: continue
    OBBS.append((rid, pos, yaw, (ex, ey, ez)))
print(f'plausible OBBs: {len(OBBS)}')

def inside(p, o):
    _, pos, yaw, ext = o
    c, s = np.cos(yaw), np.sin(yaw)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    lp = R.T @ (p - pos)
    return bool(np.all(np.abs(lp) <= np.array(ext)))

if len(S) and OBBS:
    n_in = sum(1 for p in S if any(inside(p, o) for o in OBBS))
    print(f'\nREAL spawns inside a trigger OBB: {n_in}/{len(S)} = {100*n_in/len(S):.1f}%')
    rng = np.random.default_rng(36)
    lo, hi = S.min(0), S.max(0)
    z0 = float(np.median(S[:, 2]))
    N1 = np.column_stack([rng.uniform(lo[0], hi[0], len(S)),
                          rng.uniform(lo[1], hi[1], len(S)),
                          np.full(len(S), z0)])
    n1 = sum(1 for p in N1 if any(inside(p, o) for o in OBBS))
    print(f'NULL-1 (random street pts, spawn bbox, z=street): {n1}/{len(S)} = {100*n1/len(S):.1f}%')
    c = S.mean(0)
    N2 = np.column_stack([c[0] + rng.uniform(-100, 100, len(S)),
                          c[1] + rng.uniform(-100, 100, len(S)),
                          np.full(len(S), z0)])
    n2 = sum(1 for p in N2 if any(inside(p, o) for o in OBBS))
    print(f'NULL-2 (random pts, +-100 m at centroid): {n2}/{len(S)} = {100*n2/len(S):.1f}%')
    per = [sum(1 for p in S if inside(p, o)) for o in OBBS]
    print(f'triggers containing >=1 spawn: {sum(1 for x in per if x > 0)}/{len(OBBS)}')
    # T4 link: trigger with fn Obj1900053_OnEnter — capsule-enter test
    for rid, t in trigs.items():
        if t['i0'] == 13983 or abs((t['f9'][1] + 243.51)) < 0.5:
            e3 = shapes.get(rid)
            o = [o for o in OBBS if o[0] == rid]
            ins = sum(1 for sp in S if o and inside(sp, o[0]))
            print(f'\nLua-logged trigger 1900053 (proto id 13983 pos [-243.5,-691.1,-0.2]): '
                  f'rid {rid}, f9 pos {np.round(t["f9"][1:4], 2)}, shape {e3}, '
                  f'spawns inside its OBB: {ins}')

out = dict(n_triggers=len(trigs), n_shapes=len(shapes),
           tid_hist={str(k): v for k, v in tidh.items()},
           n_spawn_objects=n9826, spawn_pts=len(spawn_pts), obbs=len(OBBS))
if len(S) and OBBS:
    out.update(real_pct=100*n_in/len(S), null1_pct=100*n1/len(S),
               null2_pct=100*n2/len(S))
json.dump(out, open('/home/z/my-project/scripts/s33_t3_null.json', 'w'), indent=1)
print('wrote s33_t3_null.json')
