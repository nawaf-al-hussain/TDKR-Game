#!/usr/bin/env python3
"""s47 T3 Python side: independent source.dae parse -> canonical binding
table + digest; 5 blocks across declaration classes; reference renders (real
binding) + shuffled-material and random-texture nulls; lightmap-region stats
for the stride-28 block. Outputs s47_t3_reference.json + PNGs (untracked)."""
import struct, io, zipfile, json, hashlib, sys, os
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session42')
import importlib.util
spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
SIZE = 700
OUT_JSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t3_reference.json'
WT_PAGE = '/tmp/my-project/work/city_slice_wt/playable'
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}

# ---------- independent source.dae parse (mat_tex15.py walk) ----------
z = zipfile.ZipFile(BDAE)
root = ET.fromstring(z.read('source.dae'))
imgs = {}
lib_i = root.find('c:library_images', NS)
if lib_i is not None:
    for im in lib_i.findall('c:image', NS):
        iid = im.get('id')
        init = im.find('c:init_from', NS)
        imgs[iid] = init.text.strip() if init is not None and init.text else ''
rows = []
lib_m = root.find('c:library_materials', NS)
for md in lib_m.findall('c:material', NS):
    inst = md.find('c:instance_effect', NS)
    sam = {}
    if inst is not None:
        surf = {}
        for sp in inst.findall('c:setparam', NS):
            sf = sp.find('c:surface/c:init_from', NS)
            if sf is not None and sf.text:
                surf[sp.get('ref')] = imgs.get(sf.text.strip(), sf.text.strip())
        for sp in inst.findall('c:setparam', NS):
            s2 = sp.find('c:sampler2D/c:source', NS)
            if s2 is not None and s2.text and s2.text.strip() in surf:
                sam[sp.get('ref')] = surf[s2.text.strip()]
    rows.append([md.get('id'), sam.get('DiffuseMap') or '', sam.get('LightMap') or ''])
mats_sorted = sorted(rows, key=lambda r: r[0])
canon = json.dumps(mats_sorted, separators=(',', ':'))
table_digest = hashlib.sha256(canon.encode()).hexdigest()
print('python table rows:', len(rows), 'digest:', table_digest[:32])
bound_d = sum(1 for r in rows if r[1])
bound_l = sum(1 for r in rows if r[2])
print('bound: DiffuseMap', bound_d, 'LightMap', bound_l)

# ---------- lod data + declarations ----------
bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]

def decl_of(mid):
    r = recs[mid]
    N = int(r[33])
    ds = []
    start = 0
    for j in range(N):
        d = bytes(r[40 + j * 12: 40 + (j + 1) * 12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size))
        start = end
    return ds

decls = {idx: decl_of(idx) for idx in range(M)}
by_class = {}
for idx in range(M):
    ds = decls[idx]
    by_class.setdefault((ds[-1][2], tuple(d[0] for d in ds)), []).append(idx)

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

seg_of = {}
mat_has_seg = set()
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    if ib // 6 >= 24 and vb <= 400000:
        cur = seg_of.get(mid)
        if cur is None or vb < cur[2]:
            seg_of[mid] = (k, off2, vb, ib, data_off)
        mat_has_seg.add(mid)

def pick(cls_key, exclude=()):
    cands = [cnd for cnd in by_class.get(cls_key, [])
             if cnd in mat_has_seg and cnd not in exclude
             and cnd < len(rows) and rows[cnd][1]
             and 'FX_Coronas' not in rows[cnd][1]]
    return cands[0] if cands else None

m73 = 73 if (73 in mat_has_seg and rows[73][1]
             and 'FX_Coronas' not in rows[73][1]) else pick((24, (0, 1, 2, 16)))
m28 = pick((28, (0, 1, 2, 16, 17)))
m2416 = pick((24, (0, 1, 16, 17)))
m2017 = pick((20, (0, 1, 17)))
m276b = None
for cnd in by_class.get((24, (0, 1, 2, 16)), []):
    if (cnd in mat_has_seg and cnd != m73 and cnd < len(rows)
            and rows[cnd][1] and 'roads_details' not in rows[cnd][1]
            and 'FX_Coronas' not in rows[cnd][1]):
        m276b = cnd
        break

blocks = []
for tag, mid in (('road276', m73), ('stride28', m28), ('cls24nc', m2416),
                 ('cls2017', m2017), ('b276b', m276b)):
    if mid is None or mid not in seg_of:
        print('missing block for', tag, mid)
        continue
    k, off2, vb, ib, data_off = seg_of[mid]
    ds = decls[mid]
    nm = rows[mid][0] if mid < len(rows) else f'mat{mid}'
    blocks.append({'tag': tag, 'k': k, 'mat': mid, 'stride': ds[-1][2],
                   'name': nm, 'diff': rows[mid][1], 'lm': rows[mid][2]})
print('blocks:')
for b in blocks:
    print('  ', b['tag'], 'seg', b['k'], 'mat', b['mat'], 'stride', b['stride'],
          'diff', b['diff'], 'lm', b['lm'])

# ---------- textures + renders ----------
tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]
_tex_cache = {}
BAD_TEX = set()

def tex_member(want):
    if want in _tex_cache:
        return _tex_cache[want]
    got = None
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            got = tg[o:o + s]
            break
    if got is None:
        raise SystemExit('tex member missing ' + want)
    _tex_cache[want] = got
    return got

def decode_etc1(name):
    if name in _tex_cache:
        return _tex_cache[name]
    if name in BAD_TEX:
        return None
    tu = tex_member(name)
    th_, tw = struct.unpack_from('<II', tu, 4)
    bw, bh = (tw + 3) // 4, (th_ + 3) // 4
    need = bw * bh * 8
    if len(tu) < 52 + need:
        BAD_TEX.add(name)
        return None
    rgba = cr.decode_etc1_cleanroom(np.frombuffer(tu, np.uint8, need, 52), tw, th_)
    _tex_cache[name] = rgba
    return rgba

def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0

def block_geom(b):
    off2 = pairs[b['k']][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    stride = b['stride']
    nv = vb // stride
    vstart = data_off + 4
    raw = np.frombuffer(ld, np.uint8, vb, vstart)
    dmap = {d[0]: d for d in decls[b['mat']]}
    posf = raw.reshape(nv, stride)[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    d0 = dmap[1]
    uv0 = s16a(raw.reshape(nv, stride)[:, d0[1]:d0[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    uv1 = None
    if 2 in dmap:
        d1 = dmap[2]
        uv1 = s16a(raw.reshape(nv, stride)[:, d1[1]:d1[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    tris = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64).reshape(-1, 3)
    return posf, uv0, uv1, tris

def raster(posf, uv, tex_img, tris, light=None, luv=None):
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
    luv_t = None
    if light is not None and luv is not None:
        luv_t = luv * 0.5 + 0.5
        luv_t = luv_t.copy()
        luv_t[:, 1] = 1.0 - luv_t[:, 1]
        LW, LH = light.shape[1], light.shape[0]
    for t in order:
        i0, i1, i2 = tris[t]
        if max(i0, i1, i2) >= len(posf):
            continue
        x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
        xlo = max(int(min(x0, x1, x2)), 0)
        xhi = min(int(max(x0, x1, x2)) + 1, SIZE - 1)
        ylo = max(int(min(y0, y1, y2)), 0)
        yhi = min(int(max(y0, y1, y2)) + 1, SIZE - 1)
        if xlo > xhi or ylo > yhi:
            continue
        gx, gy = np.meshgrid(np.arange(xlo, xhi + 1) + 0.5, np.arange(ylo, yhi + 1) + 0.5)
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
        col = tex_img[ty, tx, :3].astype(np.float32)
        if luv_t is not None:
            lu = w0 * luv_t[i0, 0] + w1 * luv_t[i1, 0] + w2 * luv_t[i2, 0]
            lv = w0 * luv_t[i0, 1] + w1 * luv_t[i1, 1] + w2 * luv_t[i2, 1]
            ltx = np.clip((lu * LW).astype(np.int64) % LW, 0, LW - 1)
            lty = np.clip((lv * LH).astype(np.int64) % LH, 0, LH - 1)
            lcol = light[lty, ltx, :3].astype(np.float32) / 255.0
            col = col * lcol
        region = img[ylo:yhi + 1, xlo:xhi + 1]
        img[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask[..., None], col, region)
    return img

def thumb16(img):
    h = np.histogram(img.reshape(-1, 3).mean(1), 32, (0, 255))[0]
    return [int(x) for x in h]

os.makedirs(WT_PAGE, exist_ok=True)
ref_out = {'table_digest': table_digest, 'rows_n': len(rows),
           'bound_d': bound_d, 'bound_l': bound_l, 'blocks': []}
rng = np.random.default_rng(47)
all_diffs = [r[1] for r in rows if r[1] and r[1] not in BAD_TEX]
for bidx, b in enumerate(blocks):
    posf, uv0, uv1, tris = block_geom(b)
    diff_img = decode_etc1(b['diff'])
    lm_img = decode_etc1(b['lm']) if b['lm'] else None
    img = raster(posf, uv0, diff_img, tris, light=lm_img, luv=uv1)
    Image.fromarray(img.astype(np.uint8)).save(f'{WT_PAGE}/s47_ref_{b["tag"]}.png')
    ob = blocks[(bidx + 1) % len(blocks)]
    odiff = decode_etc1(ob['diff'])
    olm = decode_etc1(ob['lm']) if ob['lm'] else None
    img_sh = raster(posf, uv0, odiff, tris, light=olm, luv=uv1)
    rnd_name = all_diffs[int(rng.integers(0, len(all_diffs)))]
    img_rnd = raster(posf, uv0, decode_etc1(rnd_name), tris)
    lm_stat = None
    if uv1 is not None:
        area = float((uv1[:, 0].max() - uv1[:, 0].min()) * (uv1[:, 1].max() - uv1[:, 1].min()))
        uv1s = uv1[rng.permutation(len(uv1))]
        area_n = float((uv1s[:, 0].max() - uv1s[:, 0].min()) * (uv1s[:, 1].max() - uv1s[:, 1].min()))
        lm_stat = {'tc1_area': area, 'tc1_area_null': area_n,
                   'tc1_min': [float(uv1[:, 0].min()), float(uv1[:, 1].min())],
                   'tc1_max': [float(uv1[:, 0].max()), float(uv1[:, 1].max())]}
    ref_out['blocks'].append({
        'tag': b['tag'], 'k': b['k'], 'mat': b['mat'], 'stride': b['stride'],
        'name': b['name'], 'diff': b['diff'], 'lm': b['lm'],
        'thumb_real': thumb16(img), 'thumb_shuffle': thumb16(img_sh),
        'thumb_random': thumb16(img_rnd), 'lm': lm_stat,
        'pos_min': [float(x) for x in posf.min(0)],
        'pos_max': [float(x) for x in posf.max(0)]})
    print('rendered', b['tag'], 'diff', b['diff'], 'lm', b['lm'], 'lmstat', lm_stat)

json.dump(ref_out, open(OUT_JSON, 'w'), indent=1)
print('saved', OUT_JSON)
