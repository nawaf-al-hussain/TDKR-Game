#!/usr/bin/env python3
"""s46 T2: failable render test on FIXED geometry (lod stream, bit-identical to
the GLB on the equal-count population). Isolate UV-effect vs texture-effect:
  TV(lodUV vs glbUV, same texture)  must be <  TV(lodUV, wrong-texture) nulls.
Pre-registered rule: PASS if UV-effect TV < min(texture-swap TVs) on >= 4/5 blocks."""
import struct, io, zipfile, json, re
import numpy as np
from PIL import Image

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'
TEX = f'{MODEL}/tex'
SIZE = 700
rng = np.random.default_rng(4646)

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Zz = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Zz.read('lod_data.bin')
        lt = Zz.read('lod_table.bin')
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

    def ra(ai):
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
        if m is None or 'mesh' not in node:
            continue
        k = int(m.group(1))
        mesh = js['meshes'][node['mesh']]
        segs[k] = [{'mat': js['materials'][p['material']]['name'],
                    'pos': ra(p['attributes']['POSITION']),
                    'uv0': ra(p['attributes']['TEXCOORD_0'])} for p in mesh['primitives']]
    return segs


allsegs = {}
for i in range(9):
    allsegs.update(parse_glb(f'{MODEL}/street_island1_{i:02d}.glb'))

bind = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))


def basename(t):
    return t[:-4] if t and t.lower().endswith('.tga') else t


texcache = {}


def tex(name):
    if name not in texcache:
        texcache[name] = np.asarray(Image.open(f'{TEX}/{name}.jpg').convert('RGB'), np.float32)
    return texcache[name]


def raster(pos, tris, uv, tex_img, mn, mx, size=SIZE):
    span = max(mx[0] - mn[0], mx[1] - mn[1]) * 1.04
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    img = np.zeros((size, size, 3), np.float32)
    cover = np.zeros((size, size), np.float32)
    W, H = tex_img.shape[1], tex_img.shape[0]
    tuv = uv * 0.5 + 0.5
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
        gx, gy = np.meshgrid(np.arange(minx, maxx + 1) + 0.5,
                             np.arange(miny, maxy + 1) + 0.5)
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


def histTV(a, b, ma=None, mb=None):
    m = (a.sum(2) > 0) & (b.sum(2) > 0)
    if ma is not None and mb is not None:
        m = (ma > 0) & (mb > 0)
    if m.sum() < 100:
        return None
    tv = 0.0
    for c in range(3):
        ha, _ = np.histogram(a[m][:, c], 32, (0, 256))
        hb, _ = np.histogram(b[m][:, c], 32, (0, 256))
        ha = ha / ha.sum()
        hb = hb / hb.sum()
        tv += 0.5 * np.abs(ha - hb).sum()
    return float(tv / 3.0)


# ---- blocks: 5 mats, prefer s45's segs, require equal-count single-prim ----
want = [(73, 696), (11, 100), (23, 485), (180, 1383), (196, 1403)]
blocks = []
for mat, k0 in want:
    cands = [k0] + [k for k in sorted(allsegs)
                    if k < u[0] and load_seg(k) is not None
                    and load_seg(k)['mat'] == mat and k in allsegs
                    and len(allsegs[k]) == 1
                    and len(allsegs[k][0]['pos']) == load_seg(k)['pos'].shape[0]]
    got = None
    for k in cands:
        seg = load_seg(k)
        if seg is not None and k in allsegs and len(allsegs[k]) == 1 \
                and allsegs[k][0]['pos'].shape[0] == seg['pos'].shape[0]:
            got = (mat, k, seg)
            break
    if got:
        blocks.append(got)
print('blocks:', [(m, k) for m, k, _ in blocks])

difnames = {}
for mat, k, seg in blocks:
    d = bind[mat]['bind'].get('DiffuseMap', {}).get('tga')
    difnames[mat] = basename(d)
print('engine diffuse per block:', difnames)

# ---- render battery ----
out = {}
for bi, (mat, k, seg) in enumerate(blocks):
    mn, mx = seg['pos'].min(0), seg['pos'].max(0)
    tex_i = tex(difnames[mat])
    A, cA = raster(seg['pos'], seg['tris'], seg['uv0'], tex_i, mn, mx)
    guv = allsegs[k][0]['uv0']
    B, cB = raster(seg['pos'], seg['tris'], guv, tex_i, mn, mx)
    tv_uv = histTV(A, B, cA, cB)
    # texture-swap nulls
    tv_tex = {}
    for bj, (mat2, k2, seg2) in enumerate(blocks):
        if bj == bi:
            continue
        N, cN = raster(seg['pos'], seg['tris'], seg['uv0'], tex(difnames[mat2]), mn, mx)
        tv_tex[mat2] = histTV(A, N, cA, cN)
    # shuffled-UV null
    perm = rng.permutation(len(seg['uv0']))
    S, cS = raster(seg['pos'], seg['tris'], seg['uv0'][perm], tex_i, mn, mx)
    tv_shuf = histTV(A, S, cA, cS)
    tmin = min(v for v in tv_tex.values() if v is not None)
    out[f'mat{mat}'] = {'seg': k, 'tv_uv': tv_uv, 'tv_tex': tv_tex,
                        'tv_tex_min': tmin, 'tv_shufUV': tv_shuf,
                        'pass': (tv_uv is not None and tmin is not None and tv_uv < tmin)}
    print(f"mat{mat} seg{k}: tv_uv={tv_uv:.4f} tv_tex_min={tmin:.4f} "
          f"tv_tex={ {m2: round(v, 4) for m2, v in tv_tex.items()} } tv_shufUV={tv_shuf:.4f} "
          f"pass={out[f'mat{mat}']['pass']}")

npass = sum(1 for v in out.values() if v['pass'])
print(f'PASS {npass}/5 (pre-registered: >=4/5)')
json.dump(out, open('/home/z/my-project/scripts/s46_t2_render_ab.json', 'w'), indent=1)
