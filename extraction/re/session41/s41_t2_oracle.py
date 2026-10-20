#!/usr/bin/env python3
"""S41 T2: engine-ETC1 oracle — emulate pixel_format::decompress @0x800f84
(ARM, fmt 29 = ETC1 branch) under Unicorn on real mip0 payloads and compare
against the JS/Python decoders. Null: word-swapped blocks must diverge."""
import struct, sys, zipfile
import numpy as np
from unicorn import *
import unicorn.arm_const as AC
from unicorn.arm_const import *
from unicorn import *
import unicorn.arm_const as AC
from unicorn.arm_const import *
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive, decode_blocks

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
RAW = open(SO, 'rb').read()
PHOFF = struct.unpack_from('<I', RAW, 0x1c)[0]
PHNUM = struct.unpack_from('<H', RAW, 0x2c)[0]
SEGS = []
for i in range(PHNUM):
    o = PHOFF + i * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', RAW, o)[:6]
    if t == 1 and fs > 0:
        SEGS.append((va, off, fs, ms))

BASE = 0x0  # map at preferred base (vaddrs are absolute)
FN = 0x800f84
NEW_SITES = {0x3e9208, 0xabf338}   # operator new / new[] -> bump allocator
RET_SENTINEL = 0x1000000

HEAP = 0x20000000
HEAP_SZ = 0x400000
STACK = 0x30000000
STACK_SZ = 0x200000
SCRATCH = 0x40000000  # src data

ALLOC_BASE = 0x20000000  # inside HEAP
alloc_state = {'ptr': ALLOC_BASE, 'ptrs': []}


def hook_code(uc, address, size, user_data):
    if address in NEW_SITES:
        size_req = uc.reg_read(UC_ARM_REG_R1) if address == 0x3e9208 else uc.reg_read(UC_ARM_REG_R0)
        if address == 0x3e9208:
            # operator new(unsigned int) -> arg in r0
            size_req = uc.reg_read(UC_ARM_REG_R0)
        p = alloc_state['ptr']
        alloc_state['ptr'] += (max(size_req, 8) + 0x100) & ~0xf
        alloc_state['ptrs'].append((address, p, size_req))
        uc.reg_write(UC_ARM_REG_R0, p)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))


def run_decompress(src, w, h, arg2, wordswap=False):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    img_end = max(va + ms for (va, off, fs, ms) in SEGS)
    uc.mem_map(0, ((img_end + 0xffff) & ~0xffff) + 0x1000)
    for (va, off, fs, ms) in SEGS:
        uc.mem_write(va, RAW[off:off + fs])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(HEAP, HEAP_SZ * 4)
    uc.mem_map(SCRATCH, 0x100000)
    uc.mem_map(RET_SENTINEL, 0x1000)
    data = bytes(src)
    if wordswap:
        a = np.frombuffer(data, np.uint32).byteswap()
        data = a.tobytes()
    uc.mem_write(SCRATCH, data + b'\0' * 0x100)
    sp = STACK + STACK_SZ - 0x1000
    uc.mem_write(sp, struct.pack('<5I', 14, 0, w, h, 1))
    uc.reg_write(UC_ARM_REG_SP, sp)
    uc.reg_write(UC_ARM_REG_R0, 29)   # fmt = 0x1d
    uc.reg_write(UC_ARM_REG_R1, SCRATCH)
    uc.reg_write(UC_ARM_REG_R2, arg2)
    uc.reg_write(UC_ARM_REG_R3, 14)   # GL_RGB-ish
    uc.reg_write(UC_ARM_REG_LR, RET_SENTINEL)
    uc.hook_add(UC_HOOK_CODE, hook_code)

    def hook_mem_inv(uc, access, address, size, value, user_data):
        regs = {n: uc.reg_read(getattr(AC, f'UC_ARM_REG_{n}')) for n in ('R0', 'R1', 'R2', 'R3', 'R8', 'R9', 'R10', 'R12', 'SP')}
        print(f'  MEM-FAULT access={access} addr={address:#x} size={size} pc={uc.reg_read(UC_ARM_REG_PC):#x} regs={ {k: hex(v) for k, v in regs.items()} }')
        return False
    uc.hook_add(UC_HOOK_MEM_INVALID, hook_mem_inv)
    try:
        uc.emu_start(FN, RET_SENTINEL, timeout=0, count=200_000_000)
    except UcError as e:
        dbg = {n: uc.reg_read(getattr(AC, f'UC_ARM_REG_{n}')) for n in ('R0', 'R1', 'R2', 'R3', 'R8', 'R9', 'R10', 'R12')}
        dbg = {k: hex(v) for k, v in dbg.items()}
        return {'error': f'{e} pc={uc.reg_read(UC_ARM_REG_PC):#x}', 'regs': dbg}
    ret = uc.reg_read(UC_ARM_REG_R0)
    return {'ret': ret, 'allocs': alloc_state['ptrs']}


def main():
    z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    d, ents = read_archive(z, 'actors_tex.gla')
    # pick a few mip0 payloads of different sizes
    picks = []
    for (name, off, size) in ents:
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off+52], 0)
        if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36 and mips in (8, 9) and len(picks) < 3:
            picks.append((name, wid, hgt, d[off+52:off+52+((wid+3)//4)*((hgt+3)//4)*8]))
        if len(picks) >= 3: break
    for (name, w, h, src) in picks:
        arg2 = 3 * w * h
        r = run_decompress(src, w, h, arg2)
        print(name, w, h, '->', {k: (v if k != 'allocs' else [(hex(a), hex(b), s) for a, b, s in v]) for k, v in r.items()})


if __name__ == '__main__':
    main()
