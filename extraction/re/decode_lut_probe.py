#!/usr/bin/env python3
"""Brute-force decode the 16384-B LUT payload with texture2ddecoder across
formats x geometries; score by smoothness (a color LUT ramp grid is smooth)."""
import struct
import texture2ddecoder as t2d
from PIL import Image
import numpy as np

d = open("/home/z/my-project/work/lut/000_default.tga.bin", "rb").read()
payload = d[52:52 + 16384]
print(f"payload {len(payload)} B; wrapper u32s:", struct.unpack_from("<12I", d, 0))

def score_rgba(rgba, w, h):
    img = np.frombuffer(bytes(rgba), dtype=np.uint8).reshape(h, w, 4)
    g = img[..., :3].astype(np.float32)
    dx = np.abs(np.diff(g, axis=1)).mean()
    dy = np.abs(np.diff(g, axis=0)).mean()
    return dx + dy

# 16384 B payload. bits/px candidates x geometry:
tests = []
# 4bpp formats: 32768 px -> 1024x32, 512x64, 256x128, 128x256
for (w, h) in [(1024, 32), (512, 64), (256, 128), (128, 256), (64, 512)]:
    tests.append((f"etc2rgb {w}x{h}", t2d.decode_etc2, payload, w, h))
    tests.append((f"etc1   {w}x{h}", t2d.decode_etc1, payload, w, h))
    tests.append((f"pvrtc4 {w}x{h}", lambda c, W, H: t2d.decode_pvrtc(c, W, H, False), payload, w, h))
    tests.append((f"eacr   {w}x{h}", t2d.decode_eacr, payload, w, h))
# 8bpp: 16384 px -> 512x32, 256x64, 128x128
for (w, h) in [(512, 32), (256, 64), (128, 128), (64, 256), (32, 512), (1024, 16)]:
    tests.append((f"etc2a8 {w}x{h}", t2d.decode_etc2a8, payload, w, h))
    tests.append((f"atc8   {w}x{h}", t2d.decode_atc_rgba8, payload, w, h))
    tests.append((f"bc3    {w}x{h}", t2d.decode_bc3, payload, w, h))
# 2bpp EAC R11: 65536 px -> 256x256
for (w, h) in [(256, 256), (512, 128), (128, 512), (2048, 32), (32, 2048)]:
    tests.append((f"eacr11 {w}x{h}", t2d.decode_eacr, payload, w, h))

res = []
for name, fn, chunk, w, h in tests:
    try:
        out = fn(chunk, w, h)
        s = score_rgba(out, w, h)
        res.append((s, name, out, w, h))
    except Exception as e:
        pass

res.sort(key=lambda t: t[0])
for s, name, *_ in res[:8]:
    print(f"{name}: TV={s:.3f}")

s, name, out, w, h = res[0]
img = Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")
img.save("/home/z/my-project/work/lut/000_default_probe_best.png")
print("saved best:", name)
# also save the top-3 for visual check
for i, (s, name, out, w, h) in enumerate(res[:3]):
    Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA").save(f"/home/z/my-project/work/lut/probe_{i}_{name.replace(' ', '_').replace('x', '_')}.png")
