#!/usr/bin/env python3
"""S34 T1: export batman_s34_anims.glb — r23-verified skinned Batman (body)
+ TWO glTF animations (_001_idle_stand from seg0 pool, _008_run from seg6
pool). TRS nodes (glTF-native; anims replace quat/pos cleanly). Also compute
the root/finger rest-vs-anim explanation numbers."""
import struct, math, json
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
A = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
ad = open(A, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

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
JN = {n['name']: n for n in nodes}
by_alias = {n['alias']: n['name'] for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p] for p in pal]
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11,
       11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
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

# node tree (same as r23)
need = set()
for b in range(31):
    nm = joint_nodes[b]
    while nm:
        need.add(nm); nm = parent_name(nm)
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

# bind-aligned override locals for the 4 arm roots (r23)
ALIGN = [10, 11, 16, 17]
override = {}
for b in ALIGN:
    pi = [k for k in range(31) if joint_nodes[k] == pname_of[joint_nodes[b]]][0]
    L = binds[b] @ np.linalg.inv(binds[pi])
    override[joint_nodes[b]] = L

def mat_to_trs(M_row):
    """row-vector affine -> glTF TRS (translation, quat xyzw, scale)."""
    R = M_row[:3, :3]
    t = M_row[3, :3].copy()
    # rigid expected: orthonormalize via SVD, then COLUMN rotation = R_row^T
    U, sv, Vt = np.linalg.svd(R)
    m = (U @ Vt).T          # column-vector rotation = glTF rotation matrix
    # quaternion from column rotation m
    tr = m[0, 0] + m[1, 1] + m[2, 2]
    if tr > 0:
        sq = math.sqrt(tr + 1.0) * 2
        w = 0.25 * sq
        x = (m[2, 1] - m[1, 2]) / sq
        y = (m[0, 2] - m[2, 0]) / sq
        z = (m[1, 0] - m[0, 1]) / sq
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        sq = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        w = (m[2, 1] - m[1, 2]) / sq; x = 0.25 * sq
        y = (m[0, 1] + m[1, 0]) / sq; z = (m[0, 2] + m[2, 0]) / sq
    elif m[1, 1] > m[2, 2]:
        sq = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        w = (m[0, 2] - m[2, 0]) / sq; x = (m[0, 1] + m[1, 0]) / sq
        y = 0.25 * sq; z = (m[1, 2] + m[2, 1]) / sq
    else:
        sq = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        w = (m[1, 0] - m[0, 1]) / sq; x = (m[0, 2] + m[2, 0]) / sq
        y = (m[1, 2] + m[2, 1]) / sq; z = 0.25 * sq
    q = np.array([x, y, z, w], float)
    q /= np.linalg.norm(q)
    sc = np.array([np.linalg.norm(R[:, 0]), np.linalg.norm(R[:, 1]),
                   np.linalg.norm(R[:, 2])])
    # column-form scale = row-form scale (diag) — R_row = R_col @ diag(s):
    # |R_col[:,i]| = s_i
    return t, q, sc

# node TRS
node_trs = {}
for nm in order:
    if nm in override:
        node_trs[nm] = mat_to_trs(override[nm])
    elif nm in JN:
        n = JN[nm]
        node_trs[nm] = (np.array(n['t'], float), np.array(n['q'], float),
                        np.array(n['s'], float))
    else:
        node_trs[nm] = (np.zeros(3), np.array([0, 0, 0, 1.0]), np.ones(3))

# ================= animation pools =================
def load_seg_pool(table, nent):
    pairs = [(u32a(table + 8*k), u32a(table + 8*k + 4)) for k in range(nent)]
    pos = None
    for extra in (0, 4, 8, 12, 16):
        base = table + nent*8 + extra
        p = base; ok = 0
        for kk, (off, ln) in enumerate(pairs):
            if ln == 0: continue
            if kk % 2 == 0:
                n = ln // 4
                w = [u32a(p + 4*j) for j in range(n)]
                if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2e6: break
            else:
                if ln % 16 == 0 and ln >= 0x20:
                    if not all(0.95 < math.sqrt(sum(f32a(p+16*i+4*c)**2 for c in range(4))) < 1.05
                               for i in range(ln // 16)): break
                elif ln % 12 == 0:
                    if any(abs(f32a(p+12*i+4*c)) > 1e5 for i in range(ln // 12)
                           for c in range(3)): break
                else: break
            ok += 1; p += ln
        if ok == len([1 for o_, l_ in pairs if l_]):
            pos = base; break
    assert pos is not None, f'no base for table {table:#x}'
    ch = {}
    p = pos
    for kk, (off, ln) in enumerate(pairs):
        c = kk // 2
        if ln == 0: continue
        if kk % 2 == 0:
            n = ln // 4
            ch.setdefault(c, {})['ticks'] = [u32a(p + 4*j) for j in range(n)]
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                ch.setdefault(c, {})['quat'] = [[f32a(p+16*i+4*cc) for cc in range(4)]
                                                for i in range(m)]
            elif ln % 12 == 0:
                ch.setdefault(c, {})['vec3'] = [[f32a(p+12*i+4*cc) for cc in range(3)]
                                                for i in range(ln // 12)]
        p += ln
    return ch, pos

# idle: 157 entries, data 0x536e4 (validated s34)
idle_pairs = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
idle_ch = {}
pos = 0x536e4
for kk, (off, ln) in enumerate(idle_pairs['pairs']):
    c = kk // 2
    if ln == 0: continue
    if kk % 2 == 0:
        n = ln // 4
        idle_ch.setdefault(c, {})['ticks'] = [u32a(pos + 4*j) for j in range(n)]
    else:
        if ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            idle_ch.setdefault(c, {})['quat'] = [[f32a(pos+16*i+4*cc) for cc in range(4)]
                                                 for i in range(m)]
        elif ln % 12 == 0:
            idle_ch.setdefault(c, {})['vec3'] = [[f32a(pos+12*i+4*cc) for cc in range(3)]
                                                 for i in range(ln // 12)]
    pos += ln
run_ch, run_base = load_seg_pool(0x0b2818, 156)

names = idle_pairs['names']

def build_anim(ch, label, t0=None):
    """convert channel pool -> glTF animation (channels+samplers as index lists).
    Times rebased to 0 using the min tick over EXPORTED channels only."""
    channels, samplers = [], []
    n_used = 0
    tmin = None
    for c in sorted(ch):
        nm = names[c] if c < len(names) else f'?{c}'
        bare = nm.split('-node-')[0]
        kind = nm.split('-node-')[1] if '-node-' in nm else '?'
        if bare not in node_of: continue
        if kind == 'rotation' and 'quat' in ch[c]:
            path = 'rotation'; out = ch[c]['quat']
        elif kind == 'translation' and 'vec3' in ch[c]:
            path = 'translation'; out = ch[c]['vec3']
        else:
            continue
        ticks = ch[c]['ticks']
        if tmin is None or ticks[0] < tmin: tmin = ticks[0]
        out = [[float(x) for x in k] for k in out]
        channels.append(dict(node=bare, path=path, ticks=ticks, out=out))
        n_used += 1
    # base = min start of REAL (multi-key) tracks; 2-key static streams
    # ([0, 27950]-style) must not drag the base to 0
    real_starts = [cd['ticks'][0] for cd in channels if len(cd['ticks']) > 2]
    base = (min(real_starts) if real_starts else tmin) if t0 is None else t0
    for cd in channels:
        cd['times'] = [(t - base) / 1000.0 for t in cd['ticks']]
        del cd['ticks']
    return dict(channels=channels, samplers=samplers, n=n_used, tmin=tmin)

anim_idle = build_anim(idle_ch, 'idle')
anim_run = build_anim(run_ch, 'run')
idle_tmax = max(max(idle_ch[c]['ticks']) for c in idle_ch if 'ticks' in idle_ch[c])
run_tmax = max(max(run_ch[c]['ticks']) for c in run_ch if 'ticks' in run_ch[c])
print(f'idle anim: {anim_idle["n"]} channels, t {anim_idle["tmin"]}..{idle_tmax}')
print(f'run anim: {anim_run["n"]} channels, t {anim_run["tmin"]}..{run_tmax}')

# root/finger explanation: axis-angle between rest and idle t=0
def qangle_axis(a, b):
    a = np.array(a, float); b = np.array(b, float)
    a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    if float(np.dot(a, b)) < 0: b = -b
    q = b / (np.linalg.norm(a) * np.linalg.norm(b))
    # relative rotation r = a^-1 * b
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    rw = aw*bw + ax*bx + ay*by + az*bz
    rx = aw*bx - ax*bw - ay*bz - az*by
    ry = aw*by + ax*bz - ay*bw + az*bx
    rz = aw*bz - ax*by + ay*bx - az*bw
    ang = 2 * math.degrees(math.acos(min(1.0, abs(rw))))
    s = math.sqrt(max(0.0, 1 - rw*rw))
    axis = (rx/s, ry/s, rz/s) if s > 1e-6 else (0, 0, 1)
    return ang, axis

c_bip = next(c for c in idle_ch
             if (names[c] if c < len(names) else '') == 'Bip01-node-rotation')
ang, ax = qangle_axis(JN['Bip01']['q'], idle_ch[c_bip]['quat'][0])
print(f'\nROOT: rest-vs-idle-t0 angle {ang:.2f} deg, axis ({ax[0]:.3f},{ax[1]:.3f},{ax[2]:.3f})')
fing = []
for c in idle_ch:
    nm = names[c] if c < len(names) else ''
    if '-node-rotation' not in nm or 'Finger' not in nm: continue
    bare = nm.split('-node-')[0]
    if bare in JN:
        a2, _ = qangle_axis(JN[bare]['q'], idle_ch[c]['quat'][0])
        fing.append((round(a2, 1), bare))
fing.sort(reverse=True)
print(f'FINGERS rest-vs-t0: {fing[:6]}')
json.dump(dict(root_angle=ang, root_axis=ax, fingers=fing[:8]),
          open('/home/z/my-project/scripts/s34_t1_rootexpl.json', 'w'))

# ================= GLB assembly =================
ibm_bytes = b''.join(np.asarray(invB[b], np.float32).tobytes() for b in range(31))
jindices = [node_of[joint_nodes[b]] for b in range(31)]
pos_b = verts.astype(np.float32).tobytes()
uv_b = uvs.tobytes()
wt_b = w4s.astype(np.float32).tobytes()
jn_b = b4s.astype(np.uint16).tobytes()
idx_b = ids.astype(np.uint16).tobytes()

anim_bins = []
def anim_accessors(anim, blob_off):
    """append time/output buffers, return per-channel (t_off,t_ln,t_n,o_off,o_ln,o_n,ncomp)"""
    sams = []
    for cd in anim['channels']:
        times, outs = cd['times'], cd['out']
        tb = np.array(times, np.float32).tobytes()
        ncomp = len(outs[0])
        ob = np.array(outs, np.float32).tobytes()
        t_off = blob_off
        anim_bins.append(tb)
        blob_off += len(tb)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        o_off = blob_off
        anim_bins.append(ob)
        blob_off += len(ob)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        sams.append((t_off, len(tb), len(times), o_off, len(ob), len(outs), ncomp))
    return sams, blob_off

sams_idle, blob_off = anim_accessors(anim_idle, 0)
sams_run, blob_off = anim_accessors(anim_run, blob_off)
anim_buf = b''.join(anim_bins)

# static buffer
parts = []
base = 0
offs = {}
for k, seg in (('pos', pos_b), ('uv', uv_b), ('wt', wt_b), ('jn', jn_b),
               ('idx', idx_b), ('ibm', ibm_bytes)):
    padn = (4 - base % 4) % 4
    if padn: parts.append(b'\0' * padn); base += padn
    offs[k] = base; parts.append(seg); base += len(seg)
buf = b''.join(parts)

gltf = {
    'asset': {'version': '2.0', 'generator': 'tdkr-s34'},
    'scene': 0, 'scenes': [{'nodes': [0, len(need)]}],
    'nodes': [], 'skins': [{'inverseBindMatrices': None, 'joints': jindices}],
    'meshes': [{'primitives': [{'attributes': {
        'POSITION': None, 'TEXCOORD_0': None, 'WEIGHTS_0': None,
        'JOINTS_0': None}, 'indices': None, 'material': 0}]}],
    'materials': [{'pbrMetallicRoughness': {'baseColorFactor': [0.75, 0.75, 0.78, 1]}}],
    'animations': [
        {'name': '_001_idle_stand', 'channels': [], 'samplers': []},
        {'name': '_008_run', 'channels': [], 'samplers': []},
    ],
    'accessors': [], 'bufferViews': [],
    'buffers': [{'byteLength': base + len(anim_buf)}],
}
for nm, gi in order.items():
    t, q, s = node_trs[nm]
    gnodes[gi]['translation'] = [float(x) for x in t]
    gnodes[gi]['rotation'] = [float(x) for x in q]
    gnodes[gi]['scale'] = [float(x) for x in s]
# dedicated identity mesh node carrying mesh+skin (glTF skinned-mesh pattern)
gnodes.append(dict(name='BATMAN_mesh', mesh=0, skin=0))
gltf['nodes'] = gnodes

def add_bv(off, ln):
    i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': off, 'byteLength': ln})
    return i
def add_acc(off, ln, count, ctype, typ):
    bv = add_bv(off, ln)
    i = len(gltf['accessors'])
    gltf['accessors'].append({'bufferView': bv, 'componentType': ctype,
                              'count': count, 'type': typ})
    return i

a_pos = add_acc(offs['pos'], len(pos_b), N, 5126, 'VEC3')
a_uv = add_acc(offs['uv'], len(uv_b), N, 5126, 'VEC2')
a_wt = add_acc(offs['wt'], len(wt_b), N, 5126, 'VEC4')
a_jn = add_acc(offs['jn'], len(jn_b), N, 5123, 'VEC4')
a_idx = add_acc(offs['idx'], len(idx_b), NIDX, 5123, 'SCALAR')
a_ibm = add_acc(offs['ibm'], len(ibm_bytes), 31, 5126, 'MAT4')
gltf['skins'][0]['inverseBindMatrices'] = a_ibm
prim = gltf['meshes'][0]['primitives'][0]
prim['attributes']['POSITION'] = a_pos
prim['attributes']['TEXCOORD_0'] = a_uv
prim['attributes']['WEIGHTS_0'] = a_wt
prim['attributes']['JOINTS_0'] = a_jn
prim['indices'] = a_idx

# animation accessors reference the anim_buf appended after static buf
ANIM_BUF_BASE = base
def add_anim_acc(off_in_anim, ln, count, typ):
    bv_i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': ANIM_BUF_BASE + off_in_anim,
                                'byteLength': ln})
    ai = len(gltf['accessors'])
    gltf['accessors'].append({'bufferView': bv_i, 'componentType': 5126,
                              'count': count, 'type': typ})
    return ai

for ai_name, (anim, sams) in (('_001_idle_stand', (anim_idle, sams_idle)),
                              ('_008_run', (anim_run, sams_run))):
    g = next(a for a in gltf['animations'] if a['name'] == ai_name)
    for cd, (t_off, t_ln, t_n, o_off, o_ln, o_n, ncomp) in zip(anim['channels'], sams):
        ti = add_anim_acc(t_off, t_ln, t_n, 'SCALAR')
        oi = add_anim_acc(o_off, o_ln, o_n, 'VEC4' if ncomp == 4 else 'VEC3')
        g['samplers'].append({'input': ti, 'output': oi,
                              'interpolation': 'LINEAR'})
        g['channels'].append(dict(sampler=len(g['samplers']) - 1,
                                  target=dict(node=node_of[cd['node']],
                                              path=cd['path'])))

js = json.dumps(gltf, separators=(',', ':')).encode()
jpad = js + b' ' * ((4 - len(js) % 4) % 4)
bin_all = buf + anim_buf
bpad = bin_all + b'\0' * ((4 - len(bin_all) % 4) % 4)
out = (struct.pack('<3I', 0x46546C67, 2, 12 + 8 + len(jpad) + 8 + len(bpad)) +
       struct.pack('<II', len(jpad), 0x4E4F534A) + jpad +
       struct.pack('<II', len(bpad), 0x004E4942) + bpad)
OUT = '/home/z/my-project/download'
open(f'{OUT}/batman_s34_anims.glb', 'wb').write(out)
print(f'wrote {OUT}/batman_s34_anims.glb ({len(out)} B)')

# numpy expected skinned positions at sample times for both clips
V = np.hstack([verts, np.ones((N, 1))])
def worlds_at(t_ms, ch):
    """numpy FK with animated locals (absolute), rest TRS elsewhere"""
    def local(nm):
        n = JN.get(nm)
        c = next((c for c in ch
                  if (names[c] if c < len(names) else '') == f'{nm}-node-rotation'), None)
        q = np.array(ch[c]['quat'][0], float) if False else None
        return None
    # precompute channel map
    cmap = {}
    for c in ch:
        nm = names[c] if c < len(names) else ''
        if '-node-' in nm:
            cmap.setdefault(nm.split('-node-')[0], {})[nm.split('-node-')[1]] = c
    def sample(c, t, kind):
        ts = ch[c]['ticks']; ks = ch[c][kind]
        if t <= ts[0]: return np.array(ks[0], float)
        if t >= ts[-1]: return np.array(ks[-1], float)
        hi = next(i for i in range(1, len(ts)) if ts[i] >= t)
        lo = hi - 1
        f = (t - ts[lo]) / max(1, ts[hi] - ts[lo])
        a, b = np.array(ks[lo], float), np.array(ks[hi], float)
        if kind == 'quat':
            a /= np.linalg.norm(a); b /= np.linalg.norm(b)
            dd = float(np.dot(a, b))
            if dd < 0: b = -b
            if dd > 0.9995: return a + f * (b - a)
            th = math.acos(min(1.0, abs(dd))); s_ = math.sin(th)
            return math.sin((1-f)*th)/s_*a + math.sin(f*th)/s_*b
        return a*(1-f) + b*f
    def qmat_col(q):
        x, y, z, w = q / np.linalg.norm(q)
        Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                       [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                       [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
        return Rc.T                      # row-form rotation (r23 convention)
    Ws = {}
    def world(nm):
        if nm in Ws: return Ws[nm]
        M = np.eye(4)
        trs = node_trs[nm]
        t_, q_, s_ = trs
        if nm in cmap:
            cc = cmap[nm]
            if 'rotation' in cc:
                q_ = sample(cc['rotation'], t_ms + (0), 'quat')
            if nm == 'Bip01' and 'translation' in cc:
                t_ = sample(cc['translation'], t_ms, 'vec3')
        R = qmat_col(q_)
        M[:3, :3] = R @ np.diag(s_)
        M[3, :3] = t_
        p = parent_name(nm)
        if p: M = M @ world(p)
        Ws[nm] = M
        return M
    return {b: world(joint_nodes[b]) for b in range(31)}

def skinned_at(t_ms, ch):
    W = worlds_at(t_ms, ch)
    sp = np.zeros((N, 3))
    for j in range(4):
        sel_ids = np.clip(b4s[:, j], 0, 30)
        Wj = w4s[:, j]
        for b in range(31):
            sel = sel_ids == b
            if not sel.any(): continue
            M = invB[b] @ W[b]
            sp[sel] += Wj[sel][:, None] * (V[sel] @ M)[:, :3]
    return sp

json.dump(dict(run_base=run_base), open('/home/z/my-project/scripts/s34_t1_exp.json', 'w'))

# REST anchor: no-animation skinning must reproduce the bind verts exactly
# (r23 pipeline check; NOT an animation claim). Row-form FK (r23 convention).
W_rest = {}
def world_rest(nm):
    if nm in W_rest: return W_rest[nm]
    t_, q_, s_ = node_trs[nm]
    M = np.eye(4)
    x, y, z, w = q_ / np.linalg.norm(q_)
    Rrow = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                     [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    Rrow = Rrow.T                      # qmat_row(q) = standard_col(q)^T
    M[:3, :3] = Rrow @ np.diag(s_)
    M[3, :3] = t_
    p = parent_name(nm)
    if p: M = M @ world_rest(p)
    W_rest[nm] = M
    return M
WR = {b: world_rest(joint_nodes[b]) for b in range(31)}
sp_rest = np.zeros((N, 3))
for j in range(4):
    sel_ids = np.clip(b4s[:, j], 0, 30)
    for b in range(31):
        sel = sel_ids == b
        if not sel.any(): continue
        M = invB[b] @ WR[b]
        sp_rest[sel] += w4s[sel][:, j][:, None] * (V[sel] @ M)[:, :3]
e = np.linalg.norm(sp_rest - verts, axis=1)
print(f'REST anchor (TRS nodes): exact<0.1mm {int((e < 1e-4).sum())}/1449, '
      f'mean {e.mean()*100:.4f} cm, max {e.max()*100:.4f} cm')

samples = dict(idle={str(t): skinned_at(t, idle_ch).astype(np.float32) for t in
                     (0, 400, 900, 1500, 1849)},
               run={str(t): skinned_at(t, run_ch).astype(np.float32) for t in
                    (13899, 14200, 14700, 15200, 15600)})
np.savez('/home/z/my-project/scripts/jsverify/expected_s34_anims.npz',
         rest=sp_rest.astype(np.float32),
         idle_t0=samples['idle']['0'], idle_t400=samples['idle']['400'],
         idle_t900=samples['idle']['900'], idle_t1500=samples['idle']['1500'],
         idle_t1849=samples['idle']['1849'],
         run_t13899=samples['run']['13899'], run_t14200=samples['run']['14200'],
         run_t14700=samples['run']['14700'], run_t15200=samples['run']['15200'],
         run_t15600=samples['run']['15600'])
print('wrote expected_s34_anims.npz (mixer times: idle 0..1.849 s, run 0..1.701 s)')
