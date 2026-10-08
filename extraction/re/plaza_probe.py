#!/usr/bin/env python3
"""Decisive V-convention test: render only triangles whose UVs fall in the
plaza bbox. Correct convention -> recognizable circular plaza drawn cleanly.
Wrong convention -> the same UV region contains unrelated fragments.
"""
import sys, os
import numpy as np
from PIL import Image

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from bdae_extract import parse_meshes

RAW = '/home/z/my-project/download/TDKR_assets/raw/l_gothamcity'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png/l_gothamcity_tex'
OUT = '/home/z/my-project/work/TDKR-Game/extraction/re/uvgt'

name = 'GC_LongDist_Island1_FP1'
page = Image.open(os.path.join(PNG, name + '.png')).convert('RGB')
W, H = page.size
px = np.asarray(page)  # row 0 = image top (y down)

# plaza bbox in image coords
bx0, bx1, by0, by1 = 1220, 1468, 708, 956

ms = parse_meshes(os.path.join(RAW, name + '.bdae'), verbose=False)

def render_region(mode, out):
    """mode 'gl'  : v=0 bottom  -> image y = H-1-v
       mode 'top': v=0 top    -> image y = v"""
    canvas = np.zeros((248, 248, 3), np.float32)
    cov = np.zeros((248, 248), bool)
    for mesh in ms:
        s = mesh.get('uv') if mesh.get('uv') is not None else mesh.get('uvm')
        uv = np.asarray(s, np.float64).reshape(-1, 2)
        idx = np.asarray(mesh['idx'], np.int64).reshape(-1, 3)
        for t in idx:
            p = uv[t]
            # triangle uv bbox
            umn, umx = p.min(0), p.max(0)
            if umx[0] < bx0 / W or umn[0] > bx1 / W:
                continue
            # region in v-space depends on mode
            if mode == 'gl':
                v_lo, v_hi = 1 - by1 / H, 1 - by0 / H
            else:
                v_lo, v_hi = by0 / H, by1 / H
            if umx[1] < v_lo or umn[1] > v_hi:
                continue
            # draw the triangle's interior samples that land in the plaza bbox
            a, b, c = p
            for _ in range(1):
                n = 24
                ws = np.linspace(0, 1, n)
                W1, W2 = np.meshgrid(ws, ws)
                m = (W1 + W2) <= 1
                w1, w2 = W1[m], W2[m]
                w0 = 1 - w1 - w2
                P = w0[:, None] * a + w1[:, None] * b + w2[:, None] * c
                for q in P:
                    u, v = q
                    if mode == 'gl':
                        iy = int(np.clip(H - 1 - v * H, 0, H - 1))
                    else:
                        iy = int(np.clip(v * H, 0, H - 1))
                    ix = int(np.clip(u * W, 0, W - 1))
                    if bx0 <= ix < bx1 and by0 <= iy < by1:
                        canvas[iy - by0, ix - bx0] = px[iy, ix]
                        cov[iy - by0, ix - bx0] = True
    Image.fromarray((canvas * 1).astype(np.uint8)).save(out)
    print(out, 'coverage', f'{cov.mean():.1%}')

render_region('gl', os.path.join(OUT, 'plaza_gl.png'))
render_region('top', os.path.join(OUT, 'plaza_top.png'))
