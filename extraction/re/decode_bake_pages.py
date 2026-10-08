#!/usr/bin/env python3
"""Decode the BakeGroup_* island pages + GC_LongDist FP pages (PVRv2-wrapped
ETC1, mip-chained) -> PNG, for the footprint-tile content verification."""
import struct, os, sys
import texture2ddecoder
from PIL import Image

TEX = '/home/z/my-project/download/TDKR_assets/raw/textures/l_gothamcity_tex.gla'
OUT = '/home/z/my-project/download/TDKR_assets/pages'
NAMES = [
    'BakeGroup_Island1_A0.tga', 'BakeGroup_Island1_ATLAS_low0.tga',
    'BakeGroup_Island1_B0.tga', 'BakeGroup_Island2_ATLAS_low0.tga',
]

def entries(path):
    d = open(path, 'rb').read(16)
    _, idx_size, table_bytes, n = struct.unpack('>IIII', d)
    f = open(path, 'rb')
    f.seek(16)
    tbl = f.read(n * 16)
    pool = f.read(idx_size - 16 - n * 16)
    out = {}
    for i in range(n):
        off, sz, name_off, _ = struct.unpack('>IIII', tbl[i*16:(i+1)*16])
        e = pool.find(b'\x00', name_off)
        out[pool[name_off:e].decode('latin1')] = (off, sz)
    return f, out

def decode_etc1_pvr(data, out_png):
    hdr, h, w, mips, flags, dsize, bpp = struct.unpack_from('<IIIIIII', data, 0)
    magic = data[44:48]
    assert magic == b'PVR!', magic
    payload = data[52:52 + dsize]
    size0 = ((w + 3) // 4) * ((h + 3) // 4) * 8
    mip0 = payload[:size0]
    rgba = texture2ddecoder.decode_etc1(mip0, w, h)
    img = Image.frombytes('RGBA', (w, h), bytes(rgba), 'raw', 'BGRA')
    img.save(out_png)
    print(f'{os.path.basename(out_png)}: {w}x{h} mips={mips} flags={flags:#x} bpp={bpp}')
    return img

def main():
    os.makedirs(OUT, exist_ok=True)
    f, ents = entries(TEX)
    for nm in (sys.argv[1:] or NAMES):
        if nm not in ents:
            print('missing:', nm); continue
        off, sz = ents[nm]
        f.seek(off)
        data = f.read(sz)
        out = os.path.join(OUT, nm.replace('.tga', '.png'))
        decode_etc1_pvr(data, out)

if __name__ == '__main__':
    main()
