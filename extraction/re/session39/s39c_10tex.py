#!/usr/bin/env python3
"""S39c: validate the PROVEN transform across 10 textures (mip oracle + structure)."""
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
    fault = {}
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: fault.setdefault('i', hex(uc.reg_read(uc.const.UC_ARM_REG_PC))) or uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try: mu.emu_start(0x746e34, RET, timeout=240_000_000)
    except Exception as ex: fault['ex'] = str(ex)[:60]
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4), fault

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

def transform(mip, modmode=1):
    r, g, b = (mip[:, i].astype(np.uint16) for i in range(3))
    colA = (0x8000 | (modmode << 0) | ((b >> 4) << 1) | ((g >> 3) << 5) | ((r >> 3) << 10)).astype(np.uint16)
    out = np.empty((len(mip), 8), np.uint8)
    out[:, 0:4] = mip[:, 4:8]
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/actors_tex.gla')
n = struct.unpack_from('>I', d, 12)[0]
pool = 16 + n * 16
ents = {}
order = []
for i in range(n):
    o = 16 + i * 16
    off, size, nameOff = struct.unpack_from('>3I', d, o)
    nb = pool + nameOff
    e = d.index(b'\0', nb)
    name = d[nb:e].decode('latin1')
    ents[name] = (off, size)
    order.append(name)

picked = [nm for nm in order if nm.endswith('.tga')][:60]
results = {}
done = 0
for nm in picked:
    if done >= 10: break
    off, size = ents[nm]
    if size < 52 + 40960: continue  # need 256x256 + mip1
    w, h = struct.unpack_from('<II', d, off + 4)
    if (w, h) != (256, 256): continue
    mip0 = np.frombuffer(d[off + 52:off + 52 + 32768], np.uint8).reshape(-1, 8)
    mip1 = np.frombuffer(d[off + 52 + 32768:off + 52 + 40960], np.uint8).reshape(-1, 8)
    a0, f0 = run(reorder_T(transform(mip0), 64, 64).tobytes(), 256, 256)
    a1, f1 = run(reorder_T(transform(mip1), 32, 32).tobytes(), 128, 128)
    rgb0 = a0[:, :, :3].astype(np.float64); rgb1 = a1[:, :, :3].astype(np.float64)
    ds = rgb0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - rgb1) ** 2).mean()))
    dx = float(np.abs(np.diff(rgb0, axis=1)).mean())
    uniq = int(len(np.unique(rgb0.astype(np.uint8).reshape(-1, 3), axis=0)))
    results[nm] = dict(rmse=rmse, dx=dx, uniq=uniq, fault=bool(f0))
    print(f'{nm[:44]:44s} rmse={rmse:6.2f} dx={dx:5.2f} uniq={uniq:6d} fault={bool(f0)}')
    done += 1

json.dump(results, open(f'{RE}/session39/s39c_10tex.json', 'w'), indent=1)
rms = [v['rmse'] for v in results.values()]
print(f'\nmedian rmse={np.median(rms):.2f}  (A-side proven transform; residual = mod-detail penalty)')
