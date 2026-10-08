#!/usr/bin/env python3
"""Overlay a mesh's UV0 wireframe on FULL bake pages (all candidate pages),
to locate which page (and where) actually matches the mesh's UV layout."""
import json, os, sys, glob
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from probe_uv1 import parse_meshes_uv1, TMP

PAGES = '/home/z/my-project/download/TDKR_assets/pages'
OUT = '/tmp/uv_fullpage'
S = 1024
PX = 2048

MESH = sys.argv[1] if len(sys.argv) > 1 else 'gc_footprint_ca'
PAGES_WANT = sys.argv[2:] or ['BakeGroup_Island1_A0', 'BakeGroup_Island1_B0',
                              'GC_LongDist_Island1_FP1', 'GC_LongDist_Island1_FP2',
                              'GC_LongDist_Island1_FP3']


def main():
    os.makedirs(OUT, exist_ok=True)
    path = None
    for c in os.listdir(TMP):
        stem = c[:-5].lower()
        if stem in (MESH, MESH + '_longdist'):
            path = os.path.join(TMP, c); break
    if not path:
        print('pull chunk first'); return
    ms = [m for m in parse_meshes_uv1(path) if m['count'] > 20]
    m = ms[0]
    for page in PAGES_WANT:
        fp = os.path.join(PAGES, page + '.png')
        if not os.path.exists(fp):
            print('page missing:', page); continue
        pg = Image.open(fp).convert('RGB').resize((S, S), Image.LANCZOS)
        dr = ImageDraw.Draw(pg)
        tri = m['uv0'][m['idx']].reshape(-1, 3, 2) * S
        for t in tri:
            dr.line([tuple(p) for p in t] + [tuple(t[0])], fill=(255, 90, 40), width=1)
        out = os.path.join(OUT, f'{MESH}_on_{page}.png')
        pg.save(out)
        print('wrote', out)


if __name__ == '__main__':
    main()
