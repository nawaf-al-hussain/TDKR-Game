#!/usr/bin/env python3
"""S39b: CALIBRATE the mip oracle with SYNTHETIC consistent mips.
Build fake mip0/mip1 endpoint grids that are exactly consistent (mip1 = ds2 of mip0),
encode as blocks (B=A, mod=0), engine-decode both, measure ds2-RMSE floor.
If floor ~25 -> current transform is already near-optimal; if ~5 -> still broken.
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
DATA, DEST, RET = 0x70000000, 0x71000000, 0xDED00000

def run(buf, w, h):
    emu = Emu(); mu = emu.mu
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000); mu.mem_write(DATA, buf)
    S = 0x20100000
    mu.mem_write(S - 16, struct.pack('<I', DEST)); mu.reg_write(UC_ARM_REG_SP, S - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 1)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    mu.mem_map(RET & ~0xFFF, 0x1000); mu.reg_write(UC_ARM_REG_LR, RET)
    mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.hook_add(UC_HOOK_INSN_INVALID, lambda uc, u: uc.emu_stop())
    mu.hook_add(UC_HOOK_MEM_INVALID, lambda uc, a, ad, s, v, u: uc.emu_stop())
    try: mu.emu_start(0x746e34, RET, timeout=240_000_000)
    except Exception: pass
    return np.frombuffer(bytes(mu.mem_read(DEST, w * h * 4)), np.uint8).reshape(h, w, 4)

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

def make_blocks(A, mode=1, modpat=None):
    # A: (bh, bw, 3) uint8 endpoint colors -> blocks with colA=pack(A), colB=colA, mod=pat
    bh, bw, _ = A.shape
    nb = bh * bw
    r, g, b = A[..., 0].astype(np.uint16), A[..., 1].astype(np.uint16), A[..., 2].astype(np.uint16)
    colA = mode | ((b >> 5) << 1) | ((g >> 4) << 4) | ((r >> 4) << 8) | (8 << 12)
    out = np.zeros((nb, 8), np.uint8)
    if modpat is not None:
        out[:, 0:4] = modpat
    out[:, 4:6] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 6:8] = colA.astype('<u2').view(np.uint8).reshape(-1, 2)
    return out

rng = np.random.default_rng(7)
# smooth random endpoint grid: bilinear upsample of low-res noise + per-block jitter
lo = rng.normal(128, 60, (8, 8, 3))
from PIL import Image
A0 = np.asarray(Image.fromarray(np.clip(lo, 0, 255).astype(np.uint8)).resize((64, 64), Image.BILINEAR))
A0 = A0.astype(np.int16)
# add per-block noise to make it less trivially smooth
A0 = np.clip(A0 + rng.normal(0, 6, A0.shape), 0, 255).astype(np.uint8)
A1 = A0.reshape(32, 2, 32, 2, 3).mean((1, 3)).round().astype(np.uint8)

for tag, modpat in [('mod0', None), ('checker', np.array([0xAA, 0xAA, 0xAA, 0xAA], np.uint8))]:
    B0 = morton_reorder(make_blocks(A0.reshape(64, 64, 3), modpat=modpat), 64, 64)
    B1 = morton_reorder(make_blocks(A1.reshape(32, 32, 3), modpat=modpat), 32, 32)
    a0 = run(B0.tobytes(), 256, 256)[:, :, :3].astype(np.float64)
    a1 = run(B1.tobytes(), 128, 128)[:, :, :3].astype(np.float64)
    ds = a0.reshape(128, 2, 128, 2, 3).mean((1, 3))
    rmse = float(np.sqrt(((ds - a1) ** 2).mean()))
    print(f'synthetic consistent mips ({tag}): ds2-RMSE floor = {rmse:.2f}')
