#!/usr/bin/env python3
"""T2: the 40-vs-80 stride VERDICT with the index buffer + shuffled null."""
import struct, array, math, random

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BLOCK = 0x4a58
DATA = BLOCK + 0x6c
DLEN = u32(BLOCK + 0x68)
END = DATA + DLEN
print(f'vertex data {DATA:#x}..{END:#x} ({DLEN} B); 1449 x 80 = {1449*80}')

# index buffer: scan from END for the longest plausible u16 triangle list
def read_indices(start, vmax=1500, maxn=20000):
    idx = array.array('H')
    o = start
    while o + 2 <= len(d) and len(idx) < maxn:
        v = u16(o)
        if v >= vmax:
            break
        idx.append(v)
        o += 2
    return idx, o

idx, idx_end = read_indices(END)
print(f'index buffer @ {END:#x}: {len(idx)} u16 -> {len(idx)//3} tris, '
      f'max {max(idx) if idx else -1}')
print('first 24:', list(idx[:24]))
print('bytes after indices:', d[idx_end:idx_end + 32].hex())

# index buffer stats: valid triangle list = every value < vertex count
NV = 1449
vals = list(idx)
print('index histogram head:', collections.Counter(vals).most_common(5)
      if False else '')
# positions under each hypothesis
def verts_at(base, stride, count, off=0):
    return [(f32(base + i * stride + off),
             f32(base + i * stride + off + 4),
             f32(base + i * stride + off + 8)) for i in range(count)]

def edge_stats(vs, idx):
    tot = []
    for t in range(len(idx) // 3):
        a, b, c = idx[t * 3], idx[t * 3 + 1], idx[t * 3 + 2]
        if max(a, b, c) >= len(vs):
            continue
        pa, pb, pc = vs[a], vs[b], vs[c]
        e1 = math.dist(pa, pb)
        e2 = math.dist(pb, pc)
        e3 = math.dist(pc, pa)
        tot.extend((e1, e2, e3))
    if not tot:
        return None
    tot.sort()
    n = len(tot)
    return dict(n=n, med=tot[n // 2], p90=tot[int(n * 0.9)],
                p99=tot[int(n * 0.99)], max=tot[-1])

import collections
H = 0x4a58
hdr_pos = DATA  # w0-5 = two position triples of vertex 0?
# Hypothesis A: stride 80, positions at +0 (1449 verts = 115,920 B)
vsA = verts_at(DATA, 80, NV, 0)
# Hypothesis B: stride 40
vsB = verts_at(DATA, 40, NV, 0)
# Hypothesis C: two 40-B sets back to back; positions = set1
vsC = verts_at(DATA, 40, NV, 0)
# Hypothesis D: stride 80 but positions at +28 (after the int header)?
for off in (0, 8, 12, 16, 24, 28):
    vs = verts_at(DATA, 80, min(NV, (DLEN - off) // 80), off)
    st = edge_stats(vs, idx)
    print(f'stride80 off+{off:2}: {st}')
for off in (0, 12, 24):
    vs = verts_at(DATA, 40, min(NV, (DLEN - off) // 40), off)
    st = edge_stats(vs, idx)
    print(f'stride40 off+{off:2}: {st}')
