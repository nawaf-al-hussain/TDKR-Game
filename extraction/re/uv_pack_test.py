#!/usr/bin/env python3
"""Test candidate Coord1 packings per dword-column (+16/+20/+24): rasterize mesh
triangles under each candidate UV into the assigned tile; side-by-side panels."""
import struct, sys, os, json
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/scripts')
from bdae_extract import parse_first_block

RECS = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions_v2.json'
PAGES = '/home/z/my-project/download/TDKR_assets/pages'
PX = 2048
S = 512


def load(path):
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    blk = parse_first_block(d, h[10])
    _, count, ndw, stride, start, footer, maxIdx, numIdx = blk
    extra = []
    for i in range(count):
        o = start + i * stride
        dws = [struct.unpack_from('<I', d, o + f)[0]
               for f in (16, 20, 24) if o + f + 4 <= start + (i + 1) * stride]
        extra.append(dws)
    s0 = footer + 0x14
    e = d.index(b'\0', s0)
    idx_off = s0 + ((e - s0 + 1 + 3) & ~3)
    idx = np.frombuffer(d, np.uint16, numIdx, idx_off).astype(np.uint32)
    return np.array(extra, np.uint32), idx


def cand_uvs(dw_col):
    """all candidate (u,v) decodings for one dword column."""
    u16lo = (dw_col & 0xFFFF).astype(np.float32)
    u16hi = ((dw_col >> 16) & 0xFFFF).astype(np.float32)
    b0 = (dw_col & 0xFF).astype(np.float32)
    b1 = ((dw_col >> 8) & 0xFF).astype(np.float32)
    b2 = ((dw_col >> 16) & 0xFF).astype(np.float32)
    out = {
        'u16pair/65535': np.stack([u16lo, u16hi], 1) / 65535.0,
        'b0b1/255': np.stack([b0, b1], 1) / 255.0,
        'b0b2/255': np.stack([b0, b2], 1) / 255.0,
        'u16lo+b2': np.stack([u16lo / 65535.0, b2 / 255.0], 1),
        'u16lo+b1': np.stack([u16lo / 65535.0, b1 / 255.0], 1),
    }
    return out


def main():
    mesh = sys.argv[1] if len(sys.argv) > 1 else 'gc_footprint_ca'
    recs = json.load(open(RECS))
    r = [x for x in recs if x.get('mesh') == mesh][0]
    page = (r['page'] or '').replace('.tga', '')
    su, sv, ou, ov = r['so1']
    path = None
    for c in os.listdir('/tmp/uv1_probe'):
        if c[:-5].lower() in (mesh, mesh + '_longdist'):
            path = os.path.join('/tmp/uv1_probe', c)
    dws, idx = load(path)
    pg = Image.open(os.path.join(PAGES, page + '.png')).convert('RGB')
    t0 = (int(round(ou * PX)), int(round(ov * PX)))
    tw, th = max(2, int(round(su * PX))), max(2, int(round(sv * PX)))
    crop = pg.crop((t0[0], t0[1], t0[0] + tw, t0[1] + th)).resize((S, S), Image.NEAREST)
    panels = []
    for ci, cname in enumerate(('+16', '+20', '+24')[:dws.shape[1]]):
        for name, uv in cand_uvs(dws[:, ci]).items():
            im = crop.copy()
            dr = ImageDraw.Draw(im)
            tri = uv[idx].reshape(-1, 3, 2)
            tri = (tri * [su, sv] + [ou, ov] - np.array(t0) / PX) / [su, sv] * S
            for t in tri:
                dr.line([tuple(p) for p in t] + [tuple(t[0])], fill=(255, 90, 40), width=1)
            panels.append((f'{cname}:{name}', im))
    cols = 4
    rows = (len(panels) + cols - 1) // cols
    combo = Image.new('RGB', ((S // 2 + 6) * cols, (S // 2 + 6) * rows), (12, 12, 12))
    cd = ImageDraw.Draw(combo)
    for i, (name, im) in enumerate(panels):
        x, y = (i % cols) * (S // 2 + 6), (i // cols) * (S // 2 + 6)
        combo.paste(im.resize((S // 2, S // 2), Image.NEAREST), (x, y + 12))
        cd.text((x + 4, y + 1), name, fill=(255, 255, 0))
    out = f'/tmp/uv_pack_{mesh}.png'
    combo.save(out)
    print('wrote', out, len(panels), 'panels')


if __name__ == '__main__':
    main()
