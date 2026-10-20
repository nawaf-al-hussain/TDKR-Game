#!/usr/bin/env python3
"""S41 T2: calibrate byte order for RGB565 / RGB888 / RGBA8888 against
independent deployed references (LUT PNG is lossless; JPGs are lossy but
channel-order discriminating)."""
import io, struct, sys, zipfile
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
            hdr = d[off:off+52]
            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', hdr, 0)
            return d[off+52:off+52+dsz], wid, hgt, bpp
    raise KeyError(name)

def corr(a, b):
    a = a.astype(float).reshape(-1); b = b.astype(float).reshape(-1)
    if len(a) != len(b):
        return -1
    if a.std() < 1e-6 or b.std() < 1e-6: return -1
    return float(np.corrcoef(a, b)[0, 1])

# ---- RGB565 vs lossless LUT PNG ----
buf, w, h, bpp = get('commons_tex.gla', '000_default.tga')
v = np.frombuffer(buf, '<u2').reshape(h, w)
r = ((v >> 11) & 31) * 255 // 31
g = ((v >> 5) & 63) * 255 // 63
b = (v & 31) * 255 // 31
rgb_std = np.stack([r, g, b], -1)
rgb_bgr = np.stack([b, g, r], -1)
ref = np.array(Image.open(f'{TX}/LUT_000_default.png').convert('RGB'))
print('LUT png size:', ref.shape, 'tga:', w, h)
for tag, im in (('R5G6B5', rgb_std), ('B5G6R5', rgb_bgr)):
    print(f'  {tag}: exact-match rate = {float((im == ref).all(-1).mean()):.4f}')

# ---- RGB888 vs deployed JPG (City_BKG) ----
buf, w, h, bpp = get('l_gothamcity_tex.gla', 'City_BKG.tga')
px = np.frombuffer(buf, np.uint8, w * h * 3).reshape(h, w, 3)
rgb = px[:, :, ::-1]  # memory BGR -> RGB
jpg = Image.open(f'{TX}/City_BKG.jpg').convert('RGB')
print('City_BKG tga', w, h, 'jpg', jpg.size)
if jpg.size != (w, h):
    rgb = np.array(Image.fromarray(rgb).resize(jpg.size, Image.BOX))
    mem = np.array(Image.fromarray(px).resize(jpg.size, Image.BOX))
else:
    mem = px
jr = np.asarray(jpg, float)
print(f'  as RGB(memory=BGR): corr per channel = {[round(corr(rgb[:, :, k], jr[:, :, k]), 4) for k in range(3)]}')
print(f'  as RGB(memory=RGB): corr per channel = {[round(corr(mem[:, :, k], jr[:, :, k]), 4) for k in range(3)]}')

# ---- RGBA8888 vs deployed JPG (FX_Coronas) ----
buf, w, h, bpp = get('commons_tex.gla', 'FX_Coronas_Glow.tga')
px = np.frombuffer(buf, np.uint8, w * h * 4).reshape(h, w, 4)
jpg = Image.open(f'{TX}/FX_Coronas.jpg').convert('RGB')
print('FX_Coronas_Glow tga', w, h, 'jpg', jpg.size)
for tag, order in (('RGBA', (0, 1, 2)), ('BGRA->RGB', (2, 1, 0))):
    im = px[:, :, list(order)]
    if jpg.size != (w, h):
        im = np.array(Image.fromarray(im).resize(jpg.size, Image.BOX))
    jr = np.asarray(jpg, float)
    print(f'  {tag}: corr per channel = {[round(corr(im[:, :, k], jr[:, :, k]), 4) for k in range(3)]}')
