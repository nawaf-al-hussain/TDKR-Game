#!/usr/bin/env python3
"""s50 T1 probe: per-material batch vertex/index counts for city_zone2's batching.
Any material with nvT > 65535 needs OES_element_index_uint in WebGL1; without
getExtension('OES_element_index_uint') the UNSIGNED_INT drawElements fails
silently (GL_INVALID_ENUM, no console error)."""
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

by_mat = {}
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    if not any(d[0] == 1 for d in ds):
        continue
    a, b = by_mat.get(mid, (0, 0))
    by_mat[mid] = (a + nv, b + ib // 2)
print('materials with TC0:', len(by_mat))
big = {m: v for m, v in by_mat.items() if v[0] > 65535}
print('batches needing uint32 indices (nvT > 65535):', len(big))
tot_nv = sum(v[0] for v in by_mat.values())
tot_ni = sum(v[1] for v in by_mat.values())
print('total verts %d, total idx %d' % (tot_nv, tot_ni))
for m, (nv, ni) in sorted(big.items(), key=lambda kv: -kv[1][0]):
    print('  mat %d: nvT=%d niT=%d  (%.1f%% of all verts)' % (m, nv, ni, 100.0 * nv / tot_nv))
over_tris = sum(big[m][1] for m in big)
print('triangles in uint32 batches: %d / %d = %.1f%%' % (over_tris, tot_ni, 100.0 * over_tris / tot_ni))
