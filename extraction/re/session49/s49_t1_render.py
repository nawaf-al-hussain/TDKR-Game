#!/usr/bin/env python3
"""s49 T1: engine-shader render harness (Python reference side).

Blocks: road276 anchor (mat 73 LightMapDC x2), glass7 (segs 1486-92, mat 156
NV_Glass, Default = FOG+DIFFUSE_MASK, plus LIGHTMAP alt), vcblend (seg 1493,
mat 153 LightmapVCBlendDC: LM*2 * mix(dirt,grass,vc.a) * vc.rgb), stride28
(seg 1525, mat 302 AlphaMasking). Fog variants on road276 with the LevelInit
GI record's values: ComputeFogFS (the SHIPPED path - no compiled variant
defines VERTICALFOG) at camera depths, and the deployed viewer's TEXTURE_FOG
path at 25 u for the path-difference number.
"""
import struct, io, zipfile, json
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
OUT_JSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t1_render.json'
WT_PAGE = '/tmp/my-project/work/city_slice_wt/playable'

tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2*16: idxsz2]
_ct = {}

def tex_member(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16+i*16:16+i*16+16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            return tg[o:o+s]
    return None

def decode_pvr(u8):
    tag = struct.unpack_from('<I', u8, 0)[0]
    th_, tw = struct.unpack_from('<II', u8, 4)
    bw, bh = (tw+3)//4, (th_+3)//4
    return cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, bw*bh*8, 52), tw, th_)

def unwrap_split(u8):
    if bytes(u8[:4]) != b'PK\x03\x04':
        return {'rgb': u8}
    out = {}
    pos = 0
    while pos + 30 <= len(u8) and bytes(u8[pos:pos+4]) == b'PK\x03\x04':
        csz = struct.unpack_from('<I', u8, pos+18)[0]
        nlen = struct.unpack_from('<H', u8, pos+26)[0]
        elen = struct.unpack_from('<H', u8, pos+28)[0]
        nm = u8[pos+30:pos+30+nlen].decode('latin1')
        dstart = pos+30+nlen+elen
        if nm.strip() != 'SPLIT':
            out[nm] = u8[dstart:dstart+csz]
        pos = dstart+csz
    return out

def decode_tex(name):
    if name in _ct:
        return _ct[name]
    u8 = tex_member(name)
    if u8 is None:
        raise SystemExit('missing tex ' + name)
    parts = unwrap_split(u8)
    rgb = decode_pvr(parts['rgb.pvr']) if 'rgb.pvr' in parts else decode_pvr(parts['rgb'])
    al = decode_pvr(parts['alpha.pvr'])[:, :, 0].copy() if 'alpha.pvr' in parts else None
    t = {'rgb': rgb[:, :, :3].copy(), 'a': al, 'w': rgb.shape[1], 'h': rgb.shape[0],
         'split': 'alpha.pvr' in parts}
    _ct[name] = t
    return t

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi)-4)//bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]
_decl = {}

def decl_of(mid):
    if mid in _decl:
        return _decl[mid]
    r = recs[mid]
    N = int(r[33])
    ds = []
    start = 0
    for j in range(N):
        d = bytes(r[40+j*12: 40+(j+1)*12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B*VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size))
        start = end
    _decl[mid] = ds
    return ds

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16+n*16: idxsz]
ld = lt = None
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16+i*16:16+i*16+16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o+s]))
        ld = Z.read('lod_data.bin')
        lt = Z.read('lod_table.bin')
        break
u = struct.unpack('<%dI' % (len(lt)//4), lt)
pairs = [(u[1+2*k], u[2+2*k]) for k in range(u[0])]

def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v-65536, v)/32767.0

def block_geom(k, mid):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb//stride
    vstart = data_off+4
    raw = np.frombuffer(ld, np.uint8, vb, vstart)
    dmap = {d[0]: d for d in ds}
    posf = raw.reshape(nv, stride)[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    d0 = dmap[1]
    uv0 = s16a(raw.reshape(nv, stride)[:, d0[1]:d0[1]+4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    uv1 = None
    if 2 in dmap:
        d1 = dmap[2]
        uv1 = s16a(raw.reshape(nv, stride)[:, d1[1]:d1[1]+4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    d17 = dmap.get(17)
    c0 = None
    if d17 is not None:
        c0 = raw.reshape(nv, stride)[:, d17[1]:d17[1]+4].copy()
    tris = np.frombuffer(ld, '<u2', ib//2, vstart+vb).astype(np.int64).reshape(-1, 3)
    return posf, uv0, uv1, c0, tris, stride, dmap

FOG_COLOR = (64/255.0, 102/255.0, 119/255.0, 160/255.0)
FOG_END = 140.0
FOGMAP = (-1210.0, -220.0, 1/1520.0, -1/1130.0)
VFOG_ALPHA = 0.65

_FOGTEX = None

def raster(posf, uv0, tex, tris, lm=None, luv=None, lm_scale=2.0, lm_offset=0.0,
           alpha_discard=False, alpha_thr=76.5, vcolor=None, cam_h=None,
           fog=None, lm_second=None):
    """fog None | ('CF', rgba01) | ('TF', rgba01); cam_h: top-down camera height."""
    mn, mx = posf.min(0), posf.max(0)
    span = max(mx[0]-mn[0], mx[1]-mn[1])*1.04
    cx, cy = (mn[0]+mx[0])/2, (mn[1]+mx[1])/2
    img = np.zeros((SIZE, SIZE, 3), np.float32)
    cov = np.zeros((SIZE, SIZE), bool)
    W, H = tex['w'], tex['h']
    trgb = tex['rgb']
    tal = tex['a']
    tuv = uv0*0.5+0.5
    tuv = tuv.copy()
    tuv[:, 1] = 1.0-tuv[:, 1]
    px = (posf[:, 0]-cx)/span*SIZE + SIZE/2
    py = (cy-posf[:, 1])/span*SIZE + SIZE/2
    order = np.argsort(posf[tris].mean(axis=1)[:, 2])
    AW, AH = (tal.shape[1], tal.shape[0]) if tal is not None else (0, 0)
    vcol = vcolor.astype(np.float32)/255.0 if vcolor is not None else None
    luv_t = None
    if lm is not None and luv is not None:
        luv_t = luv*0.5+0.5
        luv_t = luv_t.copy()
        luv_t[:, 1] = 1.0-luv_t[:, 1]
        LW, LH = lm['w'], lm['h']
        lrgb = lm['rgb']
    fog_tex = _FOGTEX if (fog and fog[0] == 'TF') else None
    frgb = fog_tex['rgb'] if fog_tex else None
    FTW, FTH = (fog_tex['w'], fog_tex['h']) if fog_tex else (0, 0)
    fog_col = fog[1] if fog else None
    for t in order:
        i0, i1, i2 = tris[t]
        if max(i0, i1, i2) >= len(posf):
            continue
        x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
        xlo = max(int(min(x0, x1, x2)), 0)
        xhi = min(int(max(x0, x1, x2))+1, SIZE-1)
        ylo = max(int(min(y0, y1, y2)), 0)
        yhi = min(int(max(y0, y1, y2))+1, SIZE-1)
        if xlo > xhi or ylo > yhi:
            continue
        gx, gy = np.meshgrid(np.arange(xlo, xhi+1)+0.5, np.arange(ylo, yhi+1)+0.5)
        d = (y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(d) < 1e-9:
            continue
        w0 = ((y1-y2)*(gx-x2)+(x2-x1)*(gy-y2))/d
        w1 = ((y2-y0)*(gx-x2)+(x0-x2)*(gy-y2))/d
        w2 = 1-w0-w1
        mask = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
        if not mask.any():
            continue
        uu = w0*tuv[i0, 0]+w1*tuv[i1, 0]+w2*tuv[i2, 0]
        vv = w0*tuv[i0, 1]+w1*tuv[i1, 1]+w2*tuv[i2, 1]
        tx = np.clip((uu*W).astype(np.int64) % W, 0, W-1)
        ty = np.clip((vv*H).astype(np.int64) % H, 0, H-1)
        col = trgb[ty, tx].astype(np.float32)
        if tal is not None:
            atx = np.clip((uu*AW).astype(np.int64) % AW, 0, AW-1)
            aty = np.clip((vv*AH).astype(np.int64) % AH, 0, AH-1)
            av = tal[aty, atx].astype(np.float32)
            if alpha_discard:
                keep = av >= alpha_thr
                if not keep.any():
                    continue
                mask = mask & keep
                if not mask.any():
                    continue
        if vcol is not None:
            vc = (w0[..., None]*vcol[i0]+w1[..., None]*vcol[i1]+w2[..., None]*vcol[i2])
            col = col*vc[..., :3]
        if luv_t is not None:
            lu = w0*luv_t[i0, 0]+w1*luv_t[i1, 0]+w2*luv_t[i2, 0]
            lv = w0*luv_t[i0, 1]+w1*luv_t[i1, 1]+w2*luv_t[i2, 1]
            ltx = np.clip((lu*LW).astype(np.int64) % LW, 0, LW-1)
            lty = np.clip((lv*LH).astype(np.int64) % LH, 0, LH-1)
            lcol = lrgb[lty, ltx].astype(np.float32)/255.0*lm_scale+lm_offset
            col = col*lcol
        if fog is not None and cam_h is not None:
            zz = w0*posf[i0, 2]+w1*posf[i1, 2]+w2*posf[i2, 2]
            dep = np.maximum(cam_h-zz, 0.0)
            FF = np.clip(dep/FOG_END, 0.0, 1.0)
            gray = (col[..., 0]*0.149+col[..., 1]*0.293+col[..., 2]*0.57)/255.0
            if fog[0] == 'CF':
                m = (FF*(1.0-gray))*fog_col[3]
                fc = np.array(fog_col[:3])[None, None]*255.0
                col = col*(1-m[..., None])+fc*m[..., None]
            else:
                wx = cx + (gx-SIZE/2)*span/SIZE
                wy = cy + (SIZE/2-gy)*span/SIZE
                fuvx = (wx-FOGMAP[0])*FOGMAP[2]
                fuvy = (wy-FOGMAP[1])*FOGMAP[3]
                ftx = np.clip((fuvx*FTW).astype(np.int64) % FTW, 0, FTW-1)
                fty = np.clip((fuvy*FTH).astype(np.int64) % FTH, 0, FTH-1)
                fmc = frgb[fty, ftx].astype(np.float32)
                fY = np.clip(zz*0.013+FF*0.5, 0.0, 1.0)
                fc3 = np.array(fog_col[:3])[None, None]*255.0
                fogcol2 = fmc*(1-fY[..., None])+fc3*fY[..., None]
                fA = VFOG_ALPHA*(1-fY)+fog_col[3]*fY
                fmix = np.clip(FF, 0.0, 1.0)*fA
                col = col*(1-fmix[..., None])+fogcol2*fmix[..., None]
        region = img[ylo:yhi+1, xlo:xhi+1]
        regc = cov[ylo:yhi+1, xlo:xhi+1]
        img[ylo:yhi+1, xlo:xhi+1] = np.where(mask[..., None], col, region)
        cov[ylo:yhi+1, xlo:xhi+1] = np.where(mask, True, regc)
    return img, cov

def lum(img):
    return img.mean(axis=2)

def mean_cov(img, cov):
    return float(lum(img)[cov].mean()) if cov.any() else 0.0

def hist_lum(img, cov):
    v = lum(img)[cov]
    return [int(x) for x in np.histogram(v, 32, (0, 255))[0]]

# ================= main =================
def main():
    out = {'note': 's49 T1: real effect math per compiled profile; fog per LevelInit GI record '
                   '(start 0, end 140, FogColor RGBA(64,102,119,160), ComputeFogFS = shipped path '
                   '(no compiled variant defines VERTICALFOG); deployed TEXTURE_FOG variant for diff',
           'fog_constants': {'start': 0.0, 'end': FOG_END, 'color_rgba': FOG_COLOR,
                             'fogmap': FOGMAP, 'vfog_alpha': VFOG_ALPHA,
                             'vfog_height': 0.013, 'fog_decay': 0.5,
                             'fogtex': 'GC_VerticalFOG.tga', 'lut': '000_default.tga (CCFS2 16x16x16)'},
           'blocks': []}
    global _FOGTEX
    _FOGTEX = decode_tex('GC_VerticalFOG.tga')
    print('fog tex', _FOGTEX['w'], 'x', _FOGTEX['h'], 'mean', _FOGTEX['rgb'].mean(axis=(0, 1)))

    # ---- block: road276 anchor (LightMapDC x2, s48 anchor 119.76 / 32.84) ----
    posf, uv0, uv1, c0, tris, stride, dmap = block_geom(695, 73)
    dtex = decode_tex('gothamcity_roads_details.tga')
    lmtex = decode_tex('BakeGroup_Island1_Roads0.tga')
    img_plain, cov = raster(posf, uv0, dtex, tris)
    e = {'tag': 'road276', 'k': 695, 'mat': 73, 'effect': 'LightMapDC',
         'mean_plain': mean_cov(img_plain, cov), 'cov_plain': int(cov.sum())}
    img2, cov2 = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0)
    e['mean_lm2'] = mean_cov(img2, cov2)
    e['hist_lm2'] = hist_lum(img2, cov2)
    Image.fromarray(np.clip(img2, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_road276_lm2.png')
    # fog variants (shipped ComputeFogFS) at street/sky depths
    for h in (25.0, 60.0, 100.0, 154.0):
        imgf, covf = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0,
                            cam_h=h, fog=('CF', FOG_COLOR))
        e['mean_lm2_cfog_%du' % int(h)] = mean_cov(imgf, covf)
        e['hist_lm2_cfog_%du' % int(h)] = hist_lum(imgf, covf)
        Image.fromarray(np.clip(imgf, 0, 255).astype(np.uint8)).save(
            WT_PAGE + '/s49_ref_road276_cfog_%du.png' % int(h))
    # deployed TEXTURE_FOG path at 25 u
    imgt, covt = raster(posf, uv0, dtex, tris, lm=lmtex, luv=uv1, lm_scale=2.0,
                        cam_h=25.0, fog=('TF', FOG_COLOR))
    e['mean_lm2_tfog_25u'] = mean_cov(imgt, covt)
    e['hist_lm2_tfog_25u'] = hist_lum(imgt, covt)
    Image.fromarray(np.clip(imgt, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_road276_tfog_25u.png')
    out['blocks'].append(e)
    print('road276:', json.dumps(e, indent=1))

    # ---- block: glass7 (segs 1486-1492, mat 156 NV_Glass) ----
    # Default profile FOG+DIFFUSE_MASK: Color = Diffuse * vColor0; a = Mask.g * vColor0.a
    # LIGHTMAP alt: Color = Diffuse * vColor0 * (LM*2)
    gpos, guv0, guv1, gc0, gtris = [], [], [], [], []
    base = None
    for k in range(1486, 1493):
        p, u0, u1, c0b, tr, st, dm = block_geom(k, 156)
        if base is None:
            mn = p.min(0); mx = p.max(0)
            base = (mn, mx)
        else:
            mn = np.minimum(base[0], p.min(0)); mx = np.maximum(base[1], p.max(0))
            base = (mn, mx)
        gpos.append(p); guv0.append(u0); guv1.append(u1); gc0.append(c0b); gtris.append(tr)
    span = max(base[1][0]-base[0][0], base[1][1]-base[0][1])*1.04
    cx, cy = (base[0][0]+base[1][0])/2, (base[0][1]+base[1][1])/2
    img = np.zeros((SIZE, SIZE, 3), np.float32)
    cov = np.zeros((SIZE, SIZE), bool)
    dtex_g = decode_tex('GC_footprint_AB_atlas.tga')
    mtex_g = decode_tex('GC_footprint_AB_atlas_rfl.tga')
    lmtex_g = decode_tex('confroom_lightmap.tga')
    for si in range(len(gpos)):
        p, u0, c0b, tr = gpos[si], guv0[si], gc0[si], gtris[si]
        u1s = guv1[si]
        nv = len(p)
        px = (p[:, 0]-cx)/span*SIZE + SIZE/2
        py = (cy-p[:, 1])/span*SIZE + SIZE/2
        tuv = u0*0.5+0.5
        tuv = tuv.copy(); tuv[:, 1] = 1.0-tuv[:, 1]
        vcol = c0b.astype(np.float32)/255.0
        order = np.argsort(p[tr].mean(axis=1)[:, 2])
        for t in order:
            i0, i1, i2 = tr[t]
            if max(i0, i1, i2) >= nv:
                continue
            x0, y0, x1, y1, x2, y2 = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
            xlo = max(int(min(x0, x1, x2)), 0); xhi = min(int(max(x0, x1, x2))+1, SIZE-1)
            ylo = max(int(min(y0, y1, y2)), 0); yhi = min(int(max(y0, y1, y2))+1, SIZE-1)
            if xlo > xhi or ylo > yhi:
                continue
            gx, gy = np.meshgrid(np.arange(xlo, xhi+1)+0.5, np.arange(ylo, yhi+1)+0.5)
            d = (y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(d) < 1e-9:
                continue
            w0 = ((y1-y2)*(gx-x2)+(x2-x1)*(gy-y2))/d
            w1 = ((y2-y0)*(gx-x2)+(x0-x2)*(gy-y2))/d
            w2 = 1-w0-w1
            mask = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
            if not mask.any():
                continue
            uu = w0*tuv[i0, 0]+w1*tuv[i1, 0]+w2*tuv[i2, 0]
            vv = w0*tuv[i0, 1]+w1*tuv[i1, 1]+w2*tuv[i2, 1]
            W, H = dtex_g['w'], dtex_g['h']
            tx = np.clip((uu*W).astype(np.int64) % W, 0, W-1)
            ty = np.clip((vv*H).astype(np.int64) % H, 0, H-1)
            col = dtex_g['rgb'][ty, tx].astype(np.float32)
            MW, MH = mtex_g['w'], mtex_g['h']
            mtx = np.clip((uu*MW).astype(np.int64) % MW, 0, MW-1)
            mty = np.clip((vv*MH).astype(np.int64) % MH, 0, MH-1)
            mval = mtex_g['rgb'][mty, mtx].astype(np.float32)
            vc = (w0[..., None]*vcol[i0]+w1[..., None]*vcol[i1]+w2[..., None]*vcol[i2])
            col = col*vc[..., :3]
            LW, LH = lmtex_g['w'], lmtex_g['h']
            tuv1 = u1s*0.5+0.5
            tuv1 = tuv1.copy(); tuv1[:, 1] = 1.0-tuv1[:, 1]
            lu = w0*tuv1[i0, 0]+w1*tuv1[i1, 0]+w2*tuv1[i2, 0]
            lv = w0*tuv1[i0, 1]+w1*tuv1[i1, 1]+w2*tuv1[i2, 1]
            ltx = np.clip((lu*LW).astype(np.int64) % LW, 0, LW-1)
            lty = np.clip((lv*LH).astype(np.int64) % LH, 0, LH-1)
            lcol = lmtex_g['rgb'][lty, ltx].astype(np.float32)/255.0*2.0
            col_lm = col*lcol
            region = img[ylo:yhi+1, xlo:xhi+1]
            regc = cov[ylo:yhi+1, xlo:xhi+1]
            img[ylo:yhi+1, xlo:xhi+1] = np.where(mask[..., None], col_lm, region)
            cov[ylo:yhi+1, xlo:xhi+1] = np.where(mask, True, regc)
    eg = {'tag': 'glass7', 'segs': [1486, 1487, 1488, 1489, 1490, 1491, 1492],
          'mat': 156, 'effect': 'NV_Glass', 'profile_default': 'FOG+DIFFUSE_MASK',
          'mean_glass_lm': mean_cov(img, cov), 'cov_glass': int(cov.sum()),
          'color0_mean': [float(x) for x in np.concatenate(gc0).mean(axis=0)],
          'mask_g_mean': float(mval.mean())}
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_glass7_lm.png')
    out['blocks'].append(eg)
    print('glass7:', json.dumps({k: v for k, v in eg.items() if k != 'hist'}, indent=1))

    # ---- block: vcblend (seg 1493, mat 153 LightmapVCBlendDC) ----
    p, u0, u1, c0b, tr, st, dm = block_geom(1493, 153)
    lmv = decode_tex('BakeGroup_Island1_A0.tga')
    t1 = decode_tex('GC_Park_dirt.tga')
    t2 = decode_tex('GC_Park_grass.tga')
    imgv, covv = raster(p, u0, t1, tr, lm=lmv, luv=u1, lm_scale=2.0,
                        vcolor=None)
    # blend in JS-free numpy: need custom pass -> do a second raster with t2 and mix by alpha
    imgv2, covv2 = raster(p, u0, t2, tr, lm=lmv, luv=u1, lm_scale=2.0)
    va = c0b[:, 3].astype(np.float32)/255.0
    vrgb = c0b[:, :3].astype(np.float32)/255.0
    ev = {'tag': 'vcblend', 'k': 1493, 'mat': 153, 'effect': 'LightmapVCBlendDC',
          'diffuse': 'GC_Park_dirt.tga', 'tex2': 'GC_Park_grass.tga',
          'lm': 'BakeGroup_Island1_A0.tga',
          'color0_mean': [float(x) for x in c0b.mean(axis=0)],
          'color0_alpha_mean': float(va.mean()),
          'mean_tex1_only': mean_cov(imgv, covv),
          'mean_tex2_only': mean_cov(imgv2, covv2)}
    Image.fromarray(np.clip(imgv, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_vcblend_tex1.png')
    Image.fromarray(np.clip(imgv2, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_vcblend_tex2.png')
    out['blocks'].append(ev)
    print('vcblend:', json.dumps(ev, indent=1))

    # ---- block: stride28 (seg 1525, mat 302 AlphaMasking) - s48 anchor recheck ----
    p, u0, u1, c0b, tr, st, dm = block_geom(1525, 302)
    dtx = decode_tex('GC_Z1_Props_Street_Alpha.tga')
    lmx = decode_tex('BakeGroup_Island1_A0.tga')
    imga, cova = raster(p, u0, dtx, tr, lm=lmx, luv=u1, lm_scale=2.0, lm_offset=1.0,
                        alpha_discard=True)
    ea = {'tag': 'stride28', 'k': 1525, 'mat': 302, 'effect': 'AlphaMasking',
          'mean_lm2o': mean_cov(imga, cova), 'cov_lm2o': int(cova.sum())}
    Image.fromarray(np.clip(imga, 0, 255).astype(np.uint8)).save(
        WT_PAGE + '/s49_ref_stride28_lm2o.png')
    out['blocks'].append(ea)
    print('stride28:', ea, '(s48 anchor 111.43)')

    json.dump(out, open(OUT_JSON, 'w'), indent=1)
    print('saved', OUT_JSON)

if __name__ == '__main__':
    main()
