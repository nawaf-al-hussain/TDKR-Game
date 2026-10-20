#!/usr/bin/env python3
"""S39b T2 probe2 v2: engine semantics with UNIFORM mod (no bilinear dilution).
P1a: colA full-field verification (R4G4B3 hypothesis + alpha check), additive test
P1b: alpha = colA bits 12-15?
W1:  weight table w(v) via uniform mod v, colA=white colB=0 (and inverse)
P2b: colB bit layout at uniform mod v=1 (out = B * w(1))
P2c: colB at mod v=3
P6:  opA=0 vs opA=1 (weight table switch?)
"""
import struct, json
import numpy as np

RE = '/tmp/my-project/work/TDKR-Game/extraction/re'
src = open(RE + '/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn import UC_HOOK_INSN_INVALID, UC_HOOK_MEM_INVALID
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC,
                               UC_ARM_REG_LR)

W = H = 64
NB = (W // 4) * (H // 4)
DATA, DEST = 0x70000000, 0x71000000
RET = 0xDED00000
MODU = {0: 0x00000000, 1: 0x55555555, 2: 0xAAAAAAAA, 3: 0xFFFFFFFF}

def run_engine(buf, opA=1, w=W, h=H):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, buf)
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, opA)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try:
        mu.emu_start(0x746e34, RET, timeout=60_000_000)
    except Exception:
        pass
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4)

def mkblocks(mod, colA, colB):
    b = np.zeros((NB, 8), np.uint8)
    b[:, 0:4] = np.frombuffer(struct.pack('<I', mod), np.uint8)
    b[:, 4:6] = np.frombuffer(struct.pack('<H', colA), np.uint8)
    b[:, 6:8] = np.frombuffer(struct.pack('<H', colB), np.uint8)
    return b.tobytes()

def rgba(arr):
    return arr[H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4, :4].reshape(-1, 4).mean(0).round(1)

res = {}
# W1: weights via uniform mod
w1 = {}
for v in (0, 1, 2, 3):
    out = rgba(run_engine(mkblocks(MODU[v], (1 << 1) | (1 << 6) | (1 << 11), 0)))
    outi = rgba(run_engine(mkblocks(MODU[v], 0, (1 << 1) | (1 << 6) | (1 << 11))))
    w1[v] = (list(out), list(outi))
    print(f'W1 v={v} A-side={out} B-side={outi}')
res['W1'] = {str(k): v for k, v in w1.items()}

# P1b: alpha from colA high bits. colA bit12..15 with mod=1 so output visible
p1b = {}
for k in range(11, 16):
    out = rgba(run_engine(mkblocks(MODU[1], 1 << k, 0)))
    p1b[k] = list(out)
    print(f'P1b colA bit{k} mod=1: {out}')
res['P1b'] = {str(k): v for k, v in p1b.items()}

# P1c: additivity: colA = (R=0b1011<<8)|(G=0b0110<<4)|(B=0b101<<1)
colA = (0b1011 << 8) | (0b0110 << 4) | (0b101 << 1)
out = rgba(run_engine(mkblocks(MODU[0], colA, 0)))
print('P1c combined colA', hex(colA), '->', list(out), '(predict R~4*66+... G~16+66 B~33+156)')
res['P1c'] = list(out)

# P2b: colB bits at uniform mod=1 and mod=3
p2b = {}
for v in (1, 3):
    row = {}
    for k in range(0, 16):
        out = rgba(run_engine(mkblocks(MODU[v], 0, 1 << k)))
        row[k] = list(out)
    p2b[v] = row
    print(f'P2b colB bits at mod={v}:')
    for k in range(16):
        if any(row[k]): print(f'   bit{k:2d} {row[k]}')
res['P2b'] = {str(v): {str(k): r for k, r in row.items()} for v, row in p2b.items()}

# P2c: colB = white at mod=1..3 (full B weight)
for v in (1, 2, 3):
    out = rgba(run_engine(mkblocks(MODU[v], 0, (1 << 1) | (1 << 6) | (1 << 11))))
    print(f'P2c colB=white colA=0 mod={v}: {list(out)}')
    res[f'P2c_v{v}'] = list(out)

# P6: opA=0 variant on weights
for v in (1, 2, 3):
    out = rgba(run_engine(mkblocks(MODU[v], (1 << 1) | (1 << 6) | (1 << 11), 0), opA=0))
    print(f'P6 opA=0 v={v} A-side: {list(out)}')
    res[f'P6_v{v}'] = list(out)

json.dump(res, open(f'{RE}/session39/s39b_probe2v2.json', 'w'), indent=1)
print('saved')
