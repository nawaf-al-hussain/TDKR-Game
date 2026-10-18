#!/usr/bin/env python3
"""S35 T4b: null study over the unknown template base extent B.
Volume model (data-determined): pos = f0-f2, rotation = f3-f5 deg,
scale = f6-f8; extents = B * scale (B = engine template, unknown).
For B in 1..40: fraction of SPAWN points inside some trigger volume
vs RANDOM STREET points inside some trigger volume. If spawn rate
exceeds street rate for some B, that B is evidenced; if never, the
file's trigger positions carry no activation signal at any B."""
import struct, json, math, glob
import numpy as np
from collections import defaultdict

D = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
trigs = D['triggers']
T = np.array([t['f9'][:9] for t in trigs])
tpos = T[:, :3]
tscale = T[:, 6:9]
trot = T[:, 3:6]
print(f'triggers {len(T)}; scale medians {[round(float(np.median(tscale[:, i])), 2) for i in range(3)]}')

# spawn points: prototype gc_data (r29 pipeline, same as r23 null)
GD = json.load(open('/tmp/my-project/scripts/s33_gcdata.json'))
sp = GD['spawns']
P = np.array([s['pos'] for s in sp], float)
print(f'spawns: {P.shape} x [{P[:,0].min():.0f},{P[:,0].max():.0f}] '
      f'y [{P[:,1].min():.0f},{P[:,1].max():.0f}] z [{P[:,2].min():.1f},{P[:,2].max():.1f}]')

# random street points from the navmesh soup ground cells
F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
NV = 30905 // 3
soup = np.frombuffer(d, '>f4', count=NV * 3, offset=2).astype(np.float64)
V = soup.reshape(NV, 3)
rng = np.random.default_rng(31)
street = V[(V[:, 2] > 0.5) & (V[:, 2] < 20)]
R = street[rng.choice(len(street), 600, replace=False)]
print('street pts:', R.shape)

# 2D proximity profile (rotation ignored for the profile — most triggers unrotated:
# f3 zeros 99%, f5 zeros 80%)
def inside_frac(pts, B):
    """fraction of pts within ANY trigger cylinder radius B*avg scale, |dz| < B*scale_z"""
    cnt = 0
    for p in pts:
        dd = np.linalg.norm(tpos[:, :2] - p[:2], axis=1) / ((tscale[:, 0] + tscale[:, 1]) / 2)
        zz = np.abs(tpos[:, 2] - p[2]) / tscale[:, 2]
        if (dd < B).any() and (zz < B).any() and ((dd < B) & (zz < B)).any():
            cnt += 1
    return cnt / len(pts)

if sp is not None:
    Bs = [1, 2, 3, 5, 8, 10, 15, 20, 30, 40]
    print(f'\n{"B":>4} {"spawn%":>8} {"street%":>8} {"ratio":>6}')
    for B in Bs:
        fs = inside_frac(P, B)
        fr = inside_frac(R, B)
        print(f'{B:4d} {fs*100:7.1f}% {fr*100:7.1f}% {fs/max(fr,1e-9):6.2f}')
