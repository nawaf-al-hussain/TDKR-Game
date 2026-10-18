#!/usr/bin/env python3
"""S36 T1: run CNavMeshNova::Create @0x1d17cc under Unicorn on the real .nm.

Emulates: engine readers (native), operator new/delete family (bump),
GetDevice->filesystem (fake: size+read of the .nm), CLevel::GetLevel (fake),
allocProcessBuffer, MPool::New, snprintf, memcpy/memset.
Dumps: nova fields, soup pool, 16-B cells, grid object; reader cursor log.
"""
import struct, sys, json
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session25')
from emu_services import Services
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP)

SO_PATH = '/tmp/my-project/work/re29/libKRHP.so'
SO = open(SO_PATH, 'rb').read()

MAGIC = 0x10000000
STACK = 0x20000000
HEAP = 0x30000000
BUF = 0x08000000          # .nm image
FAKE = 0x60000000         # fake objects region (device/factory/file/level/vtables)
RET_MAGIC = MAGIC + 0x3F0

READERS = {
    0x3395D8: 'ReadChar', 0x3396EC: 'Read_ucharref', 0x339758: 'ReadShort',
    0x339868: 'Read_ushortref', 0x339914: 'ReadInt', 0x339AB4: 'Read_uintref',
    0x339B94: 'ReadFloat', 0x339C58: 'Read_floatref',
    0x33B3D0: 'Read_vector3d', 0x33B4DC: 'Read_vector2d',
}
NEW_FUNCS = {0x3E91F8, 0x3E9204, 0x3E9208, 0x3E9214, 0x3E9290, 0x3E9324}
DEL_FUNCS = {0x3E9260, 0x3E9278, 0x3E935C, 0x3E9350}

class Emu:
    def __init__(self, verbose=False):
        self.mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        try:
            from unicorn import UC_CPU_ARM_CORTEX_A15
            self.mu.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A15)
        except Exception:
            pass
        try:
            from unicorn.arm_const import UC_ARM_REG_C1_C0_2, UC_ARM_REG_FPEXC
            c1 = self.mu.reg_read(UC_ARM_REG_C1_C0_2)
            self.mu.reg_write(UC_ARM_REG_C1_C0_2, c1 | (0xF << 20))
            self.mu.reg_write(UC_ARM_REG_FPEXC, 0x40000000)
        except Exception:
            pass
        self.verbose = verbose
        self.logs = []
        self.events = []
        self.heap_ptr = HEAP + 0x1000
        self.stream_obj = None
        self._map_so()
        self._map_env()
        self._install_hooks()

    # ----- setup -----
    def _map_so(self):
        mu = self.mu
        e_phoff = struct.unpack_from('<I', SO, 0x1C)[0]
        e_phentsize = struct.unpack_from('<H', SO, 0x2A)[0]
        e_phnum = struct.unpack_from('<H', SO, 0x2C)[0]
        for i in range(e_phnum):
            off = e_phoff + i * e_phentsize
            p_type, p_offset, p_vaddr, _pa, p_filesz, p_memsz, _fl, _al = \
                struct.unpack_from('<8I', SO, off)
            if p_type != 1:
                continue
            base = p_vaddr & ~0xFFF
            end = (p_vaddr + p_memsz + 0xFFF) & ~0xFFF
            try:
                mu.mem_map(base, end - base)
            except UcError:
                pass
            mu.mem_write(p_vaddr, SO[p_offset:p_offset + p_filesz])

    def _map_env(self):
        mu = self.mu
        mu.mem_map(MAGIC, 0x1000)
        mu.mem_map(STACK, 0x200000)
        mu.mem_map(HEAP, 0x8000000)      # 128 MB (soup+cells+grid ~5 MB + slack)
        mu.mem_map(BUF, 0x200000)        # 2 MB .nm window
        mu.mem_map(FAKE, 0x10000)
        mu.mem_map(0xFFF00000, 0x100000)
        mu.mem_write(8, b'\x00' * 16)
        self.svc = Services(mu, SO, self._bump, self._svc_log)
        try:
            self.svc.install_math()
        except Exception:
            pass
        self._build_fakes()

    def _bump(self, n):
        p = self.heap_ptr
        self.heap_ptr = (self.heap_ptr + max(int(n), 1) + 0x1F) & ~0xF
        return p

    def _svc_log(self, msg):
        self.logs.append(str(msg))

    def _build_fakes(self):
        mu = self.mu
        F = FAKE
        # fake level object: +0xc = COW string {p,len,cap}
        self.FAKE_LEVEL = F + 0x100
        name = b'GothamCity_502299\x00'
        name_p = F + 0x400
        mu.mem_write(name_p - 8, b'\x00' * 8)
        mu.mem_write(name_p - 4, struct.pack('<i', 0x7FFFFFFF))  # refcount
        mu.mem_write(name_p, name)
        mu.mem_write(self.FAKE_LEVEL + 0xc, struct.pack('<III', name_p, 17, 0x4000))
        # device -> factory(+0) -> subobj(+0x28) -> subVtable(+0) -> create(+0xc)
        self.FAKE_DEVICE = F + 0x200
        self.FAKE_FACTORY = F + 0x240
        self.FAKE_SUBOBJ = F + 0x280
        self.FAKE_SUBVT = F + 0x2C0
        self.FAKE_FILE = F + 0x300
        self.FAKE_FILEVT = F + 0x340
        TR_CREATE = F + 0x400
        TR_SIZE = F + 0x420
        TR_READ = F + 0x440
        mu.mem_write(self.FAKE_DEVICE + 0, struct.pack('<I', self.FAKE_FACTORY))
        mu.mem_write(self.FAKE_FACTORY + 0x28, struct.pack('<I', self.FAKE_SUBOBJ))
        mu.mem_write(self.FAKE_SUBOBJ + 0, struct.pack('<I', self.FAKE_SUBVT))
        mu.mem_write(self.FAKE_SUBVT + 0xc, struct.pack('<I', TR_CREATE))
        mu.mem_write(self.FAKE_FILE + 0, struct.pack('<I', self.FAKE_FILEVT))
        mu.mem_write(self.FAKE_FILEVT + 0x20, struct.pack('<I', TR_SIZE))
        mu.mem_write(self.FAKE_FILEVT + 0xc, struct.pack('<I', TR_READ))
        for a in (TR_CREATE, TR_SIZE, TR_READ):
            mu.mem_write(a, b'\x00' * 8)  # won't execute; hooked before

    def load_nm(self, data):
        self.nm = data
        self.mu.mem_write(BUF, data)
        self.nm_buf = BUF

    # ----- hooks -----
    def _h_reader(self, mu, address, size, ud):
        r0 = mu.reg_read(UC_ARM_REG_R0)
        try:
            cur = struct.unpack('<I', mu.mem_read(r0 + 0xC, 4))[0]
        except UcError:
            cur = 0xFFFFFFFF
        self.events.append((READERS.get(address, hex(address)), cur))

    def _h_new(self, mu, address, size, ud):
        n = mu.reg_read(UC_ARM_REG_R0)
        p = self._bump(n)
        mu.mem_write(p, b'\x00' * min(n, 0x100000))
        mu.reg_write(UC_ARM_REG_R0, p)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_glitchalloc(self, mu, address, size, ud):
        n = mu.reg_read(UC_ARM_REG_R1)
        p = self._bump(n)
        mu.reg_write(UC_ARM_REG_R0, p)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_del(self, mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_memcpy(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R0); src = mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        if n:
            mu.mem_write(dst, bytes(mu.mem_read(src, n)))
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_memset(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R0); val = mu.reg_read(UC_ARM_REG_R1) & 0xFF
        n = mu.reg_read(UC_ARM_REG_R2)
        if n:
            mu.mem_write(dst, bytes([val]) * n)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_getdevice(self, mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_R0, self.FAKE_DEVICE)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_getlevel(self, mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_R0, self.FAKE_LEVEL)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_allocproc(self, mu, address, size, ud):
        n = mu.reg_read(UC_ARM_REG_R0)
        p = self._bump(n)
        mu.mem_write(p, b'\x00' * min(n, 0x1000))
        mu.reg_write(UC_ARM_REG_R0, p)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_mpool(self, mu, address, size, ud):
        n = mu.reg_read(UC_ARM_REG_R1)
        p = self._bump(n)
        mu.mem_write(p, b'\x00' * min(n, 0x10000))
        mu.reg_write(UC_ARM_REG_R0, p)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_snprintf(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R0)
        n = mu.reg_read(UC_ARM_REG_R1)
        v = mu.reg_read(UC_ARM_REG_R3)
        s = str(v & 0xFFFFFFFF).encode()[:max(n - 1, 0)]
        mu.mem_write(dst, s + b'\x00')
        mu.reg_write(UC_ARM_REG_R0, len(s))
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_mstreamctor(self, mu, address, size, ud):
        self.stream_obj = mu.reg_read(UC_ARM_REG_R0)
        self.logs.append(f'CMemoryStream ctor this=0x{self.stream_obj:x}')
        # let it run natively

    # fake filesystem trampolines (hooked by address, never executed)
    def _h_tr_create(self, mu, address, size, ud):
        out = mu.reg_read(UC_ARM_REG_R0)
        mu.mem_write(out, struct.pack('<I', self.FAKE_FILE))
        mu.reg_write(UC_ARM_REG_R0, 0)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_tr_size(self, mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_R0, len(self.nm))
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _h_tr_read(self, mu, address, size, ud):
        dst = mu.reg_read(UC_ARM_REG_R1)
        if not dst:
            dst = mu.reg_read(UC_ARM_REG_R0)
        mu.mem_write(dst, self.nm)
        self.logs.append(f'file read -> 0x{dst:x} ({len(self.nm)} B)')
        self.file_buf = dst
        mu.reg_write(UC_ARM_REG_R0, len(self.nm))
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _install_hooks(self):
        mu = self.mu
        for a in READERS:
            mu.hook_add(UC_HOOK_CODE, self._h_reader, begin=a, end=a)
        for a in NEW_FUNCS:
            mu.hook_add(UC_HOOK_CODE, self._h_new, begin=a, end=a)
        mu.hook_add(UC_HOOK_CODE, self._h_glitchalloc, begin=0x3E9324, end=0x3E9324)
        for a in DEL_FUNCS:
            mu.hook_add(UC_HOOK_CODE, self._h_del, begin=a, end=a)
        mu.hook_add(UC_HOOK_CODE, self._h_memcpy, begin=0xA4E1C, end=0xA4E1C)
        mu.hook_add(UC_HOOK_CODE, self._h_memset, begin=0xA4E88, end=0xA4E88)
        mu.hook_add(UC_HOOK_CODE, self._h_getdevice, begin=0x3E91E4, end=0x3E91E4)
        mu.hook_add(UC_HOOK_CODE, self._h_getlevel, begin=0x478E24, end=0x478E24)
        mu.hook_add(UC_HOOK_CODE, self._h_allocproc, begin=0x935850, end=0x935850)
        mu.hook_add(UC_HOOK_CODE, self._h_mpool, begin=0x3E8A10, end=0x3E8A10)
        mu.hook_add(UC_HOOK_CODE, self._h_snprintf, begin=0xA5398, end=0xA5398)
        mu.hook_add(UC_HOOK_CODE, self._h_mstreamctor, begin=0x339238, end=0x339238)
        F = FAKE
        mu.hook_add(UC_HOOK_CODE, self._h_tr_create, begin=F + 0x400, end=F + 0x400)
        mu.hook_add(UC_HOOK_CODE, self._h_tr_size, begin=F + 0x420, end=F + 0x420)
        mu.hook_add(UC_HOOK_CODE, self._h_tr_read, begin=F + 0x440, end=F + 0x440)
        mu.hook_add(UC_HOOK_CODE, self._h_ret, begin=RET_MAGIC, end=RET_MAGIC)

    def _h_ret(self, mu, address, size, ud):
        mu.emu_stop()

    # ----- run -----
    def run_create(self):
        mu = self.mu
        nova = self._bump(0x100)
        self.nova = nova
        mu.mem_write(nova, b'\x00' * 0x100)
        mu.reg_write(UC_ARM_REG_SP, STACK + 0x180000)
        mu.reg_write(UC_ARM_REG_LR, RET_MAGIC)
        mu.reg_write(UC_ARM_REG_R0, nova)
        mu.reg_write(UC_ARM_REG_R1, 0)  # stream arg set below
        # build outer CMemoryStream-like object: {+0=buf,+0xc=0} at MAGIC+0x80
        outer = MAGIC + 0x80
        mu.mem_write(outer, struct.pack('<II', self.nm_buf, 0))
        mu.reg_write(UC_ARM_REG_R1, outer)
        try:
            mu.emu_start(0x1D17CC, RET_MAGIC, count=80_000_000)
            return 'OK'
        except UcError as e:
            pc = mu.reg_read(UC_ARM_REG_PC)
            return f'UCERR {e} pc=0x{pc:08x}'

    # ----- dump -----
    def dump(self):
        mu = self.mu
        nova = self.nova
        f = {}
        for off, name in ((0, 'f00_size'), (4, 'f04'), (8, 'f08_vcount'),
                          (0xc, 'f0c_ccount'), (0x10, 'f10_X'), (0x14, 'f14_soup'),
                          (0x18, 'f18_cells'), (0x1c, 'f1c_Y'), (0x20, 'f20'),
                          (0x24, 'f24'), (0x28, 'f28'), (0x2c, 'f2c'), (0x64, 'f64_grid')):
            f[name] = struct.unpack('<I', mu.mem_read(nova + off, 4))[0]
        return f


def main():
    nm_path = sys.argv[1] if len(sys.argv) > 1 else \
        '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'
    nm = open(nm_path, 'rb').read()
    emu = Emu()
    emu.load_nm(nm)
    status = emu.run_create()
    print('status:', status)
    print('stream_obj:', hex(emu.stream_obj or 0))
    f = emu.dump()
    print('nova fields:', json.dumps({k: (hex(v) if k.endswith(('soup', 'cells', 'grid')) else v) for k, v in f.items()}))
    mu = emu.mu
    if emu.stream_obj:
        cur = struct.unpack('<I', mu.mem_read(emu.stream_obj + 0xC, 4))[0]
        print(f'FINAL SUB-STREAM CURSOR = {cur} / file {len(nm)}  ({"BYTE-EXACT" if cur == len(nm) else "MISMATCH"})')
    # reader census
    from collections import Counter
    c = Counter(e[0] for e in emu.events)
    print('reader census:', dict(c))
    # first/last few events
    print('first reads:', emu.events[:8])
    print('last reads:', emu.events[-4:])
    json.dump({'status': status, 'fields': f, 'census': dict(c),
               'n_events': len(emu.events)},
              open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_trace.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
