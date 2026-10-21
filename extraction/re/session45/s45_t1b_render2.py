#!/usr/bin/env python3
"""s45 T1b v2: block-level A/B — engine binding chain vs deployed conversion.

Blocks: 5 segs across classes, all present in street GLBs with a diffuse on
both sides. Same camera (union AABB, lod frame), same rasterizer, same tex set.
  A_dif vs B_dif : diffuse chain (engine lod UVs + s45 binding vs GLB UVs + name binding)
  stride-28: additionally A_comb vs B_comb (lightmap x2 chain, s43-validated uv1)
Nulls: shuffled-material (rotated diffuse across blocks) and different-block pairs.
Documented provenance caveat: GLB geometry = authoring variant (vertex counts may
differ), lod = engine streaming variant; AABBs identical under (x,z,-y).
"""
import struct, io, zipfile, json, re
import numpy as np
from PIL import Image

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'
TEX = f'{MODEL}/tex'
OUT = '/home/z/my-project/scripts'
SIZE = 700

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
            seg = {'pos': pos, 'mat': hdr[10], 'stride': stride,
                   'tris': idx.reshape(-1, 3),
                   'uv0': s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2))}
            if stride == 28:
                seg['uv1'] = s16a(raw[:, 16:20].copy().view('<u2').reshape(nv, 2))
            return seg
    return None


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

bind = json.load(open(f'{OUT}/s45_t1a_bindings.json'))


def basename(t):
    return t[:-4] if t and t.lower().endswith('.tga') else t


texcache = {}


def tex(name):
    if name not in texcache:
        texcache[name] = np.asarray(Image.open(f'{TEX}/{name}.jpg').convert('RGB'), np.float32)
    return texcache[name]


def raster(pos, tris, uv, tex_img, mn, mx, size=SIZE, chain='snorm_half'):
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
        if max(i0, i1, i2) >= len(pos):
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


def img_metrics(a, b, ma=None, mb=None):
    m = (a.sum(2) > 0) & (b.sum(2) > 0)
    if ma is not None and mb is not None:
        m = ma & mb
    if m.sum() < 100:
        return None
    d = float(np.abs(a[m] - b[m]).mean())
    tv = 0.0
    for c in range(3):
        ha, _ = np.histogram(a[m][:, c], 32, (0, 256))
        hb, _ = np.histogram(b[m][:, c], 32, (0, 256))
        ha = ha / ha.sum(); hb = hb / hb.sum()
        tv += 0.5 * np.abs(ha - hb).sum()
    ga = (a @ np.array([0.299, 0.587, 0.114], np.float32))[m]
    gb = (b @ np.array([0.299, 0.587, 0.114], np.float32))[m]
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = ga.mean(), gb.mean()
    va, vb_ = ga.var(), gb.var()
    cov = ((ga - ma) * (gb - mb)).mean()
    ssim = ((2 * ma * mb + C1) * (2 * cov + C2)) / ((ma * ma + mb * mb + C1) * (va + vb_ + C2))
    return dict(meandiff=round(d, 2), histTV=round(float(tv / 3.0), 4), ssim=round(float(ssim), 4), covered=int(m.sum()))


# ---------- block selection: 5 classes ----------
blocks = []
want_mats = [73, 11, 23, 180, 196]
seen = {}
for k in sorted(allsegs):
    seg = load_seg(k)
    if seg is None:
        continue
    m = seg['mat']
    if m in want_mats and allsegs[k]:
        b = bind[m]
        if b['bind'].get('DiffuseMap', {}).get('tga'):
            if m not in seen or len(seg['pos']) > len(seen[m][2]['pos']):
                seen[m] = (f'mat{m}_{basename(b["bind"]["DiffuseMap"]["tga"])[:24]}', k, seg)
blocks = [seen[m] for m in want_mats if m in seen][:5]
# ensure one stride-28 (lightmapped) block if available
if not any(s['stride'] == 28 for _, _, s in blocks):
    for k in (1495, 1491, 1487, 1486):
        if k in allsegs:
            seg = load_seg(k)
            if seg and seg.get('uv1') is not None:
                b = bind[seg['mat']]
                dif = b['bind'].get('DiffuseMap', {}).get('tga')
                if dif:
                    blocks.append((f'mat{seg["mat"]}_{basename(dif)[:24]}_LM', k, seg))
                    break
print('blocks:')
for lab, k, seg in blocks:
    print(f'  {lab}: seg {k} mat {seg["mat"]} stride {seg["stride"]} nv {len(seg["pos"])} glbnv {sum(len(p["pos"]) for p in allsegs[k])}')

results = {}
pngA, pngB = {}, {}
for lab, k, seg in blocks:
    b = bind[seg['mat']]
    dif = b['bind']['DiffuseMap']['tga']
    lm = b['bind'].get('LightMap', {}).get('tga')
    dif_t = tex(basename(dif))
    prim = allsegs[k][0]
    pipe = prim['mat'].split('|')
    g_dif = pipe[0]
    g_dif_t = tex(g_dif)
    # camera: union AABB (lod frame); lod = (glb_x, -glb_z, glb_y) per the frame fit
    gpos = np.column_stack([prim['pos'][:, 0], -prim['pos'][:, 2], prim['pos'][:, 1]])
    allpos = np.vstack([seg['pos'], gpos])
    mn, mx = allpos.min(0), allpos.max(0)
    # A: engine
    imgA_d, covA = raster(seg['pos'], seg['tris'], seg['uv0'], dif_t, mn, mx)
    imgA = imgA_d * (covA > 0)[..., None]
    # B: deployed (diffuse chain)
    imgB_d, covB = raster(gpos, prim['idx'], prim['uv0'], g_dif_t, mn, mx, chain='identity')
    imgB = imgB_d * (covB > 0)[..., None]
    r = {'seg': k, 'mat': int(seg['mat']), 'stride': seg['stride'],
         'mine_dif': basename(dif), 'glb_dif': g_dif,
         'AB_diffuse': img_metrics(imgA, imgB, covA > 0, covB > 0)}
    # lightmap chain where the engine data has Coord1 (stride 28)
    if seg.get('uv1') is not None and lm and len(pipe) >= 3 and pipe[1]:
        lm_t = tex(basename(lm))
        g_lm_t = tex(pipe[1])
        imgA_l, _ = raster(seg['pos'], seg['tris'], seg['uv1'], lm_t, mn, mx)
        imgB_l, _ = raster(gpos, prim['idx'], prim['uv1'], g_lm_t, mn, mx, chain='identity')
        A_comb = np.clip(imgA_d * (imgA_l / 255.0) * 2.0, 0, 255) * (covA > 0)[..., None]
        B_comb = np.clip(imgB_d * (imgB_l / 255.0) * 2.0, 0, 255) * (covB > 0)[..., None]
        r['AB_combined_x2'] = img_metrics(A_comb, B_comb, covA > 0, covB > 0)
        r['mine_lm'] = basename(lm)
        r['glb_lm'] = pipe[1]
        Image.fromarray(A_comb.astype(np.uint8)).save(f'{OUT}/s45_t1b_{lab}_A_comb.png')
        Image.fromarray(B_comb.astype(np.uint8)).save(f'{OUT}/s45_t1b_{lab}_B_comb.png')
    Image.fromarray(imgA.astype(np.uint8)).save(f'{OUT}/s45_t1b_{lab}_A.png')
    Image.fromarray(imgB.astype(np.uint8)).save(f'{OUT}/s45_t1b_{lab}_B.png')
    results[lab] = r
    pngA[lab], pngB[lab] = imgA, imgB
    print(f'  {lab}: {json.dumps(r["AB_diffuse"])}')

# ---------- nulls on the diffuse chain ----------
labels = [b[0] for b in blocks]
nulls = {}
for i, lab in enumerate(labels):
    j = (i + 1) % len(labels)
    lab2 = labels[j]
    k2, seg2 = blocks[j][1], blocks[j][2]
    # render block j's engine side with block (j+1)'s diffuse (wrong texture)
    k3, seg3 = blocks[(j + 1) % len(labels)][1], blocks[(j + 1) % len(labels)][2]
    b3 = bind[seg3['mat']]
    dif3 = tex(basename(b3['bind']['DiffuseMap']['tga']))
    prim2 = allsegs[k2][0]
    gpos2 = np.column_stack([prim2['pos'][:, 0], -prim2['pos'][:, 2], prim2['pos'][:, 1]])
    ap = np.vstack([seg2['pos'], gpos2])
    mn2, mx2 = ap.min(0), ap.max(0)
    imgS_d, covS = raster(seg2['pos'], seg2['tris'], seg2['uv0'], dif3, mn2, mx2)
    imgS = imgS_d * (covS > 0)[..., None]
    r = img_metrics(imgS, pngB[lab2], covS > 0, (pngB[lab2].sum(2) > 0))
    nulls[f'{lab2}_shuffledmat_vs_B'] = r
    print(f'  null shuffled-mat {lab2}: {r}')
for i in range(len(labels)):
    la, lb = labels[i], labels[(i + 1) % len(labels)]
    r = img_metrics(pngA[la], pngB[lb], pngA[la].sum(2) > 0, pngB[lb].sum(2) > 0)
    nulls[f'diffblock_{la}_A_vs_{lb}_B'] = r
    print(f'  null diffblock {la}(A) vs {lb}(B): {r}')
results['_nulls'] = nulls
json.dump(results, open(f'{OUT}/s45_t1b_scores.json', 'w'), indent=1)
print('saved scores')
