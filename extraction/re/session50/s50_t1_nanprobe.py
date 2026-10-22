#!/usr/bin/env python3
"""s50 T1: (a) NaN/degenerate triangle stats using REAL per-material declarations;
(b) reuse gate runner to save the GL painter dump and diff vs the flat reference."""
import struct, io, zipfile
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
BI = '/tmp/my-project/work/zone/GothamCity/batch_info.bin'
g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Z.read('lod_data.bin')
        lt = Z.read('lod_table.bin')
        break
u = struct.unpack(f'<{len(lt)//4}I', lt)
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]
bi = open(BI, 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
recs = np.frombuffer(bi[4:], np.uint8).reshape((len(bi) - 4) // bstride, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]

def decl_of(mid):
    r = recs[mid]
    N = int(r[33]); ds = []; start = 0
    for j in range(N):
        d = bytes(r[40 + j * 12: 40 + (j + 1) * 12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size)); start = end
    return ds

nan_tris = 0; tot_tris = 0
nan_h_tris = 0
mats_with_nan = {}
h_all = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    d1 = [d for d in ds if d[0] == 1]
    if not d1:
        continue
    p0, p1 = d1[0][1], d1[0][2]   # start, end of Position
    raw = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, stride)
    pos = raw[:, p0:p0 + 12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    tris = np.frombuffer(ld, '<u2', ib // 2, data_off + 4 + vb).astype(np.int64).reshape(-1, 3)
    keep = (tris.max(axis=1) < nv)
    tris = tris[keep]
    tot_tris += len(tris)
    nanmask_v = ~np.isfinite(pos).all(axis=1)
    if nanmask_v.any():
        tnan = nanmask_v[tris].any(axis=1)
        if tnan.any():
            nan_tris += int(tnan.sum())
            mats_with_nan[mid] = mats_with_nan.get(mid, 0) + int(tnan.sum())
    nanh = ~np.isfinite(pos[:, 2])
    if nanh.any():
        th = nanh[tris].any(axis=1)
        nan_h_tris += int(th.sum())
    h_all.append(pos[:, 2])
H = np.concatenate(h_all)
fin = H[np.isfinite(H)]
print('total tris %d, tris with any non-finite vertex %d (%.2f%%)' % (tot_tris, nan_tris, 100.0 * nan_tris / tot_tris))
print('tris with any non-finite h %d' % nan_h_tris)
print('finite h: min %.2f max %.2f  p99.9 %.2f' % (fin.min(), fin.max(), np.percentile(fin, 99.9)))
for t in (150, 180, 200, 220):
    print('  frac finite-h verts > %d: %.5f' % (t, (fin > t).mean()))
print('mats with NaN tris (top):', sorted(mats_with_nan.items(), key=lambda kv: -kv[1])[:8])
