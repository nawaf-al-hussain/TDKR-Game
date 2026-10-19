#!/usr/bin/env python3
"""S38 T2.6: python PVRTC4bpp decoder with EMPIRICAL semantics:
mod {0->B, 1->(3A+5B)/8, 2->(5A+3B)/8, 3->A}; A=bits0-14 (555), opA=bit15;
B=bits16-30; mode bit31 ignored; alpha = 255 if opA else 255*wA/8.
Input order variants tried: linear, morton(bx-low), morton(by-low), 16x16-tiled."""
import struct
import numpy as np
from PIL import Image

d_src = open('/tmp/my-project/work/data', 'rb') if False else None
import zipfile
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
mip0 = np.frombuffer(d[off+52:off+52+32768], np.uint8)
BW, BH = w // 4, h // 4
blocks = mip0.reshape(-1, 8)

def morton(bx, by, bw_bits, swap=False):
    m = 0
    for i in range(bw_bits):
        if swap: m |= ((bx >> i) & 1) << (2*i+1); m |= ((by >> i) & 1) << (2*i)
        else:    m |= ((bx >> i) & 1) << (2*i);   m |= ((by >> i) & 1) << (2*i+1)
    return m

def expand555(v): return ((v << 3) | (v >> 2)) & 255

def decode(order):
    # endpoint images E_A, E_B per block
    EA = np.zeros((BH, BW, 4)); EB = np.zeros((BH, BW, 4))
    for by in range(BH):
        for bx in range(BW):
            if order == 'linear': bi = by * BW + bx
            elif order == 'morton_bxlow': bi = morton(bx, by, 8, swap=True)
            elif order == 'morton_bylow': bi = morton(bx, by, 8, swap=False)
            elif order.startswith('tile'):
                T = int(order[4:]); tbx, tby = bx // T, by // T; lx, ly = bx % T, by % T
                bi = (tby * (BW // T) + tbx) * (T * T) + ly * T + lx
            cw = int(struct.unpack_from('<I', blocks[bi], 4)[0])
            cA = cw & 0x7FFF; opA = (cw >> 15) & 1
            cB = (cw >> 16) & 0x7FFF
            EA[by, bx, 0] = expand555(cA & 31); EA[by, bx, 1] = expand555((cA >> 5) & 31); EA[by, bx, 2] = expand555((cA >> 10) & 31)
            EA[by, bx, 3] = 255.0 if opA else 0.0
            EB[by, bx, 0] = expand555(cB & 31); EB[by, bx, 1] = expand555((cB >> 5) & 31); EB[by, bx, 2] = expand555((cB >> 10) & 31)
            EB[by, bx, 3] = 255.0
    out = np.zeros((h, w, 4))
    for y in range(h):
        fy = (y % 4 + 0.5) / 4.0
        by0 = y // 4
        for x in range(w):
            fx = (x % 4 + 0.5) / 4.0
            bx0 = x // 4
            acc = np.zeros(4)
            wts = [(1-fx)*(1-fy), fx*(1-fy), (1-fx)*fy, fx*fy]
            for (dx, dy, wt) in zip((0,1,0,1), (0,0,1,1), wts):
                EAx = EA[(by0+dy) % BH, (bx0+dx) % BW]
                EBx = EB[(by0+dy) % BH, (bx0+dx) % BW]
                acc += wt * (EAx + EBx) / 2   # placeholder blend; refined below
            out[y, x] = acc
    return out

# proper: bilinear EA and EB separately then mod-blend per pixel with the modulation word
def decode2(order):
    EA = np.zeros((BH, BW, 4)); EB = np.zeros((BH, BW, 4))
    MOD = np.zeros((h, w), int)
    for by in range(BH):
        for bx in range(BW):
            if order == 'linear': bi = by * BW + bx
            elif order == 'morton_bxlow': bi = morton(bx, by, 8, swap=True)
            elif order == 'morton_bylow': bi = morton(bx, by, 8, swap=False)
            elif order.startswith('tile'):
                T = int(order[4:]); tbx, tby = bx // T, by // T; lx, ly = bx % T, by % T
                bi = (tby * (BW // T) + tbx) * (T * T) + ly * T + lx
            blk = blocks[bi]
            modw = int(struct.unpack_from('<I', blk, 0)[0])
            cw = int(struct.unpack_from('<I', blk, 4)[0])
            cA = cw & 0x7FFF; opA = (cw >> 15) & 1
            cB = (cw >> 16) & 0x7FFF
            EA[by, bx] = (expand555(cA & 31), expand555((cA >> 5) & 31), expand555((cA >> 10) & 31), 255.0 if opA else 0.0)
            EB[by, bx] = (expand555(cB & 31), expand555((cB >> 5) & 31), expand555((cB >> 10) & 31), 255.0)
            for yy in range(4):
                for xx in range(4):
                    MOD[by*4+yy, bx*4+xx] = (modw >> (2 * (4*yy + xx))) & 3
    # bilinear EA/EB to pixels (wrap)
    EA00 = np.repeat(np.repeat(EA, 4, 0), 4, 1)
    EB00 = np.repeat(np.repeat(EB, 4, 0), 4, 1)
    EA10 = np.roll(EA00, -4, 1); EA01 = np.roll(EA00, -4, 0); EA11 = np.roll(np.roll(EA00, -4, 0), -4, 1)
    EB10 = np.roll(EB00, -4, 1); EB01 = np.roll(EB00, -4, 0); EB11 = np.roll(np.roll(EB00, -4, 0), -4, 1)
    fxw = ((np.arange(w) % 4 + 0.5) / 4)[None, :, None]
    fyw = ((np.arange(h) % 4 + 0.5) / 4)[:, None, None]
    A_px = EA00*(1-fxw)*(1-fyw) + EA10*fxw*(1-fyw) + EA01*(1-fxw)*fyw + EA11*fxw*fyw
    B_px = EB00*(1-fxw)*(1-fyw) + EB10*fxw*(1-fyw) + EB01*(1-fxw)*fyw + EB11*fxw*fyw
    TAB = {0: (0, 8), 1: (3, 5), 2: (5, 3), 3: (8, 0)}   # (wA, wB) empirically
    out = np.zeros((h, w, 4))
    for mv, (wa, wb) in TAB.items():
        sel = MOD == mv
        out[sel] = (wa * A_px[sel] + wb * B_px[sel]) / 8
    return out.astype(np.uint8)

oracle = np.fromfile('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t2_engine_rgba_4bpp.bin', np.uint8).reshape(h, w, 4)
for order in ('linear', 'morton_bxlow', 'morton_bylow', 'tile16', 'tile8'):
    try:
        dec = decode2(order)
        diff = np.abs(dec[:, :, :3].astype(int) - oracle[:, :, :3].astype(int))
        Image.fromarray(dec[:, :, :3]).save(f'/tmp/s38_dec_{order}.png')
        print(f'{order}: mean diff {diff.mean():.1f} max {diff.max()}')
    except Exception as e:
        print(order, 'ERR', e)
