#!/usr/bin/env python3
"""s54 T4 step 1b: densest windows + world mapping. Sign conventions:
world x = (px - W/2)/scale + xm ; world z = zm - (py - H/2)/scale (page/CPU fit)."""
import numpy as np
from PIL import Image
import subprocess

# get scale/xm/zm from the CPU script (it prints the AABB line)
out = subprocess.run(['/home/z/.venv/bin/python3',
                      '/tmp/my-project/work/TDKR-Game/extraction/re/session52/s52_t1_cpu.py',
                      '--flat', '--zbuf', '--snap', '--only', 'LightMapDC',
                      '--out', '/tmp/aabb_probe'],
                     capture_output=True, text=True, timeout=560)
line = [l for l in out.stdout.splitlines() if 'AABB' in l]
print('AABB line:', line)
x0, x1, z0, z1, scale = None, None, None, None, None
if line:
    parts = line[0].split()
    x0 = float(parts[1][1:].split('[')[0]) if False else None
    # parse 'AABB x[-a b] z[-c d] scale s'
    import re
    m = re.match(r'AABB x\[(-?[\d.]+) (-?[\d.]+)\] z\[(-?[\d.]+) (-?[\d.]+)\] scale ([\d.]+)', line[0])
    x0, x1, z0, z1, scale = [float(m.group(i)) for i in range(1, 6)]
xm, zm = (x0 + x1) / 2, (z0 + z1) / 2
W, H = 1024, 605

for fx in ('StandardDiffuseDC', 'AlphaMasking'):
    im = np.asarray(Image.open('/tmp/my-project/work/city_slice_wt/playable/s53_lab_%s.png' % fx).convert('L'))
    mask = im >= 128
    ys, xs = np.where(mask)
    best = (0, 0, 0)
    S = 256
    for wy in range(0, H - S, 32):
        for wx in range(0, W - S, 32):
            c = int(mask[wy:wy + S, wx:wx + S].sum())
            if c > best[0]:
                best = (c, wx, wy)
    c, wx, wy = best
    # window center in world coords
    cx_px, cy_px = wx + S / 2, wy + S / 2
    wx_world = (cx_px - W / 2) / scale + xm
    wz_world = zm - (cy_px - H / 2) / scale
    half = (S / 2) / scale * 1.15   # 15% margin
    print('%s: %d px total; densest %dx%d = %d px at screen(%d,%d) -> world window x[%.1f %.1f] z[%.1f %.1f]'
          % (fx, len(xs), S, S, c, wx, wy, wx_world - half, wx_world + half, wz_world - half, wz_world + half))
