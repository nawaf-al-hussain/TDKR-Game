#!/usr/bin/env python3
"""s45 T4: second (runtime) signal for MC_MAX_DISTANCE = 40.0.

Micro-emulates the REAL registration block 0x147254..0x14745c (s44 decoded:
r6 = 0xb30948 -> movt 0x4220 -> lua_pushnumber @0xa499dc -> lua_setfield
@0xa49fc8 with _G(-10002) + 'MC_MAX_DISTANCE') under Unicorn, stubbing every
bl target except the two lua calls, which are hooked to LOG (name, value).
Then: overwrite check — any later write to the same name inside this block,
plus the static SetGlobal/save-loader scan (s44: 0 writes).
"""
import struct
from unicorn import *
from unicorn.arm_const import *
import unicorn.arm_const as _AC
_ARM_REGS = {f'R{i}': getattr(_AC, f'UC_ARM_REG_R{i}') for i in range(13)}

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
RAW = open(SO, 'rb').read()
PHOFF = struct.unpack_from('<I', RAW, 0x1c)[0]
PHNUM = struct.unpack_from('<H', RAW, 0x2c)[0]
SEGS = []
for i in range(PHNUM):
    o = PHOFF + i * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', RAW, o)[:6]
    if t == 1 and fs > 0:
        SEGS.append((va, off, fs, ms))

START = 0x14722C
END = 0x147264
RET = 0x1000000
STACK, STACK_SZ = 0x30000000, 0x400000
FAKE = 0x20000000
PUSHNUM = 0xa499dc
SETFIELD = 0xa49fc8

log = []


def cstr(uc, v, m=48):
    if not isinstance(v, int) or v < 0x1000 or v > 0xc40000:
        return None
    try:
        dd = uc.mem_read(v, m)
    except UcError:
        return None
    e = dd.find(b'\0')
    if e < 0:
        return None
    try:
        s = dd[:e].decode('ascii')
    except Exception:
        return None
    return s if all(32 <= ord(c) < 127 for c in s) else None


def hook(uc, address, size, ud):
    if address == PUSHNUM:
        r1 = uc.reg_read(_ARM_REGS['R1'])
        f = struct.unpack('<f', struct.pack('<I', r1 & 0xFFFFFFFF))[0]
        log.append(('PUSHNUM', f))
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        return
    if address == SETFIELD:
        r1 = uc.reg_read(_ARM_REGS['R1'])
        r2 = uc.reg_read(_ARM_REGS['R2'])
        idx = r1 - (1 << 32) if r1 > 0x80000000 else r1
        log.append(('SETFIELD', idx, cstr(uc, r2)))
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        return
    # generic stub for any other call target inside the window
    pc = uc.reg_read(UC_ARM_REG_PC)
    if START <= pc < END:
        return
    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))


uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
img_end = max(va + ms for (va, off, fs, ms) in SEGS)
uc.mem_map(0, ((img_end + 0xffff) & ~0xffff) + 0x1000)
for (va, off, fs, ms) in SEGS:
    uc.mem_write(va, RAW[off:off + fs])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(FAKE, 0x10000)
uc.mem_map(RET, 0x1000)
uc.hook_add(UC_HOOK_CODE, hook)
SP = STACK + STACK_SZ - 0x4000
uc.reg_write(UC_ARM_REG_SP, SP)
# [sp+4] -> CLuaScriptManager* whose +0x50 = lua_State* (stubbed calls read r0 only)
uc.mem_write(SP + 4, struct.pack('<I', FAKE))
uc.reg_write(UC_ARM_REG_R8, 0xb30948)   # s44: undisturbed pointer to 'MC_MAX_DISTANCE'
uc.mem_write(FAKE + 0x50, struct.pack('<I', FAKE + 0x8000))
uc.reg_write(UC_ARM_REG_LR, RET)
try:
    uc.emu_start(START, RET, timeout=20 * 1000000, count=10_000_000)
    print('micro-run OK')
except UcError as e:
    print('micro-run error:', e, 'pc=0x%x' % uc.reg_read(UC_ARM_REG_PC))

print('log sequence:')
for ev in log:
    print('  ', ev)
# verdict
pushed = [ev[1] for ev in log if ev[0] == 'PUSHNUM']
named = [ev for ev in log if ev[0] == 'SETFIELD' and ev[2] == 'MC_MAX_DISTANCE']
later_writes = (len([ev for ev in log[log.index(named[0]) + 1:] if ev[0] == 'SETFIELD' and ev[2] == 'MC_MAX_DISTANCE'])
                if named else -1)
print(f'\nMC_MAX_DISTANCE: pushed {pushed}, named-field writes {len(named)}, later overwrites in block {later_writes}')
print('VERDICT:', 'PASS' if 40.0 in pushed and len(named) == 1 and later_writes == 0 else 'CHECK')
