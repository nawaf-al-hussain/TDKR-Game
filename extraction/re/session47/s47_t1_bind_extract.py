#!/usr/bin/env python3
"""s47 T1 extraction: decode ALL sampler setparam entries in the compiled DB
and their value-node image indices; build the engine-side binding table
(entry_addr, param_name, image_idx, image_name). Entry layout (24 B):
{name*, 13, 2, 1, v1, v2}; value header at v1: {1, node(=v1+24)}; ff x4;
node at v1+24: {image_idx}. Real idx in [0,176) = binding; -1 = none."""
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

KNOWN = {'DiffuseMap', 'LightMap', 'LightMapAtlas', 'MaskMap', 'Carcolor',
         'SpecularMap', 'NormalMap', 'GlowMap', 'DetailMap', 'ReflectionMap',
         'EnvMap', 'BumpMap', 'HeightMap', 'OpacityMap', 'ShadowMap'}

entries = []
for k in range(N - 6):
    w0, w1, w2, w3, v1, v2 = (int(u32[k + j]) for j in range(6))
    if w1 == 13 and w2 == 2 and w3 == 1 and v2 == v1 + 4 and 0 < v1 < NB - 32:
        nm = cstr(w0)
        if nm is None or len(nm) > 40:
            continue
        # value header at v1: {1, node}; node at v1+24
        if int(u32[v1 // 4]) != 1 or int(u32[v1 // 4 + 1]) != v1 + 24:
            continue
        idx = int(u32[(v1 + 24) // 4])
        entries.append((k * 4, nm, v1, idx))

print('sampler setparam entries found:', len(entries))
real = [(a, nm, v1, idx) for (a, nm, v1, idx) in entries if 0 <= idx < 176]
nones = [(a, nm, v1) for (a, nm, v1, idx) in entries if idx == 0xffffffff]
other = [(a, nm, v1, idx) for (a, nm, v1, idx) in entries if idx != 0xffffffff and not (0 <= idx < 176)]
print('  with real image idx:', len(real))
print('  -1 (none):', len(nones))
print('  other idx:', len(other), other[:6])
names = {}
for (_, nm, _, _) in entries:
    names[nm] = names.get(nm, 0) + 1
print('  param names:', names)

out = []
for (a, nm, v1, idx) in real:
    i, nmptr, tgptr = imgs[idx]
    out.append({'entry': hex(a), 'name': nm, 'idx': idx,
                'image': cstr(nmptr), 'tga': cstr(tgptr)})
print('  first 8 real:', json.dumps(out[:8], indent=1))
print('  entry addr range: ', hex(min(a for a, _, _, _ in real) if real else 0),
      hex(max(a for a, _, _, _ in real) if real else 0))
json.dump({'entries': [{'entry': hex(a), 'name': nm, 'v1': hex(v1), 'idx': idx}
                        for (a, nm, v1, idx) in entries],
           'real': out},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t1_bindings_raw.json', 'w'), indent=1)
print('saved s47_t1_bindings_raw.json')
