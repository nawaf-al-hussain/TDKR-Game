#!/usr/bin/env python3
"""s43 T3: material-bound textured block render (software rasterizer).
Block = seg1486 (mat 156, stride-28: Coord0->GC_footprint_AB_atlas diffuse,
Coord1->BakeGroup lightmap) + seg1525 (mat 302: GC_Z1_Props_Street_Alpha).
Textures from the deployed gh-pages converted set (same texels the street GLB
uses). Null = shuffled-material (wrong diffuse texture). Output PNGs + scores."""
import struct, io, zipfile, json
import numpy as np
from PIL import Image

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEX = '/tmp/my-project/work/ghpages_live_wt/models/tex'
OUT = '/home/z/my-project/scripts'

g = open(P, 'rb').read()
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
cnt = u[0]
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]


def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0


def load_seg(k):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    vstart = data_off + 4
    nv = vb // 28
    raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, 28)
    pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    uv0 = s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2))
    uv1 = s16a(raw[:, 16:20].copy().view('<u2').reshape(nv, 2))
    idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
    tris = idx.reshape(-1, 3)
    tris = tris[(tris != 0xFFFF).all(axis=1)]
    return dict(pos=pos, uv0=uv0, uv1=uv1, tris=tris, mat=hdr[10])


def raster(seg, tex_img, uv, size=900, chain='snorm_half'):
    """Top-down orthographic software render. chain: snorm_half (u*0.5+0.5) or identity."""
    pos = seg['pos']
    tris = seg['tris']
    mn = pos.min(axis=0)
    mx = pos.max(axis=0)
    span = max(mx[0] - mn[0], mx[1] - mn[1]) * 1.04
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    img = np.zeros((size, size, 3), np.float32)
    cover = np.zeros((size, size), np.float32)
    W = tex_img.shape[1]
    H = tex_img.shape[0]
    tuv = uv
    if chain == 'snorm_half':
        tuv = uv * 0.5 + 0.5
    tuv = tuv.copy()
    tuv[:, 1] = 1.0 - tuv[:, 1]  # image v down
    px = (pos[:, 0] - cx) / span * size + size / 2
    py = (cy - pos[:, 1]) / span * size + size / 2
    order = np.argsort(-pos[tris[:, 0], 2] * 0 + pos[tris].mean(axis=1)[:, 2])  # bottom-first
    for t in order:
        i0, i1, i2 = tris[t]
        x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
        minx = max(int(min(x0, x1, x2)), 0)
        maxx = min(int(max(x0, x1, x2)) + 1, size - 1)
        miny = max(int(min(y0, y1, y2)), 0)
        maxy = min(int(max(y0, y1, y2)) + 1, size - 1)
        if minx > maxx or miny > maxy:
            continue
        xs = np.arange(minx, maxx + 1) + 0.5
        ys = np.arange(miny, maxy + 1) + 0.5
        gx, gy = np.meshgrid(xs, ys)
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
        sub = img[miny:maxy + 1, minx:maxx + 1]
        subc = cover[miny:maxy + 1, minx:maxx + 1]
        m3 = mask[..., None]
        sub[:] = np.where(m3, col, sub)
        subc[:] = np.where(mask, 1.0, subc)
    return img, cover


def colour_stats(img, cover):
    m = cover > 0
    if m.sum() == 0:
        return {}
    v = img[m]
    return dict(mean=[round(float(x), 2) for x in v.mean(axis=0)],
                std=[round(float(x), 2) for x in v.std(axis=0)],
                warmth=round(float(v[:, 0].mean() - v[:, 2].mean()), 2),
                covered=float(m.mean()))


def img_diff(a, b):
    m = (a.sum(axis=2) > 0) & (b.sum(axis=2) > 0)
    if m.sum() == 0:
        return None
    return float(np.abs(a[m] - b[m]).mean())


# --- load textures (converted, deployed set) ---
atlas = np.asarray(Image.open(f'{TEX}/GC_footprint_AB_atlas.jpg').convert('RGB'), np.float32)
bakeA0 = np.asarray(Image.open(f'{TEX}/BakeGroup_Island1_A0.jpg').convert('RGB'), np.float32)
street = np.asarray(Image.open(f'{TEX}/GC_Z1_Props_Street_Alpha.jpg').convert('RGB'), np.float32)
park = np.asarray(Image.open(f'{TEX}/GC_Park_atlas_props.jpg').convert('RGB'), np.float32)
print('textures:', atlas.shape, bakeA0.shape, street.shape, park.shape)

results = {}
# seg1486: mat156 -> diffuse atlas + lightmap bake page
seg = load_seg(1486)
img_d, cov = raster(seg, atlas, seg['uv0'])
img_l, _ = raster(seg, bakeA0, seg['uv1'])
img_null, covn = raster(seg, park, seg['uv0'])  # shuffled-material null (wrong diffuse)
img_comb = np.clip(img_d * (img_l / 255.0) * 1.6, 0, 255) * (cov > 0)[..., None]
results['seg1486_diffuse'] = colour_stats(img_d, cov)
results['seg1486_lightmap'] = colour_stats(img_l, cov)
results['seg1486_combined'] = colour_stats(img_comb, cov)
results['seg1486_null_park'] = colour_stats(img_null, covn)
results['seg1486_diff_vs_null'] = img_diff(img_d, img_null)
Image.fromarray(img_d.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1486_diffuse.png')
Image.fromarray(img_l.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1486_lightmap.png')
Image.fromarray(img_comb.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1486_combined.png')
Image.fromarray(img_null.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1486_null.png')

# seg1525: mat302 -> GC_Z1_Props_Street_Alpha diffuse (+BakeGroup_A0 lightmap)
seg2 = load_seg(1525)
img_d2, cov2 = raster(seg2, street, seg2['uv0'])
img_l2, _ = raster(seg2, bakeA0, seg2['uv1'])
img_null2, covn2 = raster(seg2, atlas, seg2['uv0'])
img_comb2 = np.clip(img_d2 * (img_l2 / 255.0) * 1.6, 0, 255) * (cov2 > 0)[..., None]
results['seg1525_diffuse'] = colour_stats(img_d2, cov2)
results['seg1525_lightmap'] = colour_stats(img_l2, cov2)
results['seg1525_combined'] = colour_stats(img_comb2, cov2)
results['seg1525_null_atlas'] = colour_stats(img_null2, covn2)
results['seg1525_diff_vs_null'] = img_diff(img_d2, img_null2)
Image.fromarray(img_d2.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1525_diffuse.png')
Image.fromarray(img_comb2.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1525_combined.png')
Image.fromarray(img_null2.astype(np.uint8)).save(f'{OUT}/s43_t3_seg1525_null.png')

print(json.dumps(results, indent=1))
json.dump(results, open(f'{OUT}/s43_t3_render_scores.json', 'w'), indent=1)
