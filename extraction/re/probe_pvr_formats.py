#!/usr/bin/env python3
"""Try every compressed format/offset for GC_VerticalFOG."""
import struct
import texture2ddecoder
from PIL import Image

d = open("/home/z/my-project/download/TDKR_assets/raw/l_gothamcity_tex/GC_VerticalFOG.tga.bin", "rb").read()
W = H = 1024
N = W * H // 2  # 4bpp mip0

def smoothness(rgba):
    img = Image.frombytes("RGBA", (W, H), bytes(rgba), "raw", "BGRA").convert("L")
    px = img.tobytes()
    diff = n = 0
    for y in range(0, H - 1, 41):
        row = y * W
        for x in range(0, W - 1, 59):
            i = row + x
            diff += abs(px[i] - px[i + 1]) + abs(px[i] - px[i + W])
            n += 2
    return diff / max(n, 1)

def save_scored(name, out):
    s = smoothness(out)
    print(f"{name}: smoothness={s:.2f}")
    if s < 6:
        img = Image.frombytes("RGBA", (W, H), bytes(out), "raw", "BGRA")
        img.save(f"/tmp/probe_{name}.png")
        print("   saved /tmp/probe_" + name + ".png")
    return s

results = []
for off in (0x34, 0x38, 0x3c, 0x40, 0x46, len(d) - N):
    chunk = d[off:off + N]
    if len(chunk) < N:
        continue
    results.append((f"pvrtc4@{off:#x}", texture2ddecoder.decode_pvrtc(chunk, W, H, False)))
    results.append((f"pvrtc2@{off:#x}", texture2ddecoder.decode_pvrtc(chunk, W, H, True)))
    try:
        results.append((f"atc4@{off:#x}", texture2ddecoder.decode_atc_rgb4(chunk, W, H)))
    except Exception as e:
        print("atc err", e)
    try:
        results.append((f"etc2rgb@{off:#x}", texture2ddecoder.decode_etc2(chunk, W, H)))
    except Exception:
        pass
    try:
        results.append((f"dxt1@{off:#x}", texture2ddecoder.decode_bc1(chunk, W, H)))
    except Exception:
        pass

best = min((save_scored(n, o) if len(o) == W * H * 4 else 99, n) for n, o in results)
print("BEST:", best)
