#!/usr/bin/env python3
"""S32 T3h: walkable-graph components + 87%-grid failure classification."""
import json, struct, collections
import numpy as np
from scipy import ndimage  # may not exist; fallback below

D = np.load('/tmp/s32_t3_grid.npz', allow_pickle=True)
Z, FL, SL, valid, WALKABLE = D['Z'], D['FL'], D['SL'], D['valid'], D['WALKABLE']
spawns = D['spawns']
nx, ny = Z.shape
gx0, gy0, GS = -1500.0, -1400.0, 2.0

# connected components (4-conn flood fill via BFS labeling)
lbl = np.zeros((nx, ny), np.int32)
cur = 0
from collections import deque
for i in range(nx):
    for j in range(ny):
        if WALKABLE[i, j] and lbl[i, j] == 0:
            cur += 1
            q = deque([(i, j)])
            lbl[i, j] = cur
            while q:
                a, b = q.popleft()
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    a2, b2 = a + da, b + db
                    if 0 <= a2 < nx and 0 <= b2 < ny and WALKABLE[a2, b2] \
                            and lbl[a2, b2] == 0:
                        lbl[a2, b2] = cur
                        q.append((a2, b2))
sizes = np.bincount(lbl.ravel())[1:]
big = np.sort(sizes)[::-1][:6]
print(f'walkable components: {cur}; largest sizes: {big.tolist()}')
sc = []
for s in spawns:
    i, j = int(round((s[0] - gx0) / GS)), int(round((s[1] - gy0) / GS))
    if 0 <= i < nx and 0 <= j < ny and WALKABLE[i, j]:
        sc.append(lbl[i, j])
cc = collections.Counter(sc)
print(f'spawn component distribution: {len(cc)} components; '
      f'top: {cc.most_common(5)}')

# grid failure classification: rebuild the two 87% grids from r21
# r21 grids: 5 GC grids at the 5 densest 200-m spawn buckets (21x21 over 100 m)
# recompute deterministically: spawn buckets
buck = collections.Counter()
for s in spawns:
    buck[(int(s[0] // 200), int(s[1] // 200))] += 1
top5 = [b for b, _ in buck.most_common(5)]
print('top-5 spawn buckets (200 m):', top5)


def classify_grid(bx, by, tag):
    cx, cy = bx * 200 + 100, by * 200 + 100
    half = 50.0
    n = 21
    xs = np.linspace(cx - half, cx + half, n)
    ys = np.linspace(cy - half, cy + half, n)
    pts = np.array([[x, y, 80.0] for x in xs for y in ys])
    # reuse the grid Z (2 m) as approximation? no — probe at 5 m resolution
    # via the Z grid lookup instead of re-raycasting (fast, same data)
    fails = []
    for x in xs:
        for y in ys:
            i = int(round((x - gx0) / GS))
            j = int(round((y - gy0) / GS))
            if not (0 <= i < nx and 0 <= j < ny):
                fails.append(('out', x, y))
                continue
            if not valid[i, j]:
                # check neighbors: coherent hole or isolated miss
                nb = [(i + a, j + b) for a in (-2, 0, 2) for b in (-2, 0, 2)
                      if (a, b) != (0, 0) and 0 <= i + a < nx and
                      0 <= j + b < ny]
                ng = sum(1 for a, b in nb if valid[a, b])
                if ng >= 10:
                    fails.append(('missing_data', x, y))
                else:
                    fails.append(('hole', x, y))
            elif SL[i, j] > 60:
                fails.append(('wall_face', x, y))
            elif np.isin(FL[i, j], [9, 10]):
                fails.append(('fence_stop', x, y))
    kinds = collections.Counter(k for k, *_ in fails)
    frac = 100 * (1 - len(fails) / (n * n))
    print(f'  grid {tag} @({cx},{cy}): ground {frac:.1f}%  fails {dict(kinds)}')
    return dict(tag=tag, cx=cx, cy=cy, ground_frac=frac,
                fails={k: v for k, v in kinds.items()},
                points=[[k, round(x, 1), round(y, 1)] for k, x, y in
                        fails][:600])


out = []
for k, (bx, by) in enumerate(top5):
    out.append(classify_grid(bx, by, f'GC-{k}'))
json.dump(dict(components=dict(n=int(cur),
                               largest=[int(x) for x in big.tolist()],
                               spawn_dist={str(k): v for k, v in
                                           cc.most_common(8)}),
                  grids=out),
          open('/home/z/my-project/download/s32_t3_grids.json', 'w'))
print('wrote s32_t3_grids.json')
