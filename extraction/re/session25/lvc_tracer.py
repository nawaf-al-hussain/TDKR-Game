#!/usr/bin/env python3
"""Unicorn ARM tracer for libKRHP.so lvc parsing — engine-driven T1.

Runs the REAL engine reader/Load code over real record bytes:
- libKRHP.so mapped at its vaddrs (all relevant code is ARM mode).
- CMemoryStream fake object: buffer ptr @+0x0, cursor @+0xc (the native
  readers ReadInt/ReadFloat/ReadChar/ReadByte/ReadShort mutate [this+0xc]
  themselves — we let them run and only LOG the cursor at entry).
- Numeric readers run NATIVELY (ReadInt is big-endian by construction,
  verified @0x339914: orr r3, r3, r5, lsl #24 ...).
- ReadString* are HOOKED (implemented in Python): consume u32be index into
  the stream dictionary (DICT flag byte 0 => interned strings), write a
  COW-layout std::string {p,len,cap} with a huge refcount at p-4 so any
  destructor copy is a no-op, and log the interned value.
- GlitchAlloc/GlitchFree -> bump allocator / no-op. PLT memcpy/memset ->
  implemented. Unimplemented vtable slots -> MAGIC reporter returning 0.
- GenerateComponentTemplate(int typeId, CMemoryStream*) @0x368ac0 for
  factory-miss component classes; per-class Load(this, stream) otherwise.

Tracing: entry-only code hooks on each reader record (reader_id, cursor).
Post-run, per-call byte consumption = cursor deltas; values decoded from
the record buffer with per-reader semantics.
"""
import struct
import json
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP)
from emu_services import Services

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'

MAGIC = 0x10000000          # trampolines / fake objects (4 KB)
STACK = 0x20000000          # 2 MB
HEAP = 0x30000000           # 64 MB bump heap
BUF = 0x08000000            # lvc file image (16 MB window)
STREAM = MAGIC + 0x40       # fake CMemoryStream object (64 B)
VT = MAGIC + 0x80           # fake component vtable
DICTV = 0x40000000          # dictionary vector region
DICTS = 0x41000000          # dictionary std::string objects
STRS = 0x48000000           # dictionary char data (+ refcount header)
COMP_REG = 0x53000000       # static component object (4 KB, zeroed per alloc)
RET_MAGIC = MAGIC + 0x3F0   # fake return address
VT_MAGIC_BASE = MAGIC + 0x200

GLITCH_ALLOC = 0x3E9324
GLITCH_FREE = 0x3E935C
PLT_MEMCPY = 0xA4E1C
PLT_MEMSET = 0xA4E88

READERS = {
    0x339510: 'ReadBool_ref',
    0x339574: 'Read_boolref',
    0x3395D8: 'ReadChar',
    0x339634: 'Read_charref',
    0x339690: 'ReadByte',
    0x3396EC: 'Read_ucharref',
    0x339758: 'ReadShort',
    0x3397DC: 'Read_shortref',
    0x339868: 'Read_ushortref',
    0x339914: 'ReadInt',
    0x3399D4: 'Read_intref',
    0x339AB4: 'Read_uintref',
    0x339B94: 'ReadFloat',
    0x339C58: 'Read_floatref',
    0x33A0D4: 'ReadString_ref',
    0x33AB94: 'ReadString',
    0x33AD74: 'ReadStringC_ref',
    0x33B01C: 'ReadStringW_ref',
    0x33B3D0: 'Read_vector3d',
    0x33B4DC: 'Read_vector2d',
    0x33B6AC: 'Read_vector4d',
    0x33BB10: 'ReadData_ptr',
    0x33BB40: 'ReadData_int',
}
NESTING_PARENTS = {0x33A0D4, 0x33AB94, 0x33AD74, 0x33B01C}
STR_READERS = {'ReadString_ref', 'ReadString', 'ReadStringC_ref',
               'ReadStringW_ref'}
# nested-reader folding: ReadString* call ReadInt internally; the parent
# event no longer exists (native run), so the nested ReadInt IS the STR read
# (4 B). decode_value resolves the index at census time.


def decode_value(name, buf, off, size):
    """Decode a reader's value from the record image (post-hoc)."""
    if name in STR_READERS:
        idx = struct.unpack_from('>i', buf, off)[0]
        return ('STR', idx)
    if name in ('ReadChar', 'Read_charref'):
        return ('c', struct.unpack_from('>b', buf, off)[0])
    if name in ('ReadByte', 'Read_ucharref', 'ReadBool_ref', 'Read_boolref'):
        return ('B', buf[off])
    if name in ('ReadShort', 'Read_shortref'):
        return ('s', struct.unpack_from('>h', buf, off)[0])
    if name == 'Read_ushortref':
        return ('S', struct.unpack_from('>H', buf, off)[0])
    if name in ('ReadInt', 'Read_intref'):
        return ('i', struct.unpack_from('>i', buf, off)[0])
    if name == 'Read_uintref':
        return ('I', struct.unpack_from('>I', buf, off)[0])
    if name in ('ReadFloat', 'Read_floatref'):
        return ('f', struct.unpack_from('>f', buf, off)[0])
    if name == 'Read_vector2d':
        return ('v2', struct.unpack_from('>2f', buf, off))
    if name == 'Read_vector3d':
        return ('v3', struct.unpack_from('>3f', buf, off))
    if name == 'Read_vector4d':
        return ('v4', struct.unpack_from('>4f', buf, off))
    if name in ('ReadData_ptr', 'ReadData_int'):
        return ('data', size)
    return (name, None)


class Trace:
    __slots__ = ('events',)

    def __init__(self):
        self.events = []

    def calls(self, final_cur, strings, lvc_buf):
        """Fold nesting, return [(reader, file_off, nbytes, value)]."""
        ev = self.events
        out = []
        i, n = 0, len(ev)
        while i < n:
            addr, cur = ev[i]
            name = READERS[addr]
            if addr in NESTING_PARENTS:
                if i + 1 < n and ev[i + 1][1] == cur and \
                        ev[i + 1][0] == 0x339914:
                    i += 1  # nested ReadInt inside ReadString
                if i + 1 < n:
                    size = ev[i + 1][1] - cur
                else:
                    size = final_cur - cur
                idx = struct.unpack_from('>i', lvc_buf, cur)[0]
                val = strings[idx] if 0 <= idx < len(strings) else ''
                out.append((name, cur, size, ('STR', idx), val))
            else:
                if i + 1 < n:
                    size = ev[i + 1][1] - cur
                else:
                    size = final_cur - cur
                kind, val = decode_value(name, lvc_buf, cur, size)
                out.append((name, cur, size, (kind, val), None))
            i += 1
        return out


class Tracer:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.so = open(SO, 'rb').read()
        syms = json.load(open(SYMS))
        self.by_name = {k: int(v, 16) for k, v in syms['by_name'].items()}
        self.mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        # enable VFP/NEON (Cortex-A15 model: cp10/cp11 accessible)
        try:
            from unicorn import UC_CPU_ARM_CORTEX_A15
            self.mu.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A15)
        except Exception:
            pass
        try:
            from unicorn.arm_const import UC_ARM_REG_C1_C0_2, UC_ARM_REG_FPEXC
            c1 = self.mu.reg_read(UC_ARM_REG_C1_C0_2)
            self.mu.reg_write(UC_ARM_REG_C1_C0_2, c1 | (0xF << 20))
            self.mu.reg_write(UC_ARM_REG_FPEXC, 0x40000000)   # FPEXC.EN
        except Exception:
            pass
        self.trace = Trace()
        self.logs = []
        self.heap_ptr = HEAP
        self.str_area = STRS + 0x100
        self.benign_fault = None
        self._sorted_fn_addrs = None
        self._map_so()
        self._map_env()
        self._install_hooks()

    def _map_so(self):
        mu = self.mu
        so = self.so
        e_phoff = struct.unpack_from('<I', so, 0x1C)[0]
        e_phentsize = struct.unpack_from('<H', so, 0x2A)[0]
        e_phnum = struct.unpack_from('<H', so, 0x2C)[0]
        for i in range(e_phnum):
            off = e_phoff + i * e_phentsize
            p_type, p_offset, p_vaddr, _pa, p_filesz, p_memsz, _fl, _al = \
                struct.unpack_from('<8I', so, off)
            if p_type != 1:
                continue
            base = p_vaddr & ~0xFFF
            end = (p_vaddr + p_memsz + 0xFFF) & ~0xFFF
            try:
                mu.mem_map(base, end - base)
            except UcError:
                pass
            mu.mem_write(p_vaddr, so[p_offset:p_offset + p_filesz])

    def _map_env(self):
        mu = self.mu
        mu.mem_map(MAGIC, 0x1000)
        mu.mem_map(STACK, 0x200000)
        mu.mem_map(HEAP, 0x4000000)
        mu.mem_map(BUF, 0x1000000)
        mu.mem_map(DICTV, 0x100000)
        mu.mem_map(DICTS, 0x800000)
        mu.mem_map(STRS, 0x1000000)
        mu.mem_map(COMP_REG, 0x1000)
        # null-string refcount underflow guard: COW release computes p-4;
        # for zero-initialized strings p=0 -> 0xFFFFFFFC. Map the top 1 MB
        # so those decrements land on writable zeros instead of faults.
        mu.mem_map(0xFFF00000, 0x100000)
        # NULL-global guard: unresolved GOT slots read as 0; code that
        # derefs a NULL singleton then reads [0+off] lands on the ELF
        # header. Zero those words so list loops over NULL heads see
        # empty containers instead of garbage (e.g. CQuestManager list).
        mu.mem_write(8, b'\x00' * 16)
        mu.mem_write(STREAM, b'\x00' * 64)
        mu.mem_write(STREAM + 0x34, b'\x01')
        # component vtable: ALL slots -> reporters (Load is called directly,
        # never via the vtable; the vtable only serves incidental virtual
        # calls from inside Load wrappers)
        for slot in range(0, 16):
            mu.mem_write(VT + 4 * slot,
                         struct.pack('<I', VT_MAGIC_BASE + slot * 4))
        # fake owner/parent object: [PARENT] = VT — components carry a
        # constructor-set manager pointer at +4..+0x10 that post-Load code
        # virtually calls; give it a benign all-reporter vtable.
        self.PARENT = MAGIC + 0x380
        mu.mem_write(self.PARENT, struct.pack('<I', VT))
        # engine GlitchAlloc (internal wrapper, size in r1)
        self.mu.hook_add(UC_HOOK_CODE, self._on_alloc, begin=GLITCH_ALLOC,
                         end=GLITCH_ALLOC)
        # full libc-subset service layer (GOT fill + trampolines)
        self.svc = Services(mu, self.so, self._bump, self._svc_log)
        self.svc.install_math()

    def _bump(self, n):
        p = self.heap_ptr
        self.heap_ptr = (self.heap_ptr + max(int(n), 1) + 0x1F) & ~0xF
        return p

    def _svc_log(self, msg):
        self.logs.append(msg)
        if self.verbose:
            print('[svc]', msg)

    # ---------- hooks ----------
    def _on_reader(self, mu, address, size, ud):
        cur = struct.unpack('<I', mu.mem_read(STREAM + 0xC, 4))[0]
        self.trace.events.append((address, cur))
        if address in NESTING_PARENTS:
            self._in_str = True
        elif address == 0x339914 and self._in_str:
            self._in_str = False
            idx = struct.unpack_from('>i', self.lvc, cur)[0]
            if not (-1 <= idx < len(self.dict_strings)):
                self.str_violation = (cur, idx)
                self.logs.append(
                    f'STR-INDEX-OUT-OF-RANGE @{cur:#x} idx={idx}')

    def _on_ret(self, mu, address, size, ud):
        mu.emu_stop()

    def _on_vslot(self, mu, address, size, ud):
        slot = (address - VT_MAGIC_BASE) // 4
        self.logs.append(f'virtual slot {slot} called -> 0')
        mu.reg_write(UC_ARM_REG_R0, 0)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _on_alloc(self, mu, address, size, ud):
        n = mu.reg_read(UC_ARM_REG_R1)
        p = self.heap_ptr
        self.heap_ptr = (self.heap_ptr + max(n, 1) + 0x1F) & ~0xF
        mu.reg_write(UC_ARM_REG_R0, p)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _on_free(self, mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _on_memcpy(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R0)
        src = mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        if n:
            mu.mem_write(dst, bytes(mu.mem_read(src, n)))
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _on_memset(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R0)
        val = mu.reg_read(UC_ARM_REG_R1) & 0xFF
        n = mu.reg_read(UC_ARM_REG_R2)
        if n:
            mu.mem_write(dst, bytes([val]) * n)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _install_hooks(self):
        mu = self.mu
        # ReadString* run NATIVELY: the stream dictionary is real memory
        # (vector<string*> at STREAM+0x1c/0x20), bounds checks and the
        # engine's own string operator= operate on engine-ABI objects.
        # Only the __cxa_guard_* stubs (below) make the EMPTY_STRING static
        # init run natively.
        for a in READERS:
            mu.hook_add(UC_HOOK_CODE, self._on_reader, begin=a, end=a)
        mu.hook_add(UC_HOOK_CODE, self._on_ret, begin=RET_MAGIC,
                    end=RET_MAGIC)
        for slot in range(3, 16):
            a = VT_MAGIC_BASE + slot * 4
            mu.hook_add(UC_HOOK_CODE, self._on_vslot, begin=a, end=a)

    # ---------- setup / run ----------
    def load_lvc(self, data, strings):
        """Map the lvc image once and build the stream dictionary."""
        mu = self.mu
        assert len(data) <= 0x1000000
        mu.mem_write(BUF, data)
        mu.mem_write(STREAM + 0x0, struct.pack('<I', BUF))
        self.lvc = data
        self.dict_strings = strings
        ptrs = []
        a = self.str_area
        for s in strings:
            b = s.encode('utf-8') + b'\x00'
            mu.mem_write(a + 4, b)
            mu.mem_write(a, struct.pack('<i', 0x7FFFFFFF))
            obj = DICTS + 0x100 + 32 * len(ptrs)
            mu.mem_write(obj, struct.pack('<III', a + 4, len(s), len(s)))
            ptrs.append(obj)
            a += 4 + len(b) + 8
        self.str_area = a
        self.str_area_base = a
        vec = DICTV + 0x100
        for i, p in enumerate(ptrs):
            mu.mem_write(vec + 4 * i, struct.pack('<I', p))
        mu.mem_write(STREAM + 0x1C, struct.pack('<I', vec))
        self.dict_vec_end = vec + 4 * len(ptrs)
        mu.mem_write(STREAM + 0x20, struct.pack('<I', self.dict_vec_end))
        self.dict_str_ptrs = ptrs

    def set_cursor(self, off):
        self.mu.mem_write(STREAM + 0xC, struct.pack('<I', off))

    def get_cursor(self):
        return struct.unpack('<I',
                             self.mu.mem_read(STREAM + 0xC, 4))[0]

    def new_component(self):
        """Static zeroed component object (reused across runs; no heap)."""
        mu = self.mu
        mu.mem_write(COMP_REG, b'\x00' * 0x1000)
        mu.mem_write(COMP_REG, struct.pack('<I', VT))
        for off in (4, 8, 0xC, 0x10):
            mu.mem_write(COMP_REG + off, struct.pack('<I', self.PARENT))
        return COMP_REG

    def _restore_magic(self):
        """Rewrite the fake objects a previous Load may have scribbled on
        (components write through PARENT/VT pointers). Cursor untouched."""
        mu = self.mu
        for slot in range(0, 16):
            mu.mem_write(VT + 4 * slot,
                         struct.pack('<I', VT_MAGIC_BASE + slot * 4))
        mu.mem_write(self.PARENT, struct.pack('<I', VT))
        mu.mem_write(8, b'\x00' * 16)   # NULL-global scratch (see _map_env)
        mu.mem_write(STREAM + 0x0, struct.pack('<I', BUF))
        mu.mem_write(STREAM + 0x34, b'\x01')
        mu.mem_write(STREAM + 0x35, b'\x00')
        if getattr(self, 'dict_vec_end', None):
            mu.mem_write(STREAM + 0x1C, struct.pack('<I', DICTV + 0x100))
            mu.mem_write(STREAM + 0x20,
                         struct.pack('<I', self.dict_vec_end))

    def run(self, fn_addr, args, count=5_000_000):
        mu = self.mu
        self.trace = Trace()
        self.logs = []
        self.benign_fault = None
        self.str_violation = None
        self._in_str = False
        self.str_area = self.str_area_base
        # session 26: keep_heap survives allocations across runs (native
        # GOM map populate); heap_floor is the reset target (so data
        # allocated before the walk — e.g. the GOM rb-tree — stays intact).
        if not getattr(self, 'keep_heap', False):
            self.heap_ptr = getattr(self, 'heap_floor', HEAP)
        self._restore_magic()
        regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)
        for r in regs:
            mu.reg_write(r, 0)
        for r, v in zip(regs, args):
            mu.reg_write(r, v)
        mu.reg_write(UC_ARM_REG_SP, STACK + 0x180000)
        mu.reg_write(UC_ARM_REG_LR, RET_MAGIC)
        err = None
        try:
            mu.emu_start(fn_addr, RET_MAGIC, timeout=20_000_000, count=count)
        except UcError as e:
            pc = mu.reg_read(UC_ARM_REG_PC)
            if self._pc_in_fn(pc, fn_addr):
                err = f'{e} pc=0x{pc:x}'
            else:
                # fault in post-Load engine bookkeeping (scene-graph etc.) —
                # stream reads are complete; boundary check validates.
                err = None
                self.benign_fault = f'{e} pc=0x{pc:x}'
        return err

    def _pc_in_fn(self, pc, fn):
        """True if pc lies within the symbol function that starts at fn."""
        if pc == RET_MAGIC or pc >= MAGIC:
            return False
        addrs = self._sorted_fn_addrs
        if addrs is None:
            import bisect
            addrs = sorted(self.by_name.values())
            self._sorted_fn_addrs = addrs
        import bisect
        i = bisect.bisect_right(addrs, fn) - 1
        # find the end of fn's symbol run: next distinct symbol > fn
        j = i
        while j + 1 < len(addrs) and addrs[j + 1] == addrs[i]:
            j += 1
        fn_end = addrs[j + 1] if j + 1 < len(addrs) else fn + 0x8000
        i2 = bisect.bisect_right(addrs, pc) - 1
        return addrs[i2] == addrs[i] if i >= 0 and i2 >= 0 else False
