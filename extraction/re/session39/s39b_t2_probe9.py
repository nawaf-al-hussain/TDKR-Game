#!/usr/bin/env python3
"""S39b probe9: influence region per red block position — LINEAR feeding (no reorder).
Determines the engine's block addressing exactly."""
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

def colA555(r, g, b, modmode=1):
    return 0x8000 | (modmode << 0) | ((b >> 4) << 1) | ((g >> 3) << 5) | ((r >> 3) << 10)

GREY = colA555(128, 128, 128)
RED = colA555(255, 0, 0)

def base():
    b = np.zeros((NB, 8), np.uint8)
    ca = np.full(NB, GREY, np.uint16)
    b[:, 4:6] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    b[:, 6:8] = ca.astype('<u2').view(np.uint8).reshape(-1, 2)
    return b

base_arr = run(base().tobytes())
cb = np.frombuffer(struct.pack('<H', RED), np.uint8)
for L in (0, 1, 2, 3, 4, 5, 8, 16, 17, 32, 64, 128, 255):
    b = base(); b[L, 4:6] = cb; b[L, 6:8] = cb
    arr = run(b.tobytes())
    dev = arr[:, :, 0].astype(int) - base_arr[:, :, 0].astype(int)
    nz = np.argwhere(np.abs(dev) > 8)
    if len(nz):
        r0, r1 = nz[:, 0].min(), nz[:, 0].max()
        c0, c1 = nz[:, 1].min(), nz[:, 1].max()
        peak = np.unravel_index(np.argmax(np.abs(dev)), dev.shape)
        print(f'L={L:3d} (bx={L%16:2d},by={L//16:2d}): rows {r0}-{r1} cols {c0}-{c1} peak@{peak} dev={dev[peak]}')
    else:
        print(f'L={L:3d}: NO influence')
