#!/usr/bin/env python3
"""S39 T2b: refine the in-block word transform (u32swap family) + Morton on top."""
import struct, zipfile
import numpy as np

src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC, UC_ARM_REG_LR

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
mip0 = np.frombuffer(d[off+52:off+52+w*h//2], np.uint8).copy()
BW, BH = w // 4, h // 4
NB = BW * BH
blocks = mip0.reshape(NB, 8)


def morton(by, bx, bits=6):
    m = 0
    for i in range(bits):
        m |= ((by >> i) & 1) << (2 * i)
        m |= ((bx >> i) & 1) << (2 * i + 1)
    return m


MORT = np.array([morton(by, bx) for by in range(BH) for bx in range(BW)])


def bswap32(word):
    return ((word & 0xFF) << 24) | ((word & 0xFF00) << 8) | ((word >> 8) & 0xFF00) | (word >> 24)


def treat(fn):
    o = blocks.copy()
    w0 = o[:, :4].copy().view(np.uint32).ravel()
    w1 = o[:, 4:].copy().view(np.uint32).ravel()
    w0n, w1n = fn(w0, w1)
    o[:, :4] = w0n.view(np.uint8).reshape(-1, 4)
    o[:, 4:] = w1n.view(np.uint8).reshape(-1, 4)
    return o


TREATS = {
    'u32swap':          lambda w0, w1: (w1, w0),
    'bswap32_words':    lambda w0, w1: (bswap32(w0), bswap32(w1)),
    'u16swap_words':    lambda w0, w1: (((w0 & 0xFFFF) << 16) | (w0 >> 16), ((w1 & 0xFFFF) << 16) | (w1 >> 16)),
    'u32swap_bswap32':  lambda w0, w1: (bswap32(w1), bswap32(w0)),
    'u32swap_u16swap':  lambda w0, w1: (((w1 & 0xFFFF) << 16) | (w1 >> 16), ((w0 & 0xFFFF) << 16) | (w0 >> 16)),
    'bswap32_w0_only':  lambda w0, w1: (bswap32(w0), w1),
    'bswap32_w1_only':  lambda w0, w1: (w0, bswap32(w1)),
    'u32swap_mort_gather': None,   # handled below
    'u32swap_mort_scatter': None,
}


def run_engine(data8):
    emu = Emu(); mu = emu.mu
    DATA, DEST = 0x70000000, 0x71000000
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, data8.tobytes()); mu.mem_write(DEST, bytes(w * h * 4))
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 0)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    RET = 0xDED00000
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.emu_start(0x746e34, RET, timeout=120_000_000)
    assert mu.reg_read(UC_ARM_REG_PC) == RET
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).copy().reshape(h, w, 4)


def tv(img):
    g = img[:, :, :3].astype(float)
    return float(np.abs(np.diff(g, axis=0)).mean() + np.abs(np.diff(g, axis=1)).mean())


outs = {}
for name, fn in TREATS.items():
    if name == 'u32swap_mort_gather':
        b = treat(lambda w0, w1: (w1, w0))
        arr = run_engine(b[MORT])
    elif name == 'u32swap_mort_scatter':
        b = treat(lambda w0, w1: (w1, w0))
        o = np.zeros_like(b); o[MORT] = b
        arr = run_engine(o)
    else:
        arr = run_engine(treat(fn))
    outs[name] = arr
    print(f'{name:22s} TV {tv(arr):8.2f}  mean {arr[:,:,:3].reshape(-1,3).mean(0).round(1)}')

best = min(outs, key=lambda k: tv(outs[k]))
from PIL import Image
Image.fromarray(outs[best]).save('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t2_best.png')
Image.fromarray(outs['u32swap']).save('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t2_u32swap.png')
print('BEST:', best, 'saved pngs')
