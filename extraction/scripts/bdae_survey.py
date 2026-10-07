#!/usr/bin/env python3
"""Batch-survey all bdae files: how many meshes/tris parse per file."""
import os, sys, json
sys.path.insert(0, '/home/z/my-project/scripts')
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from bdae_extract import parse_meshes

BASE = '/home/z/my-project/download/TDKR_assets/raw'
dirs = sys.argv[1:] or ['l_gothamcity', 'actors', 'vehicles', 'commons', 'l_stockexchange', 'l_policestation', 'l_thepit', 'l_underground', 'l_military', 'l_stadion', 'l_batcave', 'cinematics', 'effects', 'l_menu']
rows = []
for dd in dirs:
    p = os.path.join(BASE, dd)
    if not os.path.isdir(p):
        continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.bdae.bin'):
            continue
        path = os.path.join(p, fn)
        try:
            meshes = parse_meshes(path, verbose=False)
        except Exception as ex:
            meshes = []
        if meshes:
            rows.append(dict(archive=dd, file=fn[:-9], n=len(meshes),
                             verts=sum(m['count'] for m in meshes),
                             tris=sum(m['numIdx'] // 3 for m in meshes),
                             mats=sorted(set(m['material'] for m in meshes))))
tot_t = sum(r['tris'] for r in rows)
tot_v = sum(r['verts'] for r in rows)
print(f'{len(rows)} files with meshes, {tot_v} verts, {tot_t} tris')
for r in sorted(rows, key=lambda r: -r['tris'])[:25]:
    print(f"  {r['archive']}/{r['file']}: {r['n']} meshes {r['verts']}v {r['tris']}t mats={r['mats'][:4]}")
out = '/home/z/my-project/download/TDKR_assets/probe/bdae_mesh_survey.json'
json.dump(rows, open(out, 'w'), indent=1)
print('survey ->', out)
