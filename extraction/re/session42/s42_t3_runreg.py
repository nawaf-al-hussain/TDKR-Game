#!/usr/bin/env python3
"""s42 T3c: RUN CLuaScriptManager::RegisterScriptGlobalVariables @0x146db0 under Unicorn.
Hook every lua API entry + the two C++ helpers and LOG (name, value) at runtime —
no more static pairing guesswork. Stub all callees as no-op loggers (stack
discipline irrelevant for logging)."""
import struct, sys
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

FN = 0x146DB0          # RegisterScriptGlobalVariables(this)  [ARM]
RET = 0x1000000
STACK, STACK_SZ = 0x30000000, 0x400000
FAKE = 0x20000000      # fake CLuaScriptManager (zeroed) + fake lua_State

HOOKS = {
    0xa499dc: 'lua_pushnumber', 0xa499fc: 'lua_pushinteger', 0xa49fc8: 'lua_setfield',
    0xa49cf0: 'lua_getfield', 0xa4b754: 'luaL_register', 0xa49e48: 'lua_createtable',
    0x14966c: 'GlobalVarAddToLocalTable', 0x149178: 'SetGlobal(char*,int,bool)',
    0x1491a4: 'SetGlobal2', 0xa49fb8: 'lua_pushstring?', 0xa49cd8: 'lua_getglobal?',
    0xa4a72c: 'lua_yield?', 0xa49e94: 'lua_pushlstring?', 0xa4e94: 'lua_pushvf? (str helper)',
}

def cstr(uc, v, m=48):
    if not isinstance(v, int) or v < 0x1000 or v > 0xc40000:
        return None
    try:
        d = uc.mem_read(v, m)
    except UcError:
        return None
    e = d.find(b'\0')
    if e < 0:
        return None
    try:
        s = d[:e].decode('ascii')
        return s if all(32 <= ord(c) < 127 for c in s) else None
    except Exception:
        return None

log = []


def hook(uc, address, size, ud):
    if address not in HOOKS:
        return
    name = HOOKS[address]
    r0, r1, r2, r3 = (uc.reg_read(_ARM_REGS[f'R{i}']) for i in range(4))
    if name == 'lua_pushnumber':
        f = struct.unpack('<f', struct.pack('<I', r1 & 0xFFFFFFFF))[0]
        log.append(('PUSHNUM', f))
    elif name == 'lua_pushinteger':
        log.append(('PUSHINT', r1))
    elif name == 'lua_createtable':
        log.append(('PUSHTABLE', f'narr={r1} nrec={r2}'))
    elif name == 'lua_setfield':
        log.append(('SETFIELD', f'idx={r1 - (1 << 32) if r1 > 0x80000000 else r1}', cstr(uc, r2)))
    elif name == 'lua_getfield':
        log.append(('GETFIELD', f'idx={r1}', cstr(uc, r2)))
    elif name == 'GlobalVarAddToLocalTable':
        log.append(('REGLOCAL', cstr(uc, r1), 'bool=%d' % r2))
    elif name.startswith('SetGlobal'):
        log.append(('SETGLOBAL', cstr(uc, r1), r2, 'bool=%d' % r3))
    elif name in ('luaL_register',):
        log.append(('LUAL_REGISTER', cstr(uc, r1)))
    # stub: return immediately
    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))


def main():
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    img_end = max(va + ms for (va, off, fs, ms) in SEGS)
    uc.mem_map(0, ((img_end + 0xffff) & ~0xffff) + 0x1000)
    for (va, off, fs, ms) in SEGS:
        uc.mem_write(va, RAW[off:off + fs])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(FAKE, 0x10000)
    uc.mem_map(RET, 0x1000)
    uc.hook_add(UC_HOOK_CODE, hook)
    # fake this: vector ptrs at +0x44/0x48/0x4c = 0 (empty), lua_State* at +0x50
    uc.mem_write(FAKE + 0x44, struct.pack('<3I', 0, 0, 0))
    uc.mem_write(FAKE + 0x50, struct.pack('<I', FAKE + 0x8000))
    sp = STACK + STACK_SZ - 0x4000
    uc.reg_write(UC_ARM_REG_SP, sp)
    uc.reg_write(UC_ARM_REG_R0, FAKE)     # this
    uc.reg_write(UC_ARM_REG_LR, RET)
    try:
        uc.emu_start(FN, RET, timeout=60 * 1000000, count=200_000_000)
        print('run OK')
    except UcError as e:
        print('run error:', e, 'pc=0x%x' % uc.reg_read(UC_ARM_REG_PC))
    # collapse the log into registration sequence
    seq = []
    pending = []
    for ev in log:
        if ev[0] in ('PUSHNUM', 'PUSHINT', 'PUSHTABLE'):
            pending.append(ev)
        elif ev[0] == 'SETFIELD':
            idx = ev[1]
            val = pending.pop() if pending else None
            is_global = idx == -10002
            seq.append(('GLOBAL' if is_global else f'field({idx})', ev[2], val))
        elif ev[0] == 'SETGLOBAL':
            seq.append(('SETGLOBAL', ev[1], ev[2]))
        elif ev[0] == 'REGLOCAL':
            seq.append(('REGISTRY+', ev[1], ev[2]))
        else:
            seq.append(ev)
    for s in seq:
        print('  ', s)
    mc = [s for s in seq if s[1] and str(s[1]).startswith('MC_')]
    print('\nMC_* globals:')
    for s in mc:
        print('  ', s)


main()
