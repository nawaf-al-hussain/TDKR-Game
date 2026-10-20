#!/usr/bin/env python3
"""S39b T2: test the block byte-rotation hypothesis under the ENGINE.
File block (s39 crack)  = [3B rgb888-A][1B flags][4B mod]
Engine block (s38 probe)= [4B mod][2B colA][2B colB]
H1: engine = [b4 b5 b6 b7 | b0 b1 b2 b3]        (pure rotate)
H2: engine = [b7 b6 b5 b4 | b0 b1 b2 b3]        (mod reversed)
H3: engine = [b4 b5 b6 b7 | b1 b0 | b3 b2]      (colors u16-swapped)
Null: raw file through engine (known noise).
All runs: unicorn impl @0x746e34, opA=1, gargoyle mip0 256x256.
"""
import struct, zipfile, json
import numpy as np
from PIL import Image

RE = '/tmp/my-project/work/TDKR-Game/extraction/re'
src = open(RE + '/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
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
w, h = struct.unpack_from('<II', d, off + 4)
mip0 = d[off + 52:off + 52 + 32768]
print('gargoyle', w, 'x', h, 'mip0', len(mip0), 'blocks', len(mip0) // 8)

def rot(data, f):
    b = np.frombuffer(data, np.uint8).reshape(-1, 8).copy()
    out = np.empty_like(b)
    for i in range(8):
        out[:, i] = b[:, f[i]]
    return out.tobytes()

H1 = [4, 5, 6, 7, 0, 1, 2, 3]
H2 = [7, 6, 5, 4, 0, 1, 2, 3]
H3 = [4, 5, 6, 7, 1, 0, 3, 2]

DATA, DEST = 0x70000000, 0x71000000
RET = 0xDED00000

def run_engine(buf, opA=1):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, buf)
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, opA)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    fault = {}
    def h_insn(uc, user):
        fault['insn_pc'] = hex(uc.reg_read(UC_ARM_REG_PC)); uc.emu_stop()
    def h_mem(uc, access, address, size, value, user):
        fault['mem'] = hex(address); uc.emu_stop()
    mu.hook_add(UC_HOOK_INSN_INVALID, h_insn)
    mu.hook_add(UC_HOOK_MEM_INVALID, h_mem)
    try:
        mu.emu_start(0x746e34, RET, timeout=180_000_000)
    except Exception as ex:
        fault['ex'] = str(ex)
    out = np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4)
    return out, fault

def metrics(arr, tag):
    rgb = arr[:, :, :3].astype(np.int16)
    dx = float(np.abs(np.diff(rgb, axis=1)).mean())
    dy = float(np.abs(np.diff(rgb, axis=0)).mean())
    uniq = int(len(np.unique(arr[:, :, :3].reshape(-1, 3), axis=0)))
    nonblack = float((arr[:, :, :3].max(2) > 0).mean())
    print(f'{tag:8s} dx={dx:6.2f} dy={dy:6.2f} uniq={uniq:6d} nonblack={nonblack:.3f}')
    return dict(dx=dx, dy=dy, uniq=uniq, nonblack=nonblack)

res = {}
variants = {'raw_null': mip0, 'H1_rot': rot(mip0, H1), 'H2_modrev': rot(mip0, H2), 'H3_colswp': rot(mip0, H3)}
for tag, buf in variants.items():
    arr, fault = run_engine(buf)
    res[tag] = dict(metrics(arr, tag), fault=fault)
    Image.fromarray(arr[:, :, :3]).save(f'{RE}/session39/s39b_{tag}.png')
    np.save(f'{RE}/session39/s39b_{tag}.npy', arr)
    print('   fault:', fault)

json.dump(res, open(f'{RE}/session39/s39b_rot_test.json', 'w'), indent=1)
print('done')
