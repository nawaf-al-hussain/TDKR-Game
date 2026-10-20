#!/usr/bin/env python3
"""S41 T2 calibration round 2: bit-replication 565, normal-map structural
test for 888 order, alpha-byte structural + template test for 8888."""
import struct, sys, zipfile
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
TX = '/tmp/my-project/work/ghpages_live_wt/models/tex'

def get(arch, name):
    d, ents = read_archive(Z, arch)
    for (n, off, size) in ents:
        if n == name:
            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off+52], 0)
            return d[off+52:off+52+dsz], wid, hgt, bpp
    raise KeyError(name)

# ---- 565 with bit replication ----
buf, w, h, bpp = get('commons_tex.gla', '000_default.tga')
v = np.frombuffer(buf, '<u2').reshape(h, w)
r5 = ((v >> 11) & 31); g6 = ((v >> 5) & 63); b5 = (v & 31)
r = (r5 << 3) | (r5 >> 2); g = (g6 << 2) | (g6 >> 4); b = (b5 << 3) | (b5 >> 2)
rgb = np.stack([r, g, b], -1)
bgr = np.stack([b, g, r], -1)
ref = np.array(Image.open(f'{TX}/LUT_000_default.png').convert('RGB'))
print('565 bit-replication: R5G6B5 exact =', round(float((rgb == ref).all(-1).mean()), 4),
      ' B5G6R5 exact =', round(float((bgr == ref).all(-1).mean()), 4))

# ---- 888: normal-map structural test ----
buf, w, h, bpp = get('actors_tex.gla', 'chara_Batman_NM.tga')
px = np.frombuffer(buf, np.uint8, w * h * 3).reshape(h, w, 3).astype(float)
means = px.reshape(-1, 3).mean(0)
print(f'888 NM memory-channel means: [{means[0]:.1f} {means[1]:.1f} {means[2]:.1f}]')
print('  -> if memory=RGB: B is z (expect B high ~180+). If memory=BGR: R is z.')
# also decode per s40 convention (BGR) into an image and sanity-check the map's blue dominance
as_rgb = px  # treating memory order as RGB directly
print('  decoded-as-RGB blue-mean:', round(means[2], 1), ' red-mean:', round(means[0], 1))

# ---- 8888: alpha-byte structure + template match ----
buf, w, h, bpp = get('commons_tex.gla', 'FX_Coronas_Glow.tga')
px = np.frombuffer(buf, np.uint8, w * h * 4).reshape(h, w, 4).astype(float)
for i, tag in ((0, 'byte0'), (1, 'byte1'), (2, 'byte2'), (3, 'byte3')):
    c = px[:, :, i]
    zeros = float((c < 8).mean()); highs = float((c > 240).mean())
    print(f'8888 {tag}: zero-frac {zeros:.3f} high-frac {highs:.3f} mean {c.mean():.1f}')
print('  (alpha of a radial glow: many zeros + smooth falloff; a color channel: not)')

jpg = np.asarray(Image.open(f'{TX}/FX_Coronas.jpg').convert('L'), float)
jh, jw = jpg.shape
tile_g = px[:, :, 1]  # green as template (grayscale corr)
best = (-1, 0, 0)
th, tw = h, w
for yy in range(0, jh - th + 1, 4):
    for xx in range(0, jw - tw + 1, 4):
        win = jpg[yy:yy+th, xx:xx+tw]
        if win.std() < 1: continue
        c = np.corrcoef(win.ravel(), tile_g.ravel())[0, 1]
        if c > best[0]: best = (c, xx, yy)
print(f'8888 coarse template best corr={best[0]:.3f} at ({best[1]},{best[2]})')
c0, x0, y0 = best
win = jpg[y0:y0+th, x0:x0+tw]
for tag, ch in (('R=byte0', px[:, :, 0]), ('G=byte1', px[:, :, 1]), ('B=byte2', px[:, :, 2]), ('A=byte3', px[:, :, 3])):
    print(f'  {tag}: corr-vs-jpg = {np.corrcoef(win.ravel(), ch.ravel())[0,1]:.4f}')
