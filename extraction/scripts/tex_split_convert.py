#!/usr/bin/env python3
"""Decode TDKR ZIP_SPLIT textures: zip[SPLIT, rgb.pvr, alpha.pvr] -> merged PNG.
Reuses tex_convert.convert_file for the PVR payloads."""
import io, os, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tex_convert import decode_pvr2

RAW = "/home/z/my-project/download/TDKR_assets/raw"
OUT = "/home/z/my-project/download/TDKR_assets/textures_png"

def convert_split(path, out_png):
    z = zipfile.ZipFile(io.BytesIO(open(path, "rb").read()))
    names = z.namelist()
    rgb = alpha = None
    for n in names:
        if n.endswith("rgb.pvr"):
            rgb = decode_pvr2(z.read(n))
        elif n.endswith("alpha.pvr"):
            alpha = decode_pvr2(z.read(n))
    if rgb is None:
        raise ValueError(f"no rgb.pvr in {names}")
    img, info, fmt = rgb
    if alpha is not None and info["w"] == alpha[0].info.get("w", info["w"]):
        a = alpha[0].convert("L")
        if a.size == img.size:
            img = img.convert("RGBA")
            img.putalpha(a)
    img.save(out_png)
    return img.size, fmt

def main():
    import csv
    done = fail = 0
    for arch in sorted(os.listdir(RAW)):
        if not arch.endswith("_tex"):
            continue
        raw_dir = os.path.join(RAW, arch)
        out_dir = os.path.join(OUT, arch)
        os.makedirs(out_dir, exist_ok=True)
        for fn in sorted(os.listdir(raw_dir)):
            if not fn.endswith(".bin"):
                continue
            p = os.path.join(raw_dir, fn)
            with open(p, "rb") as fh:
                head = fh.read(4)
            if head[:2] != b"PK":
                continue
            name = fn[:-len(".bin")] if fn.endswith(".tga.bin") else fn[:-4]
            try:
                size, fmt = convert_split(p, os.path.join(out_dir, name + ".png"))
                done += 1
                print(f"[ok] {arch}/{name} {size[0]}x{size[1]} {fmt}")
            except Exception as e:
                fail += 1
                print(f"[FAIL] {arch}/{name}: {e}")
    print(f"\nDONE splits: {done} converted, {fail} failed")

if __name__ == "__main__":
    main()
