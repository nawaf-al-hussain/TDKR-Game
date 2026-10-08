#!/usr/bin/env python3
"""Analyze deployed GLB UVs vs texture page content.

Downloads (or reads local) GLB, extracts TEXCOORD_0 per primitive, compares
UV footprint against the page image structure:
 - UV bounds / distribution
 - fraction of UVs inside [0,1]
 - visual: scatter UVs over the page image -> if content alignment is right,
   UV density should sit ON structure (roads/buildings), not in empty areas.
"""
import struct, json, sys, os
import numpy as np

MODELS = '/home/z/my-project/work/TDKR-Game/gh-pages-wt/models'

def parse_glb(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'glTF'
    off = 12
    js = None
    bin_chunk = None
    while off < len(d):
        clen, ctype = struct.unpack_from('<II', d, off)
        chunk = d[off+8:off+8+clen]
        if ctype == 0x4E4F534A:
            js = json.loads(chunk)
        elif ctype == 0x004E4942:
            bin_chunk = chunk
        off += 8 + clen
    return js, bin_chunk

def read_acc(js, bin_chunk, idx):
    acc = js['accessories'][idx] if 'accessories' in js else js['accessors'][idx]
    bv = js['bufferViews'][acc['bufferView']]
    comp = {5126: 'f4', 5123: 'u2', 5121: 'u1', 5125: 'u4'}[acc['componentType']]
    n = acc['count']
    ncomp = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[acc['type']]
    start = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    arr = np.frombuffer(bin_chunk, dtype=comp, count=n*ncomp, offset=start)
    return arr.reshape(n, ncomp)

def main():
    for name in sys.argv[1:]:
        p = os.path.join(MODELS, name if name.endswith('.glb') else name + '.glb')
        js, bc = parse_glb(p)
        print(f'\n=== {os.path.basename(p)} ===')
        for mi, mesh in enumerate(js['meshes']):
            for pi, prim in enumerate(mesh['primitives']):
                mat = js['materials'][prim['material']]['name'] if 'material' in prim else '?'
                uv_acc = prim['attributes'].get('TEXCOORD_0')
                if uv_acc is None:
                    print(f'  mesh{mi} p{pi} mat={mat}: NO TEXCOORD_0')
                    continue
                uv = read_acc(js, bc, uv_acc)
                mn, mx = uv.min(0), uv.max(0)
                inside = ((uv[:,0] >= 0) & (uv[:,0] <= 1) & (uv[:,1] >= 0) & (uv[:,1] <= 1)).mean()
                print(f'  mesh{mi} p{pi} mat={mat}: n={len(uv)} uv=[{mn[0]:.3f},{mn[1]:.3f}]-[{mx[0]:.3f},{mx[1]:.3f}] inside01={inside:.2%}')
                # histogram of u in 8 bins
                h, _ = np.histogram(uv[:,0], bins=8, range=(0,1))
                print(f'    u-hist8: {list(h)}')

if __name__ == '__main__':
    main()
