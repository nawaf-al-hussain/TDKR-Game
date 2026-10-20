#!/usr/bin/env python3
"""S39b T2: block-order test — engine expects MORTON (disasm-proven corner addressing).
mip-oracle: decode(mip0) ds2 vs decode(mip1). Candidates x {linear, morton}.
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

def morton_encode(x, y):
    x &= 0xFFFF; y &= 0xFFFF
    x = (x | (x << 8)) & 0x00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333
    x = (x | (x << 1)) & 0x55555555
    y = (y | (y << 8)) & 0x00FF00FF
    y = (y | (y << 4)) & 0x0F0F0F0F
    y = (y | (y << 2)) & 0x33333333
    y = (y | (y << 1)) & 0x55555555
    return (y << 1) | x

def reorder_morton(blocks, bw, bh):
    out = np.empty_like(blocks)
    idx = np.empty(bw * bh, np.int64)
    for by in range(bh):
        for bx in range(bw):
            idx[by * bw + bx] = morton_encode(bx, by)
    out[idx] = blocks   # physical[morton(bx,by)] = logical(bx,by)
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

def transform(mip, mode_src, colb_rule):
    b0, b1, b2, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R4, G4, B3 = b0 >> 4, b1 >> 4, b2 >> 5
    mode = np.ones(len(mip), np.uint16) if mode_src == 'one' else np.zeros(len(mip), np.uint16)
    colA = mode | (B3 << 1) | (G4 << 4) | (R4 << 8) | (8 << 12)
    if colb_rule == 'same':
        colB = colA
    elif colb_rule == 'b3nib8':
        colB = (b3 & 0xF) | ((b3 >> 4) << 4) | (R4 << 8) | (8 << 12)
    elif colb_rule == 'lownib8':
        colB = ((b2 & 0xF) | ((b1 & 0xF) << 4) | ((b0 & 0xF) << 8) | (8 << 12))
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

def rgb(arr): return arr[:, :, :3].astype(np.float64)

res = {}
for tag, ms, cbr in [('one_b3nib8', 'one', 'b3nib8'), ('one_same', 'one', 'same'),
                     ('one_lownib8', 'one', 'lownib8'), ('zero_same', 'zero', 'same')]:
    t0 = transform(mip0, ms, cbr); t1 = transform(mip1, ms, cbr)
    for order in ('linear', 'morton'):
        b0 = t0 if order == 'linear' else reorder_morton(t0, 64, 64)
        b1 = t1 if order == 'linear' else reorder_morton(t1, 32, 32)
        a0 = rgb(run(b0.tobytes(), 256, 256))
        a1 = rgb(run(b1.tobytes(), 128, 128))
        ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
        rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
        dx0 = float(np.abs(np.diff(a0, axis=1)).mean())
        print(f'{tag:12s} {order:7s} mip-RMSE={rmse:7.2f} dx0={dx0:6.2f}')
        res[f'{tag}_{order}'] = dict(rmse=rmse, dx0=dx0)

json.dump(res, open(f'{RE}/session39/s39b_order_test.json', 'w'), indent=1)
best = min(res.items(), key=lambda kv: kv[1]['rmse'])
print('BEST:', best)
