#!/usr/bin/env python3
"""s45 T1b: pixel-aligned A/B render — engine bindings (lod data) vs deployed street GLB.

5 blocks across material classes. Same top-down ortho camera (lod frame), same
rasterizer, same deployed texture set (models/tex/*.jpg).
  Side A (engine): lod vertices, UV chain s43-validated (snorm16 *0.5+0.5, v down),
                   binding = s45_t1a_bindings.json (DiffuseMap/LightMap ordinals, effect mode).
  Side B (deployed): GLB prim (frame lod=(x, z, -y)), TEXCOORD_0/1, material '<dif>|<lm>|<mode>'.
Metrics: mean|diff|/255, histogram TV distance (32 bins/ch), global SSIM.
Nulls: shuffled-material (permuted diffuse across blocks), different-block pairs.
"""
import struct, io, zipfile, json, re
import numpy as np
from PIL import Image

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'
TEX = f'{MODEL}/tex'
OUT = '/home/z/my-project/scripts'
SIZE = 900

# ---------- lod segments ----------
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
    idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
    for stride in (28, 24, 20):
        if vb % stride == 0:
            nv = vb // stride
            if idx.size and idx.max() >= nv:
                continue
            raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, stride)
            pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
            if not np.isfinite(pos).all():
                continue
            seg = {'pos': pos, 'mat': hdr[10], 'stride': stride, 'tris': idx.reshape(-1, 3)}
            if stride >= 24:
                seg['uv0'] = s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2))
            if stride == 28:
                seg['uv1'] = s16a(raw[:, 16:20].copy().view('<u2').reshape(nv, 2))
            if stride == 24 and raw.shape[1] >= 24:
                # stride 24: Coord0@12, F@16 (3B), colour@20 — no lightmap uv
                seg['uv0'] = s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2))
            return seg
    return None


# ---------- GLB ----------
def parse_glb(path):
    raw = open(path, 'rb').read()
    clen, = struct.unpack_from('<I', raw, 12)
    js = json.loads(raw[20:20 + clen])
    boff = 20 + clen
    blen, = struct.unpack_from('<I', raw, boff)
    bin_ = raw[boff + 8:boff + 8 + blen]
    acc, bv = js['accessors'], js['bufferViews']

    def read_acc(ai):
        a = acc[ai]
        v = bv[a['bufferView']]
        off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
        ct = {'VEC3': 3, 'VEC2': 2, 'SCALAR': 1}[a['type']]
        dt = {5126: '<f4', 5123: '<u2', 5125: '<u4', 5121: '<u1'}[a['componentType']]
        arr = np.frombuffer(bin_, dt, a['count'] * ct, off)
        return arr.reshape(a['count'], ct) if ct > 1 else arr

    segs = {}
    for node in js['nodes']:
        m = re.fullmatch(r'seg_(\d+)', node.get('name', ''))
        if m and 'mesh' in node:
            prims = []
            for p in js['meshes'][node['mesh']]['primitives']:
                prims.append({'mat': js['materials'][p['material']]['name'],
                              'pos': read_acc(p['attributes']['POSITION']).astype(np.float64),
                              'uv0': read_acc(p['attributes']['TEXCOORD_0']).astype(np.float64),
                              'uv1': read_acc(p['attributes'].get('TEXCOORD_1', p['attributes']['TEXCOORD_0'])).astype(np.float64),
                              'idx': read_acc(p['indices']).astype(np.int64).reshape(-1, 3)})
            segs[int(m.group(1))] = prims
    return segs


allsegs = {}
for i in range(9):
    allsegs.update(parse_glb(f'{MODEL}/street_island1_{i:02d}.glb'))

# ---------- bindings ----------
bind = json.load(open(f'{OUT}/s45_t1a_bindings.json'))


def basename(t):
    return t[:-4] if t and t.lower().endswith('.tga') else t


texcache = {}


def tex(name):
    if name not in texcache:
        texcache[name] = np.asarray(Image.open(f'{TEX}/{name}.jpg').convert('RGB'), np.float32)
    return texcache[name]


# ---------- rasterizer (s43 chain) ----------
def raster(pos, tris, uv, tex_img, size=SIZE, chain='snorm_half'):
    mn = pos.min(0)
    mx = pos.max(0)
    span = max(mx[0] - mn[0], mx[1] - mn[1]) * 1.04
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    img = np.zeros((size, size, 3), np.float32)
    cover = np.zeros((size, size), np.float32)
    W, H = tex_img.shape[1], tex_img.shape[0]
    tuv = uv * 0.5 + 0.5 if chain == 'snorm_half' else uv.copy()
    tuv = tuv.copy()
    tuv[:, 1] = 1.0 - tuv[:, 1]
    px = (pos[:, 0] - cx) / span * size + size / 2
    py = (cy - pos[:, 1]) / span * size + size / 2
    order = np.argsort(pos[tris].mean(axis=1)[:, 2])
    for t in order:
        i0, i1, i2 = tris[t]
        if i0 == 0xFFFF or i1 == 0xFFFF or i2 == 0xFFFF:
            continue
        x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
        minx = max(int(min(x0, x1, x2)), 0)
        maxx = min(int(max(x0, x1, x2)) + 1, size - 1)
        miny = max(int(min(y0, y1, y2)), 0)
        maxy = min(int(max(y0, y1, y2)) + 1, size - 1)
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
        sub = img[miny:maxy + 1, minx:maxx + 1]
        subc = cover[miny:maxy + 1, minx:maxx + 1]
        m3 = mask[..., None]
        sub[:] = np.where(m3, col, sub)
        subc[:] = np.where(mask, 1.0, subc)
    return img, cover


def combine(diff_img, lm_img, cover, mode):
    if lm_img is not None and mode == '2x':
        return np.clip(diff_img * (lm_img / 255.0) * 2.0, 0, 255) * (cover > 0)[..., None]
    return diff_img * (cover > 0)[..., None]


# ---------- metrics ----------
def img_metrics(a, b):
    m = (a.sum(2) > 0) & (b.sum(2) > 0)
    if m.sum() < 100:
        return None
    d = np.abs(a[m] - b[m]).mean() / 255.0 * 255.0
    tv = 0.0
    for c in range(3):
        ha, _ = np.histogram(a[m][:, c], 32, (0, 256))
        hb, _ = np.histogram(b[m][:, c], 32, (0, 256))
        ha = ha / ha.sum(); hb = hb / hb.sum()
        tv += 0.5 * np.abs(ha - hb).sum()
    tv /= 3.0
    # global SSIM on luma, 8x8 blocks
    la = a[m].mean(1) @ np.array([0.299, 0.587, 0.114]) if False else None
    ga = (a @ np.array([0.299, 0.587, 0.114], np.float32))[m]
    gb = (b @ np.array([0.299, 0.587, 0.114], np.float32))[m]
    n = ga.size
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = ga.mean(), gb.mean()
    va, vb_ = ga.var(), gb.var()
    cov = ((ga - ma) * (gb - mb)).mean()
    ssim = ((2 * ma * mb + C1) * (2 * cov + C2)) / ((ma * ma + mb * mb + C1) * (va + vb_ + C2))
    return dict(meandiff=round(float(d), 2), histTV=round(float(tv), 4), ssim=round(float(ssim), 4), covered=int(m.sum()))


# ---------- block selection ----------
want = {'road_mat73': None, 'facade_windows': None, 'roof_mat156': 1486,
        'props_mat302': 1525, 'road_mat157': None, 'props_mat145': None}
for k in sorted(allsegs):
    h = None
    seg = load_seg(k)
    if seg is None:
        continue
    m = seg['mat']
    if m == 73 and want['road_mat73'] is None:
        want['road_mat73'] = k
    if m == 157 and want['road_mat157'] is None:
        want['road_mat157'] = k
    if m == 145 and want['props_mat145'] is None:
        want['props_mat145'] = k
    if want['facade_windows'] is None and m not in (73, 156, 157, 302, 145, 150):
        b = bind[m]
        dif = b['bind'].get('DiffuseMap', {}).get('tga') or ''
        if 'Windows' in dif:
            want['facade_windows'] = k
print('blocks:', want)

results = {}
pngs = {}
for label, k in want.items():
    if k is None:
        continue
    seg = load_seg(k)
    b = bind[seg['mat']]
    dif = b['bind'].get('DiffuseMap', {}).get('tga')
    lm = b['bind'].get('LightMap', {}).get('tga')
    isLM = (b['effect'] or '').startswith('LightMapDC')
    if dif is None:
        print(f'  {label}: seg {k} mat {seg["mat"]} has no DiffuseMap in table; skip')
        continue
    dif_t = tex(basename(dif))
    lm_t = tex(basename(lm)) if lm else None
    # engine side (stride 28 has uv1; stride 24 has none -> use lm=None per engine data)
    imgA_d, covA = raster(seg['pos'], seg['tris'], seg['uv0'], dif_t)
    imgA_l = None
    if seg.get('uv1') is not None and lm_t is not None:
        imgA_l, _ = raster(seg['pos'], seg['tris'], seg['uv1'], lm_t)
    imgA = combine(imgA_d, imgA_l, covA, '2x' if isLM else 'd')
    # deployed side
    prim = allsegs[k][0]
    pipe = prim['mat'].split('|')
    g_dif, g_lm = (pipe[0], pipe[1]) if len(pipe) >= 3 else (pipe[0], None)
    g_mode = pipe[2] if len(pipe) >= 3 else 'd'
    try:
        g_dif_t = tex(g_dif)
    except FileNotFoundError:
        g_dif_t = dif_t
    g_lm_t = tex(g_lm) if g_lm else None
    gpos = np.column_stack([prim['pos'][:, 0], prim['pos'][:, 2], -prim['pos'][:, 1]])
    imgB_d, covB = raster(gpos, prim['idx'], prim['uv0'], g_dif_t, chain='identity')
    imgB_l = None
    if g_lm_t is not None:
        imgB_l, _ = raster(gpos, prim['idx'], prim['uv1'], g_lm_t, chain='identity')
    imgB = combine(imgB_d, imgB_l, covB, g_mode)
    results[label] = {'seg': k, 'mat': int(seg['mat']), 'stride': seg['stride'],
                      'mine': {'dif': basename(dif) if dif else None, 'lm': basename(lm) if lm else None,
                               'mode': '2x' if isLM else 'd'},
                      'glb': {'dif': g_dif, 'lm': g_lm, 'mode': g_mode},
                      'AB': img_metrics(imgA, imgB)}
    pngs[label] = (imgA, imgB, covA, covB)
    Image.fromarray(imgA.astype(np.uint8)).save(f'{OUT}/s45_t1b_{label}_A_engine.png')
    Image.fromarray(imgB.astype(np.uint8)).save(f'{OUT}/s45_t1b_{label}_B_deployed.png')
    print(f'  {label}: seg {k} mat {seg["mat"]} stride {seg["stride"]} -> {results[label]["AB"]}')

# ---------- nulls ----------
labels = [l for l in want if l in pngs]
# shuffled-material null: rotate the engine-side diffuse across blocks
print('\nnulls:')
for i, lab in enumerate(labels):
    j = (i + 1) % len(labels)
    k2 = want[labels[j]]
    seg2 = load_seg(k2)
    b2 = bind[seg2['mat']]
    dif2 = b2['bind'].get('DiffuseMap', {}).get('tga')
    if dif2 is None:
        continue
    seg1 = load_seg(want[lab])
    imgS_d, covS = raster(seg1['pos'], seg1['tris'], seg1['uv0'], tex(basename(dif2)))
    isLM = (bind[seg1['mat']]['effect'] or '').startswith('LightMapDC')
    lm1 = bind[seg1['mat']]['bind'].get('LightMap', {}).get('tga')
    imgS_l = None
    if seg1.get('uv1') is not None and lm1:
        imgS_l, _ = raster(seg1['pos'], seg1['tris'], seg1['uv1'], tex(basename(lm1)))
    imgS = combine(imgS_d, imgS_l, covS, '2x' if isLM else 'd')
    imgB = pngs[lab][1]
    results.setdefault(lab, {})['null_shuffledmat_vs_B'] = img_metrics(imgS, imgB)
    print(f'  {lab}: shuffled-material(A\' vs B) -> {results[lab]["null_shuffledmat_vs_B"]}')
# different-block nulls
for i in range(len(labels) - 1):
    la, lb = labels[i], labels[i + 1]
    mA = pngs[la][0]
    mB = pngs[lb][1]
    r = img_metrics(mA, mB)
    results.setdefault('null_diffblock', {})[f'{la}_A_vs_{lb}_B'] = r
    print(f'  diffblock {la}(A) vs {lb}(B) -> {r}')

json.dump(results, open(f'{OUT}/s45_t1b_scores.json', 'w'), indent=1)
print('\nsaved s45_t1b_scores.json + PNGs')
