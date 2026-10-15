#!/usr/bin/env python3
"""Engine service layer for the Unicorn tracer: fills every JUMP_SLOT GOT
entry with a Python trampoline and implements the libc subset the lvc Load
paths actually use. Data relocations (R_ARM_GLOB_DAT) get stub pages too.
"""
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR)

TRAMP = 0x50000000        # trampoline area (one page per import)
TRAMP_STRIDE = 0x1000
GUARD = 0x51000000        # __stack_chk_guard value page
SCRATCH = 0x52000000      # errno / misc data pages

# ARM EABI: args r0-r3, float args in s0-s15 (we only see r0-r3; floats
# arrive as bit patterns in r0/r1 for our purposes).
import math


def _f(r):
    return struct.unpack('<f', struct.pack('<I', r & 0xFFFFFFFF))[0]


def _d(lo, hi):
    return struct.unpack('<d', struct.pack('<II', lo, hi))[0]


class Services:
    """Install libc-subset services for an emulated libKRHP.so."""

    def __init__(self, mu, so, bump, log):
        self.mu = mu
        self.so = so
        self.bump = bump          # callable n -> ptr
        self.log = log            # callable str -> None
        self.fired = {}
        self._parse_and_install()

    # ---------- ELF parsing ----------
    def _sections(self):
        f = self.so
        e_shoff = struct.unpack_from('<I', f, 0x20)[0]
        e_shentsize = struct.unpack_from('<H', f, 0x2E)[0]
        e_shnum = struct.unpack_from('<H', f, 0x30)[0]
        e_shstrndx = struct.unpack_from('<H', f, 0x32)[0]
        secs = []
        for i in range(e_shnum):
            off = e_shoff + i * e_shentsize
            nm, typ, flags, addr, offset, size, link, info, align, entsize = \
                struct.unpack_from('<10I', f, off)
            secs.append(dict(name=nm, typ=typ, addr=addr, offset=offset,
                             size=size, link=link, entsize=entsize))
        shstr = secs[e_shstrndx]
        for s in secs:
            s['nm'] = self._cstr(shstr['offset'], s['name'])
        return secs

    def _cstr(self, base, n):
        e = self.so.index(b'\0', base + n)
        return self.so[base + n:e].decode()

    # ---------- install ----------
    def _parse_and_install(self):
        f = self.so
        mu = self.mu
        secs = self._sections()
        dynsym = next(s for s in secs if s['nm'] == '.dynsym')
        dynstr = next(s for s in secs if s['nm'] == '.dynstr')
        self.symname = {}
        self.undef = set()
        n = dynsym['size'] // 16
        for j in range(n):
            off = dynsym['offset'] + j * 16
            nm, val, sz, info, other, shndx = struct.unpack_from(
                '<IIIBBH', f, off)
            if nm:
                self.symname[j] = self._cstr(dynstr['offset'], nm)
                if shndx == 0:
                    self.undef.add(j)
        # map regions
        nimp = 4096
        mu.mem_map(TRAMP, nimp * TRAMP_STRIDE)
        mu.mem_map(GUARD, 0x1000)
        mu.mem_map(SCRATCH, 0x10000)
        mu.mem_write(GUARD, struct.pack('<I', 0x5AFE00BA))
        # .got.plt-style JUMP_SLOTs from .rel.plt
        self.tramp_of = {}
        idx = 0
        for rn in ('.rel.plt', '.rel.dyn'):
            try:
                rel = next(s for s in secs if s['nm'] == rn)
            except StopIteration:
                continue
            cnt = rel['size'] // 8
            for j in range(cnt):
                off, info = struct.unpack_from('<II', f, rel['offset'] + j * 8)
                rtype = info & 0xFF
                symi = info >> 8
                name = self.symname.get(symi)
                if rtype == 22:            # R_ARM_JUMP_SLOT (always import)
                    t = TRAMP + idx * TRAMP_STRIDE
                    mu.mem_write(off, struct.pack('<I', t))
                    self.tramp_of[t] = name
                    idx += 1
                elif rtype == 21 and symi in self.undef:
                    # R_ARM_GLOB_DAT for UNDEFINED imports only — internal
                    # (defined) GLOB_DATs already hold correct vaddrs.
                    t = TRAMP + idx * TRAMP_STRIDE
                    mu.mem_write(off, struct.pack('<I', t))
                    self.tramp_of[t] = 'DATA:' + (name or '?')
                    idx += 1
        self.count = idx
        # hooks: one per trampoline would be 4000 hooks; instead one hook
        # over the TRAMP range with dict lookup (fires once per call).
        mu.hook_add(UC_HOOK_CODE, self._dispatch, begin=TRAMP,
                    end=TRAMP + nimp * TRAMP_STRIDE)

    # ---------- dispatch ----------
    def _dispatch(self, mu, address, size, ud):
        name = self.tramp_of.get(address)
        if name is None:
            return
        self.fired[name] = self.fired.get(name, 0) + 1
        h = getattr(self, 'h_' + name.lstrip('_').replace('.', '_'), None)
        if h is None:
            h = self.HANDLERS.get(name)
        if h is None:
            self.log(f'UNIMPLEMENTED import: {name}')
            mu.reg_write(UC_ARM_REG_R0, 0)
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
            return
        h(mu)

    def ret(self, mu, val):
        mu.reg_write(UC_ARM_REG_R0, val & 0xFFFFFFFF)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    # ---------- handlers ----------
    def h_malloc(self, mu):
        self.ret(mu, self.bump(mu.reg_read(UC_ARM_REG_R0)))

    def h_calloc(self, mu):
        n = mu.reg_read(UC_ARM_REG_R0) * mu.reg_read(UC_ARM_REG_R1)
        p = self.bump(n)
        if n:
            self.mu.mem_write(p, b'\x00' * min(n, 0x100000))
        self.ret(mu, p)

    def h_realloc(self, mu):
        # leak-and-copy heuristic: copy old contents heuristically 256B
        old = mu.reg_read(UC_ARM_REG_R0)
        n = mu.reg_read(UC_ARM_REG_R1)
        p = self.bump(n)
        if old and n:
            try:
                oldb = bytes(self.mu.mem_read(old, min(n, 0x10000)))
                self.mu.mem_write(p, oldb)
            except Exception:
                pass
        self.ret(mu, p)

    def h_free(self, mu):
        self.ret(mu, 0)

    def h_memalign(self, mu):
        al = max(mu.reg_read(UC_ARM_REG_R0), 16)
        n = mu.reg_read(UC_ARM_REG_R1)
        p = self.bump(n + al)
        p = (p + al - 1) & ~(al - 1)
        self.ret(mu, p)

    h_valloc = h_memalign

    def h_memcpy(self, mu):
        dst, src, n = (mu.reg_read(r) for r in
                       (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        if n:
            try:
                self.mu.mem_write(dst, bytes(self.mu.mem_read(src, n)))
            except Exception as e:
                self.log(f'memcpy fault dst={dst:#x} src={src:#x} n={n}: {e}')
        self.ret(mu, dst)

    h_memmove = h_memcpy

    def h_memset(self, mu):
        dst, v, n = (mu.reg_read(r) for r in
                     (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        if n:
            if n > 0x100000:
                self.log(f'memset n={n:#x} dst={dst:#x} SUSPICIOUS — clamped')
                n = min(n, 0x100000)
            self.mu.mem_write(dst, bytes([v & 0xFF]) * n)
        self.ret(mu, dst)

    def h_memcmp(self, mu):
        a, b, n = (mu.reg_read(r) for r in
                   (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        x = bytes(self.mu.mem_read(a, n)) if n else b''
        y = bytes(self.mu.mem_read(b, n)) if n else b''
        self.ret(mu, 0 if x == y else (1 if x > y else 0xFFFFFFFF))

    def h_memchr(self, mu):
        s, c, n = (mu.reg_read(r) for r in
                   (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        blk = bytes(self.mu.mem_read(s, n)) if n else b''
        i = blk.find(bytes([c & 0xFF]))
        self.ret(mu, s + i if i >= 0 else 0)

    def h_strlen(self, mu):
        s = mu.reg_read(UC_ARM_REG_R0)
        n = 0
        while bytes(self.mu.mem_read(s + n, 1)) != b'\x00' and n < 0x100000:
            n += 1
        self.ret(mu, n)

    def h_strcmp(self, mu):
        a, b = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        self.ret(mu, self._strcmp_impl(a, b, False))

    def h_strncmp(self, mu):
        a, b = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        self.ret(mu, self._strcmp_impl(a, b, False, n))

    def h_strcasecmp(self, mu):
        a, b = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        self.ret(mu, self._strcmp_impl(a, b, True))

    def h_strncasecmp(self, mu):
        a, b = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        self.ret(mu, self._strcmp_impl(a, b, True, n))

    def _strcmp_impl(self, a, b, ci, n=0x100000):
        x = self._cbytes(a, n)
        y = self._cbytes(b, n)
        if ci:
            x = x.lower()
            y = y.lower()
        m = min(len(x), len(y))
        if n:
            m = min(m, n)
            x, y = x[:n], y[:n]
        if x == y:
            return 0
        return 1 if x[:m] > y[:m] else 0xFFFFFFFF

    def _cbytes(self, s, maxn):
        out = bytearray()
        step = 64
        while len(out) < maxn:
            blk = bytes(self.mu.mem_read(s + len(out), step))
            if b'\x00' in blk:
                out += blk[:blk.index(b'\x00')]
                break
            out += blk
        return bytes(out[:maxn])

    def h_strcpy(self, mu):
        dst, src = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        data = self._cbytes(src, 0x100000)
        self.mu.mem_write(dst, data + b'\x00')
        self.ret(mu, dst)

    def h_strncpy(self, mu):
        dst, src, n = (mu.reg_read(r) for r in
                       (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        data = self._cbytes(src, n)
        data = data + b'\x00' * (n - len(data))
        self.mu.mem_write(dst, data)
        self.ret(mu, dst)

    def h_strcat(self, mu):
        dst, src = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        base = self._cbytes(dst, 0x100000)
        add = self._cbytes(src, 0x100000)
        self.mu.mem_write(dst + len(base), add + b'\x00')
        self.ret(mu, dst)

    def h_strchr(self, mu):
        s, c = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1) & 0xFF
        data = self._cbytes(s, 0x100000)
        i = data.find(bytes([c]))
        self.ret(mu, s + i if i >= 0 else 0)

    def h_strrchr(self, mu):
        s, c = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1) & 0xFF
        data = self._cbytes(s, 0x100000)
        i = data.rfind(bytes([c]))
        self.ret(mu, s + i if i >= 0 else 0)

    def h_strstr(self, mu):
        a, b = mu.reg_read(UC_ARM_REG_R0), mu.reg_read(UC_ARM_REG_R1)
        x = self._cbytes(a, 0x100000)
        y = self._cbytes(b, 0x10000)
        i = x.find(y)
        self.ret(mu, a + i if i >= 0 else 0)

    def h_strdup(self, mu):
        s = mu.reg_read(UC_ARM_REG_R0)
        data = self._cbytes(s, 0x100000)
        p = self.bump(len(data) + 1)
        self.mu.mem_write(p, data + b'\x00')
        self.ret(mu, p)

    def h_strtoul(self, mu):
        s = mu.reg_read(UC_ARM_REG_R0)
        data = self._cbytes(s, 64)
        try:
            v = int(data.split(b'\x00')[0].strip() or b'0', 0)
        except ValueError:
            v = 0
        self.ret(mu, v)

    def h_atoi(self, mu):
        s = mu.reg_read(UC_ARM_REG_R0)
        data = self._cbytes(s, 32)
        try:
            v = int(data.split(b'\x00')[0].strip() or b'0')
        except ValueError:
            v = 0
        self.ret(mu, v & 0xFFFFFFFF)

    h_atol = h_atoi

    # __cxa_atexit / atexit
    def h_cxa_atexit(self, mu):
        self.ret(mu, 0)

    h_atexit = h_cxa_atexit

    def h_cxa_guard_acquire(self, mu):
        # claim the guard so the engine's static init runs natively once
        g = mu.reg_read(UC_ARM_REG_R0)
        cur = struct.unpack('<I', bytes(
            self.mu.mem_read(g, 4)))[0] if g else 0
        if cur & 1:
            self.ret(mu, 0)
        else:
            self.ret(mu, 1)

    def h_cxa_guard_release(self, mu):
        g = mu.reg_read(UC_ARM_REG_R0)
        if g:
            self.mu.mem_write(g, struct.pack('<I', 1))
        self.ret(mu, 0)

    h_cxa_guard_abort = h_cxa_atexit

    def h_stack_chk_fail(self, mu):
        self.log('__stack_chk_fail HIT — aborting emulation')
        mu.emu_stop()

    def h_abort(self, mu):
        self.log('abort() HIT — aborting emulation')
        mu.emu_stop()

    def h_assert2(self, mu):
        self.log('__assert2 HIT — aborting emulation')
        mu.emu_stop()

    def h_errno(self, mu):
        self.ret(mu, SCRATCH)   # pointer to zeroed int

    def h_getenv(self, mu):
        self.ret(mu, 0)

    h_getpid = lambda self, mu: self.ret(mu, 1234)
    h_clock = lambda self, mu: self.ret(mu, 0)
    h_time = lambda self, mu: self.ret(mu, 0)
    h_gettimeofday = lambda self, mu: self.ret(mu, 0)

    # ---- pthread TLS family: static zeroed TLS page ----
    def h_pthread_key_create(self, mu):
        # r0 = key* out; store an index
        k = mu.reg_read(UC_ARM_REG_R0)
        self._tls_keys = getattr(self, '_tls_keys', 1) + 1
        self.mu.mem_write(k, struct.pack('<I', self._tls_keys))
        self.ret(mu, 0)

    def h_pthread_getspecific(self, mu):
        key = mu.reg_read(UC_ARM_REG_R0)
        # TLS page: 256 slots of 4 B, zeroed (setspecific may store)
        self.ret(mu, SCRATCH + 0x1000 + (key % 256) * 4)

    def h_pthread_setspecific(self, mu):
        key = mu.reg_read(UC_ARM_REG_R0)
        v = mu.reg_read(UC_ARM_REG_R1)
        self.mu.mem_write(SCRATCH + 0x1000 + (key % 256) * 4,
                          struct.pack('<I', v))
        self.ret(mu, 0)

    h_pthread_key_delete = lambda self, mu: self.ret(mu, 0)
    h_pthread_self = lambda self, mu: self.ret(mu, 0x1234)
    h_pthread_mutex_lock = lambda self, mu: self.ret(mu, 0)
    h_pthread_mutex_unlock = lambda self, mu: self.ret(mu, 0)
    h_pthread_mutex_init = lambda self, mu: self.ret(mu, 0)
    h_pthread_mutex_destroy = lambda self, mu: self.ret(mu, 0)
    h_pthread_once = lambda self, mu: self.ret(mu, 0)

    # ---- math (args may be in r0 or s0; we read r0/r1 as float bits) ----
    def _math1(self, fn):
        def h(mu):
            x = _f(mu.reg_read(UC_ARM_REG_R0))
            try:
                self.ret(mu, struct.unpack('<I', struct.pack(
                    '<f', fn(x)))[0])
            except Exception:
                self.ret(mu, 0)
        return h

    def _math2(self, fn):
        def h(mu):
            x = _f(mu.reg_read(UC_ARM_REG_R0))
            y = _f(mu.reg_read(UC_ARM_REG_R1))
            try:
                self.ret(mu, struct.unpack('<I', struct.pack(
                    '<f', fn(x, y)))[0])
            except Exception:
                self.ret(mu, 0)
        return h

    def __init_subclass__(cls):
        pass

    def install_math(self):
        for name, fn in (('sin', math.sin), ('cos', math.cos),
                         ('tan', math.tan), ('asin', math.asin),
                         ('acos', math.acos), ('atan', math.atan),
                         ('sqrt', math.sqrt), ('exp', math.exp),
                         ('log', math.log), ('log10', math.log10),
                         ('floor', math.floor), ('ceil', math.ceil),
                         ('sinh', math.sinh), ('cosh', math.cosh),
                         ('tanh', math.tanh)):
            setattr(self, 'h_' + name, self._math1(fn))
        for name, fn in (('pow', math.pow), ('atan2', math.atan2),
                         ('fmod', math.fmod), ('ldexp', lambda x, y:
                                              math.ldexp(x, int(y)))):
            setattr(self, 'h_' + name, self._math2(fn))

    HANDLERS = {}
