#!/usr/bin/env python3
"""S39b probe7: field->pixel geometry with CORRECT 555 packing.
P1: single block (8,8) colA=red, others grey -> A influence map.
P2: single block colB=white(colA=grey), mod field j=3 -> 16 deviation maps.
Sample 12x12 px around (32,32). Engine as oracle.
"""
import struct
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
W = H = 64; NB = 256
DATA, DEST, RET = 0x70000000, 0x71000000, 0xDED00000

def run(buf, opA=1):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000); mu.mem_write(DATA, buf)
    S = 0x20100000
    mu.mem_write(S - 16, struct.pack('<I', DEST)); mu.reg_write(UC_ARM_REG_SP, S - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, opA)
    mu.reg_write(UC_ARM_REG_R2, W); mu.reg_write(UC_ARM_REG_R3, H)
    mu.mem_map(RET & ~0xFFF, 0x1000); mu.reg_write(UC_ARM_REG_LR, RET)
    mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try: mu.emu_start(0x746e34, RET, timeout=60000000)
    except Exception: pass
    return np.frombuffer(bytes(mu.mem_read(DEST, W * H * 4)), np.uint8).reshape(H, W, 4)

def me(x, y):
    x &= 0xFFFF; y &= 0xFFFF
    x = (x | (x << 8)) & 0x00FF00FF; x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333; x = (x | (x << 1)) & 0x55555555
    y = (y | (y << 8)) & 0x00FF00FF; y = (y | (y << 4)) & 0x0F0F0F0F
    y = (y | (y << 2)) & 0x33333333; y = (y | (y << 1)) & 0x55555555
    return (y << 1) | x

def reorder(blocks):
    idx = np.array([me(bx, by) for by in range(16) for bx in range(16)], np.int64)
    out = np.empty_like(blocks)
    out[idx] = blocks
    return out

def colA555(r, g, b, modmode=1):
    return 0x8000 | (modmode << 0) | ((b >> 4) << 1) | ((g >> 3) << 5) | ((r >> 3) << 10)

GREY = colA555(128, 128, 128)
RED = colA555(255, 0, 0)
WHITEc = colA555(255, 255, 255)

def base():
    b = np.zeros((NB, 8), np.uint8)
    ca = np.full(NB, GREY, np.uint16)
    b[:, 4:6] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    b[:, 6:8] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    return b

BI = 8 * 16 + 8
base_arr = run(reorder(base()).tobytes())

print('=== P1: block(8,8) colA=RED (dev of R channel, region 26..38) ===')
b = base(); ca = np.frombuffer(struct.pack('<H', RED), np.uint8); b[BI, 4:6] = ca
arr = run(reorder(b).tobytes())
dev = arr[:, :, 0].astype(int) - base_arr[:, :, 0].astype(int)
reg = dev[26:38, 26:38]
for r in range(reg.shape[0]):
    print('   ', ' '.join(f'{reg[r,c]:4d}' for c in range(reg.shape[1])))

print('=== P2: block(8,8) colB=WHITE colA=grey, single field j=3 (R dev) ===')
for j in [0, 1, 2, 3, 4, 5, 8, 12, 15]:
    b = base()
    cb = np.frombuffer(struct.pack('<H', WHITEc), np.uint8)
    b[BI, 6:8] = cb
    b[BI, j // 4] = np.uint8(3 << ((j % 4) * 2)) if j < 16 else 0
    b[BI, (j // 4)] = np.uint8(3 << ((j % 4) * 2))
    arr = run(reorder(b).tobytes())
    dev = arr[:, :, 0].astype(int) - base_arr[:, :, 0].astype(int)
    reg = dev[30:38, 30:38]
    nz = np.argwhere(np.abs(dev) > 0)
    print(f'j={j:2d}: nz={len(nz)}', end=' ')
    if len(nz):
        print('max at', nz[np.argmax(np.abs(dev[30:38, 30:38][nz[:,0], nz[:,1]]))].tolist() if len(nz) else '', end=' ')
        print('vals row4:', reg[4].tolist()[:8])
    else:
        print()
