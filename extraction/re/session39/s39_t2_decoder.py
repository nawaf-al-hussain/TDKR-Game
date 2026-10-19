#!/usr/bin/env python3
"""S39 T2g: FINAL numpy PVRTC4 decoder for the real .tga files.

Layout established empirically (s39):
  - blocks LINEAR (not Morton) in file order
  - word0 = color data: A = ARGB3443 (a12-14, r8-11, g4-7, b1-3), opA=0 always;
                       B = ARGB3444 (a29-31, r24-27, g20-23, b16-19), opB=0 always
  - word1 = modulation: 2-bit/texel LSB-first (y,x), WordModMode = word0 bit0
  - bilinear upscale across P,Q,R,S (wrap) per PowerVR reference
"""
import struct, zipfile, sys
import numpy as np
from PIL import Image


def expand4(v): return ((v << 1) | (v >> 3)) & 31
def expand3(v): return ((v << 2) | v) & 31


def load_tga_mip0(path_key='GC_StockExchange_Gargoyle.tga', container=None):
    z = zipfile.ZipFile(container or '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/actors_tex.gla')
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    ents = {}
    for i in range(n):
        o = 16 + i * 16
        off, size, nameOff = struct.unpack_from('>3I', d, o)
        nb = pool + nameOff
        e = d.index(b'\0', nb)
        ents[d[nb:e].decode('latin1')] = (off, size)
    off, size = ents[path_key]
    w, h = struct.unpack_from('<II', d, off + 4)
    return d, off, w, h, size


def decode(mip0_bytes, w, h):
    BW, BH = w // 4, h // 4
    NB = BW * BH
    words = np.frombuffer(mip0_bytes, np.uint32).reshape(NB, 2).astype(np.int64)
    cw, mw = words[:, 0], words[:, 1]

    def grid(a): return a.reshape(BH, BW)
    gc, gm = grid(cw), grid(mw)
    Pc, Qc, Rc, Sc = gc, np.roll(gc, -1, 1), np.roll(gc, -1, 0), np.roll(np.roll(gc, -1, 1), -1, 0)
    Pm = gm

    # endpoint colors (5-bit internals, 0-31)
    def colA(cd):
        a = (cd >> 12) & 7
        r = expand4((cd >> 8) & 15)
        g = expand4((cd >> 4) & 15)
        b = expand3((cd >> 1) & 7)
        return np.stack([r, g, b, a], 1)
    def colB(cd):
        a = (cd >> 29) & 7
        r = expand4((cd >> 24) & 15)
        g = expand4((cd >> 20) & 15)
        b = expand4((cd >> 16) & 15)
        return np.stack([r, g, b, a], 1)

    A = {k: colA(v.reshape(-1)) for k, v in [('P', Pc), ('Q', Qc), ('R', Rc), ('S', Sc)]}
    B = {k: colB(v.reshape(-1)) for k, v in [('P', Pc), ('Q', Qc), ('R', Rc), ('S', Sc)]}

    # modulation values per P-block, LSB-first (y,x)
    modebit = (Pc & 1).reshape(-1)
    cur = Pm.reshape(-1).copy()
    vals = np.zeros((NB, 16), np.int64)
    for i in range(16):
        vals[:, i] = cur & 3
        cur >>= 2
    m0 = vals * 3
    m0 = np.where(m0 > 3, m0 - 1, m0)
    m1 = np.select([vals == 1, vals == 2, vals == 3], [4, 14, 8], 0)
    mods = np.where((modebit == 0)[:, None], m0, m1)

    img = np.zeros((h, w, 4), np.uint8)
    bys = np.repeat(np.arange(BH), BW)
    bxs = np.tile(np.arange(BW), BH)
    for ty in range(4):
        for tx in range(4):
            hP = A['P'] * 4 + ty * (A['Q'] - A['P'])
            hR = A['R'] * 4 + ty * (A['S'] - A['R'])
            vA = 4 * hP + tx * (hR - hP)
            gA = (vA >> 6) + (vA >> 1)                 # ~2x upscale (reference math)
            hP = B['P'] * 4 + ty * (B['Q'] - B['P'])
            hR = B['R'] * 4 + ty * (B['S'] - B['R'])
            vB = 4 * hP + tx * (hR - hP)
            gB = (vB >> 6) + (vB >> 1)
            # 5-bit-ish (0..63) -> 8-bit: v*4 + v>>2 approx; use exact *(255/63) table
            gA8 = gA
            gB8 = gB
            mod = mods[:, ty * 4 + tx]
            punch = mod > 10
            mm = np.where(punch, mod - 10, mod)[:, None]
            res = (gA8 * (8 - mm) + gB8 * mm) // 8
            alpha = np.where(punch, 0, (A['P'][:, 3] * 36) // 7 if False else 255)
            # alpha: blend endpoint alphas like rgb (canonical)
            aa = (A['P'][:, 3] * (8 - mm[:, 0]) + B['P'][:, 3] * mm[:, 0]) // 8
            alpha = np.where(punch, 0, aa * 255 // 7)
            res = np.concatenate([res[:, :3], alpha[:, None]], 1)
            img[bys * 4 + ty, bxs * 4 + tx] = res
    return img


def tv(img):
    g = img[:, :, :3].astype(float)
    return float(np.abs(np.diff(g, axis=0)).mean() + np.abs(np.diff(g, axis=1)).mean())


if __name__ == '__main__':
    OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session39'
    d, off, w, h, size = load_tga_mip0()
    mip0 = d[off+52:off+52+w*h//2]
    im = decode(mip0, w, h)
    print('Gargoyle:', w, 'x', h, ' TV', round(tv(im), 2), ' mean', im[:, :, :3].reshape(-1, 3).mean(0).round(1))
    Image.fromarray(im[:, :, :3]).save(f'{OUT}/s39_t2_gargoyle_final.png')
    rgba = Image.fromarray(im, 'RGBA')
    bg = Image.new('RGBA', rgba.size, (40, 44, 52, 255))
    Image.alpha_composite(bg, rgba).convert('RGB').save(f'{OUT}/s39_t2_gargoyle_final_on_bg.png')
    print('saved pngs')
