#!/usr/bin/env python3
"""S39b T2 probe5: colA bit0 = modulation-mode selector?
1) bit0=1: uniform mod v=0..3, colA=white colB=black -> per-pixel pattern
2) bit0=1: single-field j=2 (dead before) -> live?
3) bit0=0: checkerboard phase map for v=1 and v=2 (8x8 tile)
4) bit0=1: full 16-field single probes j=0..15 -> field->texel map
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

def mk(mod, colA, colB):
    b = np.zeros((NB, 8), np.uint8)
    b[:, 0:4] = np.frombuffer(struct.pack('<I', mod), np.uint8)
    b[:, 4:6] = np.frombuffer(struct.pack('<H', colA), np.uint8)
    b[:, 6:8] = np.frombuffer(struct.pack('<H', colB), np.uint8)
    return b.tobytes()

BLACK = 0
print('=== 1) colA bit0=1 (mode bit set), uniform mod, A=white B=black ===')
for v, word in [(0, 0), (1, 0x55555555), (2, 0xAAAAAAAA), (3, 0xFFFFFFFF)]:
    arr = run(mk(word, WHITE | 1, BLACK))
    t = arr[16:20, 16:20, 0]
    print(f' v={v} R tile rows: {[list(t[r]) for r in range(4)]} alpha={arr[16,16,3]}')

print('=== 3) bit0=0 checkerboard phases (v=1, v=2) 8x8 ===')
for v, word in [(1, 0x55555555), (2, 0xAAAAAAAA)]:
    arr = run(mk(word, WHITE, BLACK))
    t = arr[0:8, 0:8, 0]
    print(f' v={v}:')
    for r in range(8):
        print('   ', ' '.join(f'{t[r,c]:3d}' for c in range(8)))

print('=== 2/4) bit0=1: single-field probes j=0..15 ===')
for j in range(16):
    b = np.zeros((NB, 8), np.uint8)
    b[:, 4:6] = np.frombuffer(struct.pack('<H', WHITE | 1), np.uint8)
    b[:, (2 * j) // 8] = np.uint8(3 << ((2 * j) % 8))
    arr = run(b.tobytes())
    t = arr[0:4, 0:4, 0]
    dark = np.argwhere(t == t.min())
    row = arr[0, 0:4, 0].tolist()
    print(f' j={j:2d} byte{(2*j)//8} sh{(2*j)%8}: min={t.min():3d} darkest={[list(d) for d in dark[:3]]} row0={row}')
