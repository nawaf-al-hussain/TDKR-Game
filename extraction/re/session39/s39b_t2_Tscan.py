#!/usr/bin/env python3
"""S39b T2: transform-candidate scan. file block [3B rgb888][1B flags][4B mod]
-> engine block [4B mod][colA16][colB16].
Candidates over: mode-bit source, A4(alpha) source, colB rule.
Score = structure (neighbor dx + unique colors) on gargoyle 256x256.
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
W, H = struct.unpack_from('<II', d, off + 4)
mip0 = np.frombuffer(d[off + 52:off + 52 + 32768], np.uint8).reshape(-1, 8)
print('gargoyle', W, 'x', H, 'blocks', len(mip0))

DATA, DEST, RET = 0x70000000, 0x71000000, 0xDED00000

def run(buf):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000); mu.mem_write(DATA, buf)
    S = 0x20100000
    mu.mem_write(S - 16, struct.pack('<I', DEST)); mu.reg_write(UC_ARM_REG_SP, S - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 1)
    mu.reg_write(UC_ARM_REG_R2, W); mu.reg_write(UC_ARM_REG_R3, H)
    mu.mem_map(RET & ~0xFFF, 0x1000); mu.reg_write(UC_ARM_REG_LR, RET)
    mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try: mu.emu_start(0x746e34, RET, timeout=240_000_000)
    except Exception: pass
    return np.frombuffer(bytes(mu.mem_read(DEST, W * H * 4)), np.uint8).reshape(H, W, 4)

def transform(mip, mode_src, a4_src, colb_rule):
    b0, b1, b2, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R4, G4, B3 = b0 >> 4, b1 >> 4, b2 >> 5
    if mode_src == 'zero':   mode = np.zeros_like(b3)
    elif mode_src == 'b3b0': mode = b3 & 1
    elif mode_src == 'b3b1': mode = (b3 >> 1) & 1
    elif mode_src == 'one':  mode = np.ones_like(b3)
    if a4_src == 'fifteen':  a4 = np.full_like(b3, 15)
    elif a4_src == 'b3hi':   a4 = b3 >> 4
    elif a4_src == 'eight':  a4 = np.full_like(b3, 8)
    elif a4_src == 'zero':   a4 = np.zeros_like(b3)
    colA = (mode | (B3 << 1) | (G4 << 4) | (R4 << 8) | (a4 << 12)).astype('<u2')
    if colb_rule == 'same':
        colB = colA
    elif colb_rule == 'b3nib':   # B4=b3&0xF, G4=b3>>4, R4=R4, A4=15
        colB = (b3 & 0xF) | ((b3 >> 4) << 4) | (R4 << 8) | (15 << 12)
    elif colb_rule == 'b3nib8':  # same but A4=8 (alpha 255, no R-fold)
        colB = (b3 & 0xF) | ((b3 >> 4) << 4) | (R4 << 8) | (8 << 12)
    elif colb_rule == 'b3hi8':   # B4=b3>>4, G4=b3&0xF, R4=R4, A4=8
        colB = ((b3 >> 4) | ((b3 & 0xF) << 4) | (R4 << 8) | (8 << 12))
    elif colb_rule == 'zero':
        colB = np.zeros_like(colA)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.view(np.uint8).reshape(-1, 2)
    return out.tobytes()

def score(arr, tag, save=False):
    rgb = arr[:, :, :3].astype(np.int16)
    dx = float(np.abs(np.diff(rgb, axis=1)).mean())
    dy = float(np.abs(np.diff(rgb, axis=0)).mean())
    uniq = int(len(np.unique(rgb.reshape(-1, 3), axis=0)))
    print(f'{tag:34s} dx={dx:6.2f} dy={dy:6.2f} uniq={uniq:6d}')
    if save:
        Image.fromarray(arr[:, :, :3]).save(f'{RE}/session39/s39b_T_{tag}.png')
    return dx, dy, uniq

res = {}
cands = [
    ('zero_fifteen_same', 'zero', 'fifteen', 'same'),
    ('zero_eight_same', 'zero', 'eight', 'same'),
    ('zero_eight_b3nib', 'zero', 'eight', 'b3nib'),
    ('zero_eight_b3nib8', 'zero', 'eight', 'b3nib8'),
    ('zero_eight_b3hi8', 'zero', 'eight', 'b3hi8'),
    ('one_eight_b3nib8', 'one', 'eight', 'b3nib8'),
    ('b3b1_eight_b3nib8', 'b3b1', 'eight', 'b3nib8'),
    ('b3b0_eight_b3nib8', 'b3b0', 'eight', 'b3nib8'),
    ('zero_fifteen_b3nib', 'zero', 'fifteen', 'b3nib'),
    ('zero_zero_b3nib8', 'zero', 'zero', 'b3nib8'),
]
for tag, ms, a4s, cbr in cands:
    buf = transform(mip0, ms, a4s, cbr)
    arr = run(buf)
    res[tag] = score(arr, tag, save=True)

json.dump(res, open(f'{RE}/session39/s39b_T_scan.json', 'w'), indent=1)
best = min(res.items(), key=lambda kv: kv[1][0] + kv[1][1])
print('BEST by smoothness:', best[0])
