#!/usr/bin/env python3
"""s42 T2d: size x flip matrix to find the engine addressing rule."""
import sys, struct, zipfile
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive, decode_blocks
from s42_t2_oracle import call_decompress, DSTBUF

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d, ents = read_archive(z, 'actors_tex.gla')
picks = {}
for (name, off, size) in ents:
    hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off + 52], 0)
    if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36 and wid in (16, 128, 256) and wid not in picks:
        picks[wid] = (name, wid, hgt, d[off + 52:off + 52 + (wid // 4) * (hgt // 4) * 8])

for wid in sorted(picks):
    name, w, h, src = picks[wid]
    ref = decode_blocks(src, w, h)[:, :, :3]
    row = [f"{name} {w}x{h}:"]
    for flip in (0, 1):
        info, uc = call_decompress(src, w, h, dst_fmt=0xA, dst=DSTBUF, flip=flip)
        if 'error' in info:
            row.append(f"flip={flip}: ERR {info['error'][:40]}")
            continue
        eng = np.frombuffer(bytes(uc.mem_read(DSTBUF, w * h * 3)), np.uint8).reshape(h, w, 3)
        eq = (eng == ref).all(axis=2).mean()
        row.append(f"flip={flip}: eq={eq:.4f}")
    print("  ".join(row))
