#!/usr/bin/env python3
"""s51 T1b: analytic texture means + shared-pixel corr; locate GL noLM artifact."""
import struct, io, zipfile, glob
import numpy as np
from PIL import Image

D = '/tmp/my-project/work/city_slice_wt/playable/'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'

import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

tg = open(TEXGLA, 'rb').read()
_, idxsz2, _, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]
_mem = {}
for i in range(n2):
    o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
    nm = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
    _mem[nm.lower()] = (o, s, nm)

def decode_mips(name, want_alpha=False):
    o, s, nm = _mem[name.lower()]
    u8 = tg[o:o + s]
    if u8[:4] == b'PK\x03\x04':
        # split zip: take rgb.pvr
        pos = 0
        parts = {}
        while pos + 30 <= len(u8) and bytes(u8[pos:pos+4]) == b'PK\x03\x04':
            csz = struct.unpack_from('<I', u8, pos + 18)[0]
            nlen = struct.unpack_from('<H', u8, pos + 26)[0]
            elen = struct.unpack_from('<H', u8, pos + 28)[0]
            m = u8[pos + 30:pos + 30 + nlen].decode('latin1')
            dstart = pos + 30 + nlen + elen
            if m.strip() != 'SPLIT':
                parts[m] = u8[dstart:dstart + csz]
            pos = dstart + csz
        u8 = parts.get('rgb.pvr', parts.get('rgb'))
    th_, tw = struct.unpack_from('<II', u8, 4)
    levels = []
    off = 52
    w, h = tw, th_
    while off < len(u8) and w >= 1 and h >= 1:
        bw, bh = max(1, (w + 3) // 4), max(1, (h + 3) // 4)
        sz = bw * bh * 8
        if off + sz > len(u8):
            break
        img = cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, sz, off), w, h)
        levels.append((w, h, img[:, :, :3]))
        off += sz
        w, h = max(1, w // 2), max(1, h // 2)
        if tw == 1 and th_ == 1:
            break
        if w == 1 and h == 1 and len(levels) > 12:
            break
    return tw, th_, levels

for nm in ('gothamcity_roads_details.tga', 'BakeGroup_Island1_Roads0.tga'):
    tw, th_, levels = decode_mips(nm)
    print('%s: %dx%d levels=%d' % (nm, tw, th_, len(levels)))
    for i, (w, h, img) in enumerate(levels):
        print('   lvl%d %dx%d mean=%.2f (rgb %s)' % (i, w, h, img.mean(axis=(0, 1)).mean(),
                                                     np.round(img.mean(axis=(0, 1)), 1)))

# shared-pixel corr + per-pixel brightness histogram for the withLM pair
G = np.asarray(Image.open(D + 's50_g_mat73.png').convert('RGB'), np.float64)
R = np.asarray(Image.open(D + 's50_ref_mat73.png').convert('RGB'), np.float64)
gl_l = G.mean(axis=2); rf_l = R.mean(axis=2)
both = (gl_l > 0) & (rf_l > 0)
a = gl_l[both]; b = rf_l[both]
print('shared px: n=%d corr=%.4f meanGL=%.2f meanRef=%.2f ratio=%.3f' %
      (both.sum(), np.corrcoef(a, b)[0, 1], a.mean(), b.mean(), b.mean() / a.mean()))
# distribution of per-pixel ratio
r = b / np.maximum(a, 1e-6)
print('per-pixel ratio ref/gl: p10=%.2f p50=%.2f p90=%.2f' % tuple(np.percentile(r, [10, 50, 90])))

# find GL noLM png candidates
print('\nnoLM GL candidates:', [p.split('/')[-1] for p in glob.glob(D + 's50_g*nolm*') + glob.glob(D + '*nolm*g*.png')])
