#!/usr/bin/env python3
"""S40 T1b nulls: the ETC1 decode must separate from wrong-layout nulls.
Null A: column-major block order (transposed block grid)
Null B: shuffled block order
Null C: s39-style misread (bytes 4-7 as color word = word-swapped layout)
Real  : row-major blocks, calibrated layout (647/647 exact).
Metric vs texture2ddecoder reference: % mismatched texels, mean/max |err|.
"""
import struct, zipfile
import numpy as np
import texture2ddecoder as t2d
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from s40_t1_refdec import decode_blocks

def stats(mine, ref):
    d = np.abs(mine.astype(int) - ref.astype(int))
    mism = float(np.any(d > 0, axis=2).mean()) * 100
    return mism, float(d.mean()), int(d.max())

def run(name, arch):
    z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/' + arch)
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    ents = {}
    for i in range(n):
        off, size, nameOff = struct.unpack_from('>3I', d, 16 + i * 16)
        nb = pool + nameOff
        e = d.index(b'\0', nb)
        ents[d[nb:e].decode('latin1')] = (off, size)
    off, size = ents[name]
    hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d, off)
    BW, BH = (wid + 3) // 4, (hgt + 3) // 4
    px = bytes(d[off+52: off+52+BW*BH*8])
    ref = np.frombuffer(t2d.decode_etc1(px, wid, hgt), np.uint8).reshape(hgt, wid, 4)[:, :, [2, 1, 0, 3]]

    # real
    real = decode_blocks(px, wid, hgt)
    print(f'{name} ({wid}x{hgt}):')
    print(f'  real (row-major)      : mism {stats(real, ref)[0]:6.2f}%  mean {stats(real, ref)[1]:6.2f}  max {stats(real, ref)[2]}')

    # null A: column-major block order
    blocks = np.frombuffer(px, np.uint8).reshape(BH, BW, 8)
    colmajor = blocks.transpose(1, 0, 2).reshape(-1, 8).tobytes()
    nA = decode_blocks(colmajor, wid, hgt)
    s = stats(nA, ref); print(f'  null A (col-major blks): mism {s[0]:6.2f}%  mean {s[1]:6.2f}  max {s[2]}')

    # null B: shuffled blocks
    rng = np.random.default_rng(42)
    perm = rng.permutation(BH * BW)
    shuf = blocks.reshape(-1, 8)[perm].tobytes()
    nB = decode_blocks(shuf, wid, hgt)
    s = stats(nB, ref); print(f'  null B (shuffled blks) : mism {s[0]:6.2f}%  mean {s[1]:6.2f}  max {s[2]}')

    # null C: s39-style word-swapped read (color word <-> mod word)
    blk2 = blocks.reshape(-1, 8)[:, [4, 5, 6, 7, 0, 1, 2, 3]]
    nC = decode_blocks(blk2.tobytes(), wid, hgt)
    s = stats(nC, ref); print(f'  null C (word-swap)     : mism {s[0]:6.2f}%  mean {s[1]:6.2f}  max {s[2]}')

if __name__ == '__main__':
    run('GC_StockExchange_Gargoyle.tga', 'actors_tex.gla')
    run('BakeGroup_Island1_A0.tga', 'l_gothamcity_tex.gla')
    run('BakeGroup_Island1_Roads0.tga', 'l_gothamcity_tex.gla')
