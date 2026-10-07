#!/usr/bin/env python3
"""Export showcase GLBs for the browser viewer (Y-up, textures embedded)."""
import sys, os
sys.path.insert(0, '/home/z/my-project/scripts')
from bdae_extract import parse_meshes, write_glb

RAW = '/home/z/my-project/download/TDKR_assets/raw'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png'
OUTS = ['/home/z/my-project/public/models', '/home/z/my-project/download/TDKR_assets/meshes_glb']
for o in OUTS:
    os.makedirs(o, exist_ok=True)

SET = [
    ('gotham-island1',  f'{RAW}/l_gothamcity/GC_island1_LongDist.bdae.bin',      f'{PNG}/l_gothamcity_tex/GC_Island1_LongDist_Low.png'),
    ('gotham-island2',  f'{RAW}/l_gothamcity/GC_Island2_LongDist.bdae.bin',      f'{PNG}/l_gothamcity_tex/GC_Island2_LongDist_low.png'),
    ('gotham-roads2',   f'{RAW}/l_gothamcity/GC_LongDist_Island2_Roads.bdae.bin',f'{PNG}/l_gothamcity_tex/GC_LongDist_Island2_Roads.png'),
    ('gotham-bigbridge',f'{RAW}/l_gothamcity/GC_Bigbridge.bdae.bin',             f'{PNG}/l_gothamcity_tex/bridge_1.png'),
    ('batarang',        f'{RAW}/actors/Batarang.bdae.bin',                       f'{PNG}/actors_tex/Batarang.png'),
]
for name, src, tex in SET:
    meshes = parse_meshes(src, verbose=False)
    if not meshes:
        print(f'!! {name}: no meshes')
        continue
    tv = sum(m['count'] for m in meshes)
    tt = sum(m['numIdx'] // 3 for m in meshes)
    bb_min = [float(min(m['pos'][:, i].min() for m in meshes)) for i in range(3)]
    bb_max = [float(max(m['pos'][:, i].max() for m in meshes)) for i in range(3)]
    texname = os.path.basename(tex) if os.path.exists(tex) else None
    for out in OUTS:
        write_glb(meshes, tex, os.path.join(out, name + '.glb'), name)
    size = os.path.getsize(os.path.join(OUTS[0], name + '.glb'))
    print(f'{name}: {len(meshes)} meshes {tv}v {tt}t bounds=({bb_min[0]:.0f},{bb_min[1]:.0f},{bb_min[2]:.0f})..({bb_max[0]:.0f},{bb_max[1]:.0f},{bb_max[2]:.0f}) tex={texname} glb={size//1024}KB')
