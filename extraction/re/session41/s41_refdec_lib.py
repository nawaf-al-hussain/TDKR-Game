#!/usr/bin/env python3
"""S41 reference-decoder library (extracted verbatim from s40_t1_refdec.py,
comment CORRECTED per s41 T1: MOD below is the STANDARD ETC1 intensity
modifier table — the s40 note claiming rows 5-7 'differ from ETC2-spec
punchthrough' was wrong; these ARE the spec values)."""
import struct
import numpy as np

MOD = np.array([[2, 8, -2, -8], [5, 17, -5, -17], [9, 29, -9, -29], [13, 42, -13, -42],
                [18, 60, -18, -60], [24, 80, -24, -80], [33, 106, -33, -106],
                [47, 183, -47, -183]], np.int64)  # = STANDARD ETC1 modifier table [corrected s41]


def expand5(v): return ((v << 3) | (v >> 2)) & 255
def expand4(v): return ((v << 4) | v) & 255
EXP5 = np.array([expand5(v) for v in range(32)], np.int64)
EXP4 = np.array([expand4(v) if v < 16 else 0 for v in range(32)], np.int64)


def decode_blocks(buf, w, h):
    """TDKR .tga ETC1 layout -> HxWx4 uint8 RGBA (bit-exact, s40-verified)."""
    BW, BH = (w + 3) // 4, (h + 3) // 4
    blocks = np.frombuffer(buf, np.uint8).reshape(BH * BW, 8).astype(np.int64)
    b0, b1, b2, b3 = blocks[:, 0], blocks[:, 1], blocks[:, 2], blocks[:, 3]
    mH0, mH1, mL0, mL1 = blocks[:, 4], blocks[:, 5], blocks[:, 6], blocks[:, 7]
    diff = (b3 >> 1) & 1
    flip = b3 & 1
    t1 = (b3 >> 5) & 7
    t2 = (b3 >> 2) & 7

    base = np.stack([b0 >> 3, b1 >> 3, b2 >> 3], 1)
    delta = np.stack([b0 & 7, b1 & 7, b2 & 7], 1)
    sdelta = np.where(delta >= 4, delta - 8, delta)
    c1d = base
    c2d = np.clip(base + sdelta, 0, 31)
    c1i = np.stack([b0 >> 4, b1 >> 4, b2 >> 4], 1)
    c2i = np.stack([b0 & 15, b1 & 15, b2 & 15], 1)
    c1 = np.where(diff[:, None] == 1, c1d, c1i)
    c2 = np.where(diff[:, None] == 1, c2d, c2i)

    NB = BH * BW
    pH = (mH0 | (mH1 << 8))
    pL = (mL1 | (mL0 << 8))
    mods = np.zeros((NB, 4, 4), np.int64)
    H = np.zeros((NB, 4, 4), np.int64)
    L = np.zeros((NB, 4, 4), np.int64)
    Hcol = [2, 3, 0, 1]
    for x in range(4):
        hb = Hcol[x] * 4
        lb = x * 4
        for y in range(4):
            H[:, y, x] = (pH >> (hb + y)) & 1
            L[:, y, x] = (pL >> (lb + y)) & 1
    mods = L + (H << 1)

    out = np.zeros((NB, 4, 4, 4), np.int64)
    for y in range(4):
        for x in range(4):
            sel1 = ((flip == 0) & (x < 2)) | ((flip == 1) & (y < 2))
            c = np.where(sel1[:, None], c1, c2)
            t = np.where(sel1, t1, t2)
            exp = np.where(diff[:, None] == 1, EXP5[c], EXP4[c])
            m = mods[:, y, x]
            tab = MOD[t, m]
            v = np.clip(exp + tab[:, None], 0, 255)
            out[:, y, x, 0] = v[:, 0]
            out[:, y, x, 1] = v[:, 1]
            out[:, y, x, 2] = v[:, 2]
            out[:, y, x, 3] = 255
    img = out.reshape(BH, BW, 4, 4, 4).transpose(0, 2, 1, 3, 4).reshape(BH * 4, BW * 4, 4)
    return img[:h, :w].astype(np.uint8)


def read_archive(z, arch):
    d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/' + arch)
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    ents = []
    for i in range(n):
        off, size, nameOff = struct.unpack_from('>3I', d, 16 + i * 16)
        nb = pool + nameOff
        e = d.index(b'\0', nb)
        ents.append((d[nb:e].decode('latin1'), off, size))
    return d, ents
