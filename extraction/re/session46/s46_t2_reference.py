#!/usr/bin/env python3
"""s46 T2: Python reference values for the browser gate — seg696 geometry
digest, roads_details ETC1 top-mip digest, real + 2 null render thumbs."""
import struct, io, zipfile, json, sys
import numpy as np
from PIL import Image

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session42')
import importlib.util
spec = importlib.util.spec_from_file_location('cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'
TEX = f'{MODEL}/tex'
SIZE = 700
K = 696

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
ld = lt = None
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

off2 = pairs[K][0]
data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
hdr = struct.unpack_from('<17I', ld, off2)
stride = 20
if vb % 24 == 0:
    stride = 24
if vb % 28 == 0:
    stride = 28
nv = vb // stride
vstart = data_off + 4
raw = np.frombuffer(ld, np.uint8, vb, vstart)
pos = raw.reshape(nv, stride)[:, :12].tobytes()   # per-row positions (page-identical)
idx_bytes = ld[vstart + vb: vstart + vb + ib]
import hashlib
geo_digest = hashlib.sha256(pos).hexdigest() + ':' + hashlib.sha256(idx_bytes).hexdigest()
print('geo digest py :', geo_digest)
print('nv', nv, 'stride', stride, 'mat', hdr[10], 'tris', ib // 6)

# texture digest (ETC1 top mip)
tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]


def tex_member(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm == want:
            return tg[o:o + s]
    raise SystemExit('tex member missing ' + want)


tu = tex_member('gothamcity_roads_details.tga')
th_, tw = struct.unpack_from('<II', tu, 4)
bw, bh = (tw + 3) // 4, (th_ + 3) // 4
rgba = cr.decode_etc1_cleanroom(np.frombuffer(tu, np.uint8, bw * bh * 8, 52), tw, th_)
tex_digest = hashlib.sha256(rgba.tobytes()).hexdigest()
print('tex digest py :', tex_digest, f'({tw}x{th_})')

# ---- renders (same raster as s46_t2_render_ab) ----
def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0


posf = np.frombuffer(pos, '<f4').reshape(nv, 3).astype(np.float64)
uv0 = s16a(raw.reshape(nv, 24)[:, 12:16].copy().view('<u2').reshape(nv, 2).astype(np.int32))
tris = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64).reshape(-1, 3)


def raster(uv, tex_img):
    mn, mx = posf.min(0), posf.max(0)
    span = max(mx[0] - mn[0], mx[1] - mn[1]) * 1.04
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    img = np.zeros((SIZE, SIZE, 3), np.float32)
    W, H = tex_img.shape[1], tex_img.shape[0]
    tuv = uv * 0.5 + 0.5
    tuv = tuv.copy()
    tuv[:, 1] = 1.0 - tuv[:, 1]
    px = (posf[:, 0] - cx) / span * SIZE + SIZE / 2
    py = (cy - posf[:, 1]) / span * SIZE + SIZE / 2
    order = np.argsort(posf[tris].mean(axis=1)[:, 2])
    for t in order:
        i0, i1, i2 = tris[t]
        if max(i0, i1, i2) >= len(posf):
            continue
        x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
        minx = max(int(min(x0, x1, x2)), 0)
        maxx = min(int(max(x0, x1, x2)) + 1, SIZE - 1)
        miny = max(int(min(y0, y1, y2)), 0)
        maxy = min(int(max(y0, y1, y2)) + 1, SIZE - 1)
        if minx > maxx or miny > maxy:
            continue
        gx, gy = np.meshgrid(np.arange(minx, maxx + 1) + 0.5, np.arange(miny, maxy + 1) + 0.5)
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(d) < 1e-9:
            continue
        w0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) / d
        w1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) / d
        w2 = 1 - w0 - w1
        mask = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
        if not mask.any():
            continue
        uu = w0 * tuv[i0, 0] + w1 * tuv[i1, 0] + w2 * tuv[i2, 0]
        vv = w0 * tuv[i0, 1] + w1 * tuv[i1, 1] + w2 * tuv[i2, 1]
        tx = np.clip((uu * W).astype(np.int64) % W, 0, W - 1)
        ty = np.clip((vv * H).astype(np.int64) % H, 0, H - 1)
        col = tex_img[ty, tx].astype(np.float32)
        m3 = mask[..., None]
        img[miny:maxy + 1, minx:maxx + 1] = np.where(m3, col, img[miny:maxy + 1, minx:maxx + 1])
    return img


def thumb16(img):
    TH = 16
    th = np.zeros(TH * TH)
    cnts = np.zeros(TH * TH)
    grey = img @ np.array([0.299, 0.587, 0.114], np.float32)
    for y in range(SIZE):
        for x in range(SIZE):
            tx = min(TH - 1, x * TH // SIZE)
            ty = min(TH - 1, y * TH // SIZE)
            th[ty * TH + tx] += grey[y, x]
            cnts[ty * TH + tx] += 1
    th = np.where(cnts > 0, th / np.maximum(cnts, 1), 0)
    return [round(float(v), 2) for v in th]


roadst = rgba[:, :, :3].astype(np.float32)
img_real = raster(uv0, roadst)
Image.fromarray(img_real.astype(np.uint8)).save('/home/z/my-project/scripts/s46_t2_py_real.png')

nulls = {}
for name in ('GC_Z1_Props_Street', 'GC_Footprint_LB_Cinema'):
    nimg = np.asarray(Image.open(f'{TEX}/{name}.jpg').convert('RGB'), np.float32)
    img_n = raster(uv0, nimg)
    nulls[name] = thumb16(img_n)
    Image.fromarray(img_n.astype(np.uint8)).save(f'/home/z/my-project/scripts/s46_t2_py_null_{name}.png')

out = {'geo_digest': geo_digest, 'tex_digest': tex_digest,
       'thumb_real': thumb16(img_real), 'thumb_nulls': nulls,
       'nv': int(nv), 'mat': int(hdr[10]), 'tris': int(ib // 6)}
json.dump(out, open('/home/z/my-project/scripts/s46_t2_reference.json', 'w'), indent=1)
print('reference written; nv/mat/tris:', out['nv'], out['mat'], out['tris'])
