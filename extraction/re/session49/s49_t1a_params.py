#!/usr/bin/env python3
"""s49 T1a: per-material float/vec uniforms from the compiled scene-instance table.

Instance rows @0x5fea0, 36 B: [name][name2][0][effect][N][list][self][ffffffff][0x80]
Sampler list: N x 24 B [name_ptr][pad][type][1][vptr][vptr2]
Value block @vptr: {1, vptr+24}; data @vptr+24 (image idx for type 13, floats for others).
Task: census all types, decode float/vec values, Overbright distribution over
AlphaMasking materials, Coord scale/offset overrides. Anchors: mat 73, 302.
"""
import zipfile, io, json, struct
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
w32 = np.frombuffer(LE, '<u4', len(LE) // 4)
nb = len(LE)

def cs(p, maxn=80):
    if not (0 < p < nb): return None
    e = LE.find(b'\0', p)
    if e < 0 or e == p or e - p > maxn: return None
    try:
        t = LE[p:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def fx_name(p):
    s = cs(p) or ''
    return s.split('-fx')[0].lstrip('#')

TYPE_NAME = {13: 'texture', 7: 'vec4', 6: 'vec3', 1: 'float', 0: 'int?',
             2: 'vec2?', 3: 'vec3?', 4: 'vec4?', 5: '?', 8: '?', 9: '?'}

rows = []
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    rows.append({'idx': i, 'name': cs(ws[0]), 'effect': fx_name(ws[3]),
                 'N': ws[4], 'list': ws[5]})

def decode_value(vptr, typ):
    """value block @vptr: {1, vptr+24}; data @vptr+24."""
    if not (0 < vptr < nb - 32): return None
    h0, h1 = int(w32[vptr // 4]), int(w32[vptr // 4 + 1])
    if h0 != 1 or h1 != vptr + 24: return ('badheader', h0, h1)
    d = vptr + 24
    if typ == 13:
        return int(w32[d // 4])          # image index
    if typ == 1:                          # float
        return struct.unpack_from('<f', LE, d)[0]
    if typ == 7:                          # vec4
        return list(struct.unpack_from('<4f', LE, d))
    if typ == 6:                          # vec3
        return list(struct.unpack_from('<3f', LE, d))
    if typ == 2:                          # vec2?
        return list(struct.unpack_from('<2f', LE, d))
    # unknown: raw words
    return [hex(int(w32[d // 4 + k])) for k in range(4)]

census = {}
per_mat = {}
for r in rows:
    entries = []
    for j in range(r['N']):
        sa = r['list'] + j * 24
        sw = [int(w32[(sa + k * 4) // 4]) for k in range(6)]
        nm = cs(sw[0])
        typ = sw[2]
        val = decode_value(sw[4], typ)
        entries.append({'name': nm, 'type': typ, 'val': val})
        key = (typ, TYPE_NAME.get(typ, '?'), nm)
        census[key] = census.get(key, 0) + 1
    per_mat[r['idx']] = {'effect': r['effect'], 'name': r['name'], 'params': entries}

print('=== type census over 307 materials ===')
for k in sorted(census, key=lambda x: -census[x]):
    print(f'  type {k[0]:>2} {k[1]:<8} name {str(k[2]):<24} x {census[k]}')

print()
print('=== anchor mat 73 ===', json.dumps(per_mat[73], indent=1))
print('=== anchor mat 302 ===', json.dumps(per_mat[302], indent=1))

# Overbright distribution over AlphaMasking materials
am = [i for i, m in per_mat.items() if m['effect'] == 'AlphaMasking']
ob_vals = [p['val'] for i in am for p in per_mat[i]['params'] if p['name'] == 'Overbright']
print(f'\nAlphaMasking materials: {len(am)}; with Overbright entry: {len(ob_vals)}')
print('Overbright values:', sorted(set(round(v, 6) for v in ob_vals)))

# LightMapAtlas distribution
la = [tuple(round(x, 6) for x in p['val']) for i, m in per_mat.items()
      for p in m['params'] if p['name'] == 'LightMapAtlas' and isinstance(p['val'], list)]
import collections
print('LightMapAtlas distinct:', collections.Counter(la).most_common(6))

# scale/offset-ish names
print('\nnon-texture param names census:')
names = collections.Counter(p['name'] for m in per_mat.values() for p in m['params'] if p['type'] != 13)
print(names.most_common(20))

# mat 156 detail (stride-28, 8 segs)
print('\n=== mat 156 ===', json.dumps(per_mat[156], indent=1))
# effects census for the stride-28 families: which materials have stride 28?
json.dump({'rows': rows, 'per_mat': {str(k): v for k, v in per_mat.items()}},
          open('s49_t1a_params.json', 'w'), indent=1)
print('saved s49_t1a_params.json')
