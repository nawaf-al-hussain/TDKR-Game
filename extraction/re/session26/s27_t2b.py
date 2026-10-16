#!/usr/bin/env python3
"""s27 T2 v2: batman.bdae — header sections, stride-80 vertex field map,
dual-quat vs tangent-frame discriminators (with nulls), weights, bbox,
-skin matrix hunt."""
import struct
import math
import random

BDAE = '/home/z/my-project/work/data/batman.bdae'
d = open(BDAE, 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
i32 = lambda o: struct.unpack_from('<i', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

h = struct.unpack_from('<14I', d, 0)
print('BRES header (14 u32):')
for k, v in enumerate(h):
    print(f'  h[{k:2d}] = {v:#010x} ({v})')

BLOCK = 0x4a58
DATA = BLOCK + 0x6c
DLEN = u32(BLOCK + 0x68)
NV = 1449
print(f'\nBATMAN mesh: DATA={DATA:#x} DLEN={DLEN:#x} ({DLEN}) = {NV}*80={NV*80} '
      f'+ {DLEN - NV*80} trailer')

IDX = 0x210bc
idx = [u16(IDX + 2 * k) for k in range(5430)]
tris = [(idx[i], idx[i+1], idx[i+2]) for i in range(0, 5430, 3)]
assert max(idx) == 1448

# ---------- 1. positions @+0: edge-length null
def vs_off(off, stride=80):
    return [(f32(DATA + v * stride + off), f32(DATA + v * stride + off + 4),
             f32(DATA + v * stride + off + 8)) for v in range(NV)]

def med_edge(vs, pairs):
    es = sorted(math.dist(vs[a], vs[b]) for a, b in pairs)
    return es[len(es) // 2]

edges_pairs = set()
for a, b, c in tris:
    edges_pairs.add((min(a, b), max(a, b)))
    edges_pairs.add((min(b, c), max(b, c)))
    edges_pairs.add((min(c, a), max(c, a)))
edges_pairs = sorted(edges_pairs)

vs = vs_off(0)
real = med_edge(vs, edges_pairs)
rnd = random.Random(11)
nulls = []
for _ in range(100):
    rnd.shuffle(vs)
    nulls.append(med_edge(vs, edges_pairs))
nulls.sort()
print(f'\n[1] positions @+0 stride80: real med-edge {real:.4f} vs '
      f'null med {nulls[50]:.4f} p5 {nulls[5]:.4f} -> '
      f'{"PASS (structure)" if real < nulls[5] else "FAIL"}')

xs = [v[0] for v in vs]; ys = [v[1] for v in vs]; zs = [v[2] for v in vs]
print(f'[1b] bbox: x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] '
      f'z[{min(zs):.3f},{max(zs):.3f}]  extents '
      f'({max(xs)-min(xs):.3f}, {max(ys)-min(ys):.3f}, {max(zs)-min(zs):.3f})')

# ---------- 2. unit-quat windows and dual-quat orthogonality
print('\n[2] 4-float windows with mean |q| in [0.97, 1.03] over all vertices:')
cands = []
for off in range(0, 68, 4):
    m = 0.0
    for v in range(0, NV, 3):
        q = [f32(DATA + v * 80 + off + 4 * j) for j in range(4)]
        m += math.sqrt(sum(x * x for x in q))
    m /= len(range(0, NV, 3))
    if 0.97 < m < 1.03:
        cands.append((off, m))
        print(f'    +{off:2d}: mean|q|={m:.4f}')

for off, _ in cands:
    if off + 16 + 16 <= 80:
        dot = 0.0
        n = 0
        for v in range(0, NV, 3):
            a = [f32(DATA + v * 80 + off + 4 * j) for j in range(4)]
            b = [f32(DATA + v * 80 + off + 16 + 4 * j) for j in range(4)]
            dot += sum(x * y for x, y in zip(a, b))
            n += 1
        print(f'    <q@+{off}, q@+{off+16}> mean = {dot/n:+.4f} '
              f'(0 => dual-quat pair)')

# ---------- 3. weights at +64..80
print('\n[3] tail fields (+56..+80) as f32, per-vertex samples:')
for v in (0, 1, 2, 700, 1448):
    o = DATA + v * 80
    print(f'    v{v:4d}: ' + ' '.join(f'{f32(o + 4 * k):+.4f}'
                                      for k in range(14, 20)))
wsums = []
for v in range(NV):
    o = DATA + v * 80
    ws = [f32(o + 4 * k) for k in range(17, 20)]
    wsums.append(sum(ws))
wsums.sort()
print(f'[3b] sum(f32@+68..+80): med {wsums[NV//2]:.4f} '
      f'p5 {wsums[NV//20]:.4f} p95 {wsums[-NV//20]:.4f} (1.0 => skin weights)')

# ---------- 4. quat cluster analysis (skin-blend vs tangent-frame)
print('\n[4] quaternion direction clustering (skin-blend => few clusters):')
for off in (cands[0][0] if cands else 16,):
    seen = {}
    for v in range(NV):
        q = tuple(round(f32(DATA + v * 80 + off + 4 * j), 2) for j in range(4))
        seen[q] = seen.get(q, 0) + 1
    top = sorted(seen.items(), key=lambda kv: -kv[1])[:5]
    print(f'    q@+{off}: {len(seen)} distinct (2dp) of {NV}; '
          f'top5 {[(c, n) for c, n in top]}')
rnd = random.Random(3)
dupnull = []
for _ in range(20):
    seen = set()
    for v in range(NV):
        seen.add(tuple(round(rnd.uniform(-1, 1), 2) for _ in range(4)))
    dupnull.append(len(seen))
print(f'    random-uniform null: {sum(dupnull)/len(dupnull):.0f} distinct '
      f'(of {NV})')

# ---------- 5. -skin matrix hunt: 4x4 float blocks with [0,0,0,1]-ish rows
print('\n[5] candidate inverse-bind matrix regions (4x4 f32 runs):')
runs = []
o = 0x21000
end = len(d) - 64
while o < end:
    ok = True
    for r in range(3):
        row = [f32(o + r * 16 + 4 * c) for c in range(4)]
        if not all(-1e6 < x < 1e6 and x == x for x in row):
            ok = False
            break
    last = [f32(o + 48 + 4 * c) for c in range(4)]
    if ok and abs(last[0]) < 1e-5 and abs(last[1]) < 1e-5 \
            and abs(last[2]) < 1e-5 and abs(last[3] - 1) < 1e-5:
        runs.append(o)
        o += 64
    else:
        o += 4
if runs:
    print(f'    {len(runs)} matrix blocks, first @ {runs[0]:#x}, '
          f'last @ {runs[-1]:#x}')
    grouped = []
    start = prev = runs[0]
    for r in runs[1:]:
        if r == prev + 64:
            prev = r
        else:
            grouped.append((start, prev + 64))
            start = prev = r
    grouped.append((start, prev + 64))
    for g0, g1 in grouped[:12]:
        print(f'      contiguous group {g0:#x}..{g1:#x} '
              f'= {(g1-g0)//64} matrices')
else:
    print('    none found with [0,0,0,1] bottom row')
