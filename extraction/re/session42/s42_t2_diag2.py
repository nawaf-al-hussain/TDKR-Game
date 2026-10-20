#!/usr/bin/env python3
"""s42 T2c: localize the B128 engine-vs-reference divergence (block map + samples)."""
import sys, struct, zipfile, hashlib
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive, decode_blocks
from s42_t2_oracle import call_decompress, DSTBUF

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d, ents = read_archive(z, 'actors_tex.gla')
for (name, off, size) in ents:
    hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off + 52], 0)
    if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36 and wid == 128:
        src = d[off + 52:off + 52 + (wid // 4) * (hgt // 4) * 8]
        break
w, h = 128, 128
info, uc = call_decompress(src, w, h, dst_fmt=0xA, dst=DSTBUF)
eng = np.frombuffer(bytes(uc.mem_read(DSTBUF, w * h * 3)), np.uint8).reshape(h, w, 3).astype(np.int32)
ref = decode_blocks(src, w, h)[:, :, :3].astype(np.int32)

neq = (eng != ref).any(axis=2)
print(f"mismatched pixels: {neq.sum()} / {w*h}")
# block map
bm = neq.reshape(32, 4, 32, 4).any(axis=(1, 3))
print("mismatched blocks:", int(bm.sum()), "/ 1024")
rows = np.nonzero(bm.any(axis=1))[0]
cols = np.nonzero(bm.any(axis=0))[0]
print("block rows with mismatch:", rows.min() if len(rows) else '-', "..", rows.max() if len(rows) else '-',
      " cols:", cols.min() if len(cols) else '-', "..", cols.max() if len(cols) else '-')
# sample mismatching block
by, bx = np.argwhere(bm)[0] * 4
print(f"sample block ({by},{bx}):")
print("  eng:", eng[by:by+2, bx:bx+4].reshape(-1, 3).tolist())
print("  ref:", ref[by:by+2, bx:bx+4].reshape(-1, 3).tolist())
i = (by // 4) * 32 + (bx // 4)
print("  src block:", src[i * 8:i * 8 + 8].hex())
# is engine output == ref with rows flipped? or == ref of the block BELOW/RIGHT?
print("equal frac overall:", 1 - neq.mean())
# check engine==ref shifted by one block row
print("engine == ref shifted down 4px:", np.array_equal(eng[4:], ref[:-4]))
# check channel permutation
for p in [(0, 1, 2), (2, 1, 0), (1, 0, 2), (0, 2, 1), (1, 2, 0), (2, 0, 1)]:
    if (eng == ref[:, :, list(p)]).all():
        print("channel perm match:", p)
