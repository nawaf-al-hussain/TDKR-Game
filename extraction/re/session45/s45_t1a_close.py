#!/usr/bin/env python3
"""s45 T1a close: full per-material sampler records from source.dae (authoring),
cross-checked against the compiled image table. Output: s45_t1a_bindings.json.

For each of the 307 materials:
  - name
  - instance_effect url (effect hash)
  - setparam overrides: sampler surfaces (init_from tga) + float4/float params
  - wrap/filter state from the effect's technique pass sample_state if present
Validation:
  - mat73 diffuse == gothamcity_roads_details.tga (anchor)
  - every bound tga resolves to a compiled image-table ordinal (0..175)
"""
import xml.etree.ElementTree as ET
import zipfile, json
import numpy as np
import io

Z = zipfile.ZipFile('/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae')
root = ET.fromstring(Z.read('source.dae'))
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}

# compiled image table ordinals
bres = Z.read('little_endian_not_quantized.bdae')
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)

def cstrb(off):
    if not (0 < off < len(bres)):
        return ''
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > 120:
        return ''
    return bres[off:e].decode('ascii', 'replace')

IMG = 0x22a9c
tga2ord = {}
for i in range(176):
    a = IMG + i * 12
    tga = cstrb(int(u32[a // 4 + 2]))
    tga2ord.setdefault(tga, i)

# library images id -> file
imgs = {}
for im in root.find('c:library_images', NS).findall('c:image', NS):
    ini = im.find('c:init_from', NS)
    imgs[im.get('id')] = ini.text.strip() if ini is not None and ini.text else ''

def param_tree(el, out):
    """collect surface init_from + float params under a setparam/newparam tree"""
    for child in el:
        tag = child.tag.split('}')[1]
        if tag == 'surface':
            ini = child.find('c:init_from', NS)
            out['surface'] = ini.text.strip() if ini is not None and ini.text else ''
        elif tag == 'float4':
            out['float4'] = [float(x) for x in (child.text or '').split()]
        elif tag == 'float':
            out['float'] = float(child.text or 0)
        elif tag == 'sampler2D':
            src = child.find('c:source', NS)
            out['sampler_source'] = src.text.strip() if src is not None and src.text else ''
        param_tree(child, out)

# effects: technique pass sample_state (wrap)
wrap_state = {}
for e in root.find('c:library_effects', NS).findall('c:effect', NS):
    st = set()
    for ss in e.iter():
        tag = ss.tag.split('}')[1]
        if tag in ('wrap_s', 'wrap_t', 'min_filter', 'mag_filter', 'mip_filter'):
            st.add(f'{tag}={(ss.text or "").strip()}')
    if st:
        wrap_state[e.get('id')] = sorted(st)

mats_out = []
unresolved = set()
for m in root.find('c:library_materials', NS).findall('c:material', NS):
    inst = m.find('c:instance_effect', NS)
    rec = {'name': m.get('id'), 'effect': inst.get('url', '').lstrip('#') if inst is not None else None,
           'params': {}}
    if inst is not None:
        for sp in inst.findall('c:setparam', NS):
            sid = sp.get('ref') or sp.get('sid')
            d = {}
            param_tree(sp, d)
            if d:
                rec['params'][sid] = d
    mats_out.append(rec)

# resolve surfaces through sampler chains and image ids; map to compiled ordinals
bind = []
for i, r in enumerate(mats_out):
    surf = {}
    for sid, d in r['params'].items():
        # sampler -> source param -> surface
        src = d.get('sampler_source')
        if src:
            tgt = r['params'].get(src, {})
            f = tgt.get('surface')
        else:
            f = d.get('surface')
        if f:
            f = imgs.get(f, f)  # image id -> file
        if f:
            o = tga2ord.get(f)
            if o is None:
                unresolved.add(f)
            surf[sid] = {'tga': f, 'ordinal': o}
        elif 'float4' in d:
            surf[sid] = {'float4': d['float4']}
    bind.append({'i': i, 'name': r['name'], 'effect': r['effect'], 'bind': surf,
                 'wrap': wrap_state.get(r['effect'], [])})

json.dump(bind, open('/home/z/my-project/scripts/s45_t1a_bindings.json', 'w'), indent=0)

# validation
b73 = bind[73]['bind']
print('mat73:', json.dumps(bind[73], indent=1)[:400])
assert b73.get('DiffuseMap', {}).get('tga') == 'gothamcity_roads_details.tga', 'mat73 diffuse anchor FAIL'
print('ANCHOR mat73 diffuse OK; ordinal', b73['DiffuseMap']['ordinal'])
cnt_d = sum(1 for b in bind if 'DiffuseMap' in b['bind'])
cnt_l = sum(1 for b in bind if 'LightMap' in b['bind'])
cnt_ord = sum(1 for b in bind if 'DiffuseMap' in b['bind'] and b['bind']['DiffuseMap'].get('ordinal') is not None)
cnt_ordl = sum(1 for b in bind if 'LightMap' in b['bind'] and b['bind']['LightMap'].get('ordinal') is not None)
f4 = sum(1 for b in bind for k, v in b['bind'].items() if isinstance(v, dict) and 'float4' in v)
nontrivial_f4 = [ (b['i'], k, v['float4']) for b in bind for k, v in b['bind'].items() if isinstance(v, dict) and 'float4' in v and any(abs(x - 1) > 1e-6 for x in v['float4']) ]
print(f'DiffuseMap bound: {cnt_d}/307, LightMap bound: {cnt_l}/307')
print(f'diffuse with compiled ordinal: {cnt_ord}, lightmap with ordinal: {cnt_ordl}')
print(f'float4 params: {f4}, non-trivial: {len(nontrivial_f4)}', nontrivial_f4[:6])
print('unresolved tga (not in compiled 176):', sorted(unresolved)[:8], f'({len(unresolved)})')
wraps = {}
for b in bind:
    for w in b['wrap']:
        wraps[w] = wraps.get(w, 0) + 1
print('wrap/filter census:', wraps)
