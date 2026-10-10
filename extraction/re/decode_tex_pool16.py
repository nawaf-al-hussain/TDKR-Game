#!/usr/bin/env python3
"""Session 16: rebuild the textures_png pool from the .gla texture chunks.

Chunk formats seen in raw/l_gothamcity_tex + raw/commons_tex:
  - PK zip-split (rgb.pvr + alpha.pvr members)   -> tex_split_convert logic
  - PVR v1 wrapper [u32 hdrSize=52][h][w][mips][fcc][dsize][bpp]
    payload = d[hdrSize : hdrSize+dsize]          -> ETC2/PVRTC by bpp+fcc

Decoder selection is EMPIRICAL per (bpp, fcc): decode one calibration page
both ways, compare row-profile correlation with the deployed gh-pages JPG,
and lock the mapping for the whole pool. Saves textures_png/<arch>/<stem>.png
(same paths find_png() expects).
"""
import io
import os
import struct
import sys
import zipfile

import numpy as np
import texture2ddecoder as t2d
from PIL import Image

RAW = "/home/z/my-project/download/TDKR_assets/raw"
OUT = "/home/z/my-project/download/TDKR_assets/textures_png"
GHP_TEX = "/home/z/my-project/repo/gh-pages/models/tex"

ARCHIVES = ["l_gothamcity_tex", "commons_tex"]


def pvr_v1(path):
    d = open(path, "rb").read()
    hs, h, w, mips, fcc, dsize, bpp = struct.unpack_from("<IIIIIII", d, 0)
    if hs == 52 and dsize <= len(d) - hs:
        return dict(h=h, w=w, mips=mips, fcc=fcc, dsize=dsize, bpp=bpp,
                    payload=d[hs:hs + dsize])
    return None


def decode_etc2_rgb(p, w, h):
    out = t2d.decode_etc2(p, w, h)
    return Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")


def decode_etc2_rgba(p, w, h):
    out = t2d.decode_etc2a8(p, w, h)
    return Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")


def decode_pvrtc4(p, w, h):
    out = t2d.decode_pvrtc(p, w, h, False)
    return Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")


def decode_pvrtc2(p, w, h):
    out = t2d.decode_pvrtc(p, w, h, True)
    return Image.frombytes("RGBA", (w, h), bytes(out), "raw", "BGRA")


def decode_rgb565(p, w, h):
    a = np.frombuffer(p[:w * h * 2], "<u2").reshape(h, w)
    r = ((a >> 11) & 0x1F).astype(np.uint8)
    g = ((a >> 5) & 0x3F).astype(np.uint8)
    b = (a & 0x1F).astype(np.uint8)
    rgb = np.dstack([r * 255 // 31, g * 255 // 63, b * 255 // 31])
    return Image.frombytes("RGB", (w, h), rgb.tobytes())


def decode_rgb888(p, w, h):
    a = np.frombuffer(p[:w * h * 3], np.uint8).reshape(h, w, 3)
    return Image.frombytes("RGB", (w, h), a.tobytes())


def decode_rgba8888(p, w, h):
    a = np.frombuffer(p[:w * h * 4], np.uint8).reshape(h, w, 4)
    return Image.frombytes("RGBA", (w, h), a.tobytes())


def profile(img, size=64):
    g = np.asarray(img.convert("L").resize((size, size), Image.BILINEAR),
                   np.float32) / 255.0
    return g


def row_profile(img):
    g = np.asarray(img.convert("L"), np.float32) / 255.0
    return g.mean(1)


def pick_decoder(chunks, stem):
    """Decode `stem` both ways, compare with deployed JPG row profile."""
    dep = os.path.join(GHP_TEX, stem + ".jpg")
    if not os.path.exists(dep):
        dep = None
    rows = {}
    if dep:
        ref = np.asarray(Image.open(dep).convert("L"), np.float32) / 255.0
        ref = np.interp(np.linspace(0, 1, ref.shape[0]),
                        np.linspace(0, 1, 64), ref.mean(1) if False else ref.mean(1))
        # deployed jpg row means at 64 samples
        rimg = Image.open(dep).convert("L").resize((32, 64), Image.BILINEAR)
        ref = np.asarray(rimg, np.float32).mean(1) / 255.0
    results = {}
    for name, fn in (("etc2", decode_etc2_rgb), ("pvrtc4", decode_pvrtc4)):
        img = fn(*chunks[name])
        pr = np.asarray(img.convert("L").resize((32, 64), Image.BILINEAR),
                        np.float32).mean(1) / 255.0
        results[name] = (float(np.corrcoef(pr, ref)[0, 1]) if dep else -1.0,
                         float(pr.mean()))
    return results


def decode_chunk(path, sel):
    head = open(path, "rb").read(4)
    if head[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(open(path, "rb").read()))
        rgb = alpha = None
        info = None
        for n in z.namelist():
            if n.endswith("rgb.pvr"):
                rgb, info, fmt = decode_pvr2(z.read(n))
            elif n.endswith("alpha.pvr"):
                alpha = decode_pvr2(z.read(n))[0]
        if rgb is None:
            return None, "pk-no-rgb"
        if alpha is not None and info["w"] == alpha.info.get("w", info["w"]):
            a = alpha.convert("L")
            if a.size == rgb.size:
                rgb = rgb.convert("RGBA")
                rgb.putalpha(a)
        return rgb.convert("RGB"), "pk"
    info = pvr_v1(path)
    if info is None:
        return None, "unrecognized"
    w, h = info["w"], info["h"]
    key = (info["bpp"], info["fcc"] if info["fcc"] < 256 else "big")
    raw_fn = {(16, 0x13): decode_rgb565, (24, 0x15): decode_rgb888,
              (32, 0x12): decode_rgba8888}.get(key)
    if raw_fn is not None:
        try:
            return raw_fn(info["payload"], info["w"], info["h"]).convert("RGB"), f"raw{key[0]}"
        except Exception as e:
            return None, f"raw-decode-fail {e}"
    fn = sel.get(key)
    if fn is None:
        return None, f"no-decoder bpp={info['bpp']} fcc={info['fcc']:#x}"
    try:
        img = fn(info["payload"], w, h)
    except Exception as e:
        return None, f"decode-fail {e}"
    return img.convert("RGB"), "pvr"


def decode_pvr2(buf):
    """PVR! v2 inside zip-split members (from tex_convert.parse_pvr2)."""
    hs, hgt, wid, mips, flags, dsz, bpp, mr, mg, mb, ma, magic, nsurf = \
        struct.unpack("<13I", buf[:52])
    if not (hs == 52 and magic == 0x21525650):
        raise ValueError(f"bad PVR2 header hs={hs} magic={magic:#x}")
    off = 52
    size0 = wid * hgt // 2 if bpp == 4 else wid * hgt
    p = buf[off:off + size0]
    if bpp == 4:
        out = t2d.decode_pvrtc(p, wid, hgt, False)
    else:
        out = t2d.decode_pvrtc(p, wid, hgt, True)
    img = Image.frombytes("RGBA", (wid, hgt), bytes(out), "raw", "BGRA")
    return img, dict(w=wid, h=hgt), f"pvrtc{bpp}"


def main():
    # ---- calibration: pick decoder per (bpp, fcc) using deployed JPGs
    sel = {}
    calib_stems = ["BakeGroup_Island1_A0", "GothamCity_Road_v1_Island_1",
                   "GC_Z1_Props_Street", "GC_Park_grass"]
    by_bpp = {}
    for stem in calib_stems:
        p = os.path.join(RAW, "l_gothamcity_tex", stem + ".tga")
        if not os.path.exists(p):
            continue
        info = pvr_v1(p)
        if info is None:
            continue
        key = (info["bpp"], info["fcc"] if info["fcc"] < 256 else "big")
        if key in by_bpp:
            continue
        by_bpp[key] = (stem, (info["payload"], info["w"], info["h"]))
    for key, (stem, args) in by_bpp.items():
        dep = os.path.join(GHP_TEX, stem + ".jpg")
        if os.path.exists(dep):
            rimg = Image.open(dep).convert("L").resize((32, 64), Image.BILINEAR)
            ref = np.asarray(rimg, np.float32).mean(1) / 255.0
        else:
            ref = None
        scores = {}
        for name, fn in (("etc2", decode_etc2_rgb), ("pvrtc4", decode_pvrtc4)):
            try:
                img = fn(*args)
            except Exception as e:
                scores[name] = -9.0
                continue
            pr = np.asarray(img.convert("L").resize((32, 64), Image.BILINEAR),
                            np.float32).mean(1) / 255.0
            scores[name] = (float(np.corrcoef(pr, ref)[0, 1])
                            if ref is not None else -1.0)
        best = max(scores, key=scores.get)
        sel[key] = {"etc2": decode_etc2_rgb, "pvrtc4": decode_pvrtc4,
                    "etc2a8": decode_etc2_rgba, "pvrtc2": decode_pvrtc2}[best]
        print(f"calib bpp={key[0]} fcc={key[1]} [{stem}]: {scores} -> {best}")

    # ---- batch decode
    ok = fail = skip = 0
    for arch in ARCHIVES:
        outdir = os.path.join(OUT, arch)
        os.makedirs(outdir, exist_ok=True)
        for fn in sorted(os.listdir(os.path.join(RAW, arch))):
            stem = fn[:-4] if fn.endswith(".tga") else fn[:-4]
            out_png = os.path.join(outdir, stem + ".png")
            if os.path.exists(out_png):
                skip += 1
                continue
            img, how = decode_chunk(os.path.join(RAW, arch, fn), sel)
            if img is None:
                print(f"[FAIL] {arch}/{fn}: {how}")
                fail += 1
                continue
            img.save(out_png)
            ok += 1
    print(f"DONE: {ok} decoded, {fail} failed, {skip} skipped")


if __name__ == "__main__":
    main()
