#!/usr/bin/env python3
"""Try multiple GPU texture codecs on the same chunk to identify the real format."""
import os
import struct
import numpy as np
from PIL import Image
import texture2ddecoder as t2d

RAW = "/home/z/my-project/download/TDKR_assets/raw"
PROBE = "/home/z/my-project/download/TDKR_assets/probe"


def smoothness(img):
    g = np.asarray(img.convert("L"), dtype=np.float32)
    lap = np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:])
    return float(lap.mean())


def try_codecs(rel, tag):
    with open(os.path.join(RAW, rel), "rb") as fh:
        buf = fh.read()
    hs, h, w, mips, flags, dsz, bpp, *_ = struct.unpack("<13I", buf[:52])
    data = buf[52:]
    base4 = ((w + 3) // 4) * ((h + 3) // 4) * 8  # 4bpp base mip
    px = data[:base4]
    results = []
    tests = [
        ("etc1", lambda: t2d.decode_etc1(bytes(px), w, h)),
        ("bc1", lambda: t2d.decode_bc1(bytes(px), w, h)),
        ("atc_rgb4", lambda: t2d.decode_atc_rgb4(bytes(px), w, h)),
        ("atc_rgba8", lambda: t2d.decode_atc_rgba8_interpolated(bytes(px), w, h)),
        ("pvrtc4", lambda: t2d.decode_pvrtc(bytes(px), w, h, False)),
    ]
    for name, fn in tests:
        try:
            out = fn()
            img = Image.frombytes("RGBA", (w, h), out, "raw", "BGRA")
            s = smoothness(img)
            arr = np.asarray(img)
            results.append((name, s, float(arr[..., :3].mean())))
            img.thumbnail((512, 512))
            img.save(os.path.join(PROBE, f"codec_{tag}_{name}.png"))
        except Exception as e:
            results.append((name, None, str(e)))
    print(f"\n== {rel} ({w}x{h} flags={flags:#x}) ==")
    for name, s, m in results:
        print(f"  {name:10s} smooth={s if s is None else round(s, 1)} meanRGB={round(m, 1) if isinstance(m, float) else m}")


try_codecs("l_batcave_tex/GothamCity_Skybox_Night.tga.bin", "night")
try_codecs("l_stadion_tex/ST_skybox.tga.bin", "stadion")
