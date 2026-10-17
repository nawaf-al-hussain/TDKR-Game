#!/usr/bin/env python3
"""S32 T1l: export GLBs with REAL inverse bind matrices + rig variants,
and dump expected arrays for the three.js verifier.

Variant A (batman_s32_filerig.glb): node locals exactly as stored in the
  bdae (the engine's rest rig). Rest pose deforms the arms (rig != bind).
Variant B (batman_s32_bindpose.glb): clavicle+upperarm (4 records) locals replaced by bind-derived locals -> rest pose ==
  mesh bind pose exactly (max err 0.02 cm in numpy).

IBMs are the raw stored 64-B blocks (file row-major order == glTF
column-major order of the column-convention inverse bind).
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
JN = by_name

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]
idx = {joint_nodes[b]: b for b in range(31)}

PNAME = {0: 'Bip01_R_Calf', 1: 'Bip01_R_Thigh', 2: 'Bip01_Pelvis',
         3: 'Bip01_L_Calf', 4: 'Bip01_L_Thigh', 5: 'Bip01_Pelvis',
         6: 'Bip01_R_Hand', 7: 'Bip01_R_Hand', 8: 'Bip01_R_Forearm',
         9: 'Bip01_R_UpperArm', 10: 'Bip01_R_Clavicle', 11: 'Bip01_Spine1',
         12: 'Bip01_L_Hand', 13: 'Bip01_L_Hand', 14: 'Bip01_L_Forearm',
         15: 'Bip01_L_UpperArm', 16: 'Bip01_L_Clavicle', 17: 'Bip01_Spine1',
         18: 'Bip01_Neck', 19: 'Bip01_Spine1', 20: 'Bip01_Spine',
         21: 'Bip01_Pelvis', 22: 'Bip01',
         23: 'Bip01_L_Finger0', 24: 'Bip01_L_Finger1', 25: 'Bip01_L_Hand',
         26: 'Bip01_L_Finger2', 27: 'Bip01_R_Finger0', 28: 'Bip01_R_Finger1',
         29: 'Bip01_R_Hand', 30: 'Bip01_R_Finger2'}
BIP = {'Bip01_Pelvis': 'Bip01', 'Bip01_Spine': 'Bip01_Pelvis',
       'Bip01_Spine1': 'Bip01_Spine', 'Bip01_Neck': 'Bip01_Spine1',
       'Bip01_Head': 'Bip01_Neck'}


def parent_name(nm):
    for b, p in PNAME.items():
        if joint_nodes[b] == nm:
            return p
    return BIP.get(nm)


def qrot_row(q):
    x, y, z, w = q
    Rc = np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T


def local_row(n):
    M = np.eye(4)
    M[:3, :3] = qrot_row(n['q']) @ np.diag(n['s'])
    M[3, :3] = np.array(n['t'])
    return M


BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])

BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20)
                for i in range(N)], np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
                for i in range(N)], np.float64)
IDX_OFF, NIDX = 0x210bc, 5655
ids = np.array([struct.unpack_from('<H', d, IDX_OFF + 2 * i)
                for i in range(NIDX)], np.uint16)
uvs = np.array([[struct.unpack_from('<H', d, BASE + i * 80 + 72)[0] / 4096.0,
                 1.0 - struct.unpack_from('<H', d, BASE + i * 80 + 76)[0] /
                 4096.0] for i in range(N)], np.float32)

# node set: all ancestors of palette joints + the joints themselves
need = set()
for b in range(31):
    nm = joint_nodes[b]
    while nm:
        need.add(nm)
        nm = parent_name(nm)
chain_nodes = [n for n in nodes if n['name'] in need]
# deterministic order: parents before children
order = {}
placed = set()


def place(nm):
    if nm in placed:
        return
    p = parent_name(nm)
    if p:
        place(p)
    order[nm] = len(order)
    placed.add(nm)


for nm in sorted(need):
    place(nm)
gnodes = []
node_of = {}
for nm, gi in order.items():
    node_of[nm] = gi
    gnodes.append(dict(name=nm, children=[]))
roots = [nm for nm in order if parent_name(nm) is None]
for nm in order:
    p = parent_name(nm)
    if p:
        gnodes[node_of[p]]['children'].append(node_of[nm])


def write_glb(path, override_bones):
    # node matrices
    override = {}
    for b in override_bones:
        p = PNAME[b]
        pi = idx.get(p, -1)
        L = binds[b] @ (np.linalg.inv(binds[pi]) if pi >= 0 else np.eye(4))
        override[joint_nodes[b]] = L
    mats = []
    for nm in order:
        if nm in override:
            M = override[nm]
        elif nm in JN:
            M = local_row(JN[nm])
        else:
            M = np.eye(4)     # BATMAN/other roots: identity
        mats.append(M)
    # skins: joints in palette order
    jindices = [node_of[joint_nodes[b]] for b in range(31)]
    ibm_bytes = b''.join(struct.pack('<16f', *m.reshape(-1)) for m in invB)

    pos_b = verts.astype(np.float32).tobytes()
    uv_b = uvs.tobytes()
    wt_b = w4s.astype(np.float32).tobytes()
    jn_b = b4s.astype(np.uint16).tobytes()
    idx_b = ids.tobytes()
    mat_b = b''.join(struct.pack('<16f', *m.reshape(-1)) for m in mats)
    pad = lambda n: n + ((4 - n % 4) % 4)
    buf = pos_b + uv_b + wt_b + jn_b + idx_b + ibm_bytes + mat_b
    O1 = pad(len(pos_b)); O2 = pad(O1 + len(uv_b)); O3 = pad(O2 + len(wt_b))
    O4 = pad(O3 + len(jn_b)); O5 = pad(O4 + len(idx_b))
    O6 = pad(O5 + len(ibm_bytes))
    total_len = O6 + len(mat_b)
    buf = bytearray(total_len)
    for seg, off in ((pos_b, 0), (uv_b, O1), (wt_b, O2), (jn_b, O3),
                     (idx_b, O4), (ibm_bytes, O5), (mat_b, O6)):
        buf[off:off + len(seg)] = seg
    buf = bytes(buf)
    gltf = {
        'asset': {'version': '2.0', 'generator': 'tdkr-s32-t1'},
        'scene': 0,
        'scenes': [{'nodes': [node_of[r] for r in roots]}],
        'nodes': [{'name': g['name'],
                   'matrix': [float(x) for x in mats[gi].reshape(-1)],
                   **({'children': g['children']} if g['children'] else {})}
                  for gi, g in enumerate(gnodes)],
        'skins': [{'inverseBindMatrices': 5, 'joints': jindices}],
        'meshes': [{'primitives': [{'attributes': {'POSITION': 0,
                                                   'TEXCOORD_0': 1,
                                                   'JOINTS_0': 3,
                                                   'WEIGHTS_0': 2},
                                    'indices': 4, 'material': 0}]}],
        'materials': [{'pbrMetallicRoughness': {
            'baseColorFactor': [0.15, 0.17, 0.22, 1.0],
            'metallicFactor': 0.1, 'roughnessFactor': 0.8}}],
        'buffers': [{'byteLength': len(buf)}],
        'bufferViews': [
            {'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos_b),
             'target': 34962},
            {'buffer': 0, 'byteOffset': O1, 'byteLength': len(uv_b),
             'target': 34962},
            {'buffer': 0, 'byteOffset': O2, 'byteLength': len(wt_b),
             'target': 34962},
            {'buffer': 0, 'byteOffset': O3, 'byteLength': len(jn_b),
             'target': 34962},
            {'buffer': 0, 'byteOffset': O4, 'byteLength': len(idx_b),
             'target': 34963},
            {'buffer': 0, 'byteOffset': O5, 'byteLength': len(ibm_bytes)},
            {'buffer': 0, 'byteOffset': O6, 'byteLength': len(mat_b)},
        ],
        'accessors': [
            {'bufferView': 0, 'componentType': 5126, 'count': N,
             'type': 'VEC3', 'min': verts.min(0).tolist(),
             'max': verts.max(0).tolist()},
            {'bufferView': 1, 'componentType': 5126, 'count': N,
             'type': 'VEC2'},
            {'bufferView': 2, 'componentType': 5126, 'count': N,
             'type': 'VEC4'},
            {'bufferView': 3, 'componentType': 5123, 'count': N,
             'type': 'VEC4'},
            {'bufferView': 4, 'componentType': 5123, 'count': NIDX,
             'type': 'SCALAR'},
            {'bufferView': 5, 'componentType': 5126, 'count': 31,
             'type': 'MAT4'},
        ],
        'scenes': [{'nodes': [node_of[r] for r in roots]}],
    }
    # meshes need skins reference
    gltf['meshes'][0]['primitives'][0]['targets'] = []
    del gltf['meshes'][0]['primitives'][0]['targets']
    gltf['nodes_mesh'] = {}
    # attach mesh to the zup-fix root: create a dedicated mesh node
    gltf['nodes'].append({'name': 'BODY', 'skin': 0, 'mesh': 0})
    body_idx = len(gltf['nodes']) - 1
    gltf['scenes'][0]['nodes'].append(body_idx)
    # pad buffer to 4
    js = json.dumps(gltf, separators=(',', ':')).encode()
    while len(js) % 4:
        js += b' '
    total = 12 + 8 + len(js) + 8 + len(buf)
    with open(path, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, total))
        f.write(struct.pack('<II', len(js), 0x4E4F534A))
        f.write(js)
        f.write(struct.pack('<II', len(buf), 0x004E4942))
        f.write(buf)
    print(f'wrote {path} ({total} B)')


import os
OUT = '/home/z/my-project/download'
os.makedirs(OUT, exist_ok=True)
write_glb(f'{OUT}/batman_s32_filerig.glb', [])
write_glb(f'{OUT}/batman_s32_bindpose.glb', [10, 11, 16, 17])

# ---- expected arrays for the three.js verifier ----
V = np.hstack([verts, np.ones((N, 1))])
worlds = {b: None for b in range(31)}
# recompute worlds from the ACTUAL exported node matrices (walk glTF nodes)
gmat = {}
for nm in order:
    if nm in JN and nm not in [joint_nodes[b] for b in range(31)]:
        pass
for variant, fname, override_bones in (
        ('filerig', 'batman_s32_filerig.glb', []),
        ('bindpose', 'batman_s32_bindpose.glb', [10, 11, 16, 17])):
    override = {}
    for b in override_bones:
        p = PNAME[b]
        pi = idx.get(p, -1)
        L = binds[b] @ (np.linalg.inv(binds[pi]) if pi >= 0 else np.eye(4))
        override[joint_nodes[b]] = L
    def world(name):
        chain = [name]
        while parent_name(chain[-1]):
            chain.append(parent_name(chain[-1]))
        chain.reverse()
        M = np.eye(4)
        for nm in chain:
            if nm in override:
                M = override[nm] @ M
            elif nm in JN:
                M = local_row(JN[nm]) @ M
        return M
    W = {b: world(joint_nodes[b]) for b in range(31)}
    sp = np.zeros((N, 3))
    for j in range(4):
        sel_ids = np.clip(b4s[:, j], 0, 30)
        Wj = w4s[:, j]
        for b in range(31):
            sel = sel_ids == b
            if not sel.any():
                continue
            M = invB[b] @ W[b]
            sp[sel] += Wj[sel][:, None] * (V[sel] @ M)[:, :3]
    e = np.linalg.norm(sp - verts, axis=1)
    print(f'{variant}: numpy prediction exact<0.1cm '
          f'{int((e < 1e-3).sum())}/1449, mean {e.mean()*100:.2f} cm, '
          f'max {e.max()*100:.2f} cm')
    np.savez(f'/home/z/my-project/scripts/jsverify/expected_{variant}.npz',
             verts=verts, skinned=sp, err=e)

json.dump(dict(node_names=list(order), joints=[joint_nodes[b] for b in
                                                  range(31)],
               roots=roots),
          open('/home/z/my-project/scripts/jsverify/gltf_meta.json', 'w'))
print('expected_*.npz + gltf_meta.json written')
