#!/usr/bin/env python3
"""S39b T2 probe4: localize mod corner geometry + punch-through alpha.
E) ONE block (8,8) has mod field j=3, all else 0. Scan 16x16 px around it.
   j variants: 0 (bits0-1), 1 (bits2-3), 2 (bits4-5), 4 (bits8-9).
F) uniform mod=2, colA=white colB=black -> alpha behavior (punch-through?)
G) uniform mod=2, colA=white colB=white -> color at mod2
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
W = H = 64
NB = 256
DATA, DEST, RET = 0x70000000, 0x71000000, 0xDED00000
WHITE = (1 << 1) | (1 << 6) | (1 << 11)

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

def buf_one_field(j):
    b = np.zeros((NB, 8), np.uint8)
    b[:, 4:6] = np.frombuffer(struct.pack('<H', WHITE), np.uint8)
    b[8 * 16 + 8, 0] = 3 << (2 * (j % 4)) if j < 4 else 0
    if j >= 4:
        b[8 * 16 + 8, j // 4] = 3 << (2 * (j % 4))
    return b.tobytes()

print('=== E) single block (8,8) field j: R-channel map 16x16 around px(32,32) ===')
for j in (0, 1, 2, 4):
    arr = run(buf_one_field(j))
    reg = arr[24:40, 24:40, 0]
    dark = np.argwhere(reg == reg.min())
    print(f'j={j}: min={reg.min()} at reg-idx {dark[0]} (abs {(dark[0]+24).tolist()})')
    if j == 0:
        for r in range(reg.shape[0]):
            print('   ', ' '.join(f'{reg[r,c]:3d}' for c in range(reg.shape[1])))

print('=== F) uniform mod=2 punch-through ===')
b = np.zeros((NB, 8), np.uint8)
b[:, 0:4] = np.frombuffer(struct.pack('<I', 0xAAAAAAAA), np.uint8)
b[:, 4:6] = np.frombuffer(struct.pack('<H', WHITE), np.uint8)
arrF = run(b.tobytes())
print('colA=white colB=0 mod2 px[16:24,16:24] RGBA sample:')
print(arrF[16, 16:24].tolist())
print('alpha uniq:', np.unique(arrF[:, :, 3]))

b2 = np.zeros((NB, 8), np.uint8)
b2[:, 0:4] = np.frombuffer(struct.pack('<I', 0xAAAAAAAA), np.uint8)
b2[:, 4:6] = np.frombuffer(struct.pack('<H', WHITE), np.uint8)
b2[:, 6:8] = np.frombuffer(struct.pack('<H', WHITE), np.uint8)
arrG = run(b2.tobytes())
print('=== G) colA=colB=white mod2 ===')
print(arrG[16, 16:24].tolist())
print('alpha uniq:', np.unique(arrG[:, :, 3]))
