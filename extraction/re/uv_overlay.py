#!/usr/bin/env python3
"""Overlay mesh UV0*so1 wireframe on the assigned tile crop of the bake page.
If the binding is right, UV islands align with facade content (window blocks).
Outputs side-by-side PNGs per record to /tmp/uv_overlay/."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from probe_uv1 import parse_meshes_uv1, TMP

RECS = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions_v2.json'
PAGES = '/home/z/my-project/download/TDKR_assets/pages'
OUT = '/tmp/uv_overlay'
PX = 2048

WANT = sys.argv[1:] or ['gc_footprint_ca', 'gc_footprint_vc', 'gc_footprint_gf',
                        'gc_footprint_la', 'gc_footprint_zd']


def main():
    os.makedirs(OUT, exist_ok=True)
    recs = json.load(open(RECS))
    bym = {}
    for r in recs:
        bym.setdefault(r.get('mesh'), []).append(r)
    for mesh in WANT:
        rs = bym.get(mesh)
        if not rs:
            print('no record for', mesh); continue
        r = rs[0]
        page = (r['page'] or '').replace('.tga', '')
        su, sv, ou, ov = r['so1']
        # find chunk
        import glob
        cands = glob.glob(os.path.join(TMP, '*.bdae'))
        path = None
        for c in cands:
            stem = os.path.basename(c)[:-5].lower()
            if stem == mesh or stem == mesh + '_longdist':
                path = c; break
        if path is None:
            print('chunk not pulled for', mesh); continue
        ms = parse_meshes_uv1(path)
        pg = Image.open(os.path.join(PAGES, page + '.png')).convert('RGB')
        # tile rect in px
        t0u, t0v = int(ou * PX), int(ov * PX)
        tw, th = int(su * PX), int(sv * PX)
        crop = pg.crop((t0u, t0v, t0u + tw, t0v + th)).resize((512, 512), Image.NEAREST)
        for mi, m in enumerate(ms[:2]):
            ov_im = crop.copy()
            dr = ImageDraw.Draw(ov_im)
            tri = (m['uv0'][m['idx']].reshape(-1, 3, 2) *
                   np.array([su, sv]) + np.array([ou, ov]) -
                   np.array([ou, ov])) * 512  # uv within tile, scaled to 512
            for t in tri:
                dr.line([tuple(p) for p in t] + [tuple(t[0])], fill=(255, 80, 40), width=1)
            combo = Image.new('RGB', (1034, 512), (20, 20, 20))
            combo.paste(crop, (0, 0)); combo.paste(ov_im, (522, 0))
            name = f'{mesh}_m{mi}_{page}.png'
            combo.save(os.path.join(OUT, name))
            print('wrote', name, f'tile@({t0u},{t0v}) {tw}x{th} verts={m["count"]}')


if __name__ == '__main__':
    main()
