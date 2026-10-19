#!/usr/bin/env python3
"""S39 T2d: solve the engine's mode-0 (bit31=0) colorB formula empirically.

Feed 4x4 single-block textures in the ENGINE's convention (colors at +4:
build a standard block then u32swap). A-fields = 0. B-fields = basis
patterns. All mod bits = v: engine table {0->B, 3->A}. Read center pixel.
Then compare with the STANDARD PVRTC mode-0 formula candidates.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from s39_disasm import dis  # noqa (ensures capstone import works)
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
    mu.mem_write(STACK - 16, struct_pack(DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 0)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    RET = 0xDED00000
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.emu_start(0x746e34, RET, timeout=60_000_000)
    assert mu.reg_read(UC_ARM_REG_PC) == RET
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).copy().reshape(h, w, 4)


def struct_pack(v):
    import struct
    return struct.pack('<I', v)


MODPAT = {0: 0x00000000, 1: 0x55555555, 2: 0xAAAAAAAA, 3: 0xFFFFFFFF}


def probe(mode_bit, br, bg, bb, modv):
    """standard-layout block: colors word = 555 fields + mode bit; mod word = all v"""
    cw = (br << 10) | (bg << 5) | bb | (mode_bit << 31) | 0x8000
    block = np.array([MODPAT[modv], cw & 0xFFFFFFFF], np.uint32)   # standard: [mod, colors]
    swapped = block[[1, 0]].copy()                                  # engine: [mod, colors] -> it reads colors at +4
    # engine reads colors at +4 -> engine_word1 = colors, engine_word0 = mods
    eng = np.array([MODPAT[modv], cw & 0xFFFFFFFF], np.uint32)      # engine block: +0 mods, +4 colors
    img = run_engine(eng)
    return tuple(int(x) for x in img[2, 2])


print('mode-1 (bit31=1) controls — expect linear 555 of B:')
for br, bg, bb in [(31, 0, 0), (0, 31, 0), (0, 0, 31), (31, 31, 31), (1, 0, 0), (2, 0, 0), (16, 0, 0), (8, 0, 0)]:
    print(f'  B=({br:2d},{bg:2d},{bb:2d}) mod0 ->', probe(1, br, bg, bb, 0))

print('mode-0 (bit31=0) — the unknown:')
for br, bg, bb in [(31, 0, 0), (0, 31, 0), (0, 0, 31), (31, 31, 31), (1, 0, 0), (2, 0, 0), (16, 0, 0), (8, 0, 0)]:
    print(f'  B=({br:2d},{bg:2d},{bb:2d}) mod0 ->', probe(0, br, bg, bb, 0))

print('mode-0 with nonzero A (delta interaction), B=(8,8,8):')
for ar, ag, ab in [(0, 0, 0), (31, 0, 0), (0, 31, 0), (16, 16, 16), (1, 1, 1), (2, 2, 2)]:
    cw = (ar << 10) | (ag << 5) | ab | 0x8000   # A fields (bits 0-14) + opA
    bw = (8 << 10) | (8 << 5) | 8               # B fields (bits 16-26)
    word = cw | (bw << 16)
    eng = np.array([MODPAT[0], word & 0xFFFFFFFF], np.uint32)
    img = run_engine(eng)
    print(f'  A=({ar:2d},{ag:2d},{ab:2d}) ->', tuple(int(x) for x in img[2, 2]))
