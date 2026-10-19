#!/usr/bin/env python3
"""S38 T2.1: engine PVRTCDecompress under unicorn WITH fault diagnosis.
The s37 run hit UC_ERR_INSN_INVALID mid-run (possible partial output).
This run installs INSN_INVALID + MEM_INVALID + INTR hooks, prints the exact
faulting PC and instruction bytes, and dumps the RGBA regardless."""
import struct, sys, zipfile, json
import numpy as np
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']
from unicorn import UC_HOOK_MEM_INVALID, UC_HOOK_INSN_INVALID
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_SP, UC_ARM_REG_PC, UC_ARM_REG_LR)

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

emu = Emu(); mu = emu.mu
DATA, DEST = 0x70000000, 0x71000000
mu.mem_map(DATA, 0x100000); mu.mem_map(DEST, 0x400000)
mu.mem_write(DATA, mip0)
STACK = 0x20000000 + 0x100000
mu.mem_write(STACK - 16, struct.pack('<I', DEST))
mu.reg_write(UC_ARM_REG_SP, STACK - 16)
mu.reg_write(UC_ARM_REG_R0, DATA); mu.reg_write(UC_ARM_REG_R1, 1)
mu.reg_write(UC_ARM_REG_R2, w); mu.reg_write(UC_ARM_REG_R3, h)
RET = 0xDED00000
mu.mem_map(RET & ~0xFFF, 0x1000)
mu.reg_write(UC_ARM_REG_LR, RET)
mu.reg_write(UC_ARM_REG_PC, 0x746e34)
fault = {}
def h_insn(uc, user):
    pc = uc.reg_read(UC_ARM_REG_PC)
    fault['insn_pc'] = hex(pc)
    try: fault['insn_bytes'] = bytes(mu.mem_read(pc, 4)).hex()
    except Exception: fault['insn_bytes'] = '?'
    uc.emu_stop()
def h_mem(uc, access, address, size, value, user):
    fault['mem'] = (access, hex(address), size); uc.emu_stop()
mu.hook_add(UC_HOOK_INSN_INVALID, h_insn)
mu.hook_add(UC_HOOK_MEM_INVALID, h_mem)
try:
    mu.emu_start(0x746e34, RET, timeout=120_000_000)
    print('emu stopped; pc =', hex(mu.reg_read(UC_ARM_REG_PC)))
except Exception as ex:
    print('emu exception:', ex, '| pc =', hex(mu.reg_read(UC_ARM_REG_PC)))
print('fault:', fault)
out = bytes(mu.mem_read(DEST, w*h*4))
open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t2_engine_rgba.bin', 'wb').write(out)
arr = np.frombuffer(out, np.uint8).reshape(h, w, 4)
nb = int((arr.reshape(-1,4)[:,:3].max(1) > 0).sum())
print('nonblack px:', nb, '/', w*h)
json.dump({'fault': {k: str(v) for k, v in fault.items()}, 'nonblack': nb, 'w': w, 'h': h},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t2_oracle.json', 'w'), indent=1)
