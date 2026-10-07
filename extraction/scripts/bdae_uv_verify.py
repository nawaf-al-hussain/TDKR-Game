#!/usr/bin/env python3
"""Verify UV + texture binding: render island1 mesh with vertex colors sampled
from GC_Island1_LongDist_Low.png at the decoded UVs."""
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
from bdae_extract import parse_meshes

tex = Image.open('/home/z/my-project/download/TDKR_assets/textures_png/l_gothamcity_tex/GC_Island1_LongDist_Low.png').convert('RGB')
tw, th = tex.size
tpx = np.asarray(tex, np.uint8)
print('texture', tex.size)

meshes = parse_meshes('/home/z/my-project/download/TDKR_assets/raw/l_gothamcity/GC_island1_LongDist.bdae.bin', verbose=False)
fig, axes = plt.subplots(1, 2, figsize=(18, 9), constrained_layout=True)
for ax, (i, j) in zip(axes, ((0, 1), (0, 2))):  # top view then side
    for m in meshes:
        u = (m['uv'][:, 0] * (tw - 1)).astype(np.int32).clip(0, tw - 1)
        v = (m['uv'][:, 1] * (th - 1)).astype(np.int32).clip(0, th - 1)
        cols = tpx[th - 1 - v, u] / 255.0
        ax.scatter(m['pos'][:, i], m['pos'][:, j], s=1.2, c=cols, alpha=0.85)
    ax.set_aspect('equal'); ax.grid(alpha=0.15)
axes[0].set_title('island1_LongDist — textured top view (UV->GC_Island1_LongDist_Low.png)')
axes[1].set_title('side view (textured)')
fig.savefig('/home/z/my-project/download/TDKR_assets/probe/meshes/island1_textured.png', dpi=115)
print('saved')
