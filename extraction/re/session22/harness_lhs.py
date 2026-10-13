#!/usr/bin/env python3
"""Unicorn harness for glitch::io::loadHeadersAndSkipData @0x8e1d34 (ARM).

Runs the REAL engine function over every batch_info.bin record (file
positioned at record+32, since the caller reads the [u16 self][30 attr]
prefix itself), tracing:
  - every file->read() (offset, size) and file->seek() (delta)
  - every write into the CVertexStreams pair buffer (slot, value)
  - the resulting stream descriptor array and K = [+0xc]

Engine call: loadHeadersAndSkipData(arg0=CVertexStreamsHolder*,
arg1=SPrimitiveStreamDesc* whose [0]=IReadFile*, arg2=tailOut*, arg3=bigEndian)
File vtable slots used: +0xc read(buf, size), +0x18 seek(off, relative).

Hooks: GlitchAlloc -> bump allocator, GlitchFree -> no-op,
intrusive_ptr_add_ref/release -> no-op. Everything else runs natively.
"""
import json
import struct
import sys

from unicorn import *
from unicorn.arm_const import *

SO = "/home/z/my-project/repo/extraction/lib_libKRHP.so"
LHS = 0x8E1D34
MAGIC_PAGE = 0x10000000          # fake objects / magic trampolines
STACK_BASE = 0x20000000
HEAP_BASE = 0x30000000
GLITCH_ALLOC = 0x3E9324
GLITCH_FREE = 0x3E935C
ADD_REF = 0x3B27C8
REL_PTR = 0x1FD770
ALLOC_PS = 0x935850              # allocProcessBuffer
REL_PB = 0x9358DC                # releaseProcessBuffer
HOOK_PS = 0xA6EB58               # std list hook

VT_READ = MAGIC_PAGE + 0x200
VT_SEEK = MAGIC_PAGE + 0x240
PLT_MEMCPY = 0xA4E1C
PLT_MEMSET = 0xA4E88


class Harness:
    def __init__(self, data, base_off):
        self.data = data                  # full batch_info.bin image
        self.pos = base_off               # absolute offset in self.data
        self.base = base_off              # record start (absolute)
        self.trace = []                   # (kind, args...)
        self.mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self._map()
        self._hooks()
        self.heap_ptr = HEAP_BASE

    def _map(self):
        mu = self.mu
        so = open(SO, "rb").read()
        mu.mem_map(0, (len(so) + 0xFFF) & ~0xFFF)
        mu.mem_write(0, so)
        mu.mem_map(MAGIC_PAGE, 0x1000)
        mu.mem_map(STACK_BASE, 0x200000)
        mu.mem_map(HEAP_BASE, 0x400000)
        # file object: [0]=vtable; vtable[0xc]=VT_READ, [0x18]=VT_SEEK
        mu.mem_write(MAGIC_PAGE + 0x00, struct.pack("<I", MAGIC_PAGE + 0x100))
        mu.mem_write(MAGIC_PAGE + 0x10C, struct.pack("<I", VT_READ))
        mu.mem_write(MAGIC_PAGE + 0x118, struct.pack("<I", VT_SEEK))
        # arg1: SPrimitiveStreamDesc holder with [0] = file object
        mu.mem_write(MAGIC_PAGE + 0x300, struct.pack("<I", MAGIC_PAGE))

    # ------------- engine services -------------
    def _service(self, mu, address, size, user_data):
        if address == VT_READ:
            buf = mu.reg_read(UC_ARM_REG_R1)
            n = mu.reg_read(UC_ARM_REG_R2)
            chunk = self.data[self.pos:self.pos + n]
            if len(chunk) < n:
                chunk = chunk + b"\x00" * (n - len(chunk))
            mu.mem_write(buf, chunk)
            self.trace.append(("read", self.pos - self.base, n,
                               chunk[:min(n, 12)].hex()))
            self.pos += n
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == VT_SEEK:
            off = struct.unpack("<i", struct.pack("<I", mu.reg_read(UC_ARM_REG_R1)))[0]
            rel = mu.reg_read(UC_ARM_REG_R2)
            self.trace.append(("seek", off, rel))
            self.pos = self.pos + off if rel else self.base + off
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == GLITCH_ALLOC:
            n = mu.reg_read(UC_ARM_REG_R1)
            p = self.heap_ptr
            self.heap_ptr = (self.heap_ptr + n + 0x1F) & ~0xF
            mu.reg_write(UC_ARM_REG_R0, p)
            self.trace.append(("alloc", n, hex(p)))
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == PLT_MEMCPY:
            dst = mu.reg_read(UC_ARM_REG_R0)
            src = mu.reg_read(UC_ARM_REG_R1)
            n = mu.reg_read(UC_ARM_REG_R2)
            if n:
                mu.mem_write(dst, bytes(mu.mem_read(src, n)))
            self.trace.append(("memcpy", n))
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == PLT_MEMSET:
            dst = mu.reg_read(UC_ARM_REG_R0)
            val = mu.reg_read(UC_ARM_REG_R1) & 0xFF
            n = mu.reg_read(UC_ARM_REG_R2)
            if n:
                mu.mem_write(dst, bytes([val]) * n)
            self.trace.append(("memset", n, val))
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address in (GLITCH_FREE, ADD_REF, REL_PTR, REL_PB, HOOK_PS,
                         ALLOC_PS):
            # no-op services; allocProcessBuffer returns a small buffer
            if address == ALLOC_PS:
                p = self.heap_ptr
                self.heap_ptr = (self.heap_ptr + 0x40) & ~0xF
                mu.reg_write(UC_ARM_REG_R0, p)
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _hooks(self):
        self.mu.hook_add(UC_HOOK_CODE, self._service,
                         begin=MAGIC_PAGE, end=MAGIC_PAGE + 0x1000)
        for a in (GLITCH_ALLOC, GLITCH_FREE, ADD_REF, REL_PTR,
                  ALLOC_PS, REL_PB, HOOK_PS, PLT_MEMCPY, PLT_MEMSET):
            self.mu.hook_add(UC_HOOK_CODE, self._service, begin=a, end=a + 4)

    def run_record(self, rec_base, prefix_len=32):
        """rec_base: absolute offset of the record start in self.data."""
        mu = self.mu
        self.base = rec_base
        self.pos = rec_base + prefix_len
        self.trace = []
        arg0 = MAGIC_PAGE + 0x400        # CVertexStreams holder ([0]=cvs)
        tail = MAGIC_PAGE + 0x500        # 24B tail out
        cvs = MAGIC_PAGE + 0x600         # pre-allocated holder target
        mu.mem_write(arg0, struct.pack("<I", 0))          # [0]=0 for allocate()
        # run the real function: r0=arg0, r1=arg1(desc holder), r2=tail, r3=0 (LE)
        mu.reg_write(UC_ARM_REG_SP, STACK_BASE + 0x100000)
        mu.reg_write(UC_ARM_REG_R0, arg0)
        mu.reg_write(UC_ARM_REG_R1, MAGIC_PAGE + 0x300)
        mu.reg_write(UC_ARM_REG_R2, tail)
        mu.reg_write(UC_ARM_REG_R3, 0)
        mu.reg_write(UC_ARM_REG_LR, MAGIC_PAGE + 0x800)   # fake return
        try:
            mu.emu_start(LHS, MAGIC_PAGE + 0x800, timeout=2_000_000, count=2_000_000)
            err = None
        except UcError as e:
            err = f"{e} pc=0x{mu.reg_read(UC_ARM_REG_PC):x}"
        out = {}
        if err is None:
            cvs_ptr = struct.unpack("<I", mu.mem_read(arg0, 4))[0]
            if cvs_ptr:
                kcount = mu.mem_read(cvs_ptr + 0xC, 2)
                pairbuf = struct.unpack("<I", mu.mem_read(cvs_ptr + 0x10, 4))[0]
                nstreams = popcount_from_trace = None
                # streams array at cvs+0x14, 16B each; count from [+8] mask
                mask = struct.unpack("<I", mu.mem_read(cvs_ptr + 4, 4))[0]
                nslots = bin(mask).count("1") if mask else 0
                streams = []
                for i in range(nslots):
                    b = mu.mem_read(cvs_ptr + 0x14 + 16 * i, 16)
                    f0 = struct.unpack_from("<I", b, 4)[0]
                    f2, f3, f4 = struct.unpack_from("<3H", b, 0xA)
                    streams.append((f0, f2, f3, f4))
                # engine fills K+1 slots (pre-loop pair + K loop pairs)
                npairs = struct.unpack("<B", kcount[0:1])[0] + 1
                pairs = []
                for s in range(npairs):
                    v = struct.unpack("<6f", mu.mem_read(pairbuf + 24 * s, 24))
                    pairs.append([round(x, 9) for x in v])
                out = dict(K=npairs, mask=hex(mask), streams=streams,
                           pairs=pairs)
        out["err"] = err
        out["trace"] = self.trace
        return out


def popcount(x):
    return bin(x).count("1")


def main():
    results = {}
    for island in ("GothamCity", "GothamCity_Island2"):
        d = open(f"/home/z/my-project/work/zone/{island}/batch_info.bin", "rb").read()
        stride = struct.unpack_from("<I", d, 0)[0]
        M = (len(d) - 4) // stride
        h = Harness(d, 4)
        per = []
        for m in range(M):
            rec = 4 + stride * m
            r = h.run_record(rec)
            # summarize: strip bulky trace
            reads = [(t[1], t[2]) for t in r["trace"] if t[0] == "read"]
            seeks = [(t[1], t[2]) for t in r["trace"] if t[0] == "seek"]
            per.append(dict(m=m, K=r.get("K"), mask=r.get("mask"),
                            streams=r.get("streams"), pairs=r.get("pairs"),
                            err=r["err"],
                            reads=reads, seeks=seeks))
        results[island] = per
        # console summary for first few + error count
        errs = sum(1 for p in per if p["err"])
        print(f"{island}: {M} records, emulation errors: {errs}")
        for p in per[:3]:
            print(f"  m{p['m']}: K={p['K']} mask={p['mask']} err={p['err']}")
            print(f"      reads={p['reads']}")
            print(f"      pairs={[p['pairs']] if p['pairs'] else None}")
    json.dump(results, open("/home/z/my-project/work/harness_lhs.json", "w"))
    print("wrote /home/z/my-project/work/harness_lhs.json")


if __name__ == "__main__":
    main()
