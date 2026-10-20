#!/usr/bin/env python3
"""S39b: colB ABSOLUTE vs DELTA probe. colA=white, colB=v<<k at mod=3 (B fully shown).
absolute -> out = expand(colB). delta -> out = white +/- sext(expand(colB)).
Also: G4/R4/A4 fields of colB at nonzero colA; colB bit15 behavior.
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
WHITE = (1 << 1) | (1 << 6) | (1 << 11) | 1   # with mode bit set
MOD3 = 0xFFFFFFFF

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

print('=== colB absolute-vs-delta: colA=WHITE(140,66,33), mod=3 ===')
for name, sh, vals in [('B4', 0, [1, 2, 4, 8, 15]), ('G4', 4, [1, 2, 4, 8, 15]),
                       ('R4', 8, [1, 2, 4, 8, 15]), ('A4', 12, [1, 8, 9, 15])]:
    for v in vals:
        arr = run(mk(MOD3, WHITE, v << sh))
        px = arr[32, 32, :4].tolist()
        print(f'  colB {name}={v:2d}: out RGBA={px}')
print()
print('=== reference: colA=WHITE alone at mod=3 (w=1 -> B) vs mod=0 (A) ===')
print('  mod3 colB=0:', run(mk(MOD3, WHITE, 0))[32, 32, :4].tolist())
print('  mod0 colB=0:', run(mk(0, WHITE, 0))[32, 32, :4].tolist())
print()
print('=== colB bit15 (0x8000) with colA=WHITE ===')
for cb in [0x8000, 0x8000 | 8, 0x8000 | (15 << 4)]:
    print(f'  colB={hex(cb)}:', run(mk(MOD3, WHITE, cb))[32, 32, :4].tolist())
