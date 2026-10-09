#!/usr/bin/env python3
"""Parse the zone source.dae (original COLLADA) into the full authoritative
chain: primitive/material-symbol -> material -> effect -> sampler -> image
texture name.  Outputs zone_materials_<island>.json.
"""
import xml.etree.ElementTree as ET
import json, sys, os
import zipfile

NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}

def parse(dae_path, out_json):
    tree = ET.parse(dae_path)
    root = tree.getroot()

    # ---- image library: image id -> texture file ----
    images = {}
    for img in root.iter('{%s}image' % NS['c']):
        iid = img.get('id')
        init = img.find('{%s}init_from' % NS['c'])
        if iid and init is not None and init.text:
            images[iid] = init.text.strip()

    # ---- effects: effect id -> {sampler symbol -> image id} ----
    effects = {}
    for eff in root.iter('{%s}effect' % NS['c']):
        eid = eff.get('id')
        sam = {}
        # surface params: newparam sid -> init_from image
        surf = {}
        for np_ in eff.iter('{%s}newparam' % NS['c']):
            sid = np_.get('sid')
            sfc = np_.find('{%s}surface' % NS['c'])
            smp = np_.find('{%s}sampler2D' % NS['c'])
            if sfc is not None:
                ini = sfc.find('{%s}init_from' % NS['c'])
                if ini is not None and ini.text:
                    surf[sid] = ini.text.strip()
            if smp is not None:
                src = smp.find('{%s}source' % NS['c'])
                if src is not None and src.text:
                    sam['__sampler_src__' + sid] = src.text.strip()
        # shader binds: <bind symbol="tex" sem/param>
        binds = {}
        for sh in eff.iter():
            if sh.tag.endswith('shader') or sh.tag.split('}')[-1] in ('vertex', 'fragment', 'pass'):
                for b in sh.iter('{%s}bind' % NS['c']):
                    sym = b.get('symbol')
                    param = b.get('param') or b.get('target')
                    if sym:
                        binds[sym] = param
        effects[eid] = dict(surfaces=surf, binds=binds, sampler_src=sam)

    # ---- materials: id -> effect url ----
    materials = {}
    for mat in root.iter('{%s}material' % NS['c']):
        mid = mat.get('id')
        ie = mat.find('{%s}instance_effect' % NS['c'])
        if mid is not None and ie is not None:
            materials[mid] = (ie.get('url') or '').lstrip('#')

    # ---- geometries: primitives with material symbols ----
    geoms = {}
    for geo in root.iter('{%s}geometry' % NS['c']):
        gid = geo.get('id')
        prims = []
        mesh = geo.find('{%s}mesh' % NS['c'])
        if mesh is None:
            continue
        for tag in ('triangles', 'polylist', 'lines', 'tristrips'):
            for p in mesh.iter('{%s}%s' % (NS['c'], tag)):
                prims.append(dict(tag=tag, symbol=p.get('material'),
                                  count=int(p.get('count') or 0)))
        geoms[gid] = prims

    # ---- node instances: node -> geometry + bind_material (symbol->target) ----
    binds_list = []  # (node_name, geometry_id, [(symbol, target_mat)])
    for inst in root.iter('{%s}instance_geometry' % NS['c']):
        url = (inst.get('url') or '').lstrip('#')
        bm = inst.find('{%s}bind_material' % NS['c'])
        pairs = []
        if bm is not None:
            tc = bm.find('{%s}technique_common' % NS['c'])
            if tc is not None:
                for im in tc.iter('{%s}instance_material' % NS['c']):
                    pairs.append((im.get('symbol'), (im.get('target') or '').lstrip('#')))
        # find ancestor node name
        binds_list.append(dict(geometry=url, materials=pairs))

    # ---- resolve effect -> textures ----
    def effect_textures(eid):
        e = effects.get(eid)
        if not e:
            return {}
        out = {}
        for sym, param in e['binds'].items():
            if param and param in e['surfaces']:
                imgid = e['surfaces'][param]
                out[sym] = images.get(imgid, imgid)
        return out

    mat_tex = {}
    for mid, eid in materials.items():
        mat_tex[mid] = effect_textures(eid)

    data = dict(
        images=images,
        materials={k: v for k, v in materials.items()},
        material_textures=mat_tex,
        geometries={k: v for k, v in geoms.items() if v},
        instance_geometries=binds_list,
    )
    json.dump(data, open(out_json, 'w'), indent=1)
    print(f'{dae_path}:')
    print(f'  images: {len(images)}  materials: {len(materials)}  effects: {len(effects)}')
    print(f'  geometries with prims: {len(data["geometries"])}  instance_geoms: {len(binds_list)}')
    # sample
    for mid in list(mat_tex)[:6]:
        print(f'  MAT {mid[:50]:<52} -> {mat_tex[mid]}')
    return data

if __name__ == '__main__':
    import glob
    for isl, dae in [('GothamCity', '/home/z/my-project/work/zone/GothamCity/mat/source.dae'),
                     ('GothamCity_Island2', None)]:
        # island2 materials zip extraction if needed
        p2 = '/home/z/my-project/work/zone/GothamCity_Island2'
        if isl == 'GothamCity_Island2':
            if not os.path.exists(p2 + '/GothamCity_materials.bdae'):
                os.makedirs(p2, exist_ok=True)
                os.system(f'cd {p2} && unzip -o -q ../../zips/GothamCity_Island2.zip')
            if not os.path.exists(p2 + '/mat/source.dae'):
                os.makedirs(p2 + '/mat', exist_ok=True)
                os.system(f'cd {p2}/mat && unzip -o -q ../GothamCity_materials.bdae')
            dae = p2 + '/mat/source.dae'
        parse(dae, f'/home/z/my-project/work/zone/zone_materials_{isl}.json')
