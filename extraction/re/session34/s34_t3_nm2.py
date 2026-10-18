#!/usr/bin/env python3
"""S34 T3b: pin the float/adjacency boundary; count triangles; build cells;
validate vs collision ground with null."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)

# scan for the exact boundary: last offset where BE f32 triples stay plausible
M = (N - 2) // 4
fa = np.frombuffer(d[2:2 + M * 4], '>f4').astype(np.float64)
plaus = np.isfinite(fa) & (np.abs(fa) < 5000)
# find largest prefix such that prefix length % 9 == 0 and all plausible
p = 0
while p < M and plaus[p]:
    p += 1
print(f'plausible prefix: {p} floats; p//9 = {p//9}, rem {p%9}')
# maybe a stray plausible float inside adjacency: check p-3..p+6 values
print('around boundary:', np.round(fa[p-6:p+6], 2))
# candidate tri counts
for T in (p // 9, (p + 1) // 9, (p - 1) // 9):
    end = 2 + T * 36
    print(f'T={T}: float end byte {end}; next bytes {d[end:end+12].hex()}')

# take T = p//9 if rem small, else check p+? Let's test both T and compare
# adjacency alignment: try starts around the float end
def adj_score(start):
    """score: how many u16 LE triplets with values < T or 0xFFFF"""
    n = (N - start) // 6
    if n < 100: return 0, 0
    a = np.frombuffer(d[start:start + n * 6], '<u2').reshape(n, 3)
    ok = ((a == 0xFFFF) | (a < T)).all(axis=1)
    return ok.mean(), n

for T in sorted({p // 9, (p // 9) + 1}):
    end = 2 + T * 36
    for start in range(end - 6, end + 8):
        s, n = adj_score(start)
        if s > 0.98:
            print(f'T={T} adj start {start} (delta {start-end}): {s*100:.2f}% valid of {n}')
