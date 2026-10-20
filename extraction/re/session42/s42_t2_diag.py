#!/usr/bin/env python3
"""s42 T2b: diagnose engine-vs-reference difference (channel order? bit shift? row order?)."""
import sys, struct, zipfile
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive, decode_blocks
from s42_t2_oracle import call_decompress, DSTBUF

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d, ents = read_archive(z, 'actors_tex.gla')
for (name, off, size) in ents:
    hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off + 52], 0)
    if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36 and wid == 32:
        src = d[off + 52:off + 52 + (wid // 4) * (hgt // 4) * 8]
        break
w, h = 32, 32
info, uc = call_decompress(src, w, h, dst_fmt=0xA, dst=DSTBUF)
eng = np.frombuffer(bytes(uc.mem_read(DSTBUF, w * h * 3)), np.uint8).reshape(h, w, 3)
ref = decode_blocks(src, w, h)[:, :, :3]  # HxWx3

print("engine[0,:4]:", eng[0, :4].tolist())
print("ref   [0,:4]:", ref[0, :4].tolist())
print("engine[1,:4]:", eng[1, :4].tolist())
print("ref   [1,:4]:", ref[1, :4].tolist())

# candidate transforms
def sha(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:12]
import hashlib
cands = {
    'ref': ref,
    'ref BGR->RGB read (i.e. channels reversed)': ref[:, :, ::-1],
    'ref rows flipped': ref[::-1],
    'ref blockrows flipped': ref.reshape(8, 4, 32, 3)[:, ::-1].reshape(32, 32, 3),
    'ref transposed': ref.transpose(1, 0, 2),
}
for k, v in cands.items():
    print(f"  match {k!r}: {np.array_equal(eng, v)}")

# pixelwise: is eng == ref permuted by some fixed channel permutation?
for perm in [(0, 1, 2), (2, 1, 0), (1, 0, 2), (0, 2, 1), (1, 2, 0), (2, 0, 1)]:
    if np.array_equal(eng, ref[:, :, list(perm)]):
        print("channel permutation match:", perm)
# equality fraction per transform
print("equal frac ref:", (eng == ref).mean())
print("equal frac ref-BGR:", (eng == ref[:, :, ::-1]).mean())
print("equal frac ref-T:", (eng == ref.transpose(1, 0, 2)).mean())
# check whether engine output is CONSTANT per 4x4 block while ref differs (mod-index bit mapping issue)
bd = (eng.reshape(8, 4, 8, 4, 3) == ref.reshape(8, 4, 8, 4, 3)).all(axis=(3, 4))
print("block-level exact frac:", bd.mean(), " shape-mismatch blocks:", int((~bd).sum()), "/", bd.size)
# sample one mismatching block: compare all 16 pixel colors
bb = np.argwhere(~bd)[0]
by, bx = int(bb[0]) * 4, int(bb[1]) * 4
print(f"block at ({by},{bx}):")
print("  eng:", eng[by:by+4, bx:bx+4].reshape(-1, 3).tolist())
print("  ref:", ref[by:by+4, bx:bx+4].reshape(-1, 3).tolist())
print("  src block bytes:", src[(by // 4) * 8 + (bx // 4) * (w // 4) * 8:(by // 4) * 8 + (bx // 4) * (w // 4) * 8 + 8].hex())
