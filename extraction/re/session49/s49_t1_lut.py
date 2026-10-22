#!/usr/bin/env python3
"""s49 T1d: apply the game's ColorCorrection post (CCFS2, LUT 000_default.tga)
to the fog-applied road render -> the game's full visible chain."""
import numpy as np
from PIL import Image

lut = np.load('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_tex_000_default.npy')  # (16,512,4)
img = np.array(Image.open('/tmp/my-project/work/city_slice_wt/playable/s49_ref_road276_cfog_25u.png')).astype(np.float64)
H, W, _ = img.shape
cov = img.sum(axis=2) > 0
def apply_cc(im):
    c = im / 255.0
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    u = r * 0.0625 * 0.94 + 0.001875 + np.floor(b * 15.99) * 0.0625
    v = g
    ui = np.clip((u * 512).astype(np.int64) % 512, 0, 511)
    vi = np.clip((v * 16).astype(np.int64) % 16, 0, 15)
    return lut[vi, ui, :3]
out = apply_cc(img)
m0 = img[cov].mean() if cov.any() else 0
m1 = out[cov].mean() if cov.any() else 0
print('road276 CF-fog 25u: pre-LUT mean %.2f -> post-LUT mean %.2f' % (m0, m1))
# also LUT on the plain engine render and the pre-fog
img2 = np.array(Image.open('/tmp/my-project/work/city_slice_wt/playable/s49_ref_road276_lm2.png')).astype(np.float64)
cov2 = img2.sum(axis=2) > 0
o2 = apply_cc(img2)
print('road276 pre-fog:    pre-LUT mean %.2f -> post-LUT mean %.2f' % (img2[cov2].mean(), o2[cov2].mean()))
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
    '/tmp/my-project/work/city_slice_wt/playable/s49_ref_road276_cfog25_lut.png')
# LUT identity check on a gray ramp
ramp = np.tile(np.linspace(0, 255, 256), (8, 1))[..., None] * np.ones((8, 256, 3))
rr = apply_cc(ramp)
print('LUT ramp in/out at 0/64/128/192/255:',
      [(int(ramp[4, i, 0]), int(rr[4, i, 0])) for i in (0, 64, 128, 192, 255)])
