#!/usr/bin/env python3
"""s50 T1: material-ownership analysis of the big-diff pixels (noLM pair).
Renders the winner-material id per pixel (painter order, exact edges), then
cross-references with s50_x_bigdiff_nolm.png."""
import struct, io, zipfile
import numpy as np
from PIL import Image
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
W, H = 1024, 605

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
imgs = [(int(w32[(IMG_BASE + i * 12) // 4]), int(w32[(IMG_BASE + i * 12 + 8) // 4])) for i in range(IMG_N)]
fx_of = {}
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    rawfx = (cstr(ws[3]) or '').split('-fx')[0].lstrip('#')
    fx_of[i] = rawfx if rawfx in ('LightMapDC', 'AlphaMasking', 'SimpleAdditive', 'StandardDiffuseDC') else 'other'

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
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

segdata = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    if not any(d[0] == 1 for d in ds):
        continue
    if fx_of.get(mid, 'other') != 'LightMapDC':
        continue
    segdata.append({'k': k, 'mat': mid, 'off': data_off + 4, 'vb': vb, 'ib': ib,
                    'nv': nv, 'stride': stride, 'dmap': {d[0]: d for d in ds}})

allpos = np.concatenate([
    np.frombuffer(ld, np.uint8, s['vb'], s['off']).reshape(s['nv'], s['stride'])[:, 0:12]
    .copy().view('<f4').reshape(-1, 3) for s in segdata])
x0, x1 = allpos[:, 0].min(), allpos[:, 0].max()
z0, z1 = allpos[:, 1].min(), allpos[:, 1].max()
scale = float(min(W / (x1 - x0), H / (z1 - z0)))
xm, zm = (x0 + x1) / 2, (z0 + z1) / 2

tris_all = []; meta = []
for s in segdata:
    raw = np.frombuffer(ld, np.uint8, s['vb'], s['off']).reshape(s['nv'], s['stride'])
    pos = raw[:, 0:12].copy().view('<f4').reshape(s['nv'], 3).astype(np.float64)
    px = (pos[:, 0] - xm) * scale + W / 2
    py = (zm - pos[:, 1]) * scale + H / 2
    tris = np.frombuffer(ld, '<u2', s['ib'] // 2, s['off'] + s['vb']).astype(np.int64).reshape(-1, 3)
    tris = tris[(tris.max(axis=1) < s['nv'])]
    tris_all.append((pos, px, py, tris))
    meta.append(s)

order = []
for si, (pos, px, py, tris) in enumerate(tris_all):
    zm_t = pos[tris].mean(axis=1)[:, 2]
    order.append((zm_t, np.full(len(tris), si, np.int32), np.arange(len(tris), dtype=np.int32)))
zm_cat = np.concatenate([o[0] for o in order])
si_cat = np.concatenate([o[1] for o in order])
ti_cat = np.concatenate([o[2] for o in order])
painter = np.lexsort((ti_cat, si_cat, zm_cat))
si_cat = si_cat[painter]; ti_cat = ti_cat[painter]

midmap = np.zeros((H, W), np.int32)
for idx in range(len(zm_cat)):
    si = si_cat[idx]; ti = ti_cat[idx]
    s = meta[si]
    pos, px, py, tris = tris_all[si]
    i0, i1, i2 = tris[ti]
    x0t, y0t, x1t, y1t, x2t, y2t = px[i0], py[i0], px[i1], py[i1], px[i2], py[i2]
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
    mask = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
    if not mask.any():
        continue
    midmap[ylo:yhi + 1, xlo:xhi + 1][mask] = s['mat']

bigdiff = np.asarray(Image.open('/tmp/my-project/work/city_slice_wt/playable/s50_x_bigdiff_nolm.png').convert('L')) > 127
sel = midmap[bigdiff]
vals, cnts = np.unique(sel[sel > 0], return_counts=True)
top = sorted(zip(cnts, vals), reverse=True)[:12]
print('winner-material histogram on big-diff pixels (LightMapDC family):')
tot_bd = int(bigdiff.sum())
for c, m in top:
    print('  mat %3d  %6d px (%.1f%% of bigdiff %d)' % (m, c, 100.0 * c / tot_bd, tot_bd))
# Also: what fraction of each material's own footprint is big-diff?
for c, m in top:
    own = (midmap == m).sum()
    print('  mat %3d owns %7d px total -> %.1f%% of its own area is big-diff' % (m, own, 100.0 * c / own))
