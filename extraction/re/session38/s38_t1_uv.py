#!/usr/bin/env python3
"""S38 T1c: UV seam-continuity check vs shuffled-UV null.
Vertices sharing a position (uv-split duplicates) must sample the same texel
(mod tiling period) unless they sit on an atlas seam. Matching rate vs a null
where UV assignments are shuffled among shared-position groups.
"""
import struct, json
import numpy as np
from PIL import Image

buf = open('/home/z/my-project/download/batman_s38_textured.glb', 'rb').read()
jl = struct.unpack('<I', buf[12:16])[0]
gj = json.loads(buf[20:20 + jl]); bin_off = 20 + jl + 8
prim = gj['meshes'][0]['primitives'][0]
def acc(ai):
    a = gj['accessors'][ai]; bv = gj['bufferViews'][a['bufferView']]
    off = bin_off + bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    n = a['count']
    t = a['type']
    if t == 'VEC3': return np.frombuffer(buf, np.float32, n * 3, off).reshape(n, 3)
    if t == 'VEC2': return np.frombuffer(buf, np.float32, n * 2, off).reshape(n, 2)
    return np.frombuffer(buf, np.uint16, n, off)

V = acc(prim['attributes']['POSITION']).astype(np.float64)
UV = acc(prim['attributes']['TEXCOORD_0']).astype(np.float64)
tex = np.frombuffer(open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_batman_diffuse_src.bin', 'rb').read(), np.uint8).reshape(1024, 1024, 3)

# group by quantized position
q = np.round(V / 1e-4).astype(np.int64)
key = q[:, 0] * 2**40 + q[:, 1] * 2**20 + q[:, 2]
from collections import defaultdict
groups = defaultdict(list)
for i, k in enumerate(key): groups[int(k)].append(i)
multi = [g for g in groups.values() if len(g) > 1]
print(f'shared-position groups: {len(multi)} (verts {sum(len(g) for g in multi)})')

def sample(uv):
    # REPEAT wrap at the texture scale (atlas tiles [0,16))
    tu = np.mod(uv, 1.0)
    x = np.clip((tu[:, 0] * 1024).astype(int), 0, 1023)
    y = np.clip((tu[:, 1] * 1024).astype(int), 0, 1023)
    return tex[y, x].astype(int)

# pairs within groups: match if texel colors equal (atlas seam pairs differ)
rng = np.random.default_rng(38)
def match_rate(pairs, uvA, uvB):
    if not pairs: return 0.0
    pa = np.array([p[0] for p in pairs]); pb = np.array([p[1] for p in pairs])
    ca = sample(uvA[pa]); cb = sample(uvB[pb])
    d = np.abs(ca - cb).max(1)
    return float((d <= 8).mean())

pairs = []
for g in multi:
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            pairs.append((g[i], g[j]))
print('pairs:', len(pairs))
real = match_rate(pairs, UV, UV)
# seam-subset: pairs whose UV distance is NOT ~integer (true atlas seams)
pa = np.array([p[0] for p in pairs]); pb = np.array([p[1] for p in pairs])
duv = np.abs(UV[pa] - UV[pb])
frac_int = (np.abs(duv - np.round(duv)) < 1e-3).all(1)
print(f'pairs with integer-UV offset (same texel by REPEAT): {frac_int.mean()*100:.1f}%')
same_texel = match_rate([p for p, f in zip(pairs, frac_int) if f], UV, UV)
print(f'match rate, integer-offset pairs: {same_texel*100:.1f}%')

# NULL: shuffle UV assignment among all verts of the same group count
uv_sh = UV[rng.permutation(len(UV))]
null = match_rate(pairs, UV, uv_sh)
# NULL 2: shift all UVs by a random non-integer offset (destroys texel identity)
uv_off = UV + np.array([0.0137, 0.0091])
null2 = match_rate(pairs, UV, uv_off)

res = {
    'pairs': len(pairs),
    'match_rate_real': round(real, 4),
    'match_rate_null_shuffled_uv': round(null, 4),
    'match_rate_null_offset_uv': round(null2, 4),
    'integer_offset_pair_pct': round(float(frac_int.mean()), 4),
    'match_rate_integer_offset_pairs': round(same_texel, 4),
}
print(json.dumps(res, indent=1))
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t1_uv_seams.json', 'w'), indent=1)
print('saved s38_t1_uv_seams.json')
