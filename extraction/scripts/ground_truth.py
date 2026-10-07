#!/usr/bin/env python3
"""GROUND TRUTH extractor for TDKR bdae files.

Per file, extracts the engine's own binding chain:
  1. texture list (ordered) from meta-section strings
  2. render units: {material name, effect file, technique, sampler list ptr}
  3. sampler records: {name, type=13, -> value block: [ptr, oU, oV, sU, sV, texIdx]}
  4. meshes: geometry footer material names
  -> per mesh: DiffuseMap texture + Coord0_scaleoffset (ground truth)

Outputs JSON for the export pipeline.
"""
import struct, re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bdae_extract import parse_meshes

SAMP_SET = ('DiffuseMap', 'DiffuseMap2', 'DiffuseMap_alpha', 'LightMap', 'NormalMap',
            'NormalMap1', 'NormalMap2', 'ReflectionMap', 'ReflectionMapSampler',
            'DiffuseMaskSampler', 'SpecularLevel', 'Glossiness', 'LightMapAtlas')

def strings(d, limit):
    out = {}
    for m in re.finditer(rb'[\x20-\x7e]{3,}\x00', d[:limit]):
        start, stop = m.start(), m.end() - 1
        L = stop - start
        if start >= 4:
            (Pl,) = struct.unpack_from('<I', d, start - 4)
            if Pl == L:
                out[start] = d[start:stop].decode()   # char offset -> string
    return out

def parse_file(path):
    d = open(path, 'rb').read()
    if d[:4] != b'BRES':
        return None
    h = struct.unpack_from('<14I', d, 0)
    G = h[10]
    strs = strings(d, G)
    # ordered unique texture list (first occurrence = prefix offset order)
    texs, seen = [], set()
    for off, s in sorted(strs.items()):
        if s.endswith('.tga') and s not in seen:
            texs.append(s[:-4]); seen.add(s)
    samp_off = {off: s for off, s in strs.items() if s in SAMP_SET}

    nw = G // 4
    w = struct.unpack_from(f'<{nw}I', d, 0)

    # ---- sampler records + value blocks ----
    # value block @v2: [ptr->Coord0_scaleoffset vec4 | 0/-1, w1, w2, w3, w4, texIdx]
    samplers = []  # {off, name, scaleoffset, wrap, texIdx}
    for i in range(2, nw - 8):
        v = w[i]
        if v in samp_off and w[i+1] == v and w[i+2] == 13:
            v2 = w[i+5]
            if v2 + 24 <= len(d):
                blk = struct.unpack_from('<6I', d, v2)
                idx = blk[5]
                so = None
                if 0 < blk[0] < len(d) - 16 and blk[0] != 0xffffffff:
                    f4 = struct.unpack_from('<4f', d, blk[0])
                    # plausible scaleoffset: finite, not absurd
                    if all(abs(x) < 1e6 for x in f4) and any(x != 0 for x in f4):
                        so = [round(float(x), 6) for x in f4]
                samplers.append(dict(off=i*4, name=samp_off[v],
                                     scaleoffset=so,
                                     wrap=[blk[1], blk[2], blk[3], blk[4]],
                                     texIdx=idx))
    # ---- group sampler records into contiguous lists (gap < 8 words) ----
    lists = []
    for s in samplers:
        if lists and s['off'] - lists[-1][-1]['off'] <= 40:
            lists[-1].append(s)
        else:
            lists.append([s])
    # list start address = first record offset
    list_by_start = {L[0]['off']: L for L in lists}

    # ---- render units: {matPtr, matPtr, filePtr, techPtr, X, listPtr, ...} ----
    units = []
    for i in range(2, nw - 10):
        lp = w[i+5]
        if lp in list_by_start:
            mat = strs.get(w[i], None)
            eff = strs.get(w[i+2], None)
            tech = strs.get(w[i+3], None)
            units.append(dict(off=i*4, material=mat, effect=eff, technique=tech,
                              listStart=lp,
                              samplers={s['name']: dict(texIdx=s['texIdx'],
                                                        scaleoffset=s['scaleoffset'])
                                        for s in list_by_start[lp]}))
    # ---- meshes ----
    try:
        meshes = parse_meshes(path, verbose=False)
    except Exception:
        meshes = []
    mesh_info = [dict(offset=m['offset'], verts=m['count'], tris=m['numIdx']//3,
                      material=m['material'],
                      mn=[float(x) for x in m['mn']], mx=[float(x) for x in m['mx']])
                 for m in meshes]
    return dict(file=os.path.basename(path), textures=texs,
                units=units, meshes=mesh_info)

def join_bindings(ft):
    """mesh.material -> unit.material -> DiffuseMap tex name + scaleoffset"""
    by_mat = {}
    for u in ft['units']:
        if u['material']:
            by_mat.setdefault(u['material'], []).append(u)
    out = []
    for m in ft['meshes']:
        mat = m['material']
        u = by_mat.get(mat)
        if u:
            u = u[0]
            dm = u['samplers'].get('DiffuseMap')
            lm = u['samplers'].get('LightMap')
            tex = None
            if dm and 0 <= dm['texIdx'] < len(ft['textures']):
                tex = ft['textures'][dm['texIdx']]
            light = None
            if lm and 0 <= lm['texIdx'] < len(ft['textures']):
                light = ft['textures'][lm['texIdx']]
            out.append(dict(**m, diffuse=tex, lightmap=light,
                            scaleoffset=dm['scaleoffset'] if dm else None,
                            technique=u['technique'], effect=u['effect']))
        else:
            out.append(dict(**m, diffuse=None, lightmap=None, scaleoffset=None,
                            technique=None, effect=None))
    return out

if __name__ == '__main__':
    import glob
    files = sorted(glob.glob('/home/z/my-project/download/TDKR_assets/raw/l_gothamcity/*.bdae.bin'))
    files = [f for f in files if not any(k in f for k in ('_Collision', '_collision'))]
    results = {}
    stats = dict(files=0, with_units=0, meshes=0, bound=0)
    for f in files:
        ft = parse_file(f)
        if not ft: continue
        bound = join_bindings(ft)
        base = ft['file'].replace('.bdae.bin', '')
        results[base] = dict(textures=ft['textures'],
                             units=[dict(material=u['material'], effect=u['effect'],
                                         technique=u['technique'],
                                         samplers=u['samplers']) for u in ft['units']],
                             meshes=bound)
        stats['files'] += 1
        stats['with_units'] += 1 if ft['units'] else 0
        stats['meshes'] += len(bound)
        stats['bound'] += sum(1 for b in bound if b['diffuse'])
    with open('/home/z/my-project/scripts/ground_truth_city.json', 'w') as fp:
        json.dump(results, fp)
    print('stats:', stats)
    # sample print
    for k in ('GC_Bigbridge', 'GC_island1_LongDist', 'GC_Diner'):
        if k in results:
            print(f"\n== {k}: textures={results[k]['textures']}")
            for m in results[k]['meshes'][:6]:
                print(f"   mesh verts={m['verts']:6d} mat={m['material']!r} "
                      f"diffuse={m['diffuse']!r} lightmap={m['lightmap']!r} so={m['scaleoffset']}")
