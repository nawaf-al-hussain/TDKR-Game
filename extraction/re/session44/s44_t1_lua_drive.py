#!/usr/bin/env python3
"""s44 T1 decisive test: drive the engine's OWN Lua VM (libKRHP.so) under Unicorn.

1. lua_newstate @0xa61120 (engine-confirmed: called at 0x146bb4) with a
   Python-implemented allocator (bump arena + realloc-copy, freed-block reuse).
2. Set the global MC_MAX_DISTANCE = EMPTY TABLE (the s43-established
   registration state) via lua_createtable @0xa49e48 + lua_setfield @0xa49fc8
   on LUA_GLOBALSINDEX (-10002).
3. luaL_loadstring @0xa4c5f4 + lua_pcall @0xa4a49c of:
     - "return 5 * 5"                 (positive control  -> 25)
     - "return 5 * MC_MAX_DISTANCE"   (the question)
     - "return 5 * NEVER_SET_GLOBAL"  (nil-operand control, post-Reset state model)
4. Read results raw: TValue = 8 B {value, tt} (tt 3=number f32, 4=string at +0x10).
libc imports are satisfied by patching R_ARM_JUMP_SLOT GOT slots with magic
hook addresses (realloc/free/malloc/memcpy/memset/strlen/memmove/strtod).
"""
import struct
from unicorn import *
from unicorn.arm_const import *
import unicorn.arm_const as _AC
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

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

STACK, STACK_SZ = 0x30000000, 0x400000
HEAP, HEAP_SZ = 0x40000000, 0x10000000
FAKE_ALLOC = 0x50000000
RET_MAGIC = 0x1000000

# symbol table for extra annotations
symoff, symsize, strsym_off = 0xc1e064, 0x158e10, 0xd76e74
NAMED = {}
for i in range(symsize // 12):
    o = symoff + i * 12
    nameoff, value, size, info, other, shndx = struct.unpack_from('<IIBBHI', RAW, o)
    if not value:
        continue
    e = RAW.find(b'\0', strsym_off + nameoff, strsym_off + nameoff + 200)
    nm = RAW[strsym_off + nameoff:e].decode('ascii', 'replace')
    if nm and not nm.startswith('$'):
        NAMED.setdefault(value, nm)

LUA_NEWMODE = 0xa61120      # lua_newstate
LUA_CREATETABLE = 0xa49e48  # lua_createtable
LUA_SETFIELD = 0xa49fc8     # lua_setfield
LUA_LOADSTRING = 0xa4c5f4   # luaL_loadstring
LUA_PCALL = 0xa4a49c        # lua_pcall
LUA_GETTOP = 0xa49134       # lua_gettop
LUA_TONUMBER = 0xa49610     # lua_tonumber

# ---- GOT patch set from relocations ----
def jump_slots():
    out = {}
    e_shoff = struct.unpack_from('<I', RAW, 0x20)[0]
    e_shnum = struct.unpack_from('<H', RAW, 0x30)[0]
    dynsym_off, dynstr_off = 0x114, 0xb5a4
    def sym_name(idx):
        o = dynsym_off + idx * 12
        nameoff = struct.unpack_from('<I', RAW, o)[0]
        e = RAW.find(b'\0', dynstr_off + nameoff, dynstr_off + nameoff + 128)
        return RAW[dynstr_off + nameoff:e].decode('ascii', 'replace')
    for soff, ssize in ((0x351fc, 0x6f118), (0xa4314, 0xa88)):
        for i in range(ssize // 8):
            off, info = struct.unpack_from('<II', RAW, soff + i * 8)
            if (info & 0xff) == 22:   # R_ARM_JUMP_SLOT only (GLOB_DAT holds valid base-0 values)
                out[off] = sym_name(info >> 8)
    return out

LIBC = jump_slots()
MAGICS = {}
mid = 0
for got, nm in sorted(LIBC.items(), key=lambda kv: kv[1]):
    if nm not in MAGICS:
        MAGICS[nm] = 0x60000000 + mid * 0x100
        mid += 1

uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
for va, off, fs, ms in SEGS:
    uc.mem_map(va & ~0xfff, ((va & 0xfff) + ms + 0xfff) & ~0xfff)
    uc.mem_write(va, RAW[off:off + fs])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(HEAP, HEAP_SZ)
uc.mem_map(RET_MAGIC, 0x1000)
uc.mem_map(FAKE_ALLOC & ~0xfff, 0x1000)
uc.mem_map(0x60000000, 0x100000)
for got, nm in LIBC.items():
    if nm in MAGICS:
        uc.mem_write(got, struct.pack('<I', MAGICS[nm]))

# ---- Python-side allocator (bump + freelist, realloc preserves content) ----
class Heap:
    '''bump-only: never reuse, realloc always moves+copies (immune to aliasing)'''
    def __init__(self, uc):
        self.uc = uc
        self.base = HEAP + 0x1000
        self.cur = self.base
        self.blocks = {}
    def malloc(self, n):
        n = max(int(n), 8)
        p = self.cur
        self.cur += (n + 31) & ~31
        self.blocks[p] = n
        return p
    def free_(self, p):
        pass
    def realloc(self, p, n):
        if p == 0:
            return self.malloc(n)
        if n == 0:
            return 0
        old = self.blocks.get(p, 0)
        q = self.malloc(n)
        if q != p and old:
            take = min(old, n)
            if take:
                buf = bytes(self.uc.mem_read(p, take))
                self.uc.mem_write(q, buf)
        return q

heap = Heap(uc)

def cstr_read(a, m=64):
    d = bytes(uc.mem_read(a, m))
    e = d.find(b'\0')
    return d[:e] if e >= 0 else d

def cstr_write(a, s):
    uc.mem_write(a, s + b'\0')

STRBUF = 0x50010000
uc.mem_map(STRBUF & ~0xfff, 0x10000)
_sp = [0]

def tmpstr(s):
    if isinstance(s, str):
        s = s.encode()
    a = STRBUF + _sp[0]
    _sp[0] += (len(s) + 16) & ~15
    cstr_write(a, s)
    return a

log = []

def hook_code(uc, address, size, ud):
    if address == FAKE_ALLOC:
        ud_, p, osize, nsize = (uc.reg_read(_AC.UC_ARM_REG_R0), uc.reg_read(_AC.UC_ARM_REG_R1),
                                uc.reg_read(_AC.UC_ARM_REG_R2), uc.reg_read(_AC.UC_ARM_REG_R3))
        log.append(('ALLOC', hex(p), osize, nsize))
        if nsize == 0:
            heap.free_(p)
            r = 0
        elif p == 0:
            r = heap.malloc(nsize)
        else:
            r = heap.realloc(p, nsize)
        uc.reg_write(_AC.UC_ARM_REG_R0, r)
        uc.reg_write(_AC.UC_ARM_REG_PC, uc.reg_read(_AC.UC_ARM_REG_LR))
        return
    nm = None
    for k, v in MAGICS.items():
        if v == address:
            nm = k
            break
    if nm is None:
        return
    r0, r1, r2, r3 = (uc.reg_read(_AC.UC_ARM_REG_R0 + i) for i in range(4))
    if nm == 'realloc':
        r = heap.realloc(r1, r3)
        log.append(('realloc', hex(r1), r2, r3, hex(r)))
    elif nm == 'malloc':
        r = heap.malloc(r0)
    elif nm == 'calloc':
        r = heap.malloc(r0 * r1)
        uc.mem_write(r, b'\0' * (r0 * r1))
    elif nm == 'free':
        heap.free_(r0)
        r = 0
    elif nm in ('memcpy', 'memmove'):
        if r2:
            buf = bytes(uc.mem_read(r1, r2))
            uc.mem_write(r0, buf)
        r = r0
    elif nm == 'memset':
        if r2:
            uc.mem_write(r0, bytes([r1 & 0xff]) * r2)
        r = r0
    elif nm == 'strlen':
        r = len(cstr_read(r0, 65536))
    elif nm == 'memcmp':
        a = cstr_read(r0, r2 or 64)
        b = cstr_read(r1, r2 or 64)
        r = 0 if a == b else (1 if a > b else -1)
    elif nm == 'strtod':
        s = cstr_read(r0, 64)
        import re as _re
        m = _re.match(rb'[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?', s)
        if m:
            val = float(m.group(0))
            if r1:
                uc.mem_write(r1, struct.pack('<I', r0 + m.end()))
            dr = struct.pack('<d', val)
            uc.reg_write(_AC.UC_ARM_REG_R0, struct.unpack('<I', dr[:4])[0])
            uc.reg_write(_AC.UC_ARM_REG_R1, struct.unpack('<I', dr[4:])[0])
            log.append(('strtod', s[:16], val))
        else:
            uc.reg_write(_AC.UC_ARM_REG_R0, 0)
            uc.reg_write(_AC.UC_ARM_REG_R1, 0)
        uc.reg_write(_AC.UC_ARM_REG_PC, uc.reg_read(_AC.UC_ARM_REG_LR))
        return
    elif nm == 'abort':
        raise RuntimeError('abort() called')
    elif nm in ('__stack_chk_fail',):
        raise RuntimeError('stack chk fail')
    else:
        log.append(('UNHOOKED-CALLED', nm, hex(address)))
        r = 0
    uc.reg_write(_AC.UC_ARM_REG_R0, r)
    uc.reg_write(_AC.UC_ARM_REG_PC, uc.reg_read(_AC.UC_ARM_REG_LR))

uc.hook_add(UC_HOOK_CODE, hook_code, begin=FAKE_ALLOC, end=FAKE_ALLOC)
for nm, m in MAGICS.items():
    uc.hook_add(UC_HOOK_CODE, hook_code, begin=m, end=m)

TRACE = []
def trace_hook(uc, address, size, ud):
    if len(TRACE) < 4000:
        TRACE.append(address)

uc.hook_add(UC_HOOK_CODE, trace_hook)

def call(addr, *args, timeout=8_000_000):
    for i, a in enumerate(args):
        uc.reg_write(_AC.UC_ARM_REG_R0 + i, a)
    uc.reg_write(_AC.UC_ARM_REG_SP, STACK + STACK_SZ - 0x8000)
    uc.reg_write(_AC.UC_ARM_REG_LR, RET_MAGIC)
    try:
        uc.emu_start(addr, RET_MAGIC, timeout=timeout)
    except UcError as e:
        pc = uc.reg_read(_AC.UC_ARM_REG_PC)
        regs = {n: uc.reg_read(getattr(_AC, f'UC_ARM_REG_{n}')) for n in ('R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R12','SP','LR')}
        print(f'EMU FAULT {e} at pc={hex(pc)}')
        print('  regs:', {k: hex(v) for k, v in regs.items()})
        print(f'  last-trace={[hex(x) for x in TRACE[-12:]]}')
        print('  alloc log tail:', log[-15:])
        from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM as _MA
        _md = Cs(CS_ARCH_ARM, _MA)
        for off in (-16, 0, 16):
            try:
                b = bytes(uc.mem_read(pc + off, 16))
                for ins in _md.disasm(b, pc + off):
                    print(f'  {ins.address:x}: {ins.mnemonic} {ins.op_str}')
            except Exception:
                pass
        raise
    return uc.reg_read(_AC.UC_ARM_REG_R0)

def read_tvalue(addr):
    v, tt = struct.unpack('<II', bytes(uc.mem_read(addr, 8)))
    return v, tt

def top_value(L):
    top = struct.unpack('<I', bytes(uc.mem_read(L + 8, 4)))[0]
    return read_tvalue(top - 8), top

# ================= the test =================
print('== lua_newstate(our_alloc, ud) ==')
L = call(LUA_NEWMODE, FAKE_ALLOC, 0x12340000)
print('L =', hex(L))
assert L, 'lua_newstate returned NULL'

# set global MC_MAX_DISTANCE = empty table (engine registration model, s43)
call(LUA_CREATETABLE, L, 0, 0)
call(LUA_SETFIELD, L, 0xffffd8ee & 0xffffffff, tmpstr('MC_MAX_DISTANCE'))  # -10002
print('global MC_MAX_DISTANCE set to empty table')

CHUNKS = [
    'return 5 * 5',
    'return 5 * MC_MAX_DISTANCE',
    'return 5 * NEVER_SET_GLOBAL',
    'return 5 * 5.5',
    'return MC_MAX_DISTANCE ~= nil and "table" or "other"',
]
results = {}
for src in CHUNKS:
    ca = tmpstr(src)
    n_before = call(LUA_GETTOP, L)
    r = call(LUA_LOADSTRING, L, ca)
    n_after = call(LUA_GETTOP, L)
    status = 'loaded' if r == 0 else 'load-error'
    if r != 0:
        (v, tt), top = top_value(L)
        msg = cstr_read(v + 0x10).decode('ascii', 'replace') if tt == 4 else f'(tt={tt})'
        results[src] = {'status': 'load-failed', 'msg': msg}
        print(f'"{src}" -> LOAD FAILED: {msg}')
        call(LUA_SETTOP := LUA_SETTOP if False else LUA_GETTOP, L)  # no-op guard
        # pop the error: lua_settop(L, n_before) — need settop addr; use lua_setfield-free way:
        # lua_pop(L,1) == lua_settop(L,-2); find lua_settop: it is unnamed; use lua_replace?
        continue
    rc = call(LUA_PCALL, L, 0, 1, 0)
    if rc == 0:
        (v, tt), top = top_value(L)
        if tt == 3:
            f32 = struct.unpack('<f', struct.pack('<I', v))[0]
            results[src] = {'status': 'ok', 'type': 'number', 'value': f32}
            print(f'"{src}" -> OK number {f32}')
        elif tt == 4:
            s = cstr_read(v + 0x10).decode('ascii', 'replace')
            results[src] = {'status': 'ok', 'type': 'string', 'value': s}
            print(f'"{src}" -> OK string "{s}"')
        else:
            results[src] = {'status': 'ok', 'type': f'tt={tt}', 'value': v}
            print(f'"{src}" -> OK tt={tt} value={hex(v)}')
    else:
        (v, tt), top = top_value(L)
        msg = cstr_read(v + 0x10).decode('ascii', 'replace') if tt == 4 else f'(tt={tt} v={hex(v)})'
        results[src] = {'status': f'pcall-rc={rc}', 'msg': msg}
        print(f'"{src}" -> PCALL ERROR rc={rc}: {msg}')
        # drop the error object: reset top via lua_settop? emulate pop by writing top directly
        topaddr = L + 8
        # find lua_settop by trying lua_gettop-1 slot decrease: write top = top - 8
        t = struct.unpack('<I', bytes(uc.mem_read(topaddr, 4)))[0]
        uc.mem_write(topaddr, struct.pack('<I', t - 8))

import json
json.dump({'results': results, 'hook_log_tail': log[-20:]},
          open('/home/z/my-project/scripts/s44_t1_drive_result.json', 'w'), indent=1)
print('saved s44_t1_drive_result.json')
