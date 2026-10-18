#!/usr/bin/env python3
"""S34 T3f: test per-cell records [7 BE shorts + 1 char] after the float blob.
Score: s0-2 < 31000 (vertex ids), s3-5 < cellcount|0xFFFF (neighbors)."""
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
NV = 30827  # triples in blob (approx vertex count)

best = []
for start in range(369890, 369960):
    for stride in (14, 15, 16):
        for nc in (9000, 10275, 10276, 11000, 15000):
            n = (N - start) // stride
            if n < 5000: continue
            W = min(n, 6000)
            b = np.frombuffer(d[start:start + W * stride], np.uint8).reshape(W, stride)
            s = np.frombuffer(d[start:start + W * stride], '>i2').reshape(W, stride // 2) \
                if stride % 2 == 0 else \
                np.stack([np.frombuffer(d[start + o:start + W * stride:stride], '>i2')
                          for o in range(0, stride - 1, 2)], 1)
            nv_ok = (np.abs(s[:, :3]) < NV).all(axis=1)
            nb_ok = ((s[:, 3:6] == -1) | ((s[:, 3:6] >= 0) & (s[:, 3:6] < nc))).all(axis=1)
            best.append((float((nv_ok & nb_ok).mean()), start, stride, nc))
best.sort(reverse=True)
seen = set()
for frac, start, stride, nc in best[:10]:
    k = (round(frac, 3), stride)
    if k in seen: continue
    seen.add(k)
    print(f'start={start} stride={stride} nc={nc}: {frac*100:.2f}%')
