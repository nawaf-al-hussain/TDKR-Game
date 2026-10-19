#!/usr/bin/env python3
"""S39 T2c: is the FILE standard PVRTC4? numpy prototype on RAW data with
STANDARD semantics (colors word0, mod word1, standard weights), texel-order
and block-order variants, TV scored vs the shuffled null (64.4) and the
engine-u32swap result (31.6)."""
import struct, zipfile
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
raw = np.frombuffer(d[off+52:off+52+w*h//2], np.uint8)
BW, BH = w // 4, h // 4

words = np.frombuffer(raw.tobytes(), np.uint32).reshape(-1, 2)   # per block: w0, w1
w0 = words[:, 0].astype(np.uint32)
w1 = words[:, 1].astype(np.uint32)


def expand5(v):
    return ((v << 3) | (v >> 2)) & 255


# color A (555, bits 0-14 of w0); B (555, bits 16-30 of w0) [mode-1 only]
Ar, Ag, Ab = (w0 >> 10) & 31, (w0 >> 5) & 31, w0 & 31
Br, Bg, Bb = (w0 >> 26) & 31, (w0 >> 21) & 31, (w0 >> 16) & 31
mode = (w0 >> 31) & 1
# where mode=0 (77% here), B fields are delta-encoded — WRONG under this
# prototype; fill B with A there so the score reflects layout correctness
# rather than mode-0 damage:
Br = np.where(mode == 1, Br, Ar); Bg = np.where(mode == 1, Bg, Ag); Bb = np.where(mode == 1, Bb, Ab)

A = np.stack([expand5(Ar), expand5(Ag), expand5(Ab)], 1).astype(float)
B = np.stack([expand5(Br), expand5(Bg), expand5(Bb)], 1).astype(float)

W = np.array([[8, 0], [5, 3], [3, 5], [0, 8]], float) / 8.0   # mod -> (A*w, B*w) standard


def decode(mod_order, block_order):
    if block_order == 'linear':
        ww1 = w1
    elif block_order == 'morton':
        m = np.array([sum(((bx >> i) & 1) << (2 * i + 1) for i in range(6)) |
                      sum(((by >> i) & 1) << (2 * i) for i in range(6))
                      for by in range(BH) for bx in range(BW)])
        ww1 = w1[m]                      # fetch mod for the block Morton expects here
    mods = np.stack([(ww1 >> (2 * i)) & 3 for i in range(16)], 1)   # texel i
    idx = np.arange(16).reshape(4, 4) if mo == 'yx' else np.arange(16).reshape(4, 4).T
    img = np.zeros((h, w, 3), float)
    for by in range(BH):
        for bx in range(BW):
            k = by * BW + bx
            m4 = mods[k][idx]
            col = A[k][None, :] * W[m4, 0][..., None] + B[k][None, :] * W[m4, 1][..., None]
            img[by*4:by*4+4, bx*4:bx*4+4] = col.reshape(4, 4, 3)
    return img


def tv(img):
    return float(np.abs(np.diff(img, axis=0)).mean() + np.abs(np.diff(img, axis=1)).mean())


rng = np.random.default_rng(3)
w1_shuf = w1[rng.permutation(len(w1))]

for mo in ['yx', 'xy']:
    for bo in ['linear', 'morton']:
        img = decode(mo, bo)
        print(f'standard mo={mo} bo={bo:6s}  TV {tv(img):8.2f}  mean {img.reshape(-1,3).mean(0).round(1)}')
        if mo == 'yx' and bo == 'linear':
            Image.fromarray(img.astype(np.uint8)).save(
                '/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t2_std_proto.png')
# null: random mod words (kills texel-level structure, keeps endpoints)
mods_shuf = np.stack([(w1_shuf >> (2 * i)) & 3 for i in range(16)], 1)
img = np.zeros((h, w, 3), float)
idx = np.arange(16).reshape(4, 4)
for by in range(BH):
    for bx in range(BW):
        k = by * BW + bx
        col = A[k][None, :] * W[mods_shuf[k][idx], 0][..., None] + B[k][None, :] * W[mods_shuf[k][idx], 1][..., None]
        img[by*4:by*4+4, bx*4:bx*4+4] = col.reshape(4, 4, 3)
print(f'NULL shuffled-mods           TV {tv(img):8.2f}')
