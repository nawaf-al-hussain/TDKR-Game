#!/usr/bin/env python3
"""S36 T4: cape input-stream absence sweep WIDENED: strides 20-64 (step 4),
f32 / f16 / u16(fixed-point) positions, edge-band criterion,
random-offset nulls per (stride, format), body stream as positive control."""
import struct, json
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
N = len(md)
Nv = 394
Bv = 1449
MAXV = 393

def read_idx(off, n):
    return np.frombuffer(md, '<u2', n, off).astype(np.int64)

cape_idx = read_idx(0x2b7d8, 2006)
body_idx = np.load('/tmp/body_idx_s36.npy')  # 5430 valid u16 from 0x210ba (r35's 5655 overread)

def edge_band(V, idx, lo=1e-4, hi=0.25):
    if not np.all(np.isfinite(V)): return -1.0
    std = V.std(axis=0)
    if std.max() < 0.01 or std.max() > 2.0: return -1.0
    if np.abs(V).max() > 2.5: return -1.0
    a, b = idx[0::3], idx[1::3]
    d = np.linalg.norm(V[a] - V[b], axis=1)
    return float(((d > lo) & (d <= hi)).mean())

def verts_at(g, base, nv, step, unit):
    """V[i] = (g[b], g[b+unit], g[b+2*unit]) at i*step*unit... base in ELEMENTS"""
    V = np.empty((nv, 3), np.float32)
    e0 = base
    end = e0 + nv * step
    V[:, 0] = g[e0: end: step]
    V[:, 1] = g[e0 + 1: end + 1: step]
    V[:, 2] = g[e0 + 2: end + 2: step]
    return V

def sweep(g, base0, base1, unit, stride, nv, idx):
    step = stride // unit
    out = []
    for b in range(base0, base1, 1):
        V = verts_at(g, b, nv, step, unit)
        s = edge_band(V, idx)
        if s > 0.35:
            out.append((round(s, 3), b * unit))
    return out

g4 = np.frombuffer(md, '<f4')
g2 = np.frombuffer(md, '<f2').astype(np.float32)
print('=== positive controls (body f32) ===')
Vb = verts_at(g4, 0x4b5c // 4, Bv, 20, 4)
print('body stride 80 @0x4b5c edge-band:', round(edge_band(Vb, body_idx), 4))
print('body stride 40 @0x4b5c (misread):', round(edge_band(verts_at(g4, 0x4b5c // 4, Bv, 10, 4), body_idx), 4))
print('body stride 160 @0x4b5c (misread):', round(edge_band(verts_at(g4, 0x4b5c // 4, Bv, 40, 4), body_idx), 4))
print('cape stride 80 @0x4b5c-offset region check (body data as cape idx):',
      round(edge_band(Vb[:394].copy(), cape_idx), 4))

print('\n=== CAPE f32 sweeps ===')
results = {}
for stride in range(20, 68, 4):
    r = sweep(g4, 0x40, (N - 3 * Nv * stride) // 4 - 2, 4, stride, Nv, cape_idx)
    results[f'f32_{stride}'] = r
    print(f'f32 stride {stride:2d}: survivors>0.35 = {len(r)}', r[:3] if r else '')

print('\n=== CAPE f16 sweeps ===')
for stride in range(20, 68, 4):
    r = sweep(g2, 0x80, (N - 3 * Nv * stride) // 2 - 2, 2, stride, Nv, cape_idx)
    results[f'f16_{stride}'] = r
    print(f'f16 stride {stride:2d}: survivors>0.35 = {len(r)}', r[:3] if r else '')

print('\n=== CAPE u16 fixed-point sweeps ===')
for exp in (13, 12, 11, 10):
    gu = (np.frombuffer(md, '<u2').astype(np.float32)) * (2.0 ** -exp)
    for stride in (24, 32, 40, 48, 56, 64):
        r = sweep(gu, 0x80, (N - 3 * Nv * stride) // 2 - 2, 2, stride, Nv, cape_idx)
        results[f'u16e{exp}_{stride}'] = r
        print(f'u16 2^-{exp} stride {stride:2d}: survivors = {len(r)}', r[:2] if r else '')

print('\n=== random-offset nulls (f32, n=150 per stride) ===')
rng = np.random.default_rng(364)
for stride in (20, 40, 60, 80):
    step = stride // 4
    scores = []
    for _ in range(150):
        b = int(rng.integers(0x40, (N - 3 * Nv * stride) // 4 - 2))
        s = edge_band(verts_at(g4, b, Nv, step, 4), cape_idx)
        if s >= 0: scores.append(s)
    print(f'f32 stride {stride:2d} null: median {np.median(scores):.3f} p99 {np.percentile(scores, 99):.3f} n={len(scores)}')

tot = sum(len(v) for v in results.values())
print(f'\nTOTAL survivors across {len(results)} configs: {tot}')
json.dump({k: v[:20] for k, v in results.items()},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t4_cape.json', 'w'), indent=1)
print('CANNOT-EXCLUDE: packed 10/11-bit-in-u32 vertex formats (4 B/vertex), non-xyz-leading interleave, delta-encoded streams, compressed blocks, per-object bbox dequant for u16 (only 4 global scales tested), streams outside batman.bdae, strides <20 or >64, and f16/u16 with stride NOT multiple of 4/2 alignment.')
print('Engine-side generation evidence (r25) stands: PlayerCapeComponent::Update + updateBuffer runtime fill; Load reads 27 floats + 1 int only.')
