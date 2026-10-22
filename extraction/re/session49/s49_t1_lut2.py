#!/usr/bin/env python3
"""s49 T1d v2: LUT 000_default.tga is RGB565 (fmt 0x13, 16bpp) — rebuild + apply CCFS2."""
import struct
import numpy as np
from PIL import Image

ct = open('/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/commons_tex.gla','rb').read()
_, i2, t2, n2 = struct.unpack('>IIII', ct[:16])
p2 = ct[16+n2*16:i2]
def member2(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', ct[16+i*16:16+i*16+16])
        e = p2.index(b'\0', no)
        if p2[no:e].decode('ascii','replace').lower() == want.lower():
            return ct[o:o+s]
u8 = member2('000_default.tga')
h, w = 16, 512
px = np.frombuffer(u8, '<u2', w*h, 52).reshape(h, w)
lut = np.zeros((h, w, 3), np.float64)
lut[..., 0] = ((px >> 11) & 0x1f) * 255 / 31
lut[..., 1] = ((px >> 5) & 0x3f) * 255 / 63
lut[..., 2] = (px & 0x1f) * 255 / 31
np.save('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_lut000_565.npy', lut)

def apply_cc(im):
    c = im / 255.0
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    u = r * 0.0625 * 0.94 + 0.001875 + np.floor(b * 15.99) * 0.0625
    v = g
    ui = np.clip((u * 512).astype(np.int64) % 512, 0, 511)
    vi = np.clip((v * 16).astype(np.int64) % 16, 0, 15)
    return lut[vi, ui, :3]

ramp = np.tile(np.linspace(0, 255, 256), (8, 1))[..., None] * np.ones((8, 256, 3))
rr = apply_cc(ramp)
print('gray ramp in/out:', [(int(ramp[4, i, 0]), int(round(rr[4, i, 0]))) for i in (0, 32, 64, 96, 128, 160, 192, 224, 255)])

for name, src in (('cfog25', 's49_ref_road276_cfog_25u.png'), ('prefog', 's49_ref_road276_lm2.png'),
                  ('tfog25', 's49_ref_road276_tfog_25u.png')):
    img = np.array(Image.open('/tmp/my-project/work/city_slice_wt/playable/' + src)).astype(np.float64)
    cov = img.sum(axis=2) > 0
    out = apply_cc(img)
    print('%s: pre-LUT %.2f -> post-LUT %.2f (covered px %d)' %
          (name, img[cov].mean(), out[cov].mean(), cov.sum()))
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
        '/tmp/my-project/work/city_slice_wt/playable/s49_ref_road276_%s_lut.png' % name)
