#!/usr/bin/env python3
"""S39b T2 probe3: per-PIXEL tiles -> expansion LUTs, mod field order, bilinear, dither.
All 64x64, all blocks identical unless stated. Print the central 4x4 tile of each run.
"""
import struct, json
import numpy as np

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

W = H = 64
NB = (W // 4) * (H // 4)
DATA, DEST = 0x70000000, 0x71000000
RET = 0xDED00000

def run_engine(buf, opA=1, w=W, h=H):
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
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try:
        mu.emu_start(0x746e34, RET, timeout=60_000_000)
    except Exception:
        pass
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4)

def mkblocks(mod, colA, colB, nb=NB):
    b = np.zeros((nb, 8), np.uint8)
    b[:, 0:4] = np.frombuffer(struct.pack('<I', mod), np.uint8)
    b[:, 4:6] = np.frombuffer(struct.pack('<H', colA), np.uint8)
    b[:, 6:8] = np.frombuffer(struct.pack('<H', colB), np.uint8)
    return b.tobytes()

def tile(arr, ch=3):
    t = arr[0:4, 0:4, :4]
    return t

def show(arr, label):
    t = tile(arr)
    print(f'-- {label}')
    for r in range(4):
        print('   ', ' '.join(f'{t[r,c,0]:3d},{t[r,c,1]:3d},{t[r,c,2]:3d},{t[r,c,3]:3d}' for c in range(4)))

res = {}
WHITE = (1 << 1) | (1 << 6) | (1 << 11)

# A) colA B3 field tiles v=0..7 (mod=0)
print('===== A) colA B3 field (v<<1), mod=0 =====')
lutB = {}
for v in range(8):
    arr = run_engine(mkblocks(0, v << 1, 0))
    show(arr, f'B3 v={v}')
    lutB[v] = arr[0, 0, :4].tolist()
res['lutA_B3'] = lutB

# A2) colA G4 / R4 / A4 (v step) at mod=0 - first pixel + tile for a few
lutG, lutR, lutA4 = {}, {}, {}
for v in range(16):
    lutG[v] = run_engine(mkblocks(0, v << 4, 0))[0, 0, :4].tolist()
    lutR[v] = run_engine(mkblocks(0, v << 8, 0))[0, 0, :4].tolist()
    lutA4[v] = run_engine(mkblocks(0, v << 12, 0))[0, 0, :4].tolist()
print('===== A2) colA G4/R4/A4 first-pixel LUTs =====')
print('G4:', {v: lutG[v] for v in range(16)})
print('R4:', {v: lutR[v] for v in range(16)})
print('A4:', {v: lutA4[v] for v in range(16)})
res['lutA_G4'], res['lutA_R4'], res['lutA_A4'] = lutG, lutR, lutA4

# B) colB fields at mod=3 (all texels v=3), colA=0
print('===== B) colB fields at mod=3 =====')
lbB, lbG, lbR, lbA = {}, {}, {}, {}
for v in range(16):
    lbB[v] = run_engine(mkblocks(0xFFFFFFFF, 0, v << 0))[0, 0, :4].tolist() if v < 8 else None
    lbG[v] = run_engine(mkblocks(0xFFFFFFFF, 0, v << 4))[0, 0, :4].tolist()
    lbR[v] = run_engine(mkblocks(0xFFFFFFFF, 0, v << 8))[0, 0, :4].tolist()
    lbA[v] = run_engine(mkblocks(0xFFFFFFFF, 0, v << 12))[0, 0, :4].tolist()
print('B3:', {v: lbB[v] for v in range(8)})
print('G4:', {v: lbG[v] for v in range(16)})
print('R4:', {v: lbR[v] for v in range(16)})
print('A4:', {v: lbA[v] for v in range(16)})
res['lutB_B3'], res['lutB_G4'], res['lutB_R4'], res['lutB_A4'] = lbB, lbG, lbR, lbA

# C) mod field order: mod = 3<<(2j), colA=WHITE colB=0 -> dark texel location
print('===== C) mod field order (single field v=3) =====')
fieldmap = {}
for j in range(16):
    arr = run_engine(mkblocks(3 << (2 * j), WHITE, 0))
    t = arr[0:4, 0:4, 0]  # R channel
    dark = np.unravel_index(np.argmin(t), (4, 4))
    vals = t.tolist()
    fieldmap[j] = dict(dark=list(dark), vals=vals)
    print(f'j={j:2d} darkest={dark} row0={vals[0]}')
res['mod_field'] = fieldmap

# D) bilinear test: left 2 block-cols WHITE colA, right 2 BLACK, mod=0
b = np.zeros((NB, 8), np.uint8)
b[:, 4:6] = np.frombuffer(struct.pack('<H', WHITE), np.uint8)
arr = b.tobytes()
buf = bytearray(arr)
for i in range(NB):
    bx, by = i % 16, i // 16
    if bx >= 2:
        buf[i*8+4:i*8+8] = b'\x00\x00\x00\x00'
arr2 = run_engine(bytes(buf))
print('===== D) bilinear test: cols 0-1 white, 2-3 black (mod=0) =====')
print('row 2, cols 0..7 R:', arr2[2, 0:8, 0].tolist())
res['bilinear_row'] = arr2[2, 0:8, 0].tolist()

json.dump(res, open(f'{RE}/session39/s39b_probe3.json', 'w'), indent=1, default=str)
print('saved')
