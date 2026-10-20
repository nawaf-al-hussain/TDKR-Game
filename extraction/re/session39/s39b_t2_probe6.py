#!/usr/bin/env python3
"""S39b T2 probe6: FULL LUTs under colA bit0=1 (per-texel mod mode).
colA fields: B3(1-3) G4(4-7) R4(8-11) A4(12-15) + bit0 set.
colB fields: B4(0-3) G4(4-7) R4(8-11) A4(12-15).
Weight check v=1: expect uniform 5/8. Also colB bit0 semantics under this mode.
"""
import struct, json
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

res = {}
# colA LUTs with bit0=1, mod=0
print('=== colA LUTs (bit0=1, mod=0) ===')
for name, sh, n in [('B3', 1, 8), ('G4', 4, 16), ('R4', 8, 16), ('A4', 12, 16)]:
    lut = []
    for v in range(n):
        arr = run(mk(0, 1 | (v << sh), 0))
        lut.append(arr[32, 32, :4].tolist())
    print(f'{name}: {lut}')
    res[f'A_{name}'] = lut
# verify bit0 itself: colA=1 vs colA=0
arr = run(mk(0, 1, 0)); print('colA=1 (only bit0):', arr[32, 32, :4].tolist())
res['A_bit0'] = arr[32, 32, :4].tolist()

# colB LUTs under mod=3 (B fully weighted), colA = bit0 only
print('=== colB LUTs (mod=3, colA=1) ===')
for name, sh, n in [('B4', 0, 16), ('G4', 4, 16), ('R4', 8, 16), ('A4', 12, 16)]:
    lut = []
    for v in range(n):
        arr = run(mk(MOD3, 1, v << sh))
        lut.append(arr[32, 32, :4].tolist())
    print(f'{name}: {lut}')
    res[f'B_{name}'] = lut

# weights uniform check under bit0=1: A=white B=black
WHITE = (1 << 1) | (1 << 6) | (1 << 11)
for v, word in [(0, 0), (1, 0x55555555), (2, 0xAAAAAAAA), (3, 0xFFFFFFFF)]:
    arr = run(mk(word, WHITE | 1, 0))
    print(f'weight v={v}: {arr[32, 32, :3].tolist()} (white=140,66,33)')

json.dump(res, open(f'{RE}/session39/s39b_probe6.json', 'w'), indent=1)
print('saved')
