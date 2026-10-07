#!/usr/bin/env python3
"""
Build contact sheets (thumbnail grids) per texture archive + a skybox highlight sheet.
Private research use.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
OUT = "/home/z/my-project/download/TDKR_assets/contact_sheets"
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
THUMB = 128
COLS = 10
PAD = 6


def font(sz):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def sheet(paths, out, title, thumb=THUMB, cols=COLS):
    from PIL import ImageOps
    rows = (len(paths) + cols - 1) // cols
    W = cols * (thumb + PAD) + PAD
    H = rows * (thumb + PAD + 14) + PAD + 30
    im = Image.new("RGB", (W, H), (18, 18, 22))
    d = ImageDraw.Draw(im)
    d.text((PAD, 6), title, fill=(240, 240, 240), font=font(18))
    f = font(10)
    y0 = 30
    for i, p in enumerate(paths):
        r, c = divmod(i, cols)
        x = PAD + c * (thumb + PAD)
        y = y0 + r * (thumb + PAD + 14)
        try:
            t = Image.open(p).convert("RGB")
            t.thumbnail((thumb, thumb))
            t = ImageOps.contain(t, (thumb, thumb))
            im.paste(t, (x + (thumb - t.width) // 2, y + (thumb - t.height) // 2))
        except Exception as e:
            d.rectangle([x, y, x + thumb, y + thumb], outline=(120, 40, 40))
            d.text((x + 4, y + 4), "ERR", fill=(255, 80, 80), font=f)
        label = os.path.splitext(os.path.basename(p))[0][:22]
        d.text((x, y + thumb + 1), label, fill=(180, 180, 180), font=f)
    im.save(out)
    print(f"{out}  ({len(paths)} thumbs, {im.width}x{im.height})")


def main():
    os.makedirs(OUT, exist_ok=True)
    archives = sorted(os.path.basename(d) for d in glob.glob(os.path.join(PNG, "*_tex")))
    for arch in archives:
        pngs = sorted(glob.glob(os.path.join(PNG, arch, "*.png")))
        if not pngs:
            continue
        sheet(pngs, os.path.join(OUT, f"{arch}.jpg"), f"{arch}  ({len(pngs)} textures)")

    # skybox highlight sheet
    sky = []
    for p in sorted(glob.glob(os.path.join(PNG, "*", "*.png"))):
        n = os.path.basename(p).lower()
        if "sky" in n or "envmap" in n or "fog" in n:
            sky.append(p)
    if sky:
        sheet(sky, os.path.join(OUT, "_SKYBOXES_and_ENV.jpg"),
              f"Gotham City & level skyboxes / envmaps ({len(sky)})", thumb=256, cols=4)


if __name__ == "__main__":
    main()
