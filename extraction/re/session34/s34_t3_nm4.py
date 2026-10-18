#!/usr/bin/env python3
"""S34 T3d: map all navmesh REGIONS (float soup + adjacency each) in the .nm;
decode each; total cells; adjacency stats."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)

# plausible-float runs over the whole file (offset 2 start, 4-aligned)
M = (N - 2) // 4
fa = np.frombuffer(d[2:2 + M * 4], '>f4').astype(np.float64)
plaus = np.isfinite(fa) & (np.abs(fa) < 5000) & ~((fa == 0))
# treat exact zeros as "not float data" to separate sections? zeros exist in
# soup too... first find runs WITHOUT the zero filter, then with.
plaus2 = np.isfinite(fa) & (np.abs(fa) < 5000)
for name, mask in (('all-plausible', plaus2), ('nonzero-plausible', plaus)):
    idxp = np.flatnonzero(np.diff(np.concatenate(([0], mask.view(np.int8), [0]))))
    runs = [(int(idxp[k]), int(idxp[k + 1])) for k in range(0, len(idxp), 2)
            if idxp[k + 1] - idxp[k] >= 50]
    print(f'{name}: {len(runs)} runs >=50 floats')
    tot = sum(b - a for a, b in runs)
    print(f'  total floats {tot} (file floats {M})')
    for a, b in runs[:14]:
        seg = fa[a:b]
        x, y, z = seg[0::3], seg[1::3], seg[2::3]
        print(f'  @f32[{a:6d}] (byte {2+4*a:7d}): {b-a:6d} floats = {(b-a)//3} triples; '
              f'x {x.min():8.1f}..{x.max():8.1f}  z med {np.median(z):7.2f}')
