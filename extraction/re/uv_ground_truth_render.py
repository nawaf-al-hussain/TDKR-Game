#!/usr/bin/env python3
"""GROUND-TRUTH visual test: draw the bdae mesh triangles textured with its own
bake page, straight UV -> image, no transforms. If the game's binding is
self-consistent we get a coherent mini-city picture; smears = wrong stream.

Tries both V orientations for each stream and saves a comparison sheet.
"""
import sys, os
import numpy as np
from PIL import Image

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from bdae_extract import parse_meshes

RAW = '/home/z/my-project/download/TDKR_assets/raw/l_gothamcity'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png/l_gothamcity_tex'
OUT = '/home/z/my-project/work/TDKR-Game/extraction/re/uvgt'
os.makedirs(OUT, exist_ok=True)

def render(mesh, tex, stream, vflip, out, S=3):
    uv = np.asarray(stream, np.float64).reshape(-1, 2).copy()
    if vflip:
        uv[:, 1] = 1.0 - uv[:, 1]
    W, H = tex.size
    uv[:, 0] = np.clip(uv[:, 0], 0, 1) * (W - 1)
    uv[:, 1] = np.clip(uv[:, 1], 0, 1) * (H - 1)
    # rasterize triangles by barycentric sampling at supersample grid
    idx = np.asarray(mesh['idx'], np.int64).reshape(-1, 3)
    # bounding box in px (page space)
    xs, ys = uv[:, 0], uv[:, 1]
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    # render at S x page resolution
    canvas = np.zeros(((y1 - y0), (x1 - x0), 3), np.float32) + 0.05
    cov = np.zeros(((y1 - y0), (x1 - x0)), bool)
    tp = np.flipud(np.asarray(tex, np.float32)[:, :, :3] / 255.0)  # row0 = v=1 (bottom) -> flip so y index = v
    for t in idx:
        p = uv[t]  # 3x2 px coords
        mn = np.floor(p.min(0)).astype(int); mx = np.ceil(p.max(0)).astype(int)
        mn[0] = max(mn[0] - 1, x0); mx[0] = min(mx[0] + 2, x1)
        mn[1] = max(mn[1] - 1, y0); mx[1] = min(mx[1] + 2, y1)
        if mx[0] <= mn[0] or mx[1] <= mn[1]:
            continue
        gx, gy = np.meshgrid(np.arange(mn[0], mx[0]) + 0.5, np.arange(mn[1], mx[1]) + 0.5)
        a, b, c = p[0], p[1], p[2]
        det = (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
        if abs(det) < 1e-9:
            continue
        w1 = ((gx-a[0])*(c[1]-a[1]) - (gy-a[1])*(c[0]-a[0])) / det
        w2 = ((b[0]-a[0])*(gy-a[1]) - (b[1]-a[1])*(gx-a[0])) / det
        w0 = 1.0 - w1 - w2
        m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not m.any():
            continue
        yy = gy[m].astype(int) - y0; xx = gx[m].astype(int) - x0
        sx = gx[m].astype(int); sy = gy[m].astype(int)
        sx = np.clip(sx, 0, W-1); sy = np.clip(sy, 0, H-1)
        # tp indexed [row, col] with row = v (after flip: row = (1-v)*H -> sy IS row)
        canvas[yy, xx] = tp[sy, sx]
        cov[yy, xx] = True
    img = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8))
    img = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    img.save(out)
    print(f'{out}  cov={cov.mean():.1%} size={img.size}')

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else 'GC_LongDist_Island1_FP1'
    tex_path = os.path.join(PNG, name + '.png')
    tex = Image.open(tex_path)
    print('page:', tex_path, tex.size)
    ms = parse_meshes(os.path.join(RAW, name + '.bdae'), verbose=False)
    mesh = max(ms, key=lambda m: m['count'])
    print('mesh: verts', mesh['count'], 'stride', mesh['stride'])
    stream = mesh.get('uv')
    if stream is None:
        stream = mesh.get('uvm')
    render(mesh, tex, stream, vflip=False, out=os.path.join(OUT, f'{name}_uv_noflip.png'))
    render(mesh, tex, stream, vflip=True,  out=os.path.join(OUT, f'{name}_uv_flip.png'))

if __name__ == '__main__':
    main()
