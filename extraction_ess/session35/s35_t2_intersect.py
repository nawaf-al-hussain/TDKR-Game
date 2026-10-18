#!/usr/bin/env python3
"""S35 T2e v2: decisive intersection test for 394/194-vertex streams."""
import struct, math, collections
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
u16 = lambda o: struct.unpack_from('<H', md, o)[0]

def read_verts(vert_off, nverts):
    V = np.empty((nverts, 3), np.float32)
    for i in range(nverts):
        V[i] = struct.unpack_from('<3f', md, vert_off + i * 80)
    return V

def read_idx(off, n):
    return np.array([struct.unpack_from('<H', md, off + 2 * i)[0] for i in range(n)], np.int64)

body_idx = read_idx(0x210ba, 5655)
cape_idx = read_idx(0x2b7d8, 2006)
cape_lod_idx = read_idx(0x305b4, 891)

def layout_at(base, nv):
    ok = 0
    for i in range(nv):
        o = base + i * 80
        if o + 80 > len(md): return 0.0
        p = struct.unpack_from('<3f', md, o)
        n = struct.unpack_from('<3f', md, o + 12)
        if not all(abs(x) < 10 and math.isfinite(x) for x in p): continue
        nl = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        if not (0.7 < nl < 1.3): continue
        ur, vr = u16(o + 72), u16(o + 76)
        if ur >= 16*4096 or vr >= 16*4096: continue
        ok += 1
    return ok / nv

def edge_band(base, nv, idx, lo=1e-4, hi=0.25):
    V = read_verts(base, nv)
    idx = idx[:(len(idx) // 3) * 3]
    a, b = idx[0::3], idx[1::3]
    m = (a < nv) & (b < nv)
    d = np.linalg.norm(V[a[m]] - V[b[m]], axis=1)
    return float(((d > lo) & (d <= hi)).mean())

def variety(base, nv):
    return float(read_verts(base, nv).std())

ZONES = [('body_verts', 0x4b5c, 0x210cc), ('body_idx', 0x210ba, 0x23cc8),
         ('gap', 0x23cc8, 0x2b7d8), ('cape_idx', 0x2b7d8, 0x2b7d8 + 4012),
         ('post_idx', 0x2c7c4, 0x305b4), ('cape_lod', 0x305b4, 0x30928),
         ('binds_skin', 0x30928, 0x388a0), ('body_zerorun', 0x388a0, 0x388a0 + 115928),
         ('mid', 0x543c8, 0x5a210), ('cape_binds', 0x5a210, 0x5ad64),
         ('cape_skin', 0x5ad64, 0x5cc24), ('cape_zerorun', 0x5cc24, 0x5cc24 + 31528),
         ('tail1', 0x64000, 0x675a4), ('cdown_binds', 0x675a4, 0x680fc),
         ('cdown_skin', 0x680fc, 0x6901c), ('cdown_zerorun', 0x6901c, 0x6901c + 15528),
         ('tail2', 0x6cc84, len(md))]

def zone_of(base, nv):
    out = []
    for nm, lo, hi in ZONES:
        if base < hi and base + nv * 80 > lo:
            out.append(nm)
    return out

def sweep(nv, idx, label):
    span = nv * 80
    survivors = []
    for base in range(0x1000, len(md) - span, 4):
        if layout_at(base, nv) < 0.99:
            continue
        eb = edge_band(base, nv, idx)
        va = variety(base, nv)
        if eb >= 0.5 and va > 0.01:
            survivors.append((base, round(eb, 3), round(va, 3)))
    return survivors

print('positive control (body 1449): layout', round(layout_at(0x4b5c, 1449), 4),
      'edge', round(edge_band(0x4b5c, 1449, body_idx), 4),
      'std', round(variety(0x4b5c, 1449), 4))

for nv, idx, label in ((394, cape_idx, '394v'), (194, cape_lod_idx, '194v')):
    surv = sweep(nv, idx, label)
    zc = collections.Counter()
    others = []
    for base, eb, va in surv:
        zs = zone_of(base, nv)
        homogeneous = len(zs) == 1 and zs[0] in ('body_verts', 'cape_zerorun', 'cdown_zerorun', 'body_zerorun')
        zc[zs[0] if len(zs) == 1 else '+'.join(zs)] += 1
        if not any(zs[0] == 'body_verts' for z in [zs]):
            others.append((base, eb, va, zs))
    print(f'\n{label}: survivors {len(surv)}; zone distribution: {dict(zc)}')
    # exclude single-zone body_verts (aliasing of the real body stream)
    others = [x for x in others if x[3] != ['body_verts']]
    print(f'{label}: non-body_verts survivors: {len(others)}')
    for base, eb, va, zs in others[:12]:
        V = read_verts(base, nv)
        print(f'  0x{base:x}: edge {eb} std {va} zones={zs} bbox {V.min(0).round(2)}..{V.max(0).round(2)}')
