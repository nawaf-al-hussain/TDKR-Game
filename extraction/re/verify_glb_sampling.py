#!/usr/bin/env python3
"""Verify: sample deployed JPG with three.js flipY=false semantics at the NEW
(flipped) GLB UVs -> must reproduce the crisp coherent atlas render."""
import struct, json, os
import numpy as np
from PIL import Image

MODELS = '/home/z/my-project/work/TDKR-Game/gh-pages/models'

def parse_glb(path):
    d = open(path, 'rb').read()
    off = 12
    js = bc = None
    while off < len(d):
        clen, ctype = struct.unpack_from('<II', d, off)
        c = d[off+8:off+8+clen]
        if ctype == 0x4E4F534A: js = json.loads(c)
        elif ctype == 0x004E4942: bc = c
        off += 8 + clen
    return js, bc

def acc(js, bc, idx):
    a = js['accessors'][idx]
    bv = js['bufferViews'][a['bufferView']]
    dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a['componentType']]
    n = a['count']
    ncomp = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3}[a['type']]
    start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.frombuffer(bc, dtype=dt, count=n*ncomp, offset=start).reshape(n, ncomp)

name = 'GC_LongDist_Island1_FP1'
js, bc = parse_glb(os.path.join(MODELS, name + '.glb'))
tex = np.asarray(Image.open(os.path.join(MODELS, 'tex', name + '.jpg')).convert('RGB'), np.float32) / 255.0
H, W = tex.shape[:2]

# biggest primitive
prim = max(js['meshes'][0]['primitives'], key=lambda p: p['attributes'] and js['accessors'][p['attributes']['POSITION']]['count'])
uv = acc(js, bc, prim['attributes']['TEXCOORD_0']).astype(np.float64)
uv[:, 0] *= (W - 1)
uv[:, 1] *= (H - 1)
idx = acc(js, bc, prim['indices']).astype(np.int64).reshape(-1, 3)
print('prim verts', len(uv), 'tris', len(idx), 'uv range', uv.min(0).round(3), uv.max(0).round(3))

# three.js flipY=false semantics: row = v*H (v=0 = top row of the JPG)
canvas = np.zeros((H, W, 3), np.float32) + 0.05
cov = np.zeros((H, W), bool)
for t in idx:
    p = uv[t]
    mn = np.floor(p.min(0)).astype(int); mx = np.ceil(p.max(0)).astype(int)
    mn[0] = max(mn[0]-1, 0); mx[0] = min(mx[0]+2, W)
    mn[1] = max(mn[1]-1, 0); mx[1] = min(mx[1]+2, H)
    if mx[0] <= mn[0] or mx[1] <= mn[1]: continue
    gx, gy = np.meshgrid(np.arange(mn[0], mx[0])+0.5, np.arange(mn[1], mx[1])+0.5)
    a, b, c = p[0], p[1], p[2]
    det = (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
    if abs(det) < 1e-12: continue
    w1 = ((gx-a[0])*(c[1]-a[1]) - (gy-a[1])*(c[0]-a[0])) / det
    w2 = ((b[0]-a[0])*(gy-a[1]) - (b[1]-a[1])*(gx-a[0])) / det
    w0 = 1.0 - w1 - w2
    m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not m.any(): continue
    yy = gy[m].astype(int); xx = gx[m].astype(int)
    sx = np.clip(xx, 0, W-1); sy = np.clip(yy, 0, H-1)
    canvas[yy, xx] = tex[sy, sx]   # NO flip: row = v*H (three.js semantics)
    cov[yy, xx] = True
img = Image.fromarray((np.clip(canvas,0,1)*255).astype(np.uint8))
img = img.resize((img.width//3, img.height//3), Image.LANCZOS)
out = '/home/z/my-project/work/TDKR-Game/extraction/re/uvgt/verify_v10_threejs_semantics.png'
img.save(out)
print(out, 'cov', f'{cov.mean():.1%}')
