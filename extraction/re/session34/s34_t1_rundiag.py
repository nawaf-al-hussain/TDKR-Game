#!/usr/bin/env python3
"""S34 T1: for each first-entry candidate, greedy prefix validation; report
best prefixes, failing entry, and whether failure zone is zero-filled."""
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
n0 = pairs[0][1] // 4
L = M - n0 - 1
ok = np.ones(L, bool)
for j in range(n0 - 1):
    ok &= ua[j:L+j] < ua[j+1:L+j+1]
for j in range(n0):
    ok &= ua[j:L+j] < 3000
ok &= ua[0:L] < 200
cands = np.flatnonzero(ok)

def prefix(base):
    pos = base
    for k, (off, ln) in enumerate(pairs):
        if ln == 0:
            continue
        is_time = (k % 2 == 0)
        if is_time:
            n = ln // 4
            w = [u32a(pos + 4*j) for j in range(n)]
            if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                return k, pos, 'time'
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                for i in range(m):
                    q = [f32a(pos + 16*i + 4*c) for c in range(4)]
                    nr = math.sqrt(sum(x*x for x in q))
                    if not (0.95 < nr < 1.05): return k, pos, f'quat{i}'
            elif ln % 12 == 0:
                m = ln // 12
                for i in range(m):
                    v = [f32a(pos + 12*i + 4*c) for c in range(3)]
                    if max(abs(x) for x in v) > 1e5: return k, pos, f'vec3{i}'
            else:
                return k, pos, 'len'
        pos += ln
    return NE, pos, 'OK'

results = []
for c in cands:
    b = int(c) * 4
    k, pos, why = prefix(b)
    results.append((k, b, pos, why))
results.sort(reverse=True)
print('top prefixes:')
for k, b, pos, why in results[:10]:
    print(f'  base 0x{b:07x}: {k}/{NE} entries, fail@0x{pos:07x} ({why})')

# check zero content around the best failure
k, b, pos, why = results[0]
z = ad[pos:pos+256]
run0 = len(z) - len(z.lstrip(b'\0'))
print(f'\nbest-fail zone 0x{pos:07x}: first {run0} bytes zero; '
      f'next 32: {z[:32].hex()}')

# how many candidates reach >= 100?
import collections
print('prefix depth histogram:', collections.Counter(r[0] // 20 for r in results))
json.dump([[r[0], r[1], r[2], r[3]] for r in results[:50]],
          open('/home/z/my-project/scripts/s34_t1_rundiag.json', 'w'))
