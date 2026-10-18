#!/usr/bin/env python3
"""S36 T2-final: data-determined trigger volumes (CTriggerShapeAABB model:
half-extent = 0.5 * BuiltinBox.size * ownerScale, height=0.5*size.z*scale.z,
rot mostly 0) vs r25's assumed-B disc model. Nulls: 225 spawns + 2000 street
points; independent sets; report data-determined vs assumed parts.
Also emit an updated trigger volume table for the playable page."""
import sys, json, math, random, struct
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

random.seed(3612)
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab, templates, None)
d, strings = res['data'], res['strings']

boxes = []
for rid, off, sz in res['census'].get('1923007858', []):
    o = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = o
    try:
        f = [rr.tok('f') for _ in range(3)]
    except Exception:
        continue
    boxes.append(f)
boxes = np.array(boxes)
frac1 = float(np.mean(np.all(np.isclose(boxes, 1.0), axis=1)))
print(f'boxes={len(boxes)} all-1.0 fraction={frac1:.3f} median={np.median(boxes, axis=0)}')

trigs = []
for rid, off, sz in res['census'].get('938977454', []):
    o = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = o
    try:
        i0 = rr.tok('i')
        f9 = [rr.tok('f') for _ in range(9)]
    except Exception:
        continue
    trigs.append({'rec_id': int(rid) if not isinstance(rid, int) else rid, 'obj': i0,
                  'pos': f9[:3], 'rot': f9[3:6], 'scale': f9[6:9]})
print(f'triggers={len(trigs)}')
nonuni = sum(1 for t in trigs if any(abs(s - 1.0) > 1e-4 for s in t['rot']))
print(f'triggers with nonzero rotation: {nonuni}/{len(trigs)}')

# volumes: data-determined model (size=median box per record is unknown per
# trigger without object linkage -> use per-trigger scale x {size p50=1,1,1};
# ALSO the size distribution for sensitivity: p50/p75)
def vol_real(t, size=(1.0, 1.0, 1.0)):
    sx, sy, sz_ = t['scale']
    return (0.5 * size[0] * sx, 0.5 * size[1] * sy, 0.5 * size[2] * sz_)

hx = np.array([vol_real(t)[0] for t in trigs])
hy = np.array([vol_real(t)[1] for t in trigs])
hz = np.array([vol_real(t)[2] for t in trigs])
print(f'real-model half-extents m: hx pcts {np.percentile(hx, [50, 90, 99]).round(2)}, '
      f'hy {np.percentile(hy, [50, 90, 99]).round(2)}, hz {np.percentile(hz, [50, 90, 99]).round(2)}')

# null sets
GD = json.load(open('/home/z/my-project/scripts/s33_gcdata.json'))
spawns = [s['pos'] for s in GD['spawns']]
print('spawns:', len(spawns))
# street points: from collision ground (r25 method)
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
street_tris = cent[(WALK) & (cent[:, 2] < 5.0) & (np.abs(cent[:, 0]) < 1700) & (np.abs(cent[:, 1]) < 1400)]
rng = np.random.default_rng(36)
sel = rng.choice(len(street_tris), 2000)
street = street_tris[sel] + rng.normal(0, 1.5, (2000, 3))
print('street points:', len(street))

def inside_real(pos, t, size=(1.0, 1.0, 1.0)):
    hxv, hyv, hzv = vol_real(t, size)
    dx = abs(pos[0] - t['pos'][0]); dy = abs(pos[1] - t['pos'][1]); dz = abs(pos[2] - t['pos'][2])
    return dx <= hxv and dy <= hyv and dz <= hzv + 1.0  # +1 m feet tolerance

def inside_disc(pos, t, B):
    r = B * t['scale'][0]
    return math.hypot(pos[0] - t['pos'][0], pos[1] - t['pos'][1]) <= r

for name, pts in (('spawns', spawns), ('street', street)):
    r_real = sum(any(inside_real(pt, t) for t in trigs) for pt in pts) / len(pts)
    r_d1 = sum(any(inside_disc(pt, t, 1.0) for t in trigs) for pt in pts) / len(pts)
    r_d2 = sum(any(inside_disc(pt, t, 2.0) for t in trigs) for pt in pts) / len(pts)
    print(f'{name:7s}: real-model {r_real*100:.1f}% | disc B=1 {r_d1*100:.1f}% | B=2 {r_d2*100:.1f}%')

# nearest-trigger distance per set (real model)
def nearest(pt):
    best = 1e18
    for t in trigs:
        h = vol_real(t)
        dx = max(abs(pt[0] - t['pos'][0]) - h[0], 0)
        dy = max(abs(pt[1] - t['pos'][1]) - h[1], 0)
        dd = math.hypot(dx, dy)
        if dd < best: best = dd
    return best
nd_s = sorted(nearest(pt) for pt in spawns)
nd_t = sorted(nearest(pt) for pt in street[::10])
print(f'nearest-trigger dist: spawns median {nd_s[len(nd_s)//2]:.1f} m, within 2 m: {sum(1 for x in nd_s if x < 2)/len(nd_s)*100:.1f}%')
print(f'                      street  median {nd_t[len(nd_t)//2]:.1f} m, within 2 m: {sum(1 for x in nd_t if x < 2)/len(nd_t)*100:.1f}%')

# also: triggers with scale x huge (city-scale)
big = [t for t in trigs if t['scale'][0] > 50]
print(f'city-scale triggers (scale>50): {len(big)}')

# emit volume table for the page (patch area triggers with real volumes)
out = []
for t in trigs:
    h = vol_real(t)
    out.append({'id': t['obj'], 'pos': [round(v, 3) for v in t['pos']],
                'rot': [round(v, 2) for v in t['rot']],
                'scale': [round(v, 3) for v in t['scale']],
                'half': [round(h[0], 3), round(h[1], 3), round(h[2], 3)]})
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t2_volumes.json', 'w'))
print('volume table written:', len(out))
