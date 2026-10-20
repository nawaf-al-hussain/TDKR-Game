#!/usr/bin/env python3
"""S39b: THE CORRECT colA (555, bit15=1) + colB hypothesis scan. mip oracle (floor 0.37).
C1: colB=bit15=1 absolute = A555+delta(byte3), several delta layouts
C2: colB=bit15=0 4443: byte3=[B4|G4<<4], R4=r>>4, A3 in {0,7}
modmode bit0 in {0,1}; morton; mod verbatim.
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

def sext(v, bits):
    v = v.astype(np.int16)
    mask = 1 << (bits - 1)
    v = np.where(v & mask, v - (1 << bits), v)
    return v

def transform(mip, modmode, colb_rule, dlayout=None):
    r, g, b, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R5, G5, B4 = r >> 3, g >> 3, b >> 4
    colA = 0x8000 | (modmode << 0) | (B4 << 1) | (G5 << 5) | (R5 << 10)
    if colb_rule == 'C1':
        if dlayout == 'dB3dG3dR2':
            dB = sext(b3 & 7, 3); dG = sext((b3 >> 3) & 7, 3); dR = sext((b3 >> 6) & 3, 2)
        elif dlayout == 'dR2dG3dB3':
            dR = sext(b3 & 3, 2); dG = sext((b3 >> 2) & 7, 3); dB = sext((b3 >> 5) & 7, 3)
        elif dlayout == 'dR3dG3dB2':
            dR = sext(b3 & 7, 3); dG = sext((b3 >> 3) & 7, 3); dB = sext((b3 >> 6) & 3, 2)
        elif dlayout == 'u2each':
            dR = (b3 & 3).astype(np.int16); dG = ((b3 >> 2) & 3).astype(np.int16); dB = ((b3 >> 4) & 3).astype(np.int16)
        R5b = np.clip(R5.astype(np.int16) + dR, 0, 31).astype(np.uint16)
        G5b = np.clip(G5.astype(np.int16) + dG, 0, 31).astype(np.uint16)
        B5b = np.clip(B4.astype(np.int16) * 2 + 1 + dB, 0, 31).astype(np.uint16)  # B4->B5 midpoint then delta
        colB = (0x8000 | (B5b << 0) | (G5b << 5) | (R5b << 10)).astype(np.uint16)
    elif colb_rule == 'C2':
        B4b, G4b = b3 & 0xF, b3 >> 4
        colB = (B4b << 0) | (G4b << 4) | ((r >> 4) << 8) | (7 << 12)
    elif colb_rule == 'same':
        colB = colA
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

def rgb(arr): return arr[:, :, :3].astype(np.float64)

res = {}
cands = [('C1_dB3dG3dR2', 1, 'C1', 'dB3dG3dR2'), ('C1_dR2dG3dB3', 1, 'C1', 'dR2dG3dB3'),
         ('C1_dR3dG3dB2', 1, 'C1', 'dR3dG3dB2'), ('C1_u2each', 1, 'C1', 'u2each'),
         ('C2_a7', 1, 'C2', None), ('C2_a0', 1, 'C2', None),
         ('C1_dB3dG3dR2_m0', 0, 'C1', 'dB3dG3dR2'), ('C2_a7_m0', 0, 'C2', None),
         ('same_555', 1, 'same', None)]
for tag, mm, cbr, dl in cands:
    t0 = transform(mip0, mm, cbr, dl); t1 = transform(mip1, mm, cbr, dl)
    B0 = morton_reorder(t0, 64, 64); B1 = morton_reorder(t1, 32, 32)
    a0 = rgb(run(B0.tobytes(), 256, 256)); a1 = rgb(run(B1.tobytes(), 128, 128))
    ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
    dx0 = float(np.abs(np.diff(a0, axis=1)).mean())
    print(f'{tag:18s} mip-RMSE={rmse:8.2f} dx0={dx0:6.2f}')
    res[tag] = dict(rmse=rmse, dx0=dx0)

json.dump(res, open(f'{RE}/session39/s39b_555scan.json', 'w'), indent=1)
print('BEST:', min(res.items(), key=lambda kv: kv[1]['rmse']))
