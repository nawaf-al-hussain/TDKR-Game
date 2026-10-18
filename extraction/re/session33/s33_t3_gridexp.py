#!/usr/bin/env python3
"""S33 T3d: explain the 62.6% grid — classify probe hits street vs roof."""
import collections, json
import numpy as np

D = np.load('/tmp/s32_t3_grid.npz', allow_pickle=True)
Z, valid, WALKABLE = D['Z'], D['valid'], D['WALKABLE']
spawns = D['spawns']
nx, ny = Z.shape
gx0, gy0, GS = -1500.0, -1400.0, 2.0

buck = collections.Counter()
for s in spawns:
    buck[(int(s[0] // 200), int(s[1] // 200))] += 1
top5 = [b for b, _ in buck.most_common(5)]
print('top-5 200-m spawn buckets:', top5)

out = []
for bx, by in top5:
    cx, cy = bx * 200 + 100, by * 200 + 100
    i0, j0 = int((cx - 50 - gx0) / GS), int((cy - 50 - gy0) / GS)
    n = 25   # 2-m steps over 50 m half-width = the 21x21/100m grid approx
    zs, vs = [], []
    for i in range(i0, i0 + n):
        for j in range(j0, j0 + n):
            if 0 <= i < nx and 0 <= j < ny and valid[i, j]:
                zs.append(Z[i, j]); vs.append(WALKABLE[i, j])
    zs = np.array(zs); vs = np.array(vs, bool)
    street = zs < 5.0
    roof = zs >= 10.0
    mid = (zs >= 5) & (zs < 10)
    out.append(dict(bucket=[bx, by], probes=len(zs),
                    ground_pct=float(100 * vs.mean()) if len(zs) else None,
                    street_pct=float(100 * street.mean()),
                    roof_pct=float(100 * roof.mean()),
                    z_med=float(np.median(zs)) if len(zs) else None,
                    z_max=float(zs.max()) if len(zs) else None))
    print(f'bucket ({bx},{by}): probes {len(zs)}, ground {100*vs.mean():.1f}%, '
          f'street(<5m) {100*street.mean():.1f}%, roof(>=10m) {100*roof.mean():.1f}%, '
          f'z med {np.median(zs):.1f} max {zs.max():.1f}')
json.dump(out, open('/home/z/my-project/scripts/s33_t3_gridexp.json', 'w'), indent=1)
