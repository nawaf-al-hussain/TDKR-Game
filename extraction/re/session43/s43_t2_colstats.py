#!/usr/bin/env python3
"""s43 T2b: per-column f32 statistics for each stride class -> attribute sets.
Positions = cols 0..2 (validated). Normals: unit length. UVs: bounded.
Also: index range vs vertex count, and header field distribution per class."""
import struct, io, zipfile, collections
import numpy as np

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
off_w = sz_w = None
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        off_w, sz_w = o, s
Z = zipfile.ZipFile(io.BytesIO(g[off_w:off_w + sz_w]))
ld = Z.read('lod_data.bin')
lt = Z.read('lod_table.bin')
u = struct.unpack(f'<{len(lt)//4}I', lt)
cnt = u[0]
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]

by_stride = collections.defaultdict(list)
meta = {}
for k, (off2, sz2) in enumerate(pairs):
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    seg_id, x36, y40 = hdr[0], hdr[9], hdr[10]
    if four != 4:
        continue
    vstart = data_off + 4
    istart = vstart + vb
    idx = np.frombuffer(ld[istart:istart + ib], '<u2').astype(np.int32)
    real = idx[idx != 0xFFFF]
    mx = int(real.max()) if len(real) else 0
    st = None
    for s in (24, 20, 32, 28):
        if vb % s == 0 and mx < vb // s:
            t = np.frombuffer(ld[vstart:vstart + vb], '<f4').reshape(-1, s // 4)[:, :3]
            if np.isfinite(t).all() and np.abs(t).max() < 6000:
                st = s
                break
    if st is None:
        continue
    by_stride[st].append(k)
    meta[k] = (st, vstart, vb, ib, mx, x36, y40)

for st in sorted(by_stride):
    ks = by_stride[st]
    ncols = st // 4
    # aggregate stats over up to 60 segs per class
    cols = [[] for _ in range(ncols)]
    norms = []
    vc = []
    xs, ys = [], []
    for k in ks[:60]:
        st_, vstart, vb, ib, mx, x36, y40 = meta[k]
        nv = vb // st
        arr = np.frombuffer(ld[vstart:vstart + vb], '<f4').reshape(nv, ncols)
        for c in range(ncols):
            cols[c].append(arr[:, c])
        if ncols >= 6:
            nrm = arr[:, 3:6]
            ln = np.linalg.norm(nrm, axis=1)
            norms.append(ln)
        vc.append((nv, mx))
        xs.append(x36)
        ys.append(y40)
    print(f'=== stride {st}: {len(ks)} segs, ncols={ncols} ===')
    for c in range(ncols):
        v = np.concatenate(cols[c])
        print(f'  col{c}: min={v.min():11.4f} max={v.max():11.4f} mean={v.mean():9.4f} std={v.std():9.4f}')
    if norms:
        ln = np.concatenate(norms)
        print(f'  cols3-5 as vec: |n| min={ln.min():.6f} max={ln.max():.6f} mean={ln.mean():.6f} (unit=1)')
    nv0, mx0 = vc[0]
    nvmax_ok = all(mx < nv for (nv, mx) in vc)
    print(f'  vertices/seg: {nv0} (first), max-index < nv always: {nvmax_ok}')
    print(f'  hdr[9] X range: {min(xs)}..{max(xs)}; hdr[10] Y (material) range: {min(ys)}..{max(ys)}')
