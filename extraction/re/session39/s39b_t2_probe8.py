#!/usr/bin/env python3
"""S39b probe8: DIRECT addressing map. Red-block probes at logical (1,0), (0,1),
(2,0), (0,2), (3,3); report where each appears in the output. Plus render 555 decode."""
import struct
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

def colA555(r, g, b, modmode=1):
    return 0x8000 | (modmode << 0) | ((b >> 4) << 1) | ((g >> 3) << 5) | ((r >> 3) << 10)

GREY = colA555(128, 128, 128)
RED = colA555(255, 0, 0)

def blocks_with_red(logical_idx):
    b = np.zeros((NB, 8), np.uint8)
    ca = np.full(NB, GREY, np.uint16)
    b[:, 4:6] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    b[:, 6:8] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    ca2 = np.frombuffer(struct.pack('<H', RED), np.uint8)
    b[logical_idx, 4:6] = ca2
    b[logical_idx, 6:8] = ca2
    return b

print('=== feed blocks in LINEAR order (no reorder), red at linear idx L ===')
for L in (1, 16, 2, 32, 5):
    arr = run(blocks_with_red(L).tobytes())
    dev = arr[:, :, 0].astype(int) - 16  # grey R = GA[1]=16
    nz = np.argwhere(np.abs(dev) > 8)
    if len(nz):
        print(f'L={L:3d}: red at rows {nz[:,0].min()}-{nz[:,0].max()} cols {nz[:,1].min()}-{nz[:,1].max()}')
    else:
        print(f'L={L:3d}: not visible (max dev {np.abs(dev).max()})')

print('=== feed with my morton reorder, red at logical (bx,by) ===')
def reorder(blocks):
    idx = np.array([me(bx, by) for by in range(16) for bx in range(16)], np.int64)
    out = np.empty_like(blocks); out[idx] = blocks
    return out
for bx, by in ((1, 0), (0, 1), (2, 0), (0, 2), (3, 3)):
    arr = run(reorder(blocks_with_red(by * 16 + bx)).tobytes())
    dev = arr[:, :, 0].astype(int) - 16
    nz = np.argwhere(np.abs(dev) > 8)
    if len(nz):
        print(f'({bx},{by}): red at rows {nz[:,0].min()}-{nz[:,0].max()} cols {nz[:,1].min()}-{nz[:,1].max()}')
    else:
        print(f'({bx},{by}): not visible (max dev {np.abs(dev).max()})')
