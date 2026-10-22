#!/usr/bin/env python3
"""s48 T6: whole-zone (all 1,526 GothamCity segments) top-down render, engine
bindings from the compiled instance table, engine UVs, ETC1 textures, per-effect
shading (LightMapDC x2; AlphaMasking x2+1 with SPLIT alpha discard<0.3;
SimpleAdditive/StandardDiffuse vertex tint; unimplemented effects rendered
diffuse-only and documented). Orthographic camera over the zone AABB, 1024 px
wide; painter order = global ascending mean height. The browser page
(city_zone.html) must reproduce this render (pixel correlation)."""
import struct, io, zipfile, json, hashlib, time
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
W, H = 1024, 605
LRU_CAP = 20
OUT_PNG = '/tmp/my-project/work/city_slice_wt/playable/s48_ref_zone.png'
OUT_JSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t6_render.json'
t_start = time.time()

# ---------- compiled instance table (effects + bindings, no XML) ----------
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn:
        return None
    try:
        t = LE[off:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

IMG_BASE, IMG_N = 0x22a9c, 176
imgs = [(int(w32[(IMG_BASE + i * 12) // 4]), int(w32[(IMG_BASE + i * 12 + 8) // 4]))
        for i in range(IMG_N)]
bind = {}
fx_of = {}
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    sam = {}
    for j in range(ws[4]):
        pa = ws[5] + j * 24
        pw = [int(w32[(pa + k * 4) // 4]) for k in range(6)]
        pname = cstr(pw[0])
        if pw[2] != 13 or pw[3] != 1:
            continue
        v1 = pw[4]
        if int(w32[v1 // 4]) != 1 or int(w32[v1 // 4 + 1]) != v1 + 24:
            continue
        idx = int(w32[(v1 + 24) // 4])
        if 0 <= idx < IMG_N:
            sam[pname] = cstr(imgs[idx][1]) or ''
        elif idx == 0xffffffff:
            sam[pname] = ''
    bind[i] = (sam.get('DiffuseMap', ''), sam.get('LightMap', ''))
    fx_of[i] = (cstr(ws[3]) or '').split('-fx')[0].lstrip('#')
print('bindings from compiled table: diff %d, lm %d' %
      (sum(1 for v in bind.values() if v[0]), sum(1 for v in bind.values() if v[1])))

# ---------- geometry + declarations ----------
bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
recs = np.frombuffer(bi[4:], np.uint8).reshape((len(bi) - 4) // bstride, bstride)
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

tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]
_tex_member_cache = {}
def tex_member(want):
    if want in _tex_member_cache:
        return _tex_member_cache[want]
    got = None
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            got = tg[o:o + s]
            break
    _tex_member_cache[want] = got
    return got

def unwrap_split(u8):
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
        if nm.strip() != 'SPLIT':
            out[nm] = u8[dstart:dstart + csz]
        pos = dstart + csz
    return out

def decode_pvr(u8):
    th_, tw = struct.unpack_from('<II', u8, 4)
    bw, bh = (tw + 3) // 4, (th_ + 3) // 4
    return cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, bw * bh * 8, 52), tw, th_)

_tex_lru = {}
_stats = {'miss': 0, 'hit': 0, 'evict': 0}

def get_tex(name, want_alpha=False):
    """LRU-cached decode. Returns dict {rgb (h,w,3)u8, a or None, w, h}."""
    key = (name, want_alpha)
    if key in _tex_lru:
        _stats['hit'] += 1
        _tex_lru[key] = _tex_lru.pop(key)
        return _tex_lru[key]
    _stats['miss'] += 1
    tu = tex_member(name)
    if tu is None:
        _tex_lru[key] = None
        return None
    try:
        parts = unwrap_split(tu)
        rgb = decode_pvr(parts['rgb.pvr'] if 'rgb.pvr' in parts else parts['rgb'])
        al = None
        if want_alpha and 'alpha.pvr' in parts:
            al = decode_pvr(parts['alpha.pvr'])[:, :, 0]
        t = {'rgb': rgb[:, :, :3], 'a': al, 'w': rgb.shape[1], 'h': rgb.shape[0]}
    except Exception:
        t = None
    _tex_lru[key] = t
    if len(_tex_lru) > LRU_CAP:
        old = next(iter(_tex_lru))
        _tex_lru.pop(old)
        _stats['evict'] += 1
    return t

# ---------- pass 1: gather all segments, positions for the camera ----------
segdata = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    dmap = {d[0]: d for d in ds}
    stride = ds[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    segdata.append({'k': k, 'mat': mid, 'off': data_off + 4, 'vb': vb, 'ib': ib,
                    'nv': nv, 'stride': stride, 'dmap': dmap})
print('segments drawn:', len(segdata))
allpos = np.concatenate([
    np.frombuffer(ld, np.uint8, s['vb'], s['off']).reshape(s['nv'], s['stride'])[:, 0:12]
    .copy().view('<f4').reshape(-1, 3) for s in segdata])
x0, x1 = allpos[:, 0].min(), allpos[:, 0].max()
z0, z1 = allpos[:, 1].min(), allpos[:, 1].max()
scale = float(min(W / (x1 - x0), H / (z1 - z0)))
xm, zm = (x0 + x1) / 2, (z0 + z1) / 2
print('zone AABB x[%.1f %.1f] z[%.1f %.1f] scale %.4f px/u' % (x0, x1, z0, z1, scale))
del allpos

# ---------- pass 2: global triangle list + painter order ----------
tris_all = []
uv0_all = []
uv1_all = []
c0_all = []
meta = []
for s in segdata:
    raw = np.frombuffer(ld, np.uint8, s['vb'], s['off']).reshape(s['nv'], s['stride'])
    pos = raw[:, 0:12].copy().view('<f4').reshape(s['nv'], 3).astype(np.float64)
    px = (pos[:, 0] - xm) * scale + W / 2
    py = (zm - pos[:, 1]) * scale + H / 2
    d0 = s['dmap'].get(1)
    uv0 = None
    if d0:
        uv0 = raw[:, d0[1]:d0[1] + 4].copy().view('<i2').reshape(s['nv'], 2).astype(np.float64) / 32767.0
    d1 = s['dmap'].get(2)
    uv1 = None
    if d1:
        uv1 = raw[:, d1[1]:d1[1] + 4].copy().view('<i2').reshape(s['nv'], 2).astype(np.float64) / 32767.0
    d17 = s['dmap'].get(17)
    c0 = None
    if d17:
        c0 = raw[:, d17[1]:d17[1] + 4].astype(np.float64) / 255.0
    tris = np.frombuffer(ld, '<u2', s['ib'] // 2, s['off'] + s['vb']).astype(np.int64).reshape(-1, 3)
    keep = (tris.max(axis=1) < s['nv'])
    tris = tris[keep]
    tris_all.append((pos, px, py, tris))
    uv0_all.append(uv0)
    uv1_all.append(uv1)
    c0_all.append(c0)
    meta.append(s)
zmean = np.concatenate([p[3].astype(np.float64) @ p[0][:, 2] / len(p[3]) for p in tris_all]) \
    if False else None
# global painter order over (segIdx, triIdx) by mean height
order = []
for si, (pos, px, py, tris) in enumerate(tris_all):
    zm_t = pos[tris].mean(axis=1)[:, 2]
    order.append((zm_t, np.full(len(tris), si, np.int32), np.arange(len(tris), dtype=np.int32)))
zm_cat = np.concatenate([o[0] for o in order])
si_cat = np.concatenate([o[1] for o in order])
ti_cat = np.concatenate([o[2] for o in order])
# deterministic total order: primary mean height, ties by (seg, tri)
painter = np.lexsort((ti_cat, si_cat, zm_cat))
si_cat = si_cat[painter]
ti_cat = ti_cat[painter]
zm_cat = zm_cat[painter]
print('total triangles:', len(zm_cat), 'painter order built at %.1f s' % (time.time() - t_start))

# ---------- pass 3: raster ----------
img = np.zeros((H, W, 3), np.float32)
t_r0 = time.time()
batches = 0
tex_binds = 0
cur_tex_key = None
for idx in range(len(zm_cat)):
    si = si_cat[idx]
    ti = ti_cat[idx]
    s = meta[si]
    pos, px, py, tris = tris_all[si]
    effect = fx_of.get(s['mat'], '')
    diff_name, lm_name = bind.get(s['mat'], ('', ''))
    tex = get_tex(diff_name, want_alpha=(effect == 'AlphaMasking'))
    if tex is None:
        continue
    tex_key = (diff_name, effect == 'AlphaMasking')
    if tex_key != cur_tex_key:
        cur_tex_key = tex_key
        tex_binds += 1
    batches += 1
    i0, i1, i2 = tris[ti]
    x0t, y0t, x1t, y1t, x2t, y2t = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
    xlo = max(int(min(x0t, x1t, x2t)), 0)
    xhi = min(int(max(x0t, x1t, x2t)) + 1, W - 1)
    ylo = max(int(min(y0t, y1t, y2t)), 0)
    yhi = min(int(max(y0t, y1t, y2t)) + 1, H - 1)
    if xlo > xhi or ylo > yhi:
        continue
    gx, gy = np.meshgrid(np.arange(xlo, xhi + 1) + 0.5, np.arange(ylo, yhi + 1) + 0.5)
    d = (y1t - y2t) * (x0t - x2t) + (x2t - x1t) * (y0t - y2t)
    if abs(d) < 1e-9:
        continue
    w0 = ((y1t - y2t) * (gx - x2t) + (x2t - x1t) * (gy - y2t)) / d
    w1 = ((y2t - y0t) * (gx - x2t) + (x0t - x2t) * (gy - y2t)) / d
    w2 = 1 - w0 - w1
    mask = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
    if not mask.any():
        continue
    T, TH_ = tex['w'], tex['h']
    uv0 = uv0_all[si]
    if uv0 is None:
        continue
    tuv = np.stack([uv0[:, 0] * 0.5 + 0.5, 1.0 - (uv0[:, 1] * 0.5 + 0.5)], axis=1)
    uu = w0 * tuv[i0, 0] + w1 * tuv[i1, 0] + w2 * tuv[i2, 0]
    vv = w0 * tuv[i0, 1] + w1 * tuv[i1, 1] + w2 * tuv[i2, 1]
    tx = np.clip((uu * T).astype(np.int64) % T, 0, T - 1)
    ty = np.clip((vv * TH_).astype(np.int64) % TH_, 0, TH_ - 1)
    col = tex['rgb'][ty, tx].astype(np.float32)
    if effect == 'AlphaMasking' and tex['a'] is not None:
        AW, AH = tex['a'].shape[1], tex['a'].shape[0]
        atx = np.clip((uu * AW).astype(np.int64) % AW, 0, AW - 1)
        aty = np.clip((vv * AH).astype(np.int64) % AH, 0, AH - 1)
        av = tex['a'][aty, atx].astype(np.float32)
        keep = av >= 76.5
        if not keep.any():
            continue
        mask = mask & keep
        if not mask.any():
            continue
    if effect == 'LightMapDC' and lm_name and uv1_all[si] is not None:
        lmt = get_tex(lm_name)
        if lmt is not None:
            LW, LH = lmt['w'], lmt['h']
            luv = uv1_all[si]
            luv_t = np.stack([luv[:, 0] * 0.5 + 0.5, 1.0 - (luv[:, 1] * 0.5 + 0.5)], axis=1)
            lu = w0 * luv_t[i0, 0] + w1 * luv_t[i1, 0] + w2 * luv_t[i2, 0]
            lv = w0 * luv_t[i0, 1] + w1 * luv_t[i1, 1] + w2 * luv_t[i2, 1]
            ltx = np.clip((lu * LW).astype(np.int64) % LW, 0, LW - 1)
            lty = np.clip((lv * LH).astype(np.int64) % LH, 0, LH - 1)
            lcol = lmt['rgb'][lty, ltx].astype(np.float32) / 255.0 * 2.0
            col = col * lcol
    elif effect == 'AlphaMasking' and lm_name and uv1_all[si] is not None:
        lmt = get_tex(lm_name)
        if lmt is not None:
            LW, LH = lmt['w'], lmt['h']
            luv = uv1_all[si]
            luv_t = np.stack([luv[:, 0] * 0.5 + 0.5, 1.0 - (luv[:, 1] * 0.5 + 0.5)], axis=1)
            lu = w0 * luv_t[i0, 0] + w1 * luv_t[i1, 0] + w2 * luv_t[i2, 0]
            lv = w0 * luv_t[i0, 1] + w1 * luv_t[i1, 1] + w2 * luv_t[i2, 1]
            ltx = np.clip((lu * LW).astype(np.int64) % LW, 0, LW - 1)
            lty = np.clip((lv * LH).astype(np.int64) % LH, 0, LH - 1)
            lcol = lmt['rgb'][lty, ltx].astype(np.float32) / 255.0 * 2.0 + 1.0
            col = col * lcol
    elif effect in ('SimpleAdditive', 'StandardDiffuseDC') and c0_all[si] is not None:
        c0 = c0_all[si]
        vc = (w0[..., None] * c0[i0] + w1[..., None] * c0[i1] + w2[..., None] * c0[i2])
        col = col * vc[..., :3]
    region = img[ylo:yhi + 1, xlo:xhi + 1]
    img[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask[..., None], col, region)
print('raster done at %.1f s (batches %d, tex binds %d, tex stats %s)'
      % (time.time() - t_r0, batches, tex_binds, _stats))
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(OUT_PNG)
lum = img.mean(axis=2)
out = {'W': W, 'H': H, 'scale': scale, 'n_seg_drawn': len(segdata),
       'batches': batches, 'tex_binds': tex_binds, 'tex_stats': _stats,
       'mean_lum': float(lum.mean()),
       'digest': hashlib.sha256(np.clip(img, 0, 255).astype(np.uint8).tobytes()).hexdigest(),
       'note': 'NormalSpecOverbright/NV_Glass/LightmapVCBlendDC/unknown rendered diffuse-only (documented deviation, same both sides)'}
json.dump(out, open(OUT_JSON, 'w'), indent=1)
print('saved', OUT_PNG, 'digest', out['digest'][:16], 'mean', round(out['mean_lum'], 2))
