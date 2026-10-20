#!/usr/bin/env python3
"""S39b T2: THE ORACLE = mip self-consistency.
decode(mip0) box-downsample x2  vs  decode(mip1) -> RMSE.
Correct transform minimizes it. Also mips: 256^2=32768B @52, 128^2=8192B @36820.
Scan colA/colB/mode candidates.
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
mip1 = np.frombuffer(d[off + 52 + 32768:off + 52 + 32768 + 8192], np.uint8).reshape(-1, 8)
A1 = mip1[:, 0:3].reshape(32, 32, 3).astype(np.int16)
print('mip1 endpoint smooth:', np.abs(np.diff(A1, axis=1)).mean().round(2),
      np.abs(np.diff(A1, axis=0)).mean().round(2))

def transform(mip, mode_src, a4_val, colb_rule):
    b0, b1, b2, b3 = (mip[:, i].astype(np.uint16) for i in range(4))
    R4, G4, B3 = b0 >> 4, b1 >> 4, b2 >> 5
    if mode_src == 'zero':   mode = np.zeros(len(mip), np.uint16)
    elif mode_src == 'one':  mode = np.ones(len(mip), np.uint16)
    elif mode_src == 'b3b0': mode = b3 & 1
    colA = mode | (B3 << 1) | (G4 << 4) | (R4 << 8) | (a4_val << 12)
    if colb_rule == 'same':
        colB = colA
    elif colb_rule == 'b3nib8':
        colB = (b3 & 0xF) | ((b3 >> 4) << 4) | (R4 << 8) | (8 << 12)
    elif colb_rule == 'b3hi8':
        colB = ((b3 >> 4) | ((b3 & 0xF) << 4) | (R4 << 8) | (8 << 12))
    elif colb_rule == 'lownib8':  # B from low nibbles of rgb
        colB = ((b2 & 0xF) | ((b1 & 0xF) << 4) | ((b0 & 0xF) << 8) | (8 << 12))
    elif colb_rule == 'delta':    # colB = colA + sign-extended nibbles of b3 (lo=B, hi=G)
        db = (b3 & 0xF).astype(np.int16); db[db >= 8] -= 16
        dg = ((b3 >> 4) & 0xF).astype(np.int16); dg[dg >= 8] -= 16
        nB = np.clip((b2 >> 5) * 2 + db, 0, 15)  # B4 approx from B3*2
        nG = np.clip(G4 + dg, 0, 15)
        colB = nB | (nG << 4) | (R4 << 8) | (8 << 12)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colB.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out.tobytes()

def rgb(arr): return arr[:, :, :3].astype(np.float64)

res = {}
cands = [
    ('zero_a8_same',      'zero', 8,  'same'),
    ('zero_a8_b3nib8',    'zero', 8,  'b3nib8'),
    ('zero_a8_b3hi8',     'zero', 8,  'b3hi8'),
    ('zero_a8_lownib8',   'zero', 8,  'lownib8'),
    ('zero_a8_delta',     'zero', 8,  'delta'),
    ('one_a8_b3nib8',     'one',  8,  'b3nib8'),
    ('one_a8_lownib8',    'one',  8,  'lownib8'),
    ('one_a8_delta',      'one',  8,  'delta'),
    ('b3b0_a8_b3nib8',    'b3b0', 8,  'b3nib8'),
    ('b3b0_a8_lownib8',   'b3b0', 8,  'lownib8'),
    ('b3b0_a8_delta',     'b3b0', 8,  'delta'),
    ('one_a15_b3nib8',    'one',  15, 'b3nib8'),
    ('one_a15_lownib8',   'one',  15, 'lownib8'),
]
for tag, ms, a4, cbr in cands:
    a0 = rgb(run(transform(mip0, ms, a4, cbr), 256, 256))
    a1 = rgb(run(transform(mip1, ms, a4, cbr), 128, 128))
    ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
    dx0 = float(np.abs(np.diff(a0, axis=1)).mean())
    print(f'{tag:18s} mip-RMSE={rmse:7.2f}  dx0={dx0:6.2f}')
    res[tag] = dict(rmse=rmse, dx0=dx0)

json.dump(res, open(f'{RE}/session39/s39b_miporacle.json', 'w'), indent=1)
best = min(res.items(), key=lambda kv: kv[1]['rmse'])
print('BEST by mip-consistency:', best)
