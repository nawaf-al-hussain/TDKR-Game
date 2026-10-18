#!/usr/bin/env python3
"""S36 T2: run each .init_array entry under Unicorn; after each, check whether
the 64-B OBB template at 0xc585b8 (pointer from GOT slot 0xc07f70) became filled."""
import struct, sys
sys.path.insert(0, '/home/z/my-project/scripts')
from s36_t1_trace import Emu, RET_MAGIC, STACK
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC

SO = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()
e_shoff = struct.unpack_from('<I', SO, 0x20)[0]
e_shentsize = struct.unpack_from('<H', SO, 0x2E)[0]
e_shnum = struct.unpack_from('<H', SO, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', SO, 0x32)[0]
secs = [struct.unpack_from('<10I', SO, e_shoff + i * e_shentsize) for i in range(e_shnum)]
def sname(n):
    o = secs[e_shstrndx][4] + n
    return SO[o:SO.index(b'\0', o)].decode()
init_off = init_size = None
for s in secs:
    if sname(s[0]) == '.init_array':
        init_off, init_size = s[4], s[5]
ENTRIES = [struct.unpack_from('<I', SO, init_off + i * 4)[0] for i in range(init_size // 4)]

TEMPLATE = 0xc585b8

def read_template(mu):
    try:
        return bytes(mu.mem_read(TEMPLATE, 64))
    except Exception:
        return b'\0' * 64

filled_by = None
for idx, ent in enumerate(ENTRIES):
    emu = Emu()
    mu = emu.mu
    mu.reg_write(UC_ARM_REG_SP, STACK + 0x180000)
    mu.reg_write(UC_ARM_REG_LR, RET_MAGIC)
    mu.reg_write(UC_ARM_REG_R0, 0)
    try:
        mu.emu_start(ent, RET_MAGIC, count=40_000_000)
        status = 'ok'
    except Exception as e:
        status = f'ERR {e}'
    t = read_template(mu)
    nz = sum(1 for b in t if b)
    print(f'init[{idx:2d}] @0x{ent:06x}: {status:22s} template-nonzero-bytes={nz}')
    if nz > 0 and filled_by is None:
        filled_by = (idx, ent, t)

if filled_by:
    idx, ent, t = filled_by
    print(f'\nTEMPLATE FILLED BY init[{idx}] @0x{ent:x}')
    w = struct.unpack('<16f', t)
    print('f32:', [round(x, 4) for x in w])
    print('hex:', t.hex())
else:
    print('\nno init entry filled the template')
