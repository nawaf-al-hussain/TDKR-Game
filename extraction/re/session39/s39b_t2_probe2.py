#!/usr/bin/env python3
"""S39b T2 probe2: nail the engine's color-word semantics with synthetic blocks.
Texture 64x64 (16x16 blocks), ALL blocks identical -> output uniform = expand(colA/colB).
P1: colA = 2^k (k=1..15), colB=0          -> per-bit RGB contributions of A
P2: colA=0, colB = 2^k                    -> per-bit contributions of B (delta?)
P3: mode bit: colA bit0 / colB bit0 effect with fixed mod
P4: mod field order: colA=white, colB=black, mod = v<<(2j) -> weight(v) at texel j
P5: delta scaling: colB = colA + small deltas (sign, range)
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

def mkblocks(mod, colA, colB):
    b = np.zeros((NB, 8), np.uint8)
    m = struct.pack('<I', mod)
    a = struct.pack('<H', colA)
    bb = struct.pack('<H', colB)
    for i in range(NB):
        b[i, 0:4] = np.frombuffer(m, np.uint8)
        b[i, 4:6] = np.frombuffer(a, np.uint8)
        b[i, 6:8] = np.frombuffer(bb, np.uint8)
    return b.tobytes()

def center(arr):
    return arr[H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4, :3].reshape(-1, 3).mean(0).round(1)

res = {}
# P1: colA bits
p1 = {}
for k in range(0, 16):
    arr = run_engine(mkblocks(0, 1 << k, 0))
    p1[k] = center(arr)
print('P1 colA bits (RGB at colA=2^k, mod=0, colB=0):')
for k, v in p1.items(): print(f'  bit{k:2d} {v}')
res['P1_colA'] = {str(k): list(v) for k, v in p1.items()}

# P2: colB bits (colA=0)
p2 = {}
for k in range(0, 16):
    arr = run_engine(mkblocks(0, 0, 1 << k))
    p2[k] = center(arr)
print('P2 colB bits:')
for k, v in p2.items(): print(f'  bit{k:2d} {v}')
res['P2_colB'] = {str(k): list(v) for k, v in p2.items()}

# P4: mod field order. colA=white, colB=black.
white = (1 << 1) | (1 << 6) | (1 << 11)   # guess 555: R=bits1-5,G=6-10,B=11-15
p4 = {}
for j in range(16):
    for v in (1, 2, 3):
        arr = run_engine(mkblocks(v << (2 * j), white, 0))
        p4[f'j{j}_v{v}'] = center(arr)
print('P4 mod fields (colA=white b1|b6|b11, colB=0):')
for j in (0, 1, 2, 3, 4, 8, 15):
    print('  ', j, {v: p4[f'j{j}_v{v}'] for v in (1, 2, 3)})
res['P4_mod'] = p4

# P5: delta probing. colA=white, colB = colA + d for d in {-4..4} packed how? first: colB=white (B=A)
p5 = {}
for colB in (0, 0xFFFF, white, white ^ 0x2, white | 0x1):
    arr = run_engine(mkblocks(0, white, colB))
    p5[hex(colB)] = center(arr)
print('P5 colB variants (colA=white):', p5)
res['P5_colB'] = {k: list(v) for k, v in p5.items()}

json.dump(res, open(f'{RE}/session39/s39b_probe2.json', 'w'), indent=1)
print('saved')
