#!/usr/bin/env python3
"""Determine the true semantics of the bake-record float quads.

For each footprint bake record (mesh, page, pre-quad, post-quad) test every
candidate interpretation:
  combo: (pre-quad, runtime page) (pre, shipped) (post, runtime) (post, shipped)
  order: (u0,v0,u1,v1) | (u0,v0,du,dv) | (du,dv,u0,v0)
  flip:  none | v-flip
Score = mean edge-energy sampled at the warped UVs (bakes pack dense geometry
under the correct mapping; wrong mappings sample flat/empty areas).
"""
import json, sys, os
import numpy as np
from PIL import Image

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/scripts')
from bdae_extract import parse_meshes

PAGES = '/home/z/my-project/download/TDKR_assets/pages'
RAW = '/home/z/my-project/download/TDKR_assets/raw/l_gothamcity'
RECS = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions.json'

PAGE_IMG = {
    'BakeGroup_Island1_A0.tga': 'BakeGroup_Island1_A0.png',
    'BakeGroup_Island1_ATLAS_low0.tga': 'BakeGroup_Island1_ATLAS_low0.png',
    'BakeGroup_Island1_B0.tga': 'BakeGroup_Island1_B0.png',
    'BakeGroup_Island2_ATLAS_low0.tga': 'BakeGroup_Island2_ATLAS_low0.png',
}

def edge_map(png):
    im = np.asarray(Image.open(png).convert('L'), dtype=np.float32)
    gx = np.abs(np.diff(im, axis=1, prepend=im[:, :1]))
    gy = np.abs(np.diff(im, axis=0, prepend=im[:1, :]))
    return gx + gy

def bda_name(mesh):
    # gc_footprint_vc -> GC_Footprint_VC_LongDist.bdae
    parts = mesh.split('_')
    suffix = parts[-1].upper()
    return f'GC_Footprint_{suffix}_LongDist.bdae'

def warp_score(uv, quad, em, order, flip, S=2048):
    q = np.array(quad, dtype=np.float64)
    if order == 'minmax':
        u0, v0, u1, v1 = q
        du, dv = u1 - u0, v1 - v0
    elif order == 'origin_size':
        u0, v0, du, dv = q
    else:  # size_origin
        du, dv, u0, v0 = q
    u = u0 + uv[:, 0] * du
    v = v0 + uv[:, 1] * dv
    if flip:
        v = 1.0 - v
    px = np.clip((u * S).astype(np.int32), 0, em.shape[1] - 1)
    py = np.clip((v * S).astype(np.int32), 0, em.shape[0] - 1)
    return float(em[py, px].mean())

def main():
    recs = json.load(open(RECS))
    # footprints with LongDist bdae available + page img available
    targets = []
    for r in recs:
        m = r.get('mesh') or ''
        if 'footprint' not in m or r['lvc'] != 'GothamCity':
            continue
        if r['page'] not in PAGE_IMG:
            continue
        bda = bda_name(m)
        if not os.path.exists(os.path.join(RAW, bda)):
            continue
        targets.append((m, r))
    print(f'{len(targets)} footprint records with mesh + page available')

    d = open('/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc', 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0] if (struct := __import__('struct')) else 0

    # fetch pre-quads straight from the lvc
    import struct
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4; p += ln

    edges = {nm: edge_map(os.path.join(PAGES, f)) for f in PAGE_IMG.values() for nm in [f]}

    results = {}
    for m, r in targets:
        o = r['off']
        pre = [struct.unpack_from('>f', d, o - 16 + 4 * k)[0] for k in range(4)]
        post = r['rect']  # post-quad from session5 json
        uv = parse_meshes(os.path.join(RAW, bda_name(m)))[0]['uv'].astype(np.float64)
        rt = PAGE_IMG[r['page']]
        sh = PAGE_IMG[r['page_shipped']] if r.get('page_shipped') in PAGE_IMG.values() else None
        for qtag, quad in (('pre', pre), ('post', post)):
            for ptag, png in (('rt', rt), ('sh', sh)):
                if png is None:
                    continue
                em = edges[png]
                for order in ('minmax', 'origin_size', 'size_origin'):
                    for flip in (False, True):
                        s = warp_score(uv, quad, em, order, flip)
                        key = (qtag, ptag, order, flip)
                        results.setdefault(key, []).append(s)
    print(f"{'combo':42s} {'mean':>8s} {'median':>8s} n")
    for key, vals in sorted(results.items(), key=lambda kv: -np.mean(kv[1])):
        print(f'{str(key):42s} {np.mean(vals):8.2f} {np.median(vals):8.2f} {len(vals)}')

if __name__ == '__main__':
    main()
