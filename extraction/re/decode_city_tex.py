#!/usr/bin/env python3
"""Decode city texture containers (PVR v1 wrapper) generically + brightness report."""
import struct, sys, os
import numpy as np
import texture2ddecoder as t2d
from PIL import Image

def decode_container(path):
    d = open(path, "rb").read()
    hdr, h, w, mips, fmt, dsize, bpp = struct.unpack_from("<IIIIIII", d, 0)[:7]
    # note: field order per PVR v1: hdrSize, Height, Width, Mips, Fmt, DataSize, Bpp
    payload = d[hdr:hdr + dsize]
    return dict(hdr=hdr, h=h, w=w, mips=mips, fmt=fmt, dsize=dsize, bpp=bpp,
                payload=payload, tail=d[hdr + dsize:hdr + dsize + 8])

def decode_tex(info, path):
    w, h, p, fmt, bpp = info["w"], info["h"], info["payload"], info["fmt"], info["bpp"]
    if bpp == 4:
        out = t2d.decode_etc2(p, w, h)
    elif bpp == 8:
        out = t2d.decode_etc2a8(p, w, h)
    elif bpp == 2:
        out = t2d.decode_pvrtc(p, w, h, False)
    else:
        raise ValueError(f"bpp={bpp}")
    img = Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")
    return img

if __name__ == "__main__":
    for p in sys.argv[1:]:
        info = decode_container(p)
        print(f"{os.path.basename(p)}: {info['w']}x{info['h']} mips={info['mips']} fmt={info['fmt']:#x} bpp={info['bpp']} dsize={info['dsize']} tail={info['tail'][:4]!r}")
        try:
            img = decode_tex(info, p)
            g = np.asarray(img.convert("L"), dtype=np.float32) / 255
            print(f"   decoded: mean={g.mean():.3f} p95={np.percentile(g, 95):.3f}")
            out = p.rsplit(".", 1)[0] + "_dec.png"
            img.save(out)
            print(f"   saved {out}")
        except Exception as e:
            print("   decode FAIL:", e)
