#!/usr/bin/env python3
"""s50 T1: per-triangle survival — which mat-73 triangles does GL render?
Uses the Python (no-snap, noLM, zbuf, zoomed) render's winner-triangle map vs the
GL coverage mask from the dump."""
import struct, io, zipfile
import numpy as np
from PIL import Image

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
W, H = 1024, 605
BBOX = (-260.0, -1230.0, 85.0, -1030.0)
x0, z0, x1, z1 = BBOX
scale = float(min(W / (x1 - x0), H / (z1 - z0)))
xm, zm = (x0 + x1) / 2, (z0 + z1) / 2

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Z.read('lod_data.bin'); lt = Z.read('lod_table.bin'); bi = Z.read('batch_info.bin')
        break
u = struct.unpack(f'<{len(lt)//4}I', lt)
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]
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

# winner-triangle map for the single mat-73 segment k=695 (only mat73 seg intersecting this bbox fully)
# find it: mat 73, largest area in bbox
best = None
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    if mid != 73:
        continue
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    raw = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, stride)
    pos = raw[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    if pos[:, 0].min() > x0 and pos[:, 0].max() < x1 and pos[:, 1].min() > z0 and pos[:, 1].max() < z1:
        area = (pos[:, 0].max() - pos[:, 0].min()) * (pos[:, 1].max() - pos[:, 1].min())
        if best is None or area > best[0]:
            best = (area, k, off2, data_off, four, vb, ib, nv, stride, pos)
area, k, off2, data_off, four, vb, ib, nv, stride, pos = best
print('segment k=%d nv=%d ni=%d' % (k, nv, ib // 2))
px = (pos[:, 0] - xm) * scale + W / 2
py = (zm - pos[:, 1]) * scale + H / 2
tris = np.frombuffer(ld, '<u2', ib // 2, data_off + 4 + vb).astype(np.int64).reshape(-1, 3)
tris = tris[(tris.max(axis=1) < nv)]

# winner map: rasterize all triangles of this segment, per-pixel triangle id (last wins)
tmap = np.zeros((H, W), np.int32) - 1
cov = np.zeros((H, W), bool)
for ti, (a, b, c) in enumerate(tris):
    x0t, y0t, x1t, y1t, x2t, y2t = px[a], py[a], px[b], py[b], px[c], py[c]
    xlo = max(int(min(x0t, x1t, x2t)), 0); xhi = min(int(max(x0t, x1t, x2t)) + 1, W - 1)
    ylo = max(int(min(y0t, y1t, y2t)), 0); yhi = min(int(max(y0t, y1t, y2t)) + 1, H - 1)
    if xlo > xhi or ylo > yhi:
        continue
    gx, gy = np.meshgrid(np.arange(xlo, xhi + 1) + 0.5, np.arange(ylo, yhi + 1) + 0.5)
    d = (y1t - y2t) * (x0t - x2t) + (x2t - x1t) * (y0t - y2t)
    if abs(d) < 1e-9:
        continue
    w0 = ((y1t - y2t) * (gx - x2t) + (x2t - x1t) * (gy - y2t)) / d
    w1 = ((y2t - y0t) * (gx - x2t) + (x0t - x2t) * (gy - y2t)) / d
    w2 = 1 - w0 - w1
    m = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
    if not m.any():
        continue
    tmap[ylo:yhi + 1, xlo:xhi + 1][m] = ti
    cov[ylo:yhi + 1, xlo:xhi + 1] |= m

glimg = np.asarray(Image.open('/tmp/my-project/work/city_slice_wt/playable/s50_g_seg695.png').convert('RGB'), np.float64).mean(axis=2)[::-1]
glcov = glimg > 4

tri_px = np.zeros(len(tris), np.int64)
tri_gl = np.zeros(len(tris), np.int64)
m2 = cov & (tmap >= 0)
np.add.at(tri_px, tmap[m2], 1)
np.add.at(tri_gl, tmap[m2 & glcov], 1)
have = tri_px > 0
frac = np.where(have, tri_gl / np.maximum(tri_px, 1), -1)
full = int(((frac >= 0.9) & have).sum())
part = int((((frac >= 0.1) & (frac < 0.9)) & have).sum())
none = int(((frac < 0.1) & have).sum())
print('triangles with py-coverage: %d | GL full %d (%.0f%%), partial %d (%.0f%%), MISSING %d (%.0f%%)' % (
    have.sum(), full, 100.0 * full / have.sum(), part, 100.0 * part / have.sum(), none, 100.0 * none / have.sum()))
# characterize missing triangles: width in px
missing = have & (frac < 0.1)
present = have & (frac >= 0.9)
def width_of(t):
    a, b, c = tris[t]
    xs = np.array([px[a], px[b], px[c]]); ys = np.array([py[a], py[b], py[c]])
    # min edge-projected width approx: area/longest-edge
    e = np.hypot(xs[[1,2,0]] - xs[[0,1,2]], ys[[1,2,0]] - ys[[0,1,2]])
    ar = 0.5 * abs((xs[1]-xs[0])*(ys[2]-ys[0]) - (xs[2]-xs[0])*(ys[1]-ys[0]))
    return ar / max(e.max(), 1e-9)
wm = np.array([width_of(t) for t in range(len(tris)) if missing[t]]) if missing.any() else np.array([])
wp = np.array([width_of(t) for t in range(len(tris)) if present[t]]) if present.any() else np.array([])
print('missing tris width px: n=%d median %.3f p90 %.3f' % (len(wm), np.median(wm) if len(wm) else -1, np.percentile(wm, 90) if len(wm) else -1))
print('present tris width px: n=%d median %.3f p90 %.3f' % (len(wp), np.median(wp) if len(wp) else -1, np.percentile(wp, 90) if len(wp) else -1))
