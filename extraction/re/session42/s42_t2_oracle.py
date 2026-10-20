#!/usr/bin/env python3
"""s42 T2: ENGINE ORACLE for ETC1 — direct Unicorn call of glitch pixel_format::decompress
@0x800f84 with the argument layout derived from disassembly:
  decompress(fmt=r0, src=r1, srcSize=r2, dstFmt=r3, dst=[sp], dstCap=[sp+4], w=[sp+8], h=[sp+12], bool=[sp+16])
  - fmt 0x1d = COMPRESSED_RGB8_ETC branches to the inline ETC1 decoder @0x80110c
  - stackarg7=w, stackarg8=h (engine allocates w*3*h internally; dstFmt 0xa path @0x80185c)
Compare against the s41 Python reference decode (bit-exact), with nulls:
  N1 shuffled-block src (must MISMATCH), N2 arg permutation r3=0xe (RGBA out),
  N3 dst=NULL (engine allocates; compare via its return).
"""
import struct, sys, zipfile, hashlib, json
import numpy as np
from unicorn import *
from unicorn.arm_const import *
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
from s41_refdec_lib import read_archive, decode_blocks

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

FN = 0x800F84          # ARM entry (prologue e92d4ff0)
NEW_SITES = {0x3e9208, 0xabf338}
RET = 0x1000000
STACK, STACK_SZ = 0x30000000, 0x400000
HEAP = 0x20000000
SCRATCH = 0x40000000
DSTBUF = 0x41000000


def map_image(uc):
    img_end = max(va + ms for (va, off, fs, ms) in SEGS)
    uc.mem_map(0, ((img_end + 0xffff) & ~0xffff) + 0x1000)
    for (va, off, fs, ms) in SEGS:
        uc.mem_write(va, RAW[off:off + fs])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(HEAP, 0x1000000)
    uc.mem_map(SCRATCH, 0x100000)
    uc.mem_map(DSTBUF, 0x100000)
    uc.mem_map(RET, 0x1000)


class Alloc:
    def __init__(self):
        self.ptr = HEAP + 0x1000
        self.log = []

    def hook(self, uc, address, size, ud):
        if address not in NEW_SITES:
            return
        r0 = uc.reg_read(UC_ARM_REG_R0)
        p = self.ptr
        self.ptr += (max(r0, 8) + 0x100) & ~0xF
        self.log.append((address, p, r0))
        uc.reg_write(UC_ARM_REG_R0, p)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))


def call_decompress(src, w, h, dst_fmt=0xA, dst=None, pitch=None, flip=0, timeout_s=60):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    map_image(uc)
    al = Alloc()
    uc.hook_add(UC_HOOK_CODE, al.hook)
    uc.mem_write(SCRATCH, bytes(src) + b'\0' * 0x100)
    sp = STACK + STACK_SZ - 0x2000
    dstp = dst if dst is not None else (DSTBUF if dst_fmt == 0xA else 0)
    if pitch is None:
        pitch = w * 3
    # stack args: [dst][pitch][w][h][bool]   (pitch = bytes/row, engine writes rows at dst+y*pitch)
    uc.mem_write(sp, struct.pack('<5I', dstp, pitch, w, h, flip))
    uc.reg_write(UC_ARM_REG_SP, sp)
    uc.reg_write(UC_ARM_REG_R0, 0x1D)      # fmt COMPRESSED_RGB8_ETC
    uc.reg_write(UC_ARM_REG_R1, SCRATCH)
    uc.reg_write(UC_ARM_REG_R2, (w // 4) * 8)  # arg3 = source block-row pitch in bytes
    uc.reg_write(UC_ARM_REG_R3, dst_fmt)   # 0xa = R8G8B8 (path 0x80185c)
    uc.reg_write(UC_ARM_REG_LR, RET)
    info = {}
    try:
        uc.emu_start(FN, RET, timeout=timeout_s * 1000000, count=100_000_000)
        info['ret'] = uc.reg_read(UC_ARM_REG_R0)
        info['pc_end'] = uc.reg_read(UC_ARM_REG_PC)
        info['allocs'] = [(hex(a), hex(p), s) for a, p, s in al.log]
        # engine-allocated buffer: first alloc (w*3*h)
        if al.log:
            info['newbuf'] = al.log[0][1]
            info['newsize'] = al.log[0][2]
    except UcError as e:
        info['error'] = f'{e} pc={uc.reg_read(UC_ARM_REG_PC):#x}'
        info['allocs'] = [(hex(a), hex(p), s) for a, p, s in al.log]
        if al.log:
            info['newbuf'] = al.log[0][1]
    return info, uc


def ref_rgb888(src, w, h):
    rgba = decode_blocks(src, w, h)      # HxWx4 uint8 (our validated reference)
    return np.ascontiguousarray(rgba[:, :, :3]).tobytes(), rgba


def main():
    z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    d, ents = read_archive(z, 'actors_tex.gla')
    # full texture A: 32x32 ETC1 mip0 (64 blocks); full texture B: 128x128 (1024 blocks)
    texA = texB = None
    for (name, off, size) in ents:
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off + 52], 0)
        if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36:
            if wid == 32 and texA is None:
                texA = (name, wid, hgt, d[off + 52:off + 52 + (wid // 4) * (hgt // 4) * 8])
            if wid == 128 and texB is None:
                texB = (name, wid, hgt, d[off + 52:off + 52 + (wid // 4) * (hgt // 4) * 8])
        if texA and texB:
            break
    out = {}
    for tag, (name, w, h, src) in (('A64', texA), ('B128', texB)):
        ref, rgba = ref_rgb888(src, w, h)
        # O1: engine decode, dstFmt=0xa, dst given
        info, uc = call_decompress(src, w, h, dst_fmt=0xA, dst=DSTBUF)
        got = uc.mem_read(DSTBUF, w * h * 3) if 'error' not in info else b''
        eng = bytes(got)
        rec = {'name': name, 'w': w, 'h': h, 'blocks': len(src) // 8,
               'ref_sha': hashlib.sha256(ref).hexdigest(),
               'eng_sha': hashlib.sha256(eng).hexdigest(),
               'bitexact': eng == ref,
               'run': info}
        # O2: null — shuffled block order (must mismatch)
        rnd = np.random.RandomState(42)
        nb = len(src) // 8
        perm = rnd.permutation(nb)
        shuf = b''.join(src[i * 8:(i + 1) * 8] for i in perm)
        info2, uc2 = call_decompress(shuf, w, h, dst_fmt=0xA, dst=DSTBUF)
        got2 = bytes(uc2.mem_read(DSTBUF, w * h * 3)) if 'error' not in info2 else b''
        rec['null_shuffle_mismatches'] = got2 != ref
        # O3: dstFmt=0xe path (engine allocates internally; output RGBA? take newbuf)
        info3, uc3 = call_decompress(src, w, h, dst_fmt=0xE, dst=None, pitch=w * 4)
        rec['run_0xe'] = {'error': info3.get('error'), 'allocs': info3.get('allocs')}
        if 'newbuf' in info3 and 'error' not in info3:
            cand = bytes(uc3.mem_read(info3['newbuf'], w * h * 3))
            cand4 = bytes(uc3.mem_read(info3['newbuf'], w * h * 4))
            rec['engine_0xe_rgb_match'] = cand == ref
            rec['engine_0xe_first16'] = cand4[:16].hex()
        # N3: dst=NULL with dstFmt=0xa
        info4, uc4 = call_decompress(src, w, h, dst_fmt=0xA, dst=None)
        rec['run_dst_null'] = {'error': info4.get('error'), 'allocs': info4.get('allocs')}
        out[tag] = rec
        print(f"=== {tag}: {name} {w}x{h} ({len(src)//8} blocks)")
        print(f"  ref  sha {rec['ref_sha'][:16]}")
        print(f"  eng  sha {rec['eng_sha'][:16]}  bitexact={rec['bitexact']}")
        print(f"  run: ret={info.get('ret')} err={info.get('error')} allocs={info.get('allocs')}")
        print(f"  null_shuffle_mismatches={rec['null_shuffle_mismatches']}")
        if 'engine_0xe_rgb_match' in rec:
            print(f"  0xe path rgb match={rec['engine_0xe_rgb_match']} first16={rec.get('engine_0xe_first16')}")
        print(f"  dst-null run: {rec['run_dst_null']}")
    json.dump(out, open('/home/z/my-project/scripts/s42_t2_oracle.json', 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
