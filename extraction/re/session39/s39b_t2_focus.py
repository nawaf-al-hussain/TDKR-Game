#!/usr/bin/env python3
"""S39b: (1) byte3 cross-mip consistency (validates byte3=colB-lo).
(2) FOCUSED grid: mode x mod-byte-order x colB-high-byte, mip-RMSE oracle (floor 0.37).
"""
import struct, zipfile, json
import numpy as np

RE = '/tmp/my-project/work/TDKR-Game/extraction/re'
src = open(RE + '/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'e'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn import UC_HOOK_INSN_INVALID, UC_HOOK_MEM_INVALID
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC,
                               UC_ARM_REG_LR)
DATA, DEST, RET = 0x70000000, 0x71000000, 0xDED00000

def run(buf, w, h):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000); mu.mem_write(DATA, buf)
    S = 0x20100000
    mu.mem_write(S - 16, struct.pack('<I', DEST)); mu.reg_write(UC_ARM_REG_SP, S - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 1)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    mu.mem_map(RET & ~0xFFF, 0x1000); mu.reg_write(UC_ARM_REG_LR, RET)
    mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try: mu.emu_start(0x746e34, RET, timeout=240_000_000)
    except Exception: pass
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4)

def morton_reorder(blocks, bw, bh):
    def me(x, y):
        x &= 0xFFFF; y &= 0xFFFF
        x = (x | (x << 8)) & 0x00FF00FF; x = (x | (x << 4)) & 0x0F0F0F0F
        x = (x | (x << 2)) & 0x33333333; x = (x | (x << 1)) & 0x55555555
        y = (y | (y << 8)) & 0x00FF00FF; y = (y | (y << 4)) & 0x0F0F0F0F
        y = (y | (y << 2)) & 0x33333333; y = (y | (y << 1)) & 0x55555555
        return (y << 1) | x
    idx = np.array([me(bx, by) for by in range(bh) for bx in range(bw)], np.int64)
    out = np.empty_like(blocks)
    out[idx] = blocks
    return out

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
mip0 = np.frombuffer(d[off + 52:off + 52 + 32768], np.uint8).reshape(-1, 8)
mip1 = np.frombuffer(d[off + 52 + 32768:off + 52 + 40960], np.uint8).reshape(-1, 8)

# (1) byte3 cross-mip: b3 of mip0 ds2 vs b3 of mip1 (at block level)
b30 = mip0[:, 3].reshape(64, 64)
b31 = mip1[:, 3].reshape(32, 32)
ds_b3 = b30.reshape(32, 2, 32, 2).mean((1, 3))
agree = float(np.mean(np.abs(ds_b3 - b31) < 1.5))
corr = float(np.corrcoef(ds_b3.ravel(), b31.ravel())[0, 1])
print(f'(1) byte3 ds2-vs-mip1: corr={corr:.4f} near-agree={agree:.3f} (random ~0)')
# also mod bytes cross-mip
m30 = mip0[:, 4:8].astype(np.int16).reshape(64, 64, 4)
m31 = mip1[:, 4:8].astype(np.int16).reshape(32, 32, 4)
ds_m = m30.reshape(32, 2, 32, 2, 4).mean((1, 3))
print(f'    mod bytes ds2-vs-mip1 corr per byte:',
      [round(float(np.corrcoef(ds_m[..., i].ravel(), m31[..., i].ravel())[0, 1]), 3) for i in range(4)])

# (2) focused grid
def transform(mip, mode, modorder, r4b, a4b):
    b0, b1, b2, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R4, G4, B3 = b0 >> 4, b1 >> 4, b2 >> 5
    colA = mode | (B3 << 1) | (G4 << 4) | (R4 << 8) | (8 << 12)
    colB = (b3 & 0xF) | ((b3 >> 4) << 4) | (r4b << 8) | (a4b << 12)
    mod = mip[:, 4:8].copy()
    if modorder == 'be':      mod = mod[:, ::-1]
    elif modorder == 'sw16':  mod = mod[:, [1, 0, 3, 2]]
    elif modorder == 'nib':   mod = ((mod << 4) & 0xF0) | (mod >> 4)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mod
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

def rgb(arr): return arr[:, :, :3].astype(np.float64)

res = {}
for mode in (1, 0):
    for mo in ('le', 'be', 'sw16', 'nib'):
        for r4b, a4b, tag in ((None, 8, 'rA_a8'),):
            r4v = None
            t0 = transform(mip0, mode, mo, 0 if r4b is None else r4b, a4b)
            # r4b handled inside? simpler: rebuild with R4 of A
            b0_, b1_, b2_, b3_ = (mip0[:, i].astype(np.uint16) for i in range(4))
            t0[:, 7] = ((b0_ >> 4) | (a4b << 4)).astype(np.uint8)  # colB high byte = R4|A4<<4
            t1 = transform(mip1, mode, mo, 0, a4b)
            b0m, b1m, b2m, b3m = (mip1[:, i].astype(np.uint16) for i in range(4))
            t1[:, 7] = ((b0m >> 4) | (a4b << 4)).astype(np.uint8)
            B0 = morton_reorder(t0, 64, 64); B1 = morton_reorder(t1, 32, 32)
            a0 = rgb(run(B0.tobytes(), 256, 256)); a1 = rgb(run(B1.tobytes(), 128, 128))
            ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
            rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
            print(f'(2) mode={mode} mod={mo:5s} a4b={a4b}: RMSE={rmse:7.2f}')
            res[f'm{mode}_{mo}_a{a4b}'] = rmse

json.dump(res, open(f'{RE}/session39/s39b_focus.json', 'w'), indent=1)
print('BEST:', min(res.items(), key=lambda kv: kv[1]))
