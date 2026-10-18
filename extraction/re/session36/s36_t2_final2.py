#!/usr/bin/env python3
"""S36 T2-final2: split small (scale<10) vs large (>=10) triggers; z-aware
entry test; spawns vs city-wide street points; compare conventions."""
import sys, json, math, struct
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab, templates, None)
d, strings = res['data'], res['strings']
trigs = []
for rid, off, sz in res['census'].get('938977454', []):
    o = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = o
    i0 = rr.tok('i')
    f9 = [rr.tok('f') for _ in range(9)]
    trigs.append({'obj': i0, 'pos': f9[:3], 'rot': f9[3:6], 'scale': f9[6:9]})

small = [t for t in trigs if t['scale'][0] < 10]
large = [t for t in trigs if t['scale'][0] >= 10]
print(f'triggers: small(scale<10)={len(small)} large={len(large)}')

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
street = street_tris[rng.choice(len(street_tris), 2000)] + rng.normal(0, 1.5, (2000, 3))
GD = json.load(open('/home/z/my-project/scripts/s33_gcdata.json'))
spawns = [s['pos'] for s in GD['spawns']]

def inside(t, pt, zconv):
    hxv = 0.5 * t['scale'][0]; hyv = 0.5 * t['scale'][1]; hzv = 0.5 * t['scale'][2]
    if abs(pt[0] - t['pos'][0]) > hxv or abs(pt[1] - t['pos'][1]) > hyv:
        return False
    dz = pt[2] - t['pos'][2]
    if zconv == 'center': return abs(dz) <= hzv + 0.75
    if zconv == 'up':     return -0.75 <= dz <= 2 * hzv + 0.75
    return True

for zc in ('center', 'up'):
    rs = sum(any(inside(t, pt, zc) for t in small) for pt in spawns) / len(spawns)
    rt = sum(any(inside(t, pt, zc) for t in small) for pt in street) / len(street)
    print(f'SMALL triggers [{zc}]: spawns-in {rs*100:.1f}% | street-in {rt*100:.1f}% | ratio {"inf" if rt==0 else rs/rt:.0f}x')

# large: coverage of street (x/y only + any z)
cov = sum(any(abs(pt[0]-t['pos'][0]) <= 0.5*t['scale'][0] and abs(pt[1]-t['pos'][1]) <= 0.5*t['scale'][1] for t in large) for pt in street) / len(street)
print(f'LARGE triggers: street x/y coverage {cov*100:.1f}% (district zones), scales p50/p95 = '
      f'{np.percentile([t["scale"][0] for t in large], [50, 95]).round(1)}')
# small: nearest distance
def nearest_small(pt):
    best = 1e18
    for t in small:
        dx = max(abs(pt[0] - t['pos'][0]) - 0.5 * t['scale'][0], 0)
        dy = max(abs(pt[1] - t['pos'][1]) - 0.5 * t['scale'][1], 0)
        best = min(best, math.hypot(dx, dy))
    return best
nd_s = sorted(nearest_small(pt) for pt in spawns)
nd_t = sorted(nearest_small(pt) for pt in street[::4])
print(f'SMALL nearest-dist: spawns median {nd_s[len(nd_s)//2]:.2f} m (within 1 m: {sum(1 for x in nd_s if x < 1)/len(nd_s)*100:.1f}%) | '
      f'street median {nd_t[len(nd_t)//2]:.1f} m (within 1 m: {sum(1 for x in nd_t if x < 1)/len(nd_t)*100:.1f}%)')
json.dump({'small': len(small), 'large': len(large),
           'spawn_in_small_center': sum(any(inside(t, pt, 'center') for t in small) for pt in spawns) / len(spawns),
           'street_in_small_center': sum(any(inside(t, pt, 'center') for t in small) for pt in street) / len(street),
           'large_coverage': cov}, open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t2_null.json', 'w'))
