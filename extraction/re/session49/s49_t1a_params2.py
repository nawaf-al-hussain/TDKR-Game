#!/usr/bin/env python3
"""s49 T1a v2: full uniform census with inline value decode + SNewParam float hunt."""
import zipfile, io, json, struct, collections
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
w32 = np.frombuffer(LE, '<u4', len(LE) // 4)
nb = len(LE)
fw = lambda o: struct.unpack_from('<f', LE, o)[0]

def cs(p, maxn=80):
    if not (0 < p < nb): return None
    e = LE.find(b'\0', p)
    if e < 0 or e == p or e - p > maxn: return None
    try: t = LE[p:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def fx_name(p):
    return (cs(p) or '').split('-fx')[0].lstrip('#')

def decode_value(vptr, typ):
    if not (0 < vptr < nb - 32): return None
    if typ == 13:  # texture: {1, vptr+24}; u32 image idx @vptr+24
        return int(w32[(vptr + 24) // 4])
    # non-texture: data inline at vptr+4
    d = vptr + 4
    if typ == 1: return fw(d)
    if typ == 2: return list(struct.unpack_from('<2f', LE, d))
    if typ == 3: return list(struct.unpack_from('<3f', LE, d))
    if typ in (4, 7): return list(struct.unpack_from('<4f', LE, d))
    if typ == 6: return list(struct.unpack_from('<3f', LE, d))
    if typ == 5:
        return {'w0': hex(int(w32[vptr//4])), 'f': [fw(d), fw(d+4)]}
    return [hex(int(w32[(d)//4 + k])) for k in range(4)]

rows = []
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    params = []
    for j in range(ws[4]):
        sa = ws[5] + j * 24
        sw = [int(w32[(sa + k * 4) // 4]) for k in range(6)]
        params.append({'name': cs(sw[0]), 'type': sw[2], 'val': decode_value(sw[4], sw[2])})
    rows.append({'idx': i, 'name': cs(ws[0]), 'effect': fx_name(ws[3]), 'params': params})

print('=== anchors ===')
for m in (73, 302, 156):
    print(f'mat {m} effect={rows[m]["effect"]}:')
    for p in rows[m]['params']:
        print('   ', p['name'], 'type', p['type'], 'val', p['val'])

# Overbright: find the override + all AlphaMasking mats
am = [r for r in rows if r['effect'] == 'AlphaMasking']
print(f'\nAlphaMasking materials: {len(am)} -> idx {[r["idx"] for r in am]}')
for r in am:
    ob = [p for p in r['params'] if p['name'] == 'Overbright']
    print(f'  mat {r["idx"]}: Overbright {"OVERRIDE " + str(ob[0]["val"]) if ob else "default 1.0"}')

# LightMapAtlas values
la = collections.Counter(tuple(round(x,6) for x in p['val']) for r in rows for p in r['params'] if p['name']=='LightMapAtlas')
print('\nLightMapAtlas distinct values:', la.most_common(5))

# any scale/offset named params anywhere in instance table
print('\ninstance-table params that are NOT textures, all materials:')
for r in rows:
    for p in r['params']:
        if p['type'] != 13:
            print(f'  mat {r["idx"]:>3} {r["effect"]:<20} {p["name"]:<20} type {p["type"]} = {p["val"]}')

# --- SNewParam float hunt: scan whole binary for known uniform names ---
print('\n=== SNewParam name scan (whole binary) ===')
for want in ['Overbright', 'TexCoord0_scaleoffset', 'TexCoord1_scaleoffset',
             'FogStartEnd', 'FogColor', 'LightMapAtlas', 'ExtraDiffuse',
             'VerticalFogAlpha', 'FogMap', 'Amplitude', 'Frequency', 'Speed']:
    offs = []
    start = 0
    while True:
        j = LE.find(want.encode(), start)
        if j < 0: break
        offs.append(j)
        start = j + 1
    print(f'  {want}: {len(offs)} occurrences {[hex(o) for o in offs[:8]]}')
json.dump({'rows': rows}, open('s49_t1a_params2.json', 'w'), indent=1)
print('saved')
