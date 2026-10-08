#!/usr/bin/env python3
"""Within-tile dihedral flip test: crop the assigned tile, render mesh UV0*so1
wireframe over 4 orientations (id, flipV, flipU, flipUV), score each by
edge-weighted coverage, and save a 2x2 combo image per record."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from probe_uv1 import parse_meshes_uv1, TMP

RECS = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions_v2.json'
PAGES = '/home/z/my-project/download/TDKR_assets/pages'
OUT = '/tmp/uv_flip'
PX = 2048
S = 512

WANT = sys.argv[1:] or ['gc_footprint_ca', 'gc_footprint_vc', 'gc_footprint_gf',
                        'gc_footprint_zd', 'gc_footprint_gd']


def edges_of(gray):
    gx = np.zeros_like(gray); gy = np.zeros_like(gray)
    gx[:, 1:-1] = gray[:, 2:] - gray[:, :-2]
    gy[1:-1, :] = gray[2:, :] - gray[:-2, :]
    return np.hypot(gx, gy)


def main():
    os.makedirs(OUT, exist_ok=True)
    recs = json.load(open(RECS))
    bym = {}
    for r in recs:
        bym.setdefault(r.get('mesh'), r)
    for mesh in WANT:
        r = bym.get(mesh)
        if not r:
            print('no record', mesh); continue
        page = (r['page'] or '').replace('.tga', '')
        su, sv, ou, ov = r['so1']
        path = None
        for c in os.listdir(TMP):
            stem = c[:-5].lower()
            if stem in (mesh, mesh + '_longdist'):
                path = os.path.join(TMP, c); break
        if not path:
            print('chunk missing', mesh); continue
        ms = [m for m in parse_meshes_uv1(path) if m['count'] > 20]
        if not ms:
            print('no meshes', mesh); continue
        m = ms[0]
        pg = Image.open(os.path.join(PAGES, page + '.png')).convert('RGB')
        t0u, t0v = int(round(ou * PX)), int(round(ov * PX))
        tw, th = max(2, int(round(su * PX))), max(2, int(round(sv * PX)))
        crop = pg.crop((t0u, t0v, t0u + tw, t0v + th))
        crop_e = edges_of(np.asarray(crop.convert('L'), np.float32) / 255.0)
        # mesh uv in tile space [0..1]
        uv_t = (m['uv0'] - [ou, ov]) / [su, sv] if False else (m['uv0'] * [su, sv] + [ou, ov] - [ou, ov]) / [su, sv]
        uv_t = ((m['uv0'] * np.array([su, sv]) + np.array([ou, ov])) -
                np.array([t0u / PX, t0v / PX])) / np.array([su, sv])
        panels = []
        scores = {}
        for tag in ('id', 'fV', 'fU', 'fUV'):
            u, v = uv_t[:, 0], uv_t[:, 1]
            if 'V' in tag[1:]:
                v = 1.0 - v
            if 'U' in tag[1:]:
                u = 1.0 - u
            im = crop.resize((S, S), Image.NEAREST).copy()
            dr = ImageDraw.Draw(im)
            tri = np.stack([u, v], 1)[m['idx']].reshape(-1, 3, 2) * S
            for t in tri:
                dr.line([tuple(p) for p in t] + [tuple(t[0])], fill=(255, 90, 40), width=1)
            panels.append(im)
            # score: rasterize mask, mean content edge inside
            mask = Image.new('L', (tw, th), 0)
            drm = ImageDraw.Draw(mask)
            for t in (np.stack([u, v], 1)[m['idx']].reshape(-1, 3, 2) * [tw, th]):
                drm.polygon([tuple(p) for p in t], fill=255)
            mk = np.asarray(mask) > 0
            scores[tag] = round(float(crop_e[mk].mean() / (crop_e.mean() + 1e-9)), 2) if mk.any() else 0.0
        combo = Image.new('RGB', (S * 2 + 12, S * 2 + 12), (15, 15, 15))
        for i, (tag, im) in enumerate(zip(('id', 'fV', 'fU', 'fUV'), panels)):
            combo.paste(im, ((i % 2) * (S + 8) + 4, (i // 2) * (S + 8) + 4))
        combo.save(os.path.join(OUT, f'{mesh}_{page}.png'))
        print(mesh, page, f'tile@({t0u},{t0v}) {tw}x{th}', scores)


if __name__ == '__main__':
    main()
