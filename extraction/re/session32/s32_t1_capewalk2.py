#!/usr/bin/env python3
"""S32 T1g: cape vertex block hunt — encoding + stride detection."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()

BLK = 0x54d78
LN = 21552
raw = d[BLK:BLK + LN]

print('=== raw hex first 128 B from 0x54d78+448 ===')
print(d[BLK + 448:BLK + 448 + 128].hex(' '))
print('\n=== raw hex at 0x54d78 (first 64 B) ===')
print(raw[:64].hex(' '))

# f16 view
f16 = np.frombuffer(raw, np.float16)
nz16 = f16[f16 != 0]
print(f'\nf16 view: {len(f16)} values, nonzero {len(nz16)}, '
      f'range [{nz16.min() if len(nz16) else 0}, {nz16.max() if len(nz16) else 0}]')
print('  f16[224:272]:', np.round(f16[224:272], 3))

# u16 view
u16 = np.frombuffer(raw, np.uint16)
print(f'\nu16 view: max {u16.max()}, values > 100: {(u16 > 100).sum()}')

# autocorrelation of nonzero-ness to find stride
nzb = (np.frombuffer(raw, np.uint8) != 0).astype(np.int8)
print('\nzero-run structure: first nonzero byte at',
      int(np.argmax(nzb)), '=', hex(BLK + int(np.argmax(nzb))))
# find all zero runs > 32 B
runs = []
s = None
for i in range(LN):
    if nzb[i] == 0 and s is None:
        s = i
    elif nzb[i] != 0 and s is not None:
        if i - s >= 32:
            runs.append((s, i - s))
        s = None
if s is not None and LN - s >= 32:
    runs.append((s, LN - s))
print('  zero runs >=32 B:', [(hex(BK := BLK + a), l) for a, l in runs[:12]])

# stride candidates via periodicity of the f32 stream
f32 = np.frombuffer(raw, np.float32)
print('\nf32 value histogram buckets (nonzero):')
v = f32[f32 != 0]
print(f'  nonzero {len(v)}/{len(f32)}; '
      f'frac |v|<=1: {np.mean(np.abs(v) <= 1.001):.3f}; '
      f'frac in (1,3]: {np.mean((np.abs(v) > 1.001) & (np.abs(v) <= 3)):.3f}; '
      f'frac >3: {np.mean(np.abs(v) > 3):.3f}')

# hypothesis: region = [u16 counts/indices][f32 data]. scan for position-like
# triple runs at various strides anywhere in the block
body_hits = {}
for S in (12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80):
    for start in range(0, 512, 4):     # vertex blocks usually start early
        cnt = 0
        off = start
        while off + 12 <= LN:
            x, y, z = f32[off // 4:off // 4 + 3]
            if abs(x) <= 1.2 and abs(y) <= 1.2 and 0.0 <= z <= 2.2:
                cnt += 1
                off += S
            else:
                break
        if cnt >= 100:
            body_hits[(S, start)] = cnt
best = sorted(body_hits.items(), key=lambda kv: -kv[1])[:8]
print('position-run hits (stride, start, count):', best)

# maybe the cape verts are y-forward (cape hangs on the BACK, y<0):
print('\nlooser scan (x,z in body box, any y in [-2,2]):')
for S in (12, 16, 20, 24, 32, 48, 80):
    for start in range(0, 512, 4):
        cnt = 0
        off = start
        while off + 12 <= LN:
            x, y, z = f32[off // 4:off // 4 + 3]
            if abs(x) <= 1.2 and -2 <= y <= 2 and 0.0 <= z <= 2.2:
                cnt += 1
                off += S
            else:
                break
        if cnt >= 150:
            print(f'  stride {S} start {start}: {cnt} hits')
            x0 = f32[start // 4:start // 4 + 3]
            print(f'    first pos {np.round(x0, 3)}')

# CAPE_down region: 0x6474c len 11760 — same treatment
print('\n=== CAPE_down companion block @0x6474c (11760 B) ===')
raw2 = d[0x6474c:0x6474c + 11760]
f32b = np.frombuffer(raw2, np.float32)
nzb2 = (np.frombuffer(raw2, np.uint8) != 0).astype(np.int8)
print('  first nonzero byte at', int(np.argmax(nzb2)))
print('  f32[0:24]:', np.round(f32b[:24], 4))
s2 = int(np.argmax(nzb2))
print('  f32 around first nonzero:', np.round(f32b[max(0, s2//4-4):s2//4+20], 4))

# tail block 0x6ccb8 (5268 B)
print('\n=== tail block @0x6ccb8 (5268 B) ===')
raw3 = d[0x6ccb8:]
f32c = np.frombuffer(raw3, np.float32)
nzb3 = (np.frombuffer(raw3, np.uint8) != 0).astype(np.int8)
print('  first nonzero at', int(np.argmax(nzb3)), 'of', len(raw3))
print('  f32[0:24]:', np.round(f32c[:24], 4))
k = int(np.argmax(nzb3))
print('  f32 around first nonzero:', np.round(f32c[max(0, k//4-2):k//4+18], 4))
print('  ascii head:', bytes(b if 32 <= b < 127 else 46 for b in raw3[:64]))
