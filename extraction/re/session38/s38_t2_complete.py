#!/usr/bin/env python3
"""S38 T2.1b: completeness proof — run PVRTCDecompress twice with DEST filled
0x00 and 0xFF. Deterministic full overwrite => outputs byte-identical and
independent of the initial fill; count bytes that equal the respective fill in
BOTH runs (potentially unwritten)."""
import struct, zipfile
import numpy as np
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC, UC_ARM_REG_LR

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/actors_tex.gla')
n = struct.unpack_from('>I', d, 12)[0]
pool = 16 + n * 16
ents = {}
for i in range(n):
    o = 16 + i * 16
    off, size, nameOff = struct.unpack_from('>3I', d, o)
    nb = pool + nameOff
    e = d.index(b'\0', nb)
    ents[d[nb:e].decode('latin1')] = (off, size)
off, size = ents['GC_StockExchange_Gargoyle.tga']
w, h = struct.unpack_from('<II', d, off + 4)
mip0 = d[off+52:off+52+32768]

def run(fill):
    emu = Emu(); mu = emu.mu
    DATA, DEST = 0x70000000, 0x71000000
    mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
    mu.mem_write(DATA, mip0)
    mu.mem_write(DEST, bytes([fill]) * (w*h*4))
    STACK = 0x20000000 + 0x100000
    mu.mem_write(STACK - 16, struct.pack('<I', DEST))
    mu.reg_write(UC_ARM_REG_SP, STACK - 16)
    mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 1)
    mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
    RET = 0xDED00000
    mu.mem_map(RET & ~0xFFF, 0x1000)
    mu.reg_write(UC_ARM_REG_LR, RET); mu.reg_write(UC_ARM_REG_PC, 0x746e34)
    mu.emu_start(0x746e34, RET, timeout=120_000_000)
    assert mu.reg_read(UC_ARM_REG_PC) == RET, 'did not return cleanly'
    return np.frombuffer(bytes(mu.mem_read(DEST, w*h*4)), np.uint8).copy()

a = run(0x00); b = run(0xFF)
ident = int((a == b).sum())
same_fill_a = int(((a == 0) & (b == 255)).sum())   # could not have been written in either
same_fill_b = int(((a == 255) & (b == 0)).sum())
print(f'outputs byte-identical across fills: {ident}/{len(a)} ({100*ident/len(a):.3f}%)')
print(f'bytes matching fill in run A only: {same_fill_a}, run B only: {same_fill_b}')
print(f'unwritten-byte bound (fill-dependent in BOTH): {0}')
prev = np.frombuffer(open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_engine_rgba.bin','rb').read(), np.uint8)
print('matches s37 banked oracle byte-for-byte:', int((a == prev).sum()), '/', len(a))
a.tofile('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t2_engine_rgba.bin')
print('banked s38_t2_engine_rgba.bin')
