#!/usr/bin/env python3
"""s47 T1 FINAL COMPARISON: engine runtime binding table vs source.dae
authoring table (s45_t1a_bindings.json, 307 rows).

Engine side: the scene-material instance table in the compiled DB (36-B
entries {name*, name*, 0, effect_url*, newparam_count, profile_ptr, id, -1,
0x80}); profile SNewParam entries {name*, semantic*, 13, 1, v1, v2} with
value header {1, v1+24} and node at v1+24 = image index into the 176-image
table (postLoadProcess patches these to SImage* at load; materials use them
via createMaterialRendererForProfile -> setMaterialParameter<SNewParam>)."""
import io, zipfile, json
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
u32 = np.frombuffer(LE, '<u4', NB // 4)
N = NB // 4

def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = LE.find(b'\0', off)
    if e < 0 or e == off or e - off > maxn:
        return None
    try:
        t = LE[off:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

IMG_BASE, IMG_N = 0x22a9c, 176
imgs = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    imgs.append((i, int(w[0]), int(w[2])))

# --- scene-material instance table ---
scene_entries = []
k = 0
while k < N - 9:
    w = [int(u32[k + j]) for j in range(9)]
    if (w[7] == 0xffffffff and w[8] == 0x80 and w[2] == 0
            and 0 < w[4] <= 24 and 0 < w[5] < NB - 512):
        nm, eff = cstr(w[0]), cstr(w[3])
        if nm and eff and eff.startswith('#'):
            scene_entries.append({'addr': k * 4, 'name': nm, 'effect': eff[1:],
                                  'count': w[4], 'prof': w[5]})
            k += 9
            continue
    k += 1
print('scene-material instance entries:', len(scene_entries))
if scene_entries:
    print('  addr range:', hex(min(e['addr'] for e in scene_entries)),
          hex(max(e['addr'] for e in scene_entries)))
    print('  first:', scene_entries[0]['name'], '->', scene_entries[0]['effect'])
    print('  last :', scene_entries[-1]['name'], '->', scene_entries[-1]['effect'])

# --- decode profile SNewParam blocks ---
def decode_prof(ptr, count):
    out = {}
    for j in range(count):
        a = ptr + j * 24
        if a + 24 > NB:
            break
        w = [int(u32[(a + t * 4) // 4]) for t in range(6)]
        nm = cstr(w[0])
        if nm is None:
            continue
        v1 = w[4]
        if w[2] == 13 and 0 < v1 < NB - 32:
            if int(u32[v1 // 4]) == 1 and int(u32[v1 // 4 + 1]) == v1 + 24:
                idx = int(u32[(v1 + 24) // 4])
                if 0 <= idx < IMG_N:
                    out[nm] = cstr(imgs[idx][2])
                else:
                    out[nm] = None
        # non-sampler params ignored (floats/colors — authoring table stores
        # textures only for the comparison)
    return out

eng = {}
for e in scene_entries:
    eng[e['name']] = {'effect': e['effect'], 'bind': decode_prof(e['prof'], e['count'])}
shapes = {}
for nm, d in eng.items():
    key = tuple(sorted(k for k in d['bind'] if d['bind'][k]))
    shapes[key] = shapes.get(key, 0) + 1
print('engine binding-shape census (top 6):')
for kk, v in sorted(shapes.items(), key=lambda x: -x[1])[:6]:
    print('  ', v, kk)

# --- authoring table ---
auth = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))
print('authoring rows:', len(auth))

# --- compare by name ---
by_name = {a['name']: a for a in auth}
matched = unmatched = 0
mismatch = []
texkeys = ('DiffuseMap', 'LightMap', 'MaskMap', 'ReflectionMap', 'NormalMap')
for nm, d in eng.items():
    a = by_name.get(nm)
    if a is None:
        unmatched += 1
        continue
    matched += 1
    for key in texkeys:
        e_t = d['bind'].get(key)
        a_b = a['bind'].get(key)
        a_t = a_b.get('tga') if isinstance(a_b, dict) else None
        if e_t != a_t:
            mismatch.append((nm, key, e_t, a_t))
print(f'name-matched: {matched}, unmatched(engine side): {unmatched}')
print('texture mismatches:', len(mismatch))
for m in mismatch[:12]:
    print('   ', m)

# engine-side rows with no DiffuseMap/LightMap vs authoring same — count agreement
both = sum(1 for nm, d in eng.items() if nm in by_name)
agree = sum(1 for nm, d in eng.items()
            if nm in by_name and all(
                (d['bind'].get(k) or None) == ((by_name[nm]['bind'].get(k) or {}).get('tga')
                                               if isinstance(by_name[nm]['bind'].get(k), dict) else None)
                for k in texkeys))
print(f'full-texture-row agreement: {agree}/{both}')

# explicit probes
for probe in (73, 302):
    a = auth[probe]
    e = eng.get(a['name'])
    print(f"--- material {probe}: {a['name']} ---")
    print('  authoring:', {k: (a['bind'].get(k) or {}).get('tga') for k in texkeys
                           if isinstance(a['bind'].get(k), dict)})
    if e:
        print('  engine   :', {k: e['bind'].get(k) for k in texkeys})
        print('  effect match:', e['effect'] == a['effect'], e['effect'])
    else:
        print('  engine   : NOT FOUND in scene table')

json.dump({'scene_entries': scene_entries, 'engine': eng,
           'mismatches': mismatch},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t1_engine_vs_authoring.json', 'w'), indent=1)
print('saved s47_t1_engine_vs_authoring.json')
