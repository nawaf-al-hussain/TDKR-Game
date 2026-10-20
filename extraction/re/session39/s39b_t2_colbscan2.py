#!/usr/bin/env python3
"""S39b T2: colB derivation scan v2 (all x mode=one x MORTON).
Also render best candidate to check gargoyle visibility.
"""
import struct, zipfile, json
import numpy as np
from PIL import Image

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

def pack4443(rgb888):
    r, g, b = rgb888[..., 0], rgb888[..., 1], rgb888[..., 2]
    return (r >> 4) | ((g >> 4) << 4) | ((b >> 5) << 8)  # low byte B3<<1|G4<<4? careful:
    # engine colA: bit0 mode, B3 bits1-3, G4 bits4-7, R4 bits8-11
def packA(rgb888, mode):
    r, g, b = rgb888[..., 0].astype(np.uint16), rgb888[..., 1].astype(np.uint16), rgb888[..., 2].astype(np.uint16)
    return mode | ((b >> 5) << 1) | ((g >> 4) << 4) | ((r >> 4) << 8) | (8 << 12)

def transform(mip, colb_rule):
    rgbA = mip[:, 0:3].astype(np.int16)
    b3 = mip[:, 3].astype(np.uint16)
    colA = packA(rgbA, 1)
    if colb_rule == 'same':
        colB = colA
    elif colb_rule == 'add':
        B = np.clip(rgbA + b3.astype(np.int16)[:, None], 0, 255)
        colB = packA(B, 1)
    elif colb_rule == 'add_signed':
        s = b3.astype(np.int16).copy(); s[s >= 128] -= 256
        B = np.clip(rgbA + s[:, None], 0, 255)
        colB = packA(B, 1)
    elif colb_rule == 'grey':
        colB = 1 | ((b3 & 7) << 1) | (((b3 >> 4) & 0xF) << 4) | (((b3 >> 4) & 0xF) << 8) | (8 << 12)
    elif colb_rule == 'grey_lo':
        colB = 1 | ((b3 & 7) << 1) | ((b3 & 0xF) << 4) | ((b3 & 0xF) << 8) | (8 << 12)
    elif colb_rule == 'invert':
        colB = packA(255 - rgbA, 1)
    elif colb_rule == 'ch2x34':
        dR = ((b3 >> 0) & 3).astype(np.int16) * 34
        dG = ((b3 >> 2) & 3).astype(np.int16) * 34
        dB = ((b3 >> 4) & 3).astype(np.int16) * 34
        B = np.clip(rgbA + np.stack([dR, dG, dB], 1), 0, 255)
        colB = packA(B, 1)
    elif colb_rule == 'b3nib8':
        colB = (b3 & 0xF) | ((b3 >> 4) << 4) | ((rgbA[:, 0].astype(np.uint16) >> 4) << 8) | (8 << 12)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

def rgb(arr): return arr[:, :, :3].astype(np.float64)

res = {}
for rule in ['same', 'add', 'add_signed', 'grey', 'grey_lo', 'invert', 'ch2x34', 'b3nib8']:
    t0 = morton_reorder(transform(mip0, rule), 64, 64)
    t1 = morton_reorder(transform(mip1, rule), 32, 32)
    a0 = rgb(run(t0.tobytes(), 256, 256))
    a1 = rgb(run(t1.tobytes(), 128, 128))
    ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
    dx0 = float(np.abs(np.diff(a0, axis=1)).mean())
    print(f'{rule:11s} mip-RMSE={rmse:7.2f} dx0={dx0:6.2f}')
    res[rule] = dict(rmse=rmse, dx0=dx0)
    if rule == 'same':
        Image.fromarray(a0.astype(np.uint8)).save(f'{RE}/session39/s39b_best_same_morton.png')

json.dump(res, open(f'{RE}/session39/s39b_colbscan2.json', 'w'), indent=1)
print('BEST:', min(res.items(), key=lambda kv: kv[1]['rmse']))
