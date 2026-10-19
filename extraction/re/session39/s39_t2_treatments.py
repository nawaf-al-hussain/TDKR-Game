#!/usr/bin/env python3
"""S39 T2: decisive input-treatment search for the real-data PVRTC gap.

The engine decoder (ground truth) fetches input blocks in Morton order
(s38 proven). The real .tga data decodes to structured noise as-is. We run
the ENGINE on the REAL Gargoyle mip0 under 8 input treatments and score the
output by total variation (natural texture << noise). Null: random block
shuffles. If any treatment yields TV well under the null, the file->engine
mapping is found.
"""
import struct, zipfile, sys
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
print(f'Gargoyle: {w}x{h}, chain {size} B (mip0 {w*h//2})')
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
INV = np.argsort(MORT)  # position of linear index in morton order


def t_raw():
    return blocks.copy()


def t_mort_scatter():   # input[morton] = file[linear]
    o = np.zeros_like(blocks)
    o[MORT] = blocks
    return o


def t_mort_gather():    # input[linear] = file[morton]
    return blocks[MORT]


def t_mort_scatter_bx():
    m2 = np.array([morton(bx, by) for by in range(BH) for bx in range(BW)])
    o = np.zeros_like(blocks)
    o[m2] = blocks
    return o


def t_mort_gather_bx():
    m2 = np.array([morton(bx, by) for by in range(BH) for bx in range(BW)])
    return blocks[m2]


def t_transpose():       # column-major block order
    o = blocks.reshape(BH, BW, 8).transpose(1, 0, 2).reshape(NB, 8)
    return o.copy()


def t_u32swap():
    o = blocks.copy()
    tmp = o[:, :4].copy(); o[:, :4] = o[:, 4:]; o[:, 4:] = tmp
    return o


def t_byterev():
    return blocks[:, ::-1].copy()


TREATS = {'raw': t_raw, 'mort_scatter_bylow': t_mort_scatter,
          'mort_gather_bylow': t_mort_gather, 'mort_scatter_bxlow': t_mort_scatter_bx,
          'mort_gather_bxlow': t_mort_gather_bx, 'transpose': t_transpose,
          'u32swap_raw': t_u32swap, 'byterev_raw': t_byterev}


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


results = {}
rng = np.random.default_rng(39)
null_blocks = [blocks[rng.permutation(NB)] for _ in range(4)]
for name, fn in TREATS.items():
    arr = run_engine(fn())
    results[name] = tv(arr)
    print(f'{name:22s} TV {results[name]:8.2f}  mean rgb {arr[:,:,:3].reshape(-1,3).mean(0).round(1)}')
for i, nb_ in enumerate(null_blocks):
    arr = run_engine(nb_)
    print(f'NULL_shuffle_{i}        TV {tv(arr):8.2f}')
    results[f'null_shuffle_{i}'] = tv(arr)
np.save('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t2_tvs.npy',
        results, allow_pickle=True)
best = min((v, k) for k, v in results.items() if not k.startswith('null'))
nullm = np.mean([v for k, v in results.items() if k.startswith('null')])
print(f'BEST: {best[1]} TV {best[0]:.2f}  vs null mean {nullm:.2f}')
