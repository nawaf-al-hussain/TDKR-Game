#!/usr/bin/env python3
"""S34 T3e: precise adjacency alignment: score FIRST 2000 triplets only;
sweep start byte, endian, T; then verify T triplets consume exactly to a
clean section end; extract cells; ground validation vs collision."""
import struct
import numpy as np

F = '/home/z/my-project/work/game_config/GothamCity_502299_navdata.nm' if False else '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)

best = []
for T in range(10270, 10282):
    end = 2 + T * 36
    for start in range(max(0, end - 20), min(end + 24, N - 12000)):
        for dt, tag in (('>', 'BE'), ('<', 'LE')):
            W = 2000
            a = np.frombuffer(d[start:start + W * 6], dt + 'u2').reshape(W, 3).astype(np.int64)
            ok = ((a == 0xFFFF) | (a < T)).all(axis=1)
            best.append((ok.mean(), T, start, tag, end))
best.sort(key=lambda t: -t[0])
seen = set()
for frac, T, start, tag, end in best[:12]:
    key = (round(frac, 3), T, start, tag)
    if key in seen: continue
    seen.add(key)
    print(f'T={T} start={start} (floatEnd={end}, delta {start-end:+d}) {tag}: '
          f'{frac*100:.2f}% of first 2000')
