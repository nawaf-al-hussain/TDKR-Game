#!/usr/bin/env python3
"""S34 T1: find run data block via first-entry signature (32 asc ticks
[0..~1100]) then full sequential validation of all 156 entries."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

T = 0x204bb70
NE = 156
pairs = [(u32a(T + 8*k), u32a(T + 8*k + 4)) for k in range(NE)]

M = N // 4
ua = np.frombuffer(ad[:M*4], np.uint32).astype(np.int64)
# first entry: 32 ticks ascending, ticks[0] < 200, ticks[-1] <= 3000
n0 = pairs[0][1] // 4
L = M - n0 - 1
ok = np.ones(L, bool)
for j in range(n0 - 1):
    ok &= ua[j:L+j] < ua[j+1:L+j+1]
for j in range(n0):
    ok &= ua[j:L+j] < 3000
ok &= ua[0:L] < 200
cands = np.flatnonzero(ok)
print(f'{len(cands)} first-entry candidates')

def validate(base):
    pos = base
    for k, (off, ln) in enumerate(pairs):
        if ln == 0: continue
        is_time = (k % 2 == 0)
        if is_time:
            n = ln // 4
            w = [u32a(pos + 4*j) for j in range(n)]
            if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                return False, pos
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                for i in range(m):
                    q = [f32a(pos + 16*i + 4*c) for c in range(4)]
                    nr = math.sqrt(sum(x*x for x in q))
                    if not (0.95 < nr < 1.05): return False, pos
            elif ln % 12 == 0:
                m = ln // 12
                for i in range(m):
                    v = [f32a(pos + 12*i + 4*c) for c in range(3)]
                    if max(abs(x) for x in v) > 1e5: return False, pos
            else: return False, pos
        pos += ln
    return True, pos

hits = []
for c in cands:
    b = int(c) * 4
    okv, end = validate(b)
    if okv:
        hits.append((b, end))
        print(f'FULL VALIDATION @0x{b:07x}..0x{end:07x}')
print(f'\n{len(hits)} full hits')
json.dump([[h[0], h[1]] for h in hits],
          open('/home/z/my-project/scripts/s34_t1_runbase.json', 'w'))
