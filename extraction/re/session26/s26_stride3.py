#!/usr/bin/env python3
"""T2: THE STRIDE VERDICT — decode positions at stride 80 vs 40 and compare
triangle edge-length coherence with the real index buffer. Shuffled null."""
import struct, math, random, collections

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BLOCK = 0x4a58
DATA = BLOCK + 0x6c
DLEN = u32(BLOCK + 0x68)
IDX_REGION = DATA + DLEN            # 0x21080
IDX_BYTES = 0x23b28 - IDX_REGION

# index list: after the "Batman" name header; u16 stream
i0 = 0x210b4
n_idx = 5430
idx = [u16(0x210bc + 2 * k) for k in range(n_idx)]
mx = max(idx)
print(f'index list: {n_idx} entries, max {mx} (vertex count >= {mx + 1})')
print('first 12:', idx[:12], ' tris:', n_idx // 3)

NV = mx + 1
# hypothesis layouts for the POSITION triple of vertex v:
#   A: stride 80, pos at +0          (the original claim)
#   B: stride 80, pos at +0 AND second pos at +12 (both decoded; use +0)
#   C: stride 40, pos at +0 (data = 2900 half-records)
#   D: stride 80 but vertex 0 at DATA, positions from the SECOND triple
#      (+12) — the head vertex 0.606, 0.154, 1.916
#   E: the position stream is the FIRST 1449x12 B = positions packed,
#      followed by the rest (stream-segregated layout)
def vs_stride(base, stride, n, off=0):
    return [(f32(base + v * stride + off), f32(base + v * stride + off + 4),
             f32(base + v * stride + off + 8)) for v in range(n)]

def edges(vs):
    out = []
    for t in range(len(idx) // 3):
        a, b, c = idx[3 * t], idx[3 * t + 1], idx[3 * t + 2]
        if max(a, b, c) >= len(vs):
            return None
        out += [math.dist(vs[a], vs[b]), math.dist(vs[b], vs[c]),
                math.dist(vs[c], vs[a])]
    out.sort()
    return out

def report(name, vs):
    e = edges(vs)
    if e is None:
        print(f'{name}: index out of range')
        return
    n = len(e)
    print(f'{name}: med {e[n//2]:.4f}  p90 {e[int(n*.9)]:.4f}  '
          f'p99 {e[int(n*.99)]:.4f}  max {e[-1]:.3f}')

report('A stride80 pos+0  ', vs_stride(DATA, 80, NV))
report('B stride80 pos+12 ', vs_stride(DATA, 80, NV, 12))
report('C stride40 pos+0  ', vs_stride(DATA, 40, NV))
report('E packed pos first', vs_stride(DATA, 12, NV))

# where do plausible positions live? scan all offsets 0..64 step 4 at
# stride 80 and 40, rank by median edge
best = []
for stride in (40, 80):
    for off in range(0, 72, 4):
        n = min(NV, (DLEN - off) // stride)
        vs = vs_stride(DATA, stride, n, off)
        e = edges(vs)
        if e:
            best.append((e[len(e) // 2], stride, off))
best.sort()
print('\nbest (median edge, stride, off):')
for b in best[:6]:
    print(f'  med {b[0]:.4f}  stride {b[1]}  off {b[2]}')

# shuffled null for the best layout
med0, s0, o0 = best[0]
vs = vs_stride(DATA, s0, min(NV, (DLEN - o0) // s0), o0)
e_real = edges(vs)
n = len(e_real)
rnd = random.Random(7)
meds = []
idx2 = idx[:]
for _ in range(200):
    random.shuffle(idx2)
    e = edges(vs)
    meds.append(e[n // 2])
meds.sort()
print(f'\nshuffled null (200): median-edge null-median {meds[100]:.3f} '
      f'null-p5 {meds[10]:.3f} vs REAL {e_real[n//2]:.4f} '
      f'-> z >> 0 = {"PASS" if e_real[n//2] < meds[10] else "FAIL"}')
