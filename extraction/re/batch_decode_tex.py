#!/usr/bin/env python3
"""Batch-decode texture .tga.bin containers from both texture .gla archives
into textures_png/<sub>/<name>.png (pool for export_city)."""
import struct, os, sys
import numpy as np
import texture2ddecoder as t2d
from PIL import Image

BASE = "/home/z/my-project/download/TDKR_assets/raw/textures"
OUT = "/home/z/my-project/download/TDKR_assets/textures_png"

ARCHIVES = {
    "l_gothamcity_tex": "l_gothamcity_tex.gla",
    "commons_tex": "commons_tex.gla",
}

def decode(payload, w, h, bpp, fmt):
    if bpp == 4:
        return t2d.decode_etc2(payload, w, h)
    if bpp == 8:
        return t2d.decode_etc2a8(payload, w, h)
    if bpp == 2:
        return t2d.decode_pvrtc(payload, w, h, False)
    if bpp == 16 and fmt == 0x13:  # RGB565 raw -> BGRA byte order (PIL path below)
        u16 = np.frombuffer(payload[: w * h * 2], dtype="<u2").reshape(h, w)
        r = ((u16 >> 11) & 0x1F).astype(np.uint8)
        g = ((u16 >> 5) & 0x3F).astype(np.uint8)
        b = (u16 & 0x1F).astype(np.uint8)
        bgr = np.stack([b << 3 | b >> 2, g << 2 | g >> 4, r << 3 | r >> 2], -1)
        rgba = np.zeros((h, w, 4), np.uint8)
        rgba[..., :3] = bgr
        rgba[..., 3] = 255
        return rgba.ravel().view(np.uint32)
    if bpp == 24 and fmt in (0x15, 21):  # RGB888 raw -> BGRA
        arr = np.frombuffer(payload[: w * h * 3], dtype=np.uint8).reshape(h, w, 3)
        rgba = np.zeros((h, w, 4), np.uint8)
        rgba[..., :3] = arr[..., [2, 1, 0]]
        rgba[..., 3] = 255
        return rgba.ravel().view(np.uint32)
    if bpp == 32 and fmt in (0x12, 18):  # RGBA8888 raw
        arr = np.frombuffer(payload[: w * h * 4], dtype=np.uint8).reshape(h, w, 4)
        rgba = arr[..., [2, 1, 0, 3]]  # RGBA->BGRA
        return rgba.ravel().view(np.uint32)
    raise ValueError(f"bpp={bpp} fmt={fmt:#x}")

for sub, arc in ARCHIVES.items():
    d = open(os.path.join(BASE, arc), "rb").read()
    tag, idx_size, table_bytes, n = struct.unpack(">IIII", d[:16])
    pool = d[16 + n * 16: idx_size]
    od = os.path.join(OUT, sub)
    os.makedirs(od, exist_ok=True)
    done = fail = skip = 0
    for i in range(n):
        off, sz, name_off, _ = struct.unpack(">IIII", d[16 + i * 16: 32 + i * 16])
        end = pool.find(b"\x00", name_off)
        nm = pool[name_off:end].decode("latin1", "replace")
        stem = nm.rsplit(".", 1)[0]
        outp = os.path.join(od, stem + ".png")
        if os.path.exists(outp):
            skip += 1
            continue
        blob = d[off:off + sz]
        try:
            if blob[:4] == b"PK\x03\x04":  # ZIP_SPLIT: SPLIT marker + rgb.pvr + alpha.pvr
                import zipfile, io
                z = zipfile.ZipFile(io.BytesIO(blob))
                blob = z.read("rgb.pvr")
            hdr, h, w, mips, fmt, dsize, bpp = struct.unpack_from("<IIIIIII", blob, 0)[:7]
            if dsize > len(blob) - hdr or w == 0 or h == 0:
                fail += 1
                print(f"BADHDR {nm} hdr={hdr} {w}x{h} dsize={dsize} chunk={sz}", file=sys.stderr)
                continue
            rgba = decode(blob[hdr:hdr + dsize], w, h, bpp, fmt)
            img = Image.frombytes("RGBA", (w, h), bytes(rgba), "raw", "BGRA")
            img.save(outp)
            done += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {nm}: {e}", file=sys.stderr)
    print(f"{sub}: done={done} skip={skip} fail={fail} (of {n})")
