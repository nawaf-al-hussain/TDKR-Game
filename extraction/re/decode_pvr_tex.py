#!/usr/bin/env python3
"""
Decode Gameloft .tga.bin PVR containers (PVRTC4) -> PNG.
Layout: [u52 game wrapper: hdrSize=52, w, h, mips, fcc, dataSize, 4, pad]
        [PVR! v2 texture data: mips...]
"""
import struct, sys, os
import texture2ddecoder
from PIL import Image

def decode(path, out_png=None):
    d = open(path, "rb").read()
    hdr_size, w, h, mips, fcc, data_size, bpp = struct.unpack_from("<IIIIIIX".replace("X", "I"), d, 0)[0:7]
    hdr_size, w, h, mips, fcc, data_size = struct.unpack_from("<IIIIII", d, 0)
    bpp = struct.unpack_from("<I", d, 24)[0]
    magic = d[hdr_size:hdr_size + 4]
    print(f"{os.path.basename(path)}: {w}x{h} mips={mips} fcc={fcc:#x} bpp={bpp} magic={magic!r} dataSize={data_size}")

    data = d[hdr_size + 4:]  # skip PVR! magic; rest = mip chain
    # PVRTC4 decode mip0
    size0 = w * h // 2  # 4bpp
    mip0 = data[:size0]
    out = texture2ddecoder.decode_pvrtc(mip0, w, h, texture2ddecoder.PVRTCType.PVRTC_4bpp_RGB if hasattr(texture2ddecoder, 'PVRTCType') else False)
    img = Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")
    if out_png:
        img.save(out_png)
        print(f"   saved {out_png}")
    return img

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else \
        "/home/z/my-project/download/TDKR_assets/raw/l_gothamcity_tex/GC_VerticalFOG.tga.bin"
    dst = sys.argv[2] if len(sys.argv) > 2 else \
        "/home/z/my-project/work/TDKR-Game/gh-pages/models/tex/GC_VerticalFOG.png"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    decode(src, dst)
