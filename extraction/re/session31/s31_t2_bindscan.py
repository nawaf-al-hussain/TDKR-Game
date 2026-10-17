#!/usr/bin/env python3
"""S31 T2: scan the whole bdae for arrays of orthonormal row-affine 64-B
blocks (inverse-bind matrices). Report every run >= 4 with count + offsets."""
import struct, math

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
N = len(d)

def blk_ok(o):
    m = struct.unpack_from('<16f', d, o)
    if m[3] != 0.0 or m[7] != 0.0 or m[11] != 0.0 or m[15] != 1.0:
        return False
    R = (m[0:3], m[4:7], m[8:11])
    for i in range(3):
        n = math.sqrt(sum(x * x for x in R[i]))
        if abs(n - 1) > 1e-3:
            return False
    d01 = sum(R[0][i] * R[1][i] for i in range(3))
    d02 = sum(R[0][i] * R[2][i] for i in range(3))
    d12 = sum(R[1][i] * R[2][i] for i in range(3))
    if abs(d01) > 1e-3 or abs(d02) > 1e-3 or abs(d12) > 1e-3:
        return False
    return True

runs = []
o = 0x23b8
while o < N - 64:
    if blk_ok(o):
        start = o
        cnt = 0
        while o < N - 64 and blk_ok(o):
            cnt += 1
            o += 64
        if cnt >= 4:
            runs.append((start, cnt))
    else:
        o += 4
print('orthonormal affine runs (>=4 blocks):')
for start, cnt in runs:
    print(f'  @0x{start:x}: {cnt} blocks  (end 0x{start + cnt*64:x})')
    for k in range(min(3, cnt)):
        m = struct.unpack_from('<16f', d, start + k * 64)
        print(f'    blk{k}: t=({m[12]:.4f},{m[13]:.4f},{m[14]:.4f}) '
              f'R0=({m[0]:.4f},{m[1]:.4f},{m[2]:.4f})')
