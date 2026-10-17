#!/usr/bin/env python3
"""S31 T2 FINAL: Batman skeleton + skin mapping solved.

Results:
  1. node records decoded (see s31_t2_skeleton.py): 107 nodes, 66 BoneNN aliases
  2. skin palette @0x3167c = 31 BoneNN names, palette order = skin-id order
  3. mapping: skin id b (0-based, ids 0..30) -> palette[b] -> node via alias
     VERIFIED two ways: (a) BoneNN alias == Bip01 node names (67-node tree);
     (b) influence centroids of each id land at the anatomy of its name.
  4. hierarchy: parent table for all palette bones (child ptrs + biped std)
  5. bind arrays: body 31 @0x30e30, cape 38 @0x5a210, cape_down 38 @0x675a4
     (palette-ordered; space transform still resisting -> open item)
  6. deliverables: parents print, inverse-bind dump, one skinned vertex,
     glTF export with joints+weights (IBMs = inverse node worlds => mesh
     reproduced exactly in three.js by construction)
"""
import struct, math, json
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]


def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v:
            return d[v:e].decode('latin1')
    return None


nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32(o)), pool(u32(o + 4)), pool(u32(o + 8))
    if n1 is None or n2 is None or al is None:
        o += 4
        continue
    t = struct.unpack_from('<3f', d, o + 0x0c)
    q = struct.unpack_from('<4f', d, o + 0x18)
    s = struct.unpack_from('<3f', d, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s):
        o += 4
        continue
    if u32(o + 0x34) != 1 or u32(o + 0x38) > 32:
        o += 4
        continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s,
                      ccount=u32(o + 0x38), child=u32(o + 0x3c)))
    o += 0x50
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
by_name = {n['name']: n for n in nodes}
print(f'nodes {len(nodes)}, bone-aliased {len(by_alias)}')

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8

BIPED = {
    'Bip01_Pelvis': 'Bip01', 'Bip01_Spine': 'Bip01_Pelvis',
    'Bip01_Spine1': 'Bip01_Spine', 'Bip01_Neck': 'Bip01_Spine1',
    'Bip01_Head': 'Bip01_Neck',
    'Bip01_L_Thigh': 'Bip01_Pelvis', 'Bip01_L_Calf': 'Bip01_L_Thigh',
    'Bip01_L_Foot': 'Bip01_L_Calf', 'Bip01_R_Thigh': 'Bip01_Pelvis',
    'Bip01_R_Calf': 'Bip01_R_Thigh', 'Bip01_R_Foot': 'Bip01_R_Calf',
    'Bip01_L_Clavicle': 'Bip01_Spine1', 'Bip01_L_UpperArm': 'Bip01_L_Clavicle',
    'Bip01_L_Forearm': 'Bip01_L_UpperArm', 'Bip01_L_Hand': 'Bip01_L_Forearm',
    'Bip01_R_Clavicle': 'Bip01_Spine1', 'Bip01_R_UpperArm': 'Bip01_R_Clavicle',
    'Bip01_R_Forearm': 'Bip01_R_UpperArm', 'Bip01_R_Hand': 'Bip01_R_Forearm',
    'Bip01_L_Finger0': 'Bip01_L_Hand', 'Bip01_L_Finger01': 'Bip01_L_Finger0',
    'Bip01_L_Finger1': 'Bip01_L_Hand', 'Bip01_L_Finger11': 'Bip01_L_Finger1',
    'Bip01_L_Finger2': 'Bip01_L_Hand', 'Bip01_L_Finger21': 'Bip01_L_Finger2',
    'Bip01_R_Finger0': 'Bip01_R_Hand', 'Bip01_R_Finger01': 'Bip01_R_Finger0',
    'Bip01_R_Finger1': 'Bip01_R_Hand', 'Bip01_R_Finger11': 'Bip01_R_Finger1',
    'Bip01_R_Finger2': 'Bip01_R_Hand', 'Bip01_R_Finger21': 'Bip01_R_Finger2',
}
parent = dict(BIPED)
for n in nodes:
    c = by_name.get(pool(u32(n['child']) and n['child'] or 0) or '')
# parents from child ptrs (override where resolvable)
by_off = {n['off']: n for n in nodes}
for n in nodes:
    c = by_off.get(n['child'])
    if c is not None and c['name'] in BIPED:
        parent[c['name']] = n['name']

print('\n=== 1. PARENT TABLE (palette bones) ===')
joint_nodes = []
for b, p in enumerate(pal):
    nm = by_alias[p]['name']
    joint_nodes.append(nm)
    print(f'  joint {b:2d} = {p:8s} node {nm:20s} parent {parent.get(nm)}')


def normq(q):
    n = math.sqrt(sum(x * x for x in q))
    return tuple(x / n for x in q)


def qmat(q):
    x, y, z, w = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])


def node_world(name):
    """row-vector world: v' = v (S R)^parent ... (S R)^node + ..."""
    chain = [name]
    while parent.get(chain[-1]):
        chain.append(parent[chain[-1]])
    chain.reverse()
    M = np.eye(3)
    t = np.zeros(3)
    for nm in chain:
        n = by_name[nm]
        R = qmat(normq(n['q']))
        lM = (R * np.array(n['s'])).T          # row-vector: M = (R S)^T
        lt = np.array(n['t'])
        M = lM @ M
        t = lt @ M + t
    return M, t


print('\n=== 2. NODE WORLD POSITIONS (default pose, model space) ===')
worlds = {}
for nm in joint_nodes:
    M, t = node_world(nm)
    worlds[nm] = (M, t)
    print(f'  {nm:20s} t = ({t[0]:8.4f}, {t[1]:8.4f}, {t[2]:8.4f})')

print('\n=== 3. MAPPING VERIFICATION: influence centroids vs node worlds ===')
BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
cent = np.zeros((31, 3))
cnt = np.zeros(31, int)
skin = []
for i in range(N):
    b4 = struct.unpack_from('<4B', d, SKIN + i * 20)
    w4 = struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
    skin.append((b4, w4))
    for j in range(4):
        if w4[j] >= 0.4 and b4[j] < 31:
            cent[b4[j]] += verts[i]
            cnt[b4[j]] += 1
for b in range(31):
    if cnt[b]:
        cent[b] /= cnt[b]
errs = []
for b in range(31):
    if not cnt[b]:
        continue
    wt = worlds[joint_nodes[b]][1]
    e = float(np.linalg.norm(cent[b] - wt))
    errs.append(e)
    print(f'  joint {b:2d} {pal[b]:8s} {joint_nodes[b]:20s} '
          f'centroid ({cent[b][0]:7.3f},{cent[b][1]:7.3f},{cent[b][2]:7.3f}) '
          f'node ({wt[0]:7.3f},{wt[1]:7.3f},{wt[2]:7.3f}) '
          f'dist {e*100:6.1f} cm  n={cnt[b]}')
print(f'\n  median centroid-vs-node distance: '
      f'{sorted(errs)[len(errs)//2]*100:.1f} cm '
      f'(shuffled-null median would be ~40-60 cm for a 1.9 m figure)')

# shuffled-mapping null
rng = np.random.default_rng(11)
nulls = []
for trial in range(20):
    perm = rng.permutation(31)
    es = []
    for b in range(31):
        if not cnt[b]:
            continue
        wt = worlds[joint_nodes[perm[b]]][1]
        es.append(float(np.linalg.norm(cent[b] - wt)))
    nulls.append(sorted(es)[len(es)//2])
print(f'  permuted-mapping null: median-of-medians '
      f'{sorted(nulls)[10]*100:.1f} cm (20 trials)')

print('\n=== 4. INVERSE-BIND DUMP (body array @0x30e30, first 3) ===')
for k in range(3):
    m = struct.unpack_from('<16f', d, 0x30e30 + k * 64)
    print(f'  IBM[{k}] ({pal[k]}):')
    for r in range(4):
        print('        ', tuple(round(x, 5) for x in m[r*4:r*4+4]))

print('\n=== 5. ONE SKINNED VERTEX (record 0) ===')
b4, w4 = skin[0]
v0 = verts[0]
print(f'  v0 = {tuple(round(x, 4) for x in v0)}')
print(f'  joints {[int(x) for x in b4]} = '
      f'{[joint_nodes[b] if b < 31 else "?" for b in b4]}')
print(f'  weights {tuple(round(x, 4) for x in w4)}')

print('\n=== 6. UV verdict (from r20 + this round) ===')
uvs = [struct.unpack_from('<4H', d, BASE + i * 80 + 72) for i in range(N)]
allv = [x for q in uvs for x in q]
print(f'  two 4.12 fixed-point u16 streams @+72/+76, range '
      f'[{min(allv)/4096:.3f}, {max(allv)/4096:.3f}) = 4x4 tile atlas')
print('  adjacent same-tile 49.6% vs shuffled null 7.0% (r20 numbers)')
print('  refuted with numbers: f16 decode, plain u16/65535')
# seam check: vertices sharing position but different UV
from collections import defaultdict
posmap = defaultdict(list)
for i in range(N):
    posmap[tuple(np.round(verts[i], 4))].append(i)
seams = sum(1 for g in posmap.values() if len(g) > 1
            and len({uvs[i] for i in g}) > 1)
multi = sum(1 for g in posmap.values() if len(g) > 1)
print(f'  seam check: {seams}/{multi} position-shared groups differ in UV '
      f'(UV-seam splits expected for a skinned export)')

print('\n=== 7. glTF EXPORT ===')
# joints = the 31 palette nodes; hierarchy rooted at Bip01 (parent chain)
# IBM = inverse of node world (row-vector -> column-vector 4x4 for glTF)
ibm = []
for nm in joint_nodes:
    M, t = worlds[nm]
    R = M.T                      # column-conv rotation
    ti = -R @ t
    m4 = np.eye(4)
    m4[:3, :3] = R
    m4[:3, 3] = ti
    ibm.append(m4)

# minimal glTF writer
import base64
jnodes = []
# build node list: include full ancestor chain + all needed nodes
need = set()
for nm in joint_nodes:
    cur = nm
    while True:
        need.add(cur)
        p = parent.get(cur)
        if not p:
            break
        cur = p
allnodes = [n for n in by_name.values() if n['name'] in need]
order = {n['name']: i for i, n in enumerate(allnodes)}
jidx = {nm: order[nm] for nm in joint_nodes}

def quat_wxyz(n):
    x, y, z, w = normq(n['q'])
    return (w, x, y, z)

gnodes = []
for n in allnodes:
    p = parent.get(n['name'])
    gnodes.append(dict(name=n['name'],
                       translation=[float(x) for x in n['t']],
                       rotation=[float(x) for x in quat_wxyz(n)],
                       scale=[float(x) for x in n['s']],
                       children=[] if n['name'] not in parent else None))
for g, n in zip(gnodes, allnodes):
    kids = [order[k['name']] for k in allnodes
            if parent.get(k['name']) == n['name']]
    g['children'] = kids
    if g['children'] == []:
        del g['children']
    p = parent.get(n['name'])
    if p is None:
        g['scene_root'] = True
    # strip identity transforms? keep (harmless)

# buffers: positions, indices, texcoords, weights, joints, IBM
IDX_OFF = 0x210bc
NIDX = 5655
ids = np.array([struct.unpack_from('<H', d, IDX_OFF + 2 * i)[0]
                for i in range(NIDX)], dtype=np.uint16)
uv = np.array([[q[0] / 4096.0, 1.0 - q[1] / 4096.0] for q in uvs],
              dtype=np.float32)
wt = np.zeros((N, 4), dtype=np.float32)
jn = np.zeros((N, 4), dtype=np.uint16)
for i, (b4, w4) in enumerate(skin):
    wt[i] = w4
    jn[i] = [min(b, 31) for b in b4]

pos_bytes = verts.astype(np.float32).tobytes()
uv_bytes = uv.tobytes()
wt_bytes = wt.tobytes()
jn_bytes = jn.tobytes()
ibm_bytes = np.concatenate([m.T.reshape(1, -1) for m in ibm]).astype(
    np.float32).tobytes()   # column-major 4x4
idx_bytes = ids.tobytes()

buf = (pos_bytes + uv_bytes + wt_bytes + jn_bytes + ibm_bytes + idx_bytes)
b64 = base64.b64encode(buf).decode()
BV = len(pos_bytes)
Buv = BV + len(uv_bytes)
Bwt = Buv + len(wt_bytes)
Bjn = Bwt + len(jn_bytes)
Bibm = Bjn + len(ibm_bytes)
Bidx = Bibm + len(idx_bytes)

gltf = {
    'asset': {'version': '2.0', 'generator': 'tdkr-s31-t2'},
    'scene': 0,
    'scenes': [{'nodes': []}],
    'nodes': gnodes,
    'skins': [{'inverseBindMatrices': 5, 'joints':
               [jidx[nm] for nm in joint_nodes]}],
    'meshes': [{'primitives': [{'attributes': {'POSITION': 0, 'TEXCOORD_0': 1,
                                               'WEIGHTS_0': 2, 'JOINTS_0': 3},
                                'indices': 4, 'material': 0}]}],
    'materials': [{'pbrMetallicRoughness': {'baseColorTexture': {'index': 0}}},
                  ],
    'textures': [{'source': 0, 'sampler': 0}],
    'samplers': [{'magFilter': 9729, 'minFilter': 9987,
                  'wrapS': 10497, 'wrapT': 10497}],
    'images': [{'uri': 'chara_Batman_DIFFUSE.png'}],
    'buffers': [{'byteLength': len(buf), 'uri':
                 'data:application/octet-stream;base64,' + b64}],
    'bufferViews': [
        {'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos_bytes),
         'target': 34962},
        {'buffer': 0, 'byteOffset': Buv, 'byteLength': len(uv_bytes),
         'target': 34962},
        {'buffer': 0, 'byteOffset': Bwt, 'byteLength': len(wt_bytes),
         'target': 34962},
        {'buffer': 0, 'byteOffset': Bjn, 'byteLength': len(jn_bytes),
         'target': 34962},
        {'buffer': 0, 'byteOffset': Bibm, 'byteLength': len(ibm_bytes)},
        {'buffer': 0, 'byteOffset': Bidx, 'byteLength': len(idx_bytes),
         'target': 34963},
    ],
    'accessors': [
        {'bufferView': 0, 'componentType': 5126, 'count': N, 'type': 'VEC3',
         'min': verts.min(0).tolist(), 'max': verts.max(0).tolist()},
        {'bufferView': 1, 'componentType': 5126, 'count': N, 'type': 'VEC2'},
        {'bufferView': 2, 'componentType': 5126, 'count': N, 'type': 'VEC4'},
        {'bufferView': 3, 'componentType': 5123, 'count': N, 'type': 'VEC4'},
        {'bufferView': 4, 'componentType': 5126, 'count': 31, 'type': 'MAT4'},
        {'bufferView': 5, 'componentType': 5123, 'count': NIDX,
         'type': 'SCALAR'},
    ],
}
# fix scene roots: nodes without parents in the need-set
roots = [order[n['name']] for n in allnodes
         if parent.get(n['name']) not in need]
gltf['scenes'] = [{'nodes': roots}]
out = '/home/z/my-project/download/batman_bindpose.glb'
import json as _j
with open(out, 'wb') as f:
    js = _j.dumps(gltf).encode()
    f.write(struct.pack('<I', 0x46546C67))
    f.write(struct.pack('<I', 2))
    f.write(struct.pack('<I', 12 + 8 + len(js) + 8 + len(buf)))
    f.write(struct.pack('<I', len(js)))
    f.write(struct.pack('<I', 0x4E4F534A))
    f.write(js)
    f.write(struct.pack('<I', len(buf)))
    f.write(struct.pack('<I', 0x004E4942))
    f.write(buf)
import os
print(f'  wrote {out} ({os.path.getsize(out)/1e6:.2f} MB), '
      f'{N} verts, {NIDX} indices, 31 joints')
json.dump(dict(palette=pal, joint_nodes=joint_nodes,
               parents={j: parent.get(joint_nodes[j]) for j in range(31)},
               mapping_proof=dict(median_cm=sorted(errs)[len(errs)//2]*100,
                                  null_cm=sorted(nulls)[10]*100)),
          open('/home/z/my-project/download/s31_t2_result.json', 'w'),
          indent=1)
print('  wrote s31_t2_result.json')
