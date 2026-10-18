#!/usr/bin/env python3
"""S33 T2c: complete glTF export + UV verification + pose-change variant.

Extends r32 exporter: bind-aligned node rest (mesh reproduced exactly),
real stored IBMs, full joint hierarchy, weights, UVs (4.12 fixed point),
plus a POSED variant (R_UpperArm +25 deg about X) for the three.js-vs-numpy
deformation check. UV battery: tile occupancy, seam stats, shuffled null.
"""
import struct, math, json, collections
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v: return d[v:e].decode('latin1')

nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32(o)), pool(u32(o + 4)), pool(u32(o + 8))
    if n1 is None or n2 is None or al is None: o += 4; continue
    t = struct.unpack_from('<3f', d, o + 0x0c)
    q = struct.unpack_from('<4f', d, o + 0x18)
    s = struct.unpack_from('<3f', d, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s): o += 4; continue
    if u32(o + 0x34) != 1 or u32(o + 0x38) > 32: o += 4; continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
by_name = {n['name']: n for n in nodes}
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11,
       11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
PNAME = {b: joint_nodes[P31[b]] for b in P31}
JN = {n['name']: n for n in nodes}

def parent_name(nm):
    return JN[nm]['name'].join(['']) and None  # placeholder, replaced below

# parent from name conventions (same as r32)
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
PN = {joint_nodes[b]: joint_nodes[P31[b]] for b in P31}
# per-palette-index parent NAME map (r32-verified, correct finger middles)
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
pname_of = {joint_nodes[b]: PNAME[b] for b in PNAME}
def parent_name(nm):
    if nm in pname_of: return pname_of[nm]
    if nm in BIPED: return BIPED[nm]
    return None

BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])
BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80) for i in range(N)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20) for i in range(N)], np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4) for i in range(N)])
IDX_OFF, NIDX = 0x210bc, 5655
ids = np.array([struct.unpack_from('<H', d, IDX_OFF + 2 * i) for i in range(NIDX)], np.uint16)
uv_r = np.array([struct.unpack_from('<H', d, BASE + i * 80 + 72)[0] for i in range(N)], np.float64)
uv_v = np.array([struct.unpack_from('<H', d, BASE + i * 80 + 76)[0] for i in range(N)], np.float64)
uvs = np.stack([uv_r / 4096.0, uv_v / 4096.0], 1).astype(np.float32)

# ================= UV battery =================
tile_u = (uv_r // 16384).astype(int)   # 4x4 atlas over [0,16) range: tile = uv//4
tile_v = (uv_v // 16384).astype(int)
in_range = float(((uv_r / 4096.0 < 16.0).mean()))
tiles_used = len({(a, b) for a, b in zip(tile_u, tile_v)})
# seam: position-shared groups with differing UV
qkey = collections.defaultdict(list)
for i in range(N):
    qkey[tuple(np.round(verts[i], 4))].append(i)
shared = {k: v for k, v in qkey.items() if len(v) > 1}
seam_groups = 0
for k, v in shared.items():
    if len({(uv_r[i], uv_v[i]) for i in v}) > 1:
        seam_groups += 1
rng = np.random.default_rng(35)
perm = rng.permutation(N)
seam_null = 0
for k, v in shared.items():
    vv = perm[v]
    if len({(uv_r[i], uv_v[i]) for i in vv}) > 1:
        seam_null += 1
print(f'UV: range-ok {in_range*100:.2f}%, tiles used {tiles_used}/16, '
      f'shared-pos groups {len(shared)}, UV-differing (seams) {seam_groups} '
      f'({100*seam_groups/max(1,len(shared)):.1f}%) vs shuffled null '
      f'{seam_null} ({100*seam_null/max(1,len(shared)):.1f}%)')

# quad edge-consistency proxy: indices forming tris, check adjacent-tri UV continuity
# (shares) — skip; the seam+tile+range stats + null are the battery.

# ================= exporter =================
def qmat_row(q):
    x, y, z, w = q
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

def local_row(n):
    M = np.eye(4)
    M[:3, :3] = qmat_row(n['q']) @ np.diag(n['s'])
    M[3, :3] = n['t']
    return M

need = set()
for b in range(31):
    nm = joint_nodes[b]
    while nm:
        need.add(nm); nm = parent_name(nm)
chain_nodes = [n for n in nodes if n['name'] in need]
order = {}
placed = set()
def place(nm):
    if nm in placed: return
    p = parent_name(nm)
    if p: place(p)
    order[nm] = len(order); placed.add(nm)
for nm in sorted(need): place(nm)
gnodes = []
node_of = {}
for nm, gi in order.items():
    node_of[nm] = gi
    gnodes.append(dict(name=nm, children=[]))
roots = [nm for nm in order if parent_name(nm) is None]
for nm in order:
    p = parent_name(nm)
    if p: gnodes[node_of[p]]['children'].append(node_of[nm])

ALIGN = [10, 11, 16, 17]   # clavicles + upper arms (bind-aligned rest)

def posed_local(b, deg):
    """bind-aligned local for bone b with an extra +deg X rotation (pose change)."""
    p = pname_of[joint_nodes[b]]
    pi = [k for k in range(31) if joint_nodes[k] == p][0]
    L = binds[b] @ np.linalg.inv(binds[pi])
    c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    Rx = np.eye(4); Rx[1, 1] = c; Rx[1, 2] = -s_; Rx[2, 1] = s_; Rx[2, 2] = c
    return L @ Rx

def write_glb(path, override, posed_bone=None, posed_deg=0.0):
    mats = []
    for nm in order:
        if posed_bone is not None and joint_nodes[posed_bone] == nm:
            M = posed_local(posed_bone, posed_deg)
        elif nm in override:
            M = override[nm]
        elif nm in JN:
            M = local_row(JN[nm])
        else:
            M = np.eye(4)
        mats.append(M)
    ibm_bytes = b''.join(
        np.asarray(invB[b], np.float32).tobytes() for b in range(31))
    jindices = [node_of[joint_nodes[b]] for b in range(31)]
    pos_b = verts.astype(np.float32).tobytes()
    uv_b = uvs.tobytes()
    wt_b = w4s.astype(np.float32).tobytes()
    jn_b = b4s.astype(np.uint16).tobytes()
    idx_b = ids.astype(np.uint16).tobytes()
    def pad(n): return (4 - n % 4) % 4
    O1 = pad(len(pos_b)); O2 = pad(O1 + len(uv_b)); O3 = pad(O2 + len(wt_b))
    O4 = pad(O3 + len(jn_b)); O5 = pad(O4 + len(idx_b)); O6 = pad(O5 + len(idx_b) + 0)
    # recompute offsets properly
    base = 0
    offs = {}
    parts = []
    for k, seg in (('pos', pos_b), ('uv', uv_b), ('wt', wt_b), ('jn', jn_b),
                   ('idx', idx_b), ('ibm', ibm_bytes)):
        padn = (4 - base % 4) % 4
        if padn:
            parts.append(b'\0' * padn)
            base += padn
        offs[k] = base
        parts.append(seg)
        base += len(seg)
    buf = b''.join(parts)
    total = base
    gltf = {
        'asset': {'version': '2.0', 'generator': 'tdkr-s33'},
        'scene': 0, 'scenes': [{'nodes': [node_of[r] for r in roots]}],
        'nodes': gnodes,
        'skins': [{'inverseBindMatrices': None, 'joints': jindices}],
        'meshes': [{'primitives': [{'attributes': {
            'POSITION': None, 'TEXCOORD_0': None, 'WEIGHTS_0': None,
            'JOINTS_0': None}, 'indices': None, 'material': 0}]}],
        'materials': [{'pbrMetallicRoughness': {'baseColorFactor': [0.75, 0.75, 0.78, 1]}}],
        'accessors': [], 'bufferViews': [], 'buffers': [{'byteLength': total}],
    }
    def add_acc(data, comps, comp_type, btype):
        bv_i = len(gltf['bufferViews'])
        gltf['bufferViews'].append({'buffer': 0, 'byteOffset': offs[btype],
                                    'byteLength': len(data)})
        ai = len(gltf['accessors'])
        gltf['accessors'].append({'bufferView': bv_i, 'componentType': comp_type,
                                  'count': comps, 'type': None})
        return ai
    def add_acc_typed(data, count, ctype, typ, btype):
        bv_i = len(gltf['bufferViews'])
        gltf['bufferViews'].append({'buffer': 0, 'byteOffset': offs[btype],
                                    'byteLength': len(data)})
        ai = len(gltf['accessors'])
        gltf['accessors'].append({'bufferView': bv_i, 'componentType': ctype,
                                  'count': count, 'type': typ})
        return ai
    a_pos = add_acc_typed(pos_b, N, 5126, 'VEC3', 'pos')
    a_uv = add_acc_typed(uv_b, N, 5126, 'VEC2', 'uv')
    a_wt = add_acc_typed(wt_b, N, 5126, 'VEC4', 'wt')
    a_jn = add_acc_typed(jn_b, N, 5123, 'VEC4', 'jn')
    a_idx = add_acc_typed(idx_b, NIDX, 5123, 'SCALAR', 'idx')
    bv_i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': offs['ibm'],
                                'byteLength': len(ibm_bytes)})
    a_ibm = len(gltf['accessors'])
    gltf['accessors'].append({'bufferView': bv_i, 'componentType': 5126,
                              'count': 31, 'type': 'MAT4'})
    gltf['skins'][0]['inverseBindMatrices'] = a_ibm
    prim = gltf['meshes'][0]['primitives'][0]
    prim['attributes']['POSITION'] = a_pos
    prim['attributes']['TEXCOORD_0'] = a_uv
    prim['attributes']['WEIGHTS_0'] = a_wt
    prim['attributes']['JOINTS_0'] = a_jn
    prim['indices'] = a_idx
    # set node local matrices as TRS
    for gi, M in enumerate(mats):
        # row-vector affine flattened row-major (three.js reads it as the
        # transposed column-vector matrix = same point map; r32 convention)
        gnodes[gi]['matrix'] = [float(x) for x in np.asarray(M, np.float64).reshape(-1)]
    js = json.dumps(gltf, separators=(',', ':')).encode()
    jpad = js + b' ' * ((4 - len(js) % 4) % 4)
    bpad = buf + b'\0' * ((4 - len(buf) % 4) % 4)
    out = (struct.pack('<3I', 0x46546C67, 2, 12 + 8 + len(jpad) + 8 + len(bpad)) +
           struct.pack('<II', len(jpad), 0x4E4F534A) + jpad +
           struct.pack('<II', len(bpad), 0x004E4942) + bpad)
    open(path, 'wb').write(out)
    return path

override = {}
for b in ALIGN:
    L = binds[b] @ np.linalg.inv(binds[PNAME_INDEX[b]]) if False else None

# bind-aligned override for the 4 bones
PNAME_INDEX = {joint_nodes[b]: P31[b] for b in P31}
override = {}
for b in ALIGN:
    pi = [k for k in range(31) if joint_nodes[k] == pname_of[joint_nodes[b]]][0]
    L = binds[b] @ np.linalg.inv(binds[pi])
    override[joint_nodes[b]] = L

OUT = '/home/z/my-project/download'
write_glb(f'{OUT}/batman_s33_full.glb', override)
write_glb(f'{OUT}/batman_s33_posed25.glb', override, posed_bone=17, posed_deg=25.0)
print(f'wrote {OUT}/batman_s33_full.glb + batman_s33_posed25.glb')

# ---- numpy expected arrays for verifier (full + posed) ----
V = np.hstack([verts, np.ones((N, 1))])
def worlds(posed_bone=None, posed_deg=0.0):
    def world(name):
        chain = [name]
        while parent_name(chain[-1]):
            chain.append(parent_name(chain[-1]))
        chain.reverse()
        M = np.eye(4)
        for nm in chain:
            if posed_bone is not None and joint_nodes[posed_bone] == nm:
                M = posed_local(posed_bone, posed_deg) @ M
            elif nm in override:
                M = override[nm] @ M
            elif nm in JN:
                M = local_row(JN[nm]) @ M
        return M
    return {b: world(joint_nodes[b]) for b in range(31)}

for tag, pb, pd in (('full', None, 0), ('posed25', 17, 25.0)):
    W = worlds(pb, pd)
    sp = np.zeros((N, 3))
    for j in range(4):
        sel_ids = np.clip(b4s[:, j], 0, 30)
        Wj = w4s[:, j]
        for b in range(31):
            sel = sel_ids == b
            if not sel.any(): continue
            M = invB[b] @ W[b]
            sp[sel] += Wj[sel][:, None] * (V[sel] @ M)[:, :3]
    e = np.linalg.norm(sp - verts, axis=1)
    print(f'{tag} numpy: exact<0.1mm {int((e < 1e-4).sum())}/1449, '
          f'mean {e.mean()*100:.3f} cm, max {e.max()*100:.3f} cm')
    np.savez(f'/home/z/my-project/scripts/jsverify/expected_s33_{tag}.npz',
             verts=verts.astype(np.float32), skinned=sp.astype(np.float32))

# bone-length rigidity check under the 25-deg pose (numpy side, correct parents)
jset = {nm: k for k, nm in enumerate(joint_nodes)}
pid = [jset.get(pname_of.get(joint_nodes[b]), b) or
       (jset[pname_of[joint_nodes[b]]] if joint_nodes[b] in pname_of
        and pname_of[joint_nodes[b]] in jset else b) for b in range(31)]
pid = [jset[pname_of[joint_nodes[b]]] if joint_nodes[b] in pname_of
       and pname_of[joint_nodes[b]] in jset else b for b in range(31)]
W0 = worlds(); W1 = worlds(17, 25.0)
dl = max(abs(np.linalg.norm(W0[b][3, :3] - W0[pid[b]][3, :3]) -
             np.linalg.norm(W1[b][3, :3] - W1[pid[b]][3, :3]))
         for b in range(31) if b != pid[b])
print(f'rigidity under pose change: max bone-length delta {dl*1000:.3f} mm')

json.dump(dict(uv=dict(range_ok=in_range, tiles=tiles_used,
                       shared_groups=len(shared), seams=seam_groups,
                       seam_null=seam_null),
               glbs=[f'{OUT}/batman_s33_full.glb', f'{OUT}/batman_s33_posed25.glb']),
          open('/home/z/my-project/scripts/s33_t2_gltf.json', 'w'), indent=1)
