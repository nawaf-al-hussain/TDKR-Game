#!/usr/bin/env python3
"""s43 T2d: smoothness discriminator for the stride-24 normal encoding.
Correct vertex-normal encoding minimizes the mean |n_i - n_j| across index edges
(smooth shading). Candidates: snorm8@16, 1010102@16, oct8@16, plus snorm8@12."""
import struct, io, zipfile, collections
import numpy as np

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
members = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    members[nm] = (o, s)
zo, zs = members['GothamCity.zip']
Z = zipfile.ZipFile(io.BytesIO(g[zo:zo + zs]))
ld = Z.read('lod_data.bin')
lt = Z.read('lod_table.bin')
u = struct.unpack(f'<{len(lt)//4}I', lt)
cnt = u[0]
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]


def s8a(v):
    v = v.astype(np.int16)
    return np.where(v >= 128, v - 256, v) / 127.0


def s10(v):
    v = v.astype(np.int32)
    return np.where(v >= 512, v - 1024, v) / 511.0


def edge_smooth(nrm, idx, nv):
    tris = idx.reshape(-1, 3)
    tris = tris[(tris != 0xFFFF).all(axis=1)]
    if len(tris) == 0:
        return None
    i0 = tris[:, 0]
    i1 = tris[:, 1]
    i2 = tris[:, 2]
    d = (np.abs(nrm[i0] - nrm[i1]).sum(axis=1) +
         np.abs(nrm[i1] - nrm[i2]).sum(axis=1) +
         np.abs(nrm[i2] - nrm[i0]).sum(axis=1)) / (3 * len(tris))
    return float(d.mean())


results = collections.defaultdict(list)
for k in range(1526):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    if four != 4:
        continue
    vstart = data_off + 4
    idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
    real = idx[idx != 0xFFFF]
    if len(real) == 0:
        continue
    mx = int(real.max())
    cands = [s for s in (24, 20, 32, 28) if vb % s == 0 and mx < vb // s]
    if not cands or cands[0] != 24:
        continue
    nv = vb // 24
    raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, 24)
    # snorm8@16
    n_s8 = s8a(raw[:, 16:19])
    # 1010102@16
    p = raw[:, 16:20].copy().view('<u4').reshape(nv)
    n_10 = np.stack([s10(p & 0x3ff), s10((p >> 10) & 0x3ff), s10((p >> 20) & 0x3ff)], axis=1)
    # oct8@16: two snorm8 -> reconstruct z
    ox = s8a(raw[:, 16:17])
    oy = s8a(raw[:, 17:18])
    oz = 1.0 - np.abs(ox) - np.abs(oy)
    n_oct = np.concatenate([ox, oy, oz], axis=1)
    n_oct = n_oct / np.linalg.norm(n_oct, axis=1, keepdims=True)
    for name, nrm in (('s8@16', n_s8), ('1010@16', n_10), ('oct8@16', n_oct)):
        s = edge_smooth(nrm, idx, nv)
        if s is not None:
            results[name].append(s)
    # variance of the raw field itself (constant fields = degenerate)
    results['field@16_range'].append(float(np.ptp(raw[:, 16:20].astype(np.int32), axis=0).min()))

print('=== smoothness (lower = better) over stride-24 segs ===')
for name, vals in results.items():
    v = np.array(vals)
    print(f'  {name:14s}: n={len(v)} mean={v.mean():.4f} median={np.median(v):.4f}')
