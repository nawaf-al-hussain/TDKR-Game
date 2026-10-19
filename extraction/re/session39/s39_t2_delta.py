#!/usr/bin/env python3
"""S39 T2e: recover the engine's delta-style extraction f(X_r, Y_r).

Engine color word (word at +4): bits 0-14 = 'P' (delta-style <<1 extraction
per disasm), bits 16-30 = 'Q' (plain 555). mod=0 selects P, mod=3 selects Q.
Sweep P_r x Q_r over the RED channel to recover f. w=4,h=4 single block.
"""
import numpy as np
import struct

src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC, UC_ARM_REG_LR


def run_engine(block8, w=4, h=4):
    emu = Emu(); mu = emu.mu
    DATA, DEST = 0x70000000, 0x71000000
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, block8.tobytes()); mu.mem_write(DEST, bytes(w * h * 4))
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 0)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    RET = 0xDED00000
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.emu_start(0x746e34, RET, timeout=60_000_000)
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).copy().reshape(h, w, 4)


MOD0 = 0x00000000   # all mod bits = 0 -> P
MOD3 = 0xFFFFFFFF   # all mod bits = 3 -> Q


def probe(p_r, q_r, modword):
    word = (p_r << 10) | 0x8000 | (q_r << 26)   # P_r at bits 10-14, opA, Q_r at 26-30
    eng = np.array([modword, word], np.uint32)  # +0 mod, +4 colors (engine convention)
    img = run_engine(eng)
    return int(img[2, 2, 0])                    # red out


print('P sweep (Q=0, mod0):')
pv = {}
for v in [0, 1, 2, 3, 4, 7, 8, 12, 15, 16, 24, 31]:
    pv[v] = probe(v, 0, MOD0)
    print(f'  P_r={v:2d} -> R={pv[v]}')
print('Q sweep (P=0, mod3):')
qv = {}
for v in [0, 1, 2, 8, 16, 31]:
    qv[v] = probe(0, v, MOD3)
    print(f'  Q_r={v:2d} -> R={qv[v]}')
print('interaction (P=8, Q sweep, mod0):')
for v in [0, 1, 8, 16, 31]:
    print(f'  Q_r={v:2d} -> R={probe(8, v, MOD0)}')
print('interaction (P=16, Q sweep, mod0):')
for v in [0, 1, 8, 16, 31]:
    print(f'  Q_r={v:2d} -> R={probe(16, v, MOD0)}')
