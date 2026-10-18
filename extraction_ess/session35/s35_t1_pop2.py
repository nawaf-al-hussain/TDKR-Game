#!/usr/bin/env python3
"""S35 T1a3: analyze the two 28-B record populations; find chain break;
check f4!=0 population for interval-tiling semantics."""
import struct, json

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

recs = []
i = 0
while True:
    o = 0xcd00 + i * 0x1c
    f = [u32a(o + 4 * k) for k in range(7)]
    if f[3] == 0 or f[3] >= N: break
    recs.append(f)
    i += 1
print(f'records with valid ptr: {len(recs)}')

# population split
A = [(i, f) for i, f in enumerate(recs) if f[1] == 0 and f[2] == 0]   # f4=f8=0
B = [(i, f) for i, f in enumerate(recs) if not (f[1] == 0 and f[2] == 0)]
print(f'A (f4=f8=0): {len(A)}   B (f4 or f8 !=0): {len(B)}')

# chain validity within A
breaks = []
for k in range(len(A) - 1):
    i, f = A[k]; j, g = A[k + 1]
    if f[3] + f[4] != g[3]:
        breaks.append((k, i, j))
print(f'A chain breaks: {len(breaks)}; first 5: {breaks[:5]}')

# B records: are f0..f4 proper [start,end) intervals? ascending? tiling?
b0 = [f[0] for _, f in B]; b1 = [f[1] for _, f in B]
print(f'B: f0 asc: {all(b0[k]<=b0[k+1] for k in range(len(b0)-1))}, '
      f'f1 asc: {all(b1[k]<=b1[k+1] for k in range(len(b1)-1))}, '
      f'f0<f1 always: {all(a<b for a,b in zip(b0,b1))}')
# tiling: next.f0 == f1?
tiling = sum(1 for k in range(len(B)-1) if B[k+1][1][0] == B[k][1][1])
print(f'B tiling (next.f0==f1): {tiling}/{len(B)-1}')
# B chain?
bb = sum(1 for k in range(len(B)-1) if B[k][1][3] + B[k][1][4] == B[k+1][1][3])
print(f'B chain (ptr+dist==next): {bb}/{len(B)-1}')

print('\nfirst 10 B records (idx, f0..f18):')
for i, f in B[:10]:
    print(f'  rec{i:4d}: ' + ' '.join(f'{v:9d}' for v in f))
print('last 5 B records:')
for i, f in B[-5:]:
    print(f'  rec{i:4d}: ' + ' '.join(f'{v:9d}' for v in f))

# interleave pattern: are A and B alternating? print index classes
pat = ''.join('A' if f[1]==0 and f[2]==0 else 'B' for _, f in recs[:80])
print('\ninterleave first 80:', pat)
# count transitions
trans = sum(1 for k in range(len(recs)-1) if (recs[k][1]==0 and recs[k][2]==0) != (recs[k+1][1]==0 and recs[k+1][2]==0))
print(f'A/B transitions: {trans}')

# B ptr targets: where do they point (zone)?
import collections
zones = collections.Counter()
for i, f in B:
    zones[f[3] >> 20] += 1
print('B ptr zones (MB buckets):', dict(zones))
# A ptr targets
zonesA = collections.Counter()
for i, f in A:
    zonesA[f[3] >> 20] += 1
print('A ptr zones:', dict(zonesA))

# f18 of B records
b18 = [f[6] for _, f in B]
print(f'B f18: zero {sum(1 for v in b18 if v==0)}, ==f0 {sum(1 for v,f in B if f[6]==f[0])}/{len(B)}')
