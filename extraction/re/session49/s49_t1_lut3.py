#!/usr/bin/env python3
"""s49 T1d v3: LUT layout = 32 blue blocks x 16 px, RGB565, CCFS (cells=32) mapping."""
import numpy as np
from PIL import Image

lut = np.load('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_lut000_565.npy')  # (16,512,3)

def apply_cc(im):
    c = im / 255.0
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    # CCFS.glsl: u = r*cellsize*r_scale + r_off + floor(b*c16)*cellsize ; v = g
    cellsize = 1.0/32.0
    u = r * cellsize * 0.9375 + 0.03125 * cellsize + np.floor(b * (32.0-0.0001)) * cellsize
    v = g
    ui = np.clip((u * 512).astype(np.int64) % 512, 0, 511)
    vi = np.clip((v * 16).astype(np.int64) % 16, 0, 15)
    return lut[vi, ui, :3]

ramp = np.tile(np.linspace(0, 255, 256), (8, 1))[..., None] * np.ones((8, 256, 3))
rr = apply_cc(ramp)
print('gray ramp:', [(int(ramp[4, i, 0]), int(round(rr[4, i, 0]))) for i in (0, 32, 64, 96, 128, 160, 192, 224, 255)])
for name, src in (('cfog25', 's49_ref_road276_cfog_25u.png'), ('prefog', 's49_ref_road276_lm2.png'),
                  ('tfog25', 's49_ref_road276_tfog_25u.png')):
    img = np.array(Image.open('/tmp/my-project/work/city_slice_wt/playable/' + src)).astype(np.float64)
    cov = img.sum(axis=2) > 0
    out = apply_cc(img)
    print('%s: pre-LUT %.2f -> post-LUT %.2f' % (name, img[cov].mean(), out[cov].mean()))
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
        '/tmp/my-project/work/city_slice_wt/playable/s49_ref_road276_%s_lut.png' % name)
