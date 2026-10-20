#!/usr/bin/env python3
"""S39b: LINEARIZATION probes to pin the engine's exact bilinear geometry.
Base: all blocks A=grey(128), B=A, mod=0, mode=1, morton order.
P1: one block's colA = red -> influence map (R-deviation) around it.
P2: one block colB=blue + mod=0xFFFFFFFF -> where B appears.
P3: one block, single mod field j, colA=grey colB=white -> field->pixel+weight map.
All at logical block (8,8) => px (32..36). Sample 24x24 region.
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

GREY = 1 | (8 << 1) | (8 << 4) | (8 << 8) | (8 << 12)   # B3=8?? no B3 is 3-bit: use b>>5 of 128 = 4
# pack(128,128,128): R4=8, G4=8, B3=4 -> colA = mode| (4<<1) | (8<<4) | (8<<8) | (8<<12)
def colA_of(r, g, b, mode=1):
    return mode | ((b >> 5) << 1) | ((g >> 4) << 4) | ((r >> 4) << 8) | (8 << 12)

GREY = colA_of(128, 128, 128)
RED = colA_of(255, 0, 0)
BLUE = colA_of(0, 0, 255)
WHITE = colA_of(255, 255, 255)

def base_blocks():
    b = np.zeros((NB, 8), np.uint8)
    ca = np.full(NB, GREY, np.uint16)
    b[:, 4:6] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    b[:, 6:8] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    return b

BI = 8 * 16 + 8  # linear index of logical block (8,8)?? row-major: by*16+bx

print('=== P1: block (8,8) colA=RED, rest grey ===')
b = base_blocks(); b[BI, 4:6] = np.frombuffer(struct.pack('<H', RED), np.uint8)
arr = run(morton_reorder(b, 16, 16).tobytes())
base = run(morton_reorder(base_blocks(), 16, 16).tobytes())
dev = arr[:, :, 0].astype(int) - base[:, :, 0].astype(int)
reg = dev[24:44, 24:44]
for r in range(reg.shape[0]):
    print('   ', ' '.join(f'{reg[r,c]:4d}' for c in range(reg.shape[1])))
