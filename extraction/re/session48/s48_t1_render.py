#!/usr/bin/env python3
"""s48 T1: engine LightMapDC math applied to the textured block renders.

Shader facts (extracted s18, effects.gla LightMapDC-f/v.glsl, re-verified s48):
  LightMapColor = texture2D(LightMap, vCoord1) * 2.0;          // hardcoded x2
  Color = DiffuseMapColor * LightMapColor;                     // vertex color removed
  TDKR_SPLIT_ALPHA+HAS_ALPHA: DiffuseMapColor = vec4(tex(DiffuseMap).rgb,
                                                     tex(DiffuseMap_alpha).r);
  vCoord1 = (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw
  s45: LightMapAtlas = (1,1,0,0) on all 284 carriers; s43: Coord1 scale/offset = (1,0)
  -> vCoord1 = TC1_raw, GL_REPEAT wrap.

ALSO restores the Python-side SPLIT-zip unwrap (rgb.pvr + alpha.pvr) that was
lost before the s47 T3 commit: the committed s47_t3_reference.py crashes on
GC_Z1_Props_Street_Alpha.tga (PK zip fed to the ETC1 header parse); the
committed JSON was produced by an earlier fixed version.
"""
import struct, io, zipfile, json, os
import numpy as np
from PIL import Image
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
SIZE = 700
OUT_JSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t1_render.json'
WT_PAGE = '/tmp/my-project/work/city_slice_wt/playable'
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}
import xml.etree.ElementTree as ET

# ---------- binding table (same parse as s47, for block bindings) ----------
z = zipfile.ZipFile(BDAE)
root = ET.fromstring(z.read('source.dae'))
imgs = {}
lib_i = root.find('c:library_images', NS)
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
print('authoring rows:', len(rows), 'diff bound', sum(1 for r in rows if r[1]),
      'lm bound', sum(1 for r in rows if r[2]))

# ---------- geometry + declarations (s47 T2 END-offset semantics) ----------
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

# ---------- SPLIT-aware texture decode ----------
tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]
_tex_cache = {}

def tex_member(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            return tg[o:o + s]
    raise SystemExit('tex member missing ' + want)

def decode_pvr(u8):
    tag = struct.unpack_from('<I', u8, 0)[0]
    if tag != 0x34:
        raise ValueError('bad TDKR tex tag %x' % tag)
    th_, tw = struct.unpack_from('<II', u8, 4)
    if bytes(u8[44:48]) != b'PVR!':
        raise ValueError('bad PVR tag')
    bw, bh = (tw + 3) // 4, (th_ + 3) // 4
    need = bw * bh * 8
    rgba = cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, need, 52), tw, th_)
    return rgba

def unwrap_split(u8):
    """PK zip wrapper (SPLIT, rgb.pvr, alpha.pvr) -> dict; plain tex -> {'rgb': u8}."""
    if bytes(u8[:4]) != b'PK\x03\x04':
        return {'rgb': u8}
    out = {}
    pos = 0
    while pos + 30 <= len(u8) and bytes(u8[pos:pos + 4]) == b'PK\x03\x04':
        csz = struct.unpack_from('<I', u8, pos + 18)[0]
        nlen = struct.unpack_from('<H', u8, pos + 26)[0]
        elen = struct.unpack_from('<H', u8, pos + 28)[0]
        nm = u8[pos + 30:pos + 30 + nlen].decode('latin1')
        dstart = pos + 30 + nlen + elen
        data = u8[dstart:dstart + csz]
        if nm.strip() != 'SPLIT':
            out[nm] = data
        pos = dstart + csz
    return out

def decode_tex(name):
    """-> {'rgb': (h,w,3)u8, 'a': (h,w)u8 or None, 'w','h', 'split': bool}"""
    if name in _tex_cache:
        return _tex_cache[name]
    parts = unwrap_split(tex_member(name))
    rgb = decode_pvr(parts['rgb.pvr']) if 'rgb.pvr' in parts else decode_pvr(parts['rgb'])
    al = None
    if 'alpha.pvr' in parts:
        al = decode_pvr(parts['alpha.pvr'])[:, :, 0].copy()
    t = {'rgb': rgb[:, :, :3].copy(), 'a': al, 'w': rgb.shape[1], 'h': rgb.shape[0],
         'split': 'alpha.pvr' in parts}
    _tex_cache[name] = t
    return t

def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0

def block_geom(k, mid):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    stride = decl_of(mid)[-1][2]
    nv = vb // stride
    vstart = data_off + 4
    raw = np.frombuffer(ld, np.uint8, vb, vstart)
    dmap = {d[0]: d for d in decl_of(mid)}
    posf = raw.reshape(nv, stride)[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    d0 = dmap[1]
    uv0 = s16a(raw.reshape(nv, stride)[:, d0[1]:d0[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    uv1 = None
    if 2 in dmap:
        d1 = dmap[2]
        uv1 = s16a(raw.reshape(nv, stride)[:, d1[1]:d1[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    tris = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64).reshape(-1, 3)
    return posf, uv0, uv1, tris, stride

# ---------- effect-aware raster ----------
def raster(posf, uv0, tex, tris, lm=None, luv=None, lm_scale=2.0, lm_offset=0.0,
           alpha_discard=False, alpha_thr=128.0, vcolor=None):
    """Effect-aware top-down raster.
    LightMapDC:    Color.rgb = Diffuse.rgb * (LightMap.rgb * lm_scale)  [x2 hardcoded]
    SimpleAdditive:Color.rgb = Diffuse.rgb * vColor.rgb (vertex Color0/255; NO lightmap
                   — the effect's FS has no LightMap sample and its VS has no Coord1)
    SPLIT textures: alpha layer = DiffuseMap_alpha.r (own texture dims);
    alpha_discard: ALPHA_TEST-style discard (a < 0.5). Returns (img, coverage)."""
    mn, mx = posf.min(0), posf.max(0)
    span = max(mx[0] - mn[0], mx[1] - mn[1]) * 1.04
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    img = np.zeros((SIZE, SIZE, 3), np.float32)
    cov = np.zeros((SIZE, SIZE), bool)
    W, H = tex['w'], tex['h']
    trgb = tex['rgb']
    tal = tex['a']
    tuv = uv0 * 0.5 + 0.5
    tuv = tuv.copy()
    tuv[:, 1] = 1.0 - tuv[:, 1]
    px = (posf[:, 0] - cx) / span * SIZE + SIZE / 2
    py = (cy - posf[:, 1]) / span * SIZE + SIZE / 2
    order = np.argsort(posf[tris].mean(axis=1)[:, 2])
    AW, AH = (tal.shape[1], tal.shape[0]) if tal is not None else (0, 0)
    vcol = None
    if vcolor is not None:
        vcol = vcolor.astype(np.float32) / 255.0
    luv_t = None
    if lm is not None and luv is not None:
        luv_t = luv * 0.5 + 0.5
        luv_t = luv_t.copy()
        luv_t[:, 1] = 1.0 - luv_t[:, 1]
        LW, LH = lm['w'], lm['h']
        lrgb = lm['rgb']
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
        col = trgb[ty, tx].astype(np.float32)
        if tal is not None:
            atx = np.clip((uu * AW).astype(np.int64) % AW, 0, AW - 1)
            aty = np.clip((vv * AH).astype(np.int64) % AH, 0, AH - 1)
            av = tal[aty, atx].astype(np.float32)
            if alpha_discard:
                keep = av >= alpha_thr
                if not keep.any():
                    continue
                mask = mask & keep
                if not mask.any():
                    continue
        if vcol is not None:
            vc = (w0[..., None] * vcol[i0] + w1[..., None] * vcol[i1]
                  + w2[..., None] * vcol[i2])
            col = col * vc[..., :3]
        if luv_t is not None:
            lu = w0 * luv_t[i0, 0] + w1 * luv_t[i1, 0] + w2 * luv_t[i2, 0]
            lv = w0 * luv_t[i0, 1] + w1 * luv_t[i1, 1] + w2 * luv_t[i2, 1]
            ltx = np.clip((lu * LW).astype(np.int64) % LW, 0, LW - 1)
            lty = np.clip((lv * LH).astype(np.int64) % LH, 0, LH - 1)
            lcol = lrgb[lty, ltx].astype(np.float32) / 255.0 * lm_scale + lm_offset
            col = col * lcol
        region = img[ylo:yhi + 1, xlo:xhi + 1]
        regc = cov[ylo:yhi + 1, xlo:xhi + 1]
        img[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask[..., None], col, region)
        cov[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask, True, regc)
    return img, cov

def lum(img):
    return img.mean(axis=2)

def lum_hist(img, cov):
    v = lum(img)[cov]
    h = np.histogram(v, 32, (0, 255))[0]
    return [int(x) for x in h]

def rgb_hist(img, cov):
    v = img[cov].astype(np.int64)
    idx = (v[:, 0] // 64) * 16 + (v[:, 1] // 64) * 4 + (v[:, 2] // 64)
    h = np.bincount(idx, minlength=64)
    return [int(x) for x in h]

# ---------- blocks ----------
BLOCKS = [
    {'tag': 'road276', 'k': 695, 'mat': 73},
    {'tag': 'stride28', 'k': 1525, 'mat': 302},
    {'tag': 'cls24nc', 'k': 100, 'mat': 11},
    {'tag': 'cls2017', 'k': 28, 'mat': 300},
    {'tag': 'road696', 'k': 696, 'mat': 73},
]
for b in BLOCKS:
    b['diff'] = rows[b['mat']][1]
    b['lmname'] = rows[b['mat']][2]
    b['stride'] = decl_of(b['mat'])[-1][2]
    print(b['tag'], 'mat', b['mat'], 'stride', b['stride'], 'diff', b['diff'], 'lm', b['lmname'])

# ---------- authoritative per-material effect: scene instance table (307) ----------
def instance_fx_table():
    bdae = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read(
        'little_endian_not_quantized.bdae')
    w32 = np.frombuffer(bdae, '<u4', len(bdae) // 4)
    nb = len(bdae)
    fx = {}
    for i in range(307):
        a = 0x5fea0 + i * 36
        ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
        e = int(bdae.find(b'\0', ws[3])) if 0 < ws[3] < nb else -1
        nm = bdae[ws[3]:e].decode('ascii', 'replace') if e > ws[3] else ''
        fx[i] = nm.split('-fx')[0].lstrip('#')
    return fx

fx_of = instance_fx_table()
rng = np.random.default_rng(48)
out = {'blocks': [],
       'note': 'effects from the compiled scene-instance table (307 rows, 307/307 == authoring URLs); '
               'LightMapDC Color=Diff*(LM*2); AlphaMasking Color=Diff*(LM*2+Overbright[default 1.0 '
               'from AlphaMasking.bdae]) with SPLIT alpha.r discard a<0.3; SimpleAdditive/'
               'StandardDiffuseDC Color=Diff*vColor'}
lms = {}
for b in BLOCKS:
    posf, uv0, uv1, tris, stride = block_geom(b['k'], b['mat'])
    dtex = decode_tex(b['diff'])
    lmtex = decode_tex(b['lmname']) if b['lmname'] else None
    b['_geom'] = (posf, uv0, uv1, tris)
    b['_dtex'] = dtex
    b['_lmtex'] = lmtex
    if lmtex is not None and b['lmname'] not in lms:
        lms[b['lmname']] = lmtex

for b in BLOCKS:
    posf, uv0, uv1, tris = b['_geom']
    dtex = b['_dtex']
    lmtex = b['_lmtex']
    has_alpha = dtex['split']
    effect = fx_of.get(b['mat'], '?')
    entry = {'tag': b['tag'], 'k': b['k'], 'mat': b['mat'], 'stride': b['stride'],
             'diff': b['diff'], 'lm': b['lmname'], 'has_alpha_split': has_alpha,
             'effect': effect}
    # 1) deployed-mode render (diffuse only) — continuity with s46/s47 gate
    img0, cov0 = raster(posf, uv0, dtex, tris)
    entry['mean_plain'] = float(lum(img0)[cov0].mean())
    entry['cov_plain'] = int(cov0.sum())
    entry['hist_plain_lum'] = lum_hist(img0, cov0)
    entry['hist_plain_rgb'] = rgb_hist(img0, cov0)
    Image.fromarray(np.clip(img0, 0, 255).astype(np.uint8)).save(
        f'{WT_PAGE}/s48_ref_{b["tag"]}_plain.png')
    if effect == 'LightMapDC':
        # 2) engine mode: Color = Diffuse * (LM * 2.0)
        img2, cov2 = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0)
        entry['mean_lm2'] = float(lum(img2)[cov2].mean())
        entry['cov_lm2'] = int(cov2.sum())
        entry['hist_lm2_lum'] = lum_hist(img2, cov2)
        entry['hist_lm2_rgb'] = rgb_hist(img2, cov2)
        Image.fromarray(np.clip(img2, 0, 255).astype(np.uint8)).save(
            f'{WT_PAGE}/s48_ref_{b["tag"]}_lm2.png')
        img1, cov1 = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=1.0)
        entry['mean_lm1'] = float(lum(img1)[cov1].mean())
        entry['hist_lm1_lum'] = lum_hist(img1, cov1)
        other = lms[[nm2 for nm2 in lms if nm2 != b['lmname']][0]]
        imgs, covs = raster(posf, uv0, dtex, tris, lm=other, luv=uv1, lm_scale=2.0)
        entry['mean_lm2_swapatlas'] = float(lum(imgs)[covs].mean())
        entry['swap_delta_mean'] = float(np.abs(lum(imgs) - lum(img2))[covs].mean())
    elif effect == 'AlphaMasking':
        # engine mode: Color = Diffuse * (LM*2 + Overbright[1.0]); alpha = SPLIT
        # alpha.r (own dims); discard fAlpha < 0.3 (76.5/255)
        imga, cova = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0,
                            lm_offset=1.0, alpha_discard=True, alpha_thr=76.5)
        entry['mean_lm2o'] = float(lum(imga)[cova].mean())
        entry['cov_lm2o'] = int(cova.sum())
        entry['hist_lm2o_lum'] = lum_hist(imga, cova)
        entry['hist_lm2o_rgb'] = rgb_hist(imga, cova)
        Image.fromarray(np.clip(imga, 0, 255).astype(np.uint8)).save(
            f'{WT_PAGE}/s48_ref_{b["tag"]}_lm2o.png')
        # no-discard variant for coverage stats
        imgnd, covnd = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0,
                              lm_offset=1.0)
        entry['mean_lm2o_nodiscard'] = float(lum(imgnd)[covnd].mean())
        entry['discard_kept_fraction'] = float(cova.sum()) / max(1, int(covnd.sum()))
        # the two WRONG models, for the record
        off2 = pairs[b['k']][0]
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        rawv = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(vb // b['stride'], b['stride'])
        c0 = rawv[:, 24:28]
        entry['color0_mean'] = [float(x) for x in c0.mean(axis=0)]
        imgv, covv = raster(posf, uv0, dtex, tris, vcolor=c0)
        entry['mean_vcolor_wrongmodel'] = float(lum(imgv)[covv].mean())
        imgw, covw = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0)
        entry['mean_lm2_wrongmodel'] = float(lum(imgw)[covw].mean())
    elif effect in ('SimpleAdditive', 'StandardDiffuseDC'):
        # engine mode: Color = Diffuse * vColor (Color0/255 at its declared slot)
        off2 = pairs[b['k']][0]
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        ds = decl_of(b['mat'])
        d17 = [d for d in ds if d[0] == 17]
        stride = ds[-1][2]
        rawv = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(vb // stride, stride)
        if d17:
            c0 = rawv[:, d17[0][1]:d17[0][1] + 4]
            entry['color0_mean'] = [float(x) for x in c0.mean(axis=0)]
            entry['color0_unique'] = int(len(np.unique(c0, axis=0)))
            imga, cova = raster(posf, uv0, dtex, tris, vcolor=c0)
            entry['mean_additive'] = float(lum(imga)[cova].mean())
            entry['cov_additive'] = int(cova.sum())
            entry['hist_additive_lum'] = lum_hist(imga, cova)
            entry['hist_additive_rgb'] = rgb_hist(imga, cova)
            Image.fromarray(np.clip(imga, 0, 255).astype(np.uint8)).save(
                f'{WT_PAGE}/s48_ref_{b["tag"]}_additive.png')
        else:
            entry['mean_additive'] = entry['mean_plain']
    else:
        img2, cov2 = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0)
        entry['mean_lm2'] = float(lum(img2)[cov2].mean())
        entry['cov_lm2'] = int(cov2.sum())
        entry['hist_lm2_lum'] = lum_hist(img2, cov2)
        entry['hist_lm2_rgb'] = rgb_hist(img2, cov2)
        Image.fromarray(np.clip(img2, 0, 255).astype(np.uint8)).save(
            f'{WT_PAGE}/s48_ref_{b["tag"]}_lm2.png')
    # 4) lightmap page-region check (s133=1, s145=0 -> vCoord1 = TC1_raw, REPEAT)
    if lmtex is not None and uv1 is not None and effect == 'LightMapDC':
        uv01 = uv1 * 0.5 + 0.5
        bmin = uv01.min(axis=0); bmax = uv01.max(axis=0)
        area = float((bmax[0] - bmin[0]) * (bmax[1] - bmin[1]))
        img2l = lum(img2)[cov2]
        LW, LH = lmtex['w'], lmtex['h']
        page = lum(lmtex['rgb'].astype(np.float32))
        ru = rng.random(20000); rv = rng.random(20000)
        rtx = (ru * LW).astype(np.int64) % LW; rty = (rv * LH).astype(np.int64) % LH
        rsamp = page[rty, rtx]
        thr = 16.0
        obs_nonempty = float((img2l >= thr).mean())
        rnd_nonempty = float((rsamp >= thr).mean())
        entry['tc1_bbox'] = [float(bmin[0]), float(bmin[1]), float(bmax[0]), float(bmax[1])]
        entry['tc1_area'] = area
        entry['lm_sampled_mean'] = float(img2l.mean())
        entry['lm_page_mean'] = float(page.mean())
        entry['lm_enrichment_nonempty'] = (obs_nonempty / rnd_nonempty) if rnd_nonempty > 0 else None
        entry['lm_nonempty_obs'] = obs_nonempty
        entry['lm_nonempty_rnd'] = rnd_nonempty
    out['blocks'].append(entry)
    print(b['tag'], 'plain', round(entry['mean_plain'], 2),
          'lm2', round(entry.get('mean_lm2', -1), 2),
          'lm2o', round(entry.get('mean_lm2o', -1), 2),
          'additive', round(entry.get('mean_additive', -1), 2),
          'tc1_area', entry.get('tc1_area'), 'lm_enrich', entry.get('lm_enrichment_nonempty'))

json.dump(out, open(OUT_JSON, 'w'), indent=1)
print('saved', OUT_JSON)
