#!/usr/bin/env python3
"""
TDKR PVR2 texture converter (PVRTC4/2 + uncompressed) -> PNG.
Private research use. Usage:
  tex_convert.py probe          # small validation set, saved to probe/
  tex_convert.py all [--limit N per archive]
"""
import os
import struct
import sys

import numpy as np
from PIL import Image
import texture2ddecoder

RAW = "/home/z/my-project/download/TDKR_assets/raw"
OUT = "/home/z/my-project/download/TDKR_assets/textures_png"
PROBE = "/home/z/my-project/download/TDKR_assets/probe"

PVR2_MAGIC = 0x21525650  # "PVR!" little-endian


def parse_pvr2(buf: bytes):
    """Return dict header info + pixel data offset, or raise."""
    if len(buf) < 52:
        raise ValueError("too small")
    hs, hgt, wid, mips, flags, dsz, bpp, mr, mg, mb, ma, magic, nsurf = struct.unpack(
        "<13I", buf[:52]
    )
    if hs == 52 and magic == PVR2_MAGIC:
        return dict(h=height_ok(hgt), w=width_ok(wid), mips=mips, flags=flags,
                    dsz=dsz, bpp=bpp, masks=(mr, mg, mb, ma), nsurf=nsurf, off=52, ver=2)
    if hs == 44:
        # legacy PVR2 without magic field: 11 u32s
        hs2, hgt2, wid2, mips2, flags2, dsz2, bpp2, mr2, mg2, mb2, ma2 = struct.unpack(
            "<11I", buf[:44]
        )
        return dict(h=hgt2, w=wid2, mips=mips2, flags=flags2, dsz=dsz2, bpp=bpp2,
                    masks=(mr2, mg2, mb2, ma2), nsurf=1, off=44, ver=2)
    raise ValueError(f"unrecognized PVR header hs={hs} magic={magic:#x}")


def height_ok(v):
    return v


def width_ok(v):
    return v


def expand5(v):
    return ((v << 3) | (v >> 2)).astype(np.uint8)


def expand6(v):
    return ((v << 2) | (v >> 4)).astype(np.uint8)


def expand4(v):
    return ((v << 4) | v).astype(np.uint8)


def decode_pvr2(buf: bytes, mips_first=True):
    info = parse_pvr2(buf)
    w, h, bpp = info["w"], info["h"], info["bpp"]
    data = buf[info["off"]:]
    masks = info["masks"]

    if bpp == 4:
        # 4bpp payload in this build is ETC1 (validated visually; PVRTC = noise)
        base = ((w + 3) // 4) * ((h + 3) // 4) * 8
        px = data[:base] if mips_first else data[-base:]
        out = texture2ddecoder.decode_etc1(bytes(px), w, h)
        img = Image.frombytes("RGBA", (w, h), out, "raw", "BGRA")
        fmt = "ETC1"
    elif bpp == 2:
        base = ((w + 7) // 8) * ((h + 3) // 4) * 8
        px = data[:base] if mips_first else data[-base:]
        out = texture2ddecoder.decode_etc2(bytes(px), w, h) if hasattr(texture2ddecoder, "decode_etc2") else texture2ddecoder.decode_etc1(bytes(px), w, h)
        img = Image.frombytes("RGBA", (w, h), out, "raw", "BGRA")
        fmt = "ETC?"
    elif bpp == 16:
        mr, mg, mb, ma = masks
        px = np.frombuffer(data[: w * h * 2], dtype="<u2").reshape(h, w)
        if ma == 0xF0000000 and (mr & 0xFFFF) == 0x0000F000:
            r = expand4((px >> 8) & 0xF); g = expand4((px >> 4) & 0xF)
            b = expand4(px & 0xF); a = expand4((px >> 12) & 0xF)
            fmt = "RGBA4444"
        elif ma == 0x1 and mr == 0x7C00:
            r = expand5((px >> 10) & 0x1F); g = expand5((px >> 5) & 0x1F)
            b = expand5(px & 0x1F); a = ((px >> 15) & 1) * 255
            fmt = "RGBA5551"
        else:  # masks are zeroed in this build; default RGB565
            r = expand5((px >> 11) & 0x1F); g = expand6((px >> 5) & 0x3F)
            b = expand5(px & 0x1F); a = np.full((h, w), 255, np.uint8)
            fmt = "RGB565"
        img = Image.fromarray(np.dstack([r, g, b, a.astype(np.uint8)]))
    elif bpp == 24:
        px = np.frombuffer(data[: w * h * 3], dtype=np.uint8).reshape(h, w, 3)
        rgb = px[:, :, ::-1]  # memory BGR -> RGB (validated on GC_Skybox)
        img = Image.fromarray(rgb).convert("RGBA")
        fmt = "RGB888"
    elif bpp == 32:
        px = np.frombuffer(data[: w * h * 4], dtype=np.uint8).reshape(h, w, 4)
        img = Image.frombytes("RGBA", (w, h), px.tobytes(), "raw", "BGRA")
        fmt = "RGBA8888"
    else:
        raise ValueError(f"unsupported bpp {bpp}")
    return img, info, fmt


def smoothness(img: Image.Image) -> float:
    """Laplacian energy — low = smooth (sky/water), high = noise (bad decode)."""
    g = np.asarray(img.convert("L"), dtype=np.float32)
    lap = np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:])
    return float(lap.mean())


def convert_file(path, mips_first=True):
    with open(path, "rb") as fh:
        buf = fh.read()
    return decode_pvr2(buf, mips_first)


def probe():
    os.makedirs(PROBE, exist_ok=True)
    cases = [
        ("commons_tex/GC_Skybox.tga.bin", "skybox24"),
        ("l_batcave_tex/GothamCity_Skybox_Night.tga.bin", "night_mipfirst"),
        ("l_batcave_tex/GothamCity_Skybox_Night.tga.bin", "night_miplast"),
        ("l_gothamcity_tex/002_GothamCity.tga.bin", "gotham_mipfirst"),
        ("commons_tex/000_default.tga.bin", "default"),
    ]
    for rel, tag in cases:
        p = os.path.join(RAW, rel)
        if not os.path.exists(p):
            print("missing:", rel)
            continue
        try:
            img, info, fmt = convert_file(p, mips_first=(tag != "night_miplast"))
            img.thumbnail((512, 512))
            outp = os.path.join(PROBE, f"{tag}.png")
            img.save(outp)
            print(f"{tag:16s} {info['w']}x{info['h']} bpp={info['bpp']} fmt={fmt} "
                  f"masks={[hex(m) for m in info['masks']]} smooth={smoothness(img):.1f} -> {outp}")
        except Exception as e:
            print(f"{tag:16s} FAILED: {e}")

    # inspect BAD headers
    import glob as g
    bad = []
    for f in g.glob(os.path.join(RAW, "*_tex/*.bin")):
        with open(f, "rb") as fh:
            head = fh.read(52)
        if len(head) >= 52:
            vals = struct.unpack("<13I", head)
            if vals[11] != PVR2_MAGIC:
                bad.append((f, vals[:7]))
    print(f"\n{len(bad)} BAD files; first 5 headers (hs,h,w,mips,flags,dsz,bpp):")
    for f, v in bad[:5]:
        print(" ", os.path.basename(f), v)


def full_run(archive_filter=None):
    import csv
    import glob as g
    import time

    os.makedirs(OUT, exist_ok=True)
    rows = []
    t0 = time.time()
    done = fail = zips = 0
    archives = sorted(os.path.basename(d) for d in g.glob(os.path.join(RAW, "*_tex")))
    for arch in archives:
        if archive_filter and archive_filter not in arch:
            continue
        outdir = os.path.join(OUT, arch)
        os.makedirs(outdir, exist_ok=True)
        files = sorted(g.glob(os.path.join(RAW, arch, "*.bin")))
        ok = 0
        for f in files:
            base = os.path.basename(f)
            name = base
            for suf in (".tga.bin", ".bin", ".tga"):
                if name.lower().endswith(suf):
                    name = name[: -len(suf)]
                    break
            try:
                with open(f, "rb") as fh:
                    head = fh.read(4)
                if head[:2] == b"PK":  # SPLIT stream continuation zip
                    zips += 1
                    rows.append(dict(archive=arch, name=name, w=0, h=0, bpp=0,
                                     fmt="ZIP_SPLIT", flags=0, mips=0,
                                     png="", src=base))
                    continue
                img, info, fmt = convert_file(f)
                png = os.path.join(outdir, name + ".png")
                img.save(png, compress_level=6)
                rows.append(dict(archive=arch, name=name, w=info["w"], h=info["h"],
                                 bpp=info["bpp"], fmt=fmt, flags=hex(info["flags"]),
                                 mips=info["mips"], png=png, src=base))
                ok += 1
            except Exception as e:
                fail += 1
                rows.append(dict(archive=arch, name=name, w=0, h=0, bpp=0,
                                 fmt=f"FAIL:{e}", flags=0, mips=0, png="", src=base))
        done += ok
        print(f"[{arch}] converted={ok}/{len(files)} total_done={done} "
              f"fail={fail} elapsed={time.time()-t0:.0f}s", flush=True)

    with open(os.path.join(OUT, "_textures_manifest.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nDONE: {done} textures converted, {zips} zip-splits kept raw, "
          f"{fail} failures. manifest -> {OUT}/_textures_manifest.csv", flush=True)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "probe":
        probe()
    elif len(sys.argv) > 1 and sys.argv[1] == "all":
        full_run(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
