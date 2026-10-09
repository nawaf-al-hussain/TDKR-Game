#!/usr/bin/env python3
"""Full authoritative material table for the zone street tier.

source.dae structure (probed):
  <material id="tiles_KjsfSXF4YP_30KKziHtRb">
    <instance_effect url="#LightMapDC-fx_...">
      <setparam ref="texture23"><surface><init_from>image13</init_from></surface></setparam>
      <setparam ref="LightMap"><sampler2D><source>texture23</source></sampler2D></setparam>
      <setparam ref="texture24"><surface><init_from>image17</init_from></surface></setparam>
      <setparam ref="DiffuseMap"><sampler2D><source>texture24</source></sampler2D></setparam>
      <setparam ref="LightMapAtlas"><float4>1 1 0 0</float4></setparam>
  Chain: sampler ref -> textureN surface -> imageN -> <image id><init_from>FILE.tga

Outputs per material: {sampler_symbol: texture_file} + LightMapAtlas float4.
"""
import xml.etree.ElementTree as ET
import json, sys, os

C = 'http://www.collada.org/2005/11/COLLADASchema'

def q(tag):
    return '{%s}%s' % (C, tag)

def parse_dae(dae_path):
    root = ET.parse(dae_path).getroot()

    # image id -> texture file
    images = {}
    for img in root.iter(q('image')):
        iid = img.get('id')
        init = img.find(q('init_from'))
        if iid and init is not None and init.text:
            images[iid] = init.text.strip()

    # effect-level defaults: newparam sid -> surface init_from
    eff_surf = {}
    for eff in root.iter(q('effect')):
        eid = eff.get('id')
        surf = {}
        for np_ in eff.iter(q('newparam')):
            sfc = np_.find(q('surface'))
            if sfc is not None:
                ini = sfc.find(q('init_from'))
                if ini is not None and ini.text:
                    surf[np_.get('sid')] = ini.text.strip()
        eff_surf[eid] = surf

    # materials with per-instance setparam overrides
    materials = {}
    for mat in root.iter(q('material')):
        mid = mat.get('id')
        ie = mat.find(q('instance_effect'))
        if ie is None:
            continue
        eid = (ie.get('url') or '').lstrip('#')
        surface_of = {}          # textureN -> imageN (instance overrides)
        sampler_of = {}          # sampler symbol -> textureN
        atlas = None
        extra_floats = {}
        for sp in ie.findall(q('setparam')):
            ref = sp.get('ref')
            sfc = sp.find(q('surface'))
            smp = sp.find(q('sampler2D'))
            f4 = sp.find(q('float4'))
            fl = sp.find(q('float'))
            if sfc is not None:
                ini = sfc.find(q('init_from'))
                if ini is not None and ini.text:
                    surface_of[ref] = ini.text.strip()
            elif smp is not None:
                src = smp.find(q('source'))
                if src is not None and src.text:
                    sampler_of[ref] = src.text.strip()
            elif f4 is not None and f4.text:
                extra_floats[ref] = [float(x) for x in f4.text.split()]
                if 'Atlas' in ref:
                    atlas = extra_floats[ref]
            elif fl is not None and fl.text:
                extra_floats[ref] = float(fl.text.strip())
        # resolve samplers -> texture files
        texs = {}
        for sym, texref in sampler_of.items():
            imgid = surface_of.get(texref)
            if imgid is None:
                imgid = eff_surf.get(eid, {}).get(texref)  # effect default
            if imgid:
                texs[sym] = images.get(imgid, imgid)
        # also direct surface refs used as samplers
        materials[mid] = dict(effect=eid, textures=texs,
                              atlas=atlas, floats=extra_floats)
    return images, materials

if __name__ == '__main__':
    all_out = {}
    for isl, dae in (('island1', '/home/z/my-project/work/zone/GothamCity/mat/source.dae'),
                     ('island2', '/home/z/my-project/work/zone/GothamCity_Island2/mat/source.dae')):
        if not os.path.exists(dae):
            print(f'!! missing {dae}')
            continue
        images, materials = parse_dae(dae)
        print(f'{isl}: images={len(images)} materials={len(materials)}')
        texmat = {}
        for mid, m in materials.items():
            if m['textures']:
                texmat[mid] = m
        print(f'  materials with resolved textures: {len(texmat)}')
        from collections import Counter
        fx = Counter(m['effect'].split('-fx')[0] for m in materials.values())
        print('  effects:', dict(fx))
        # which textures appear?
        allt = Counter()
        for m in texmat.values():
            for s, t in m['textures'].items():
                allt[(s, t)] += 1
        for (s, t), n in allt.most_common(25):
            print(f'   {n:>4} {s:<22} {t}')
        all_out[isl] = dict(images=images, materials=materials)
    json.dump(all_out, open('/home/z/my-project/work/zone/zone_materials_full.json', 'w'), indent=1)
    print('-> /home/z/my-project/work/zone/zone_materials_full.json')
