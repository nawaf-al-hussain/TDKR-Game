#!/usr/bin/env python3
"""S39 T2f: full canonical PVRTC4 decoder (PowerVR reference port, vectorized).

Tests BOTH file word orders ([mod,color] canonical vs [color,mod]) with
Morton block order. Expansion: proper (v<<3|v>>2). TV + PNG output.
"""
import struct, zipfile, sys
import numpy as np
from PIL import Image

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
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
off, size = ents['GC_StockExchange_Gargoyle.tga']
w, h = struct.unpack_from('<II', d, off + 4)
BW, BH = w // 4, h // 4
NB = BW * BH
raw_words = np.frombuffer(d[off+52:off+52+w*h//2], np.uint32).reshape(NB, 2)


def expand5(v):
    return ((v << 3) | (v >> 2)) & 255


def morton_idx(BW, BH):
    bits = max(BW, BH).bit_length() - 1
    out = np.zeros(BW * BH, np.int64)
    for by in range(BH):
        for bx in range(BW):
            m = 0
            for i in range(bits):
                m |= ((by >> i) & 1) << (2 * i)
                m |= ((bx >> i) & 1) << (2 * i + 1)
            out[by * BW + bx] = m
    return out


MODS_MORTON = morton_idx(BW, BH)          # file index for block (bx,by)


def get_colorA(cd):   # (N,) color words -> (N,4) r,g,b,a in 0-31/0-15
    r = np.zeros(len(cd), np.int64); g = np.zeros(len(cd), np.int64); b = np.zeros(len(cd), np.int64); a = np.zeros(len(cd), np.int64)
    op = (cd & 0x8000) != 0
    # opaque: 554-ish
    r[op] = (cd[op] >> 10) & 31
    g[op] = (cd[op] >> 5) & 31
    b[op] = ((cd[op] & 0x1e) | ((cd[op] & 0x1e) >> 4))
    a[op] = 15
    t = ~op
    r[t] = ((cd[t] & 0xf00) >> 7) | ((cd[t] & 0xf00) >> 11)
    g[t] = ((cd[t] & 0xf0) >> 3) | ((cd[t] & 0xf0) >> 7)
    b[t] = ((cd[t] & 0xe) << 1) | ((cd[t] & 0xe) >> 2)
    a[t] = (cd[t] & 0x7000) >> 11
    return np.stack([r, g, b, a], 1)


def get_colorB(cd):
    r = np.zeros(len(cd), np.int64); g = np.zeros(len(cd), np.int64); b = np.zeros(len(cd), np.int64); a = np.zeros(len(cd), np.int64)
    op = (cd & 0x80000000) != 0
    r[op] = (cd[op] >> 26) & 31
    g[op] = (cd[op] >> 21) & 31
    b[op] = (cd[op] >> 16) & 31
    a[op] = 15
    t = ~op
    r[t] = ((cd[t] & 0xf000000) >> 23) | ((cd[t] & 0xf000000) >> 27)
    g[t] = ((cd[t] & 0xf00000) >> 19) | ((cd[t] & 0xf00000) >> 23)
    b[t] = ((cd[t] & 0xf0000) >> 15) | ((cd[t] & 0xf0000) >> 19)
    a[t] = (cd[t] & 0x70000000) >> 27
    return np.stack([r, g, b, a], 1)


def unpack_mods(modw, colw):
    """(N,16) modulation values in texel order y*4+x, 0..14 (14=punch)."""
    WordModMode = colw & 1
    bits = modw.copy()
    vals = np.zeros((len(modw), 16), np.int64)
    cur = bits * 0 + modw
    for i in range(16):                      # y outer, x inner, LSB first
        v = cur & 3
        if i == 0:
            pass
        vals[:, i] = v
        cur = cur >> 2
    # map
    m0 = vals * 3
    m0 = np.where(m0 > 3, m0 - 1, m0)                     # {0,3,5,8}
    m1 = np.where(vals == 1, 4, np.where(vals == 2, 14, np.where(vals == 3, 8, 0)))
    return np.where((WordModMode == 0)[:, None], m0, m1)


def decode(word_order, expand=True):
    if word_order == 'canonical':      # [mod, color]
        modw, colw = raw_words[:, 0], raw_words[:, 1]
    else:                              # [color, mod]
        colw, modw = raw_words[:, 0], raw_words[:, 1]
    modw = modw.astype(np.int64)[MODS_MORTON]; colw = colw.astype(np.int64)[MODS_MORTON]
    # neighbor grids (wrap)
    def grid(arr): return arr.reshape(BH, BW)
    gmod, gcol = grid(modw), grid(colw)
    Pm, Pc = gmod, gcol
    Qm, Qc = np.roll(gmod, -1, 1), np.roll(gcol, -1, 1)
    Rm, Rc = np.roll(gmod, -1, 0), np.roll(gcol, -1, 0)
    Sm, Sc = np.roll(Qm, -1, 0), np.roll(Qc, -1, 0)

    def flat(x): return x.reshape(-1)
    mods = unpack_mods(flat(Pm), flat(Pc))          # (NB,16) for the P word only

    # bilinear upscaled endpoint colors per block (vectorized over blocks, 4x4 texels)
    A = {k: get_colorA(flat(v)) for k, v in [('P', Pc), ('Q', Qc), ('R', Rc), ('S', Sc)]}
    B = {k: get_colorB(flat(v)) for k, v in [('P', Pc), ('Q', Qc), ('R', Rc), ('S', Sc)]}

    img = np.zeros((h, w, 4), np.uint8)
    WW = 4
    # port of interpolateColors (4bpp): out[y,x] = g(4*hP_y + x*(hR_y-hP_y)),
    # g(v)=(v>>6)+(v>>1); hP_y = P + y*(Q-P); hR_y = R + y*(S-R)
    for ty in range(4):
        for tx in range(4):
            upsA = []; upsB = []
            for ch in range(4):
                pass
            hP = A['P'] * 4 + ty * (A['Q'] - A['P'])     # hP after ty iterations
            hR = A['R'] * 4 + ty * (A['S'] - A['R'])
            dY = hR - hP
            vA = 4 * hP + tx * dY
            gA = (vA >> 6) + (vA >> 1)
            hP = B['P'] * 4 + ty * (B['Q'] - B['P'])
            hR = B['R'] * 4 + ty * (B['S'] - B['R'])
            dY = hR - hP
            vB = 4 * hP + tx * dY
            gB = (vB >> 6) + (vB >> 1)
            if expand:
                gA = np.stack([expand5(gA[:, 0]), expand5(gA[:, 1]), expand5(gA[:, 2]), gA[:, 3] * 17], 1)
                gB = np.stack([expand5(gB[:, 0]), expand5(gB[:, 1]), expand5(gB[:, 2]), gB[:, 3] * 17], 1)
            mod = mods[:, ty * 4 + tx]
            punch = mod > 10
            mm = np.where(punch, mod - 10, mod)
            res = gA * (8 - mm)[:, None] + gB * mm[:, None]
            res = (res >> 3).astype(np.int64)
            alpha = np.where(punch, 0, res[:, 3])
            res = np.concatenate([res[:, :3], alpha[:, None]], 1)
            # block positions
            bys = np.repeat(np.arange(BH), BW)
            bxs = np.tile(np.arange(BW), BH)
            img[bys * 4 + ty, bxs * 4 + tx] = res
    return img


def tv(img):
    g = img[:, :, :3].astype(float)
    return float(np.abs(np.diff(g, axis=0)).mean() + np.abs(np.diff(g, axis=1)).mean())


OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session39'
for order in ['canonical', 'swapped']:
    im = decode(order)
    print(f'{order:10s} TV {tv(im):8.2f}  mean {im[:,:,:3].reshape(-1,3).mean(0).round(1)}')
    Image.fromarray(im[:,:,:3]).save(f'{OUT}/s39_t2_full_{order}.png')
