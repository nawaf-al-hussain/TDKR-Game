#!/usr/bin/env python3
"""S39c: byte3 semantics — HIGH-FREQUENCY CORRELATION oracle (transposed morton).
Rules: same / C1 delta variants / C2 4443-colB. Winner = max cross-detail correlation."""
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

def me_T(x, y):
    x &= 0xFFFF; y &= 0xFFFF
    x = (x | (x << 8)) & 0x00FF00FF; x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333; x = (x | (x << 1)) & 0x55555555
    y = (y | (y << 8)) & 0x00FF00FF; y = (y | (y << 4)) & 0x0F0F0F0F
    y = (y | (y << 2)) & 0x33333333; y = (y | (y << 1)) & 0x55555555
    return (x << 1) | y

def reorder_T(blocks, bw, bh):
    idx = np.array([me_T(bx, by) for by in range(bh) for bx in range(bw)], np.int64)
    out = np.empty_like(blocks); out[idx] = blocks
    return out

def sext(v, bits):
    v = v.astype(np.int16)
    m = 1 << (bits - 1)
    return np.where(v & m, v - (1 << bits), v)

def transform(mip, rule):
    r, g, b, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R5, G5, B4 = r >> 3, g >> 3, b >> 4
    colA = (0x8000 | (1 << 0) | (B4 << 1) | (G5 << 5) | (R5 << 10)).astype(np.uint16)
    if rule == 'same':
        colB = colA
    elif rule == 'C1_dR2dG3dB3':
        dR = sext(b3 & 3, 2); dG = sext((b3 >> 2) & 7, 3); dB = sext((b3 >> 5) & 7, 3)
        Rb = np.clip(R5.astype(np.int16) + dR, 0, 31).astype(np.uint16)
        Gb = np.clip(G5.astype(np.int16) + dG, 0, 31).astype(np.uint16)
        Bb = np.clip(B4.astype(np.int16) * 2 + 1 + dB, 0, 31).astype(np.uint16)
        colB = (0x8000 | (Bb << 0) | (Gb << 5) | (Rb << 10)).astype(np.uint16)
    elif rule == 'C1_dB3dG3dR2':
        dB = sext(b3 & 7, 3); dG = sext((b3 >> 3) & 7, 3); dR = sext((b3 >> 6) & 3, 2)
        Rb = np.clip(R5.astype(np.int16) + dR, 0, 31).astype(np.uint16)
        Gb = np.clip(G5.astype(np.int16) + dG, 0, 31).astype(np.uint16)
        Bb = np.clip(B4.astype(np.int16) * 2 + 1 + dB, 0, 31).astype(np.uint16)
        colB = (0x8000 | (Bb << 0) | (Gb << 5) | (Rb << 10)).astype(np.uint16)
    elif rule == 'C2':
        colB = ((b3 & 0xF) | ((b3 >> 4) << 4) | ((r >> 4) << 8) | (7 << 12)).astype(np.uint16)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

def hp(x):
    return x - np.round(x.reshape(x.shape[0] // 2 * 2, 2, -1).repeat(2, 0) if False else 0) if False else x

def highpass(a):
    # simple 1px laplacian-ish highpass
    lp = (a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:]) / 4.0
    return a[1:-1, 1:-1] - lp

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

res = {}
for rule in ['same', 'C1_dR2dG3dB3', 'C1_dB3dG3dR2', 'C2']:
    a0 = run(reorder_T(transform(mip0, rule), 64, 64).tobytes(), 256, 256)[:, :, :3].astype(np.float64)
    a1 = run(reorder_T(transform(mip1, rule), 32, 32).tobytes(), 128, 128)[:, :, :3].astype(np.float64)
    ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
    h0 = highpass(ds.mean(2)); h1 = highpass(a1.mean(2))
    corr = float(np.corrcoef(h0.ravel(), h1.ravel())[0, 1])
    print(f'{rule:14s} rmse={rmse:6.2f}  detail-corr={corr:+.4f}')
    res[rule] = dict(rmse=rmse, corr=corr)

json.dump(res, open(f'{RE}/session39/s39c_byte3.json', 'w'), indent=1)
print('BEST by detail-corr:', max(res.items(), key=lambda kv: kv[1]['corr']))
