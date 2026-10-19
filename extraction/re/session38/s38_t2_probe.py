#!/usr/bin/env python3
"""S38 T2.3: SYNTHETIC PROBE of the engine PVRTCDecompress.
Feed hand-built blocks with known endpoint/modulation semantics; read back
what the engine actually produces. Determines: word order, channel order,
555 expansion, modulation table, bilinear geometry — empirically."""
import struct
import numpy as np
from PIL import Image
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC, UC_ARM_REG_LR

W = H = 64   # 16x16 blocks
def run(data, flag=1, w=W, h=H):
    emu = Emu(); mu = emu.mu
    DATA, DEST = 0x70000000, 0x71000000
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, data)
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, flag)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    RET = 0xDED00000
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.emu_start(0x746e34, RET, timeout=120_000_000)
    assert mu.reg_read(UC_ARM_REG_PC) == RET
    return np.frombuffer(bytes(mu.mem_read(DEST, w*h*4)), np.uint8).reshape(h, w, 4)

def blk(mod_word, color_word):
    return struct.pack('<II', mod_word, color_word)

def col555(r, g, b, opaque=1):
    return (r & 31) | ((g & 31) << 5) | ((b & 31) << 10) | ((opaque & 1) << 15)

RED = col555(31, 0, 0)
BLUE = col555(0, 0, 31)
GREEN = col555(0, 31, 0)
WHITE = col555(31, 31, 31)
BLACK = col555(0, 0, 0)

tests = {}
# T1: uniform block, mod=0 (expect colorA=red everywhere if mod 0 -> A)
tests['T1_mod0_redA'] = blk(0x00000000, RED | (BLUE << 16))
# T2: uniform block, all mod=1 (0x55555555) -> expect colorB=blue if mod1 -> B
tests['T2_mod1_blueB'] = blk(0x55555555, RED | (BLUE << 16))
# T3: all mod=2 (0xAAAAAAAA) -> blend or third entry
tests['T3_mod2'] = blk(0xAAAAAAAA, RED | (BLUE << 16))
# T4: all mod=3 (0xFFFFFFFF) -> blend/black?
tests['T4_mod3'] = blk(0xFFFFFFFF, RED | (BLUE << 16))
# T5: uniform GREEN vs WHITE (channel-order check with opaque=0 on A)
tests['T5_chans'] = blk(0x00000000, GREEN | (WHITE << 16))
# T6: opacity flag off on A (alpha check)
tests['T6_alpha'] = blk(0x00000000, col555(31, 0, 0, 0) | (BLUE << 16))
# T7: mode bit set (444+delta?) — colorA red, colB field 444-encoded green, mode=1
tests['T7_mode1'] = blk(0x00000000, RED | (1 << 31) | (0x0F << 16))  # colB 444 = 15,15,15?

out = {}
for name, data in tests.items():
    blocks = data * (16 * 16)
    a = run(blocks)
    center = a[32, 32]
    corner = a[2, 2]
    out[name] = {'center_rgba': [int(x) for x in center], 'corner_rgba': [int(x) for x in corner]}
    print(f'{name}: center {tuple(int(x) for x in center)} corner {tuple(int(x) for x in corner)}')

# T8: HORIZONTAL GRADIENT probe — bilinear geometry.
# Left half blocks: A=black B=black; right half: A=white B=white.
# If endpoints live at block corners with bilinear across the grid, the
# transition spans ~1 block (4 px) around x=32; a per-block NEAREST gives a
# sharp edge; different corner conventions shift the ramp.
blocks = bytearray()
for by in range(16):
    for bx in range(16):
        cA = WHITE if bx >= 8 else BLACK
        blocks += blk(0x00000000, cA | (cA << 16))
a = run(bytes(blocks))
row = a[32, 26:38, 0]
out['T8_gradient_row'] = [int(x) for x in row]
print('T8 gradient row (x=26..38):', out['T8_gradient_row'])

import json
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t2_probe.json', 'w'), indent=1)
print('saved s38_t2_probe.json')
