#!/usr/bin/env python3
"""S35 T1e: export batman_s36_anims.glb — r34-verified rig (Neck clavicle,
no overrides) + THREE glTF animations assembled via the engine-derived
chunk mapping: idle [0,5000]=segs0+1+2, run [30000,30666]=segs11+12,
jump _010_run_jump_start [34000,34900]=segs13+14. Also dumps numpy FK
expected skinned positions for the three.js verify."""
import struct, math, json
import numpy as np

exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split("print('\\n=== battery")[0])

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
JN = {n['name']: n for n in nodes}
by_alias = {n['alias']: n['name'] for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p] for p in pal]
PNAME = {0: 'Bip01_R_Calf', 1: 'Bip01_R_Thigh', 2: 'Bip01_Pelvis',
         3: 'Bip01_L_Calf', 4: 'Bip01_L_Thigh', 5: 'Bip01_Pelvis',
         6: 'Bip01_R_Hand', 7: 'Bip01_R_Hand', 8: 'Bip01_R_Forearm',
         9: 'Bip01_R_UpperArm', 10: 'Bip01_R_Clavicle', 11: 'Bip01_Neck',
         12: 'Bip01_L_Hand', 13: 'Bip01_L_Hand', 14: 'Bip01_L_Forearm',
         15: 'Bip01_L_UpperArm', 16: 'Bip01_L_Clavicle', 17: 'Bip01_Neck',
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
    'Bip01_L_Clavicle': 'Bip01_Neck',      # r34 correction
    'Bip01_L_UpperArm': 'Bip01_L_Clavicle',
    'Bip01_L_Forearm': 'Bip01_L_UpperArm', 'Bip01_L_Hand': 'Bip01_L_Forearm',
    'Bip01_R_Clavicle': 'Bip01_Neck',      # r34 correction
    'Bip01_R_UpperArm': 'Bip01_R_Clavicle',
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
BASE, NV, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80) for i in range(NV)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20) for i in range(NV)], np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4) for i in range(NV)])
IDX_OFF, NIDX = 0x210bc, 5655
ids = np.array([struct.unpack_from('<H', d, IDX_OFF + 2 * i) for i in range(NIDX)], np.uint16)
uv_r = np.array([struct.unpack_from('<H', d, BASE + i * 80 + 72)[0] for i in range(NV)], np.float64)
uv_v = np.array([struct.unpack_from('<H', d, BASE + i * 80 + 76)[0] for i in range(NV)], np.float64)
uvs = np.stack([uv_r / 4096.0, uv_v / 4096.0], 1).astype(np.float32)

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
for nm in order:
    p = parent_name(nm)
    if p: gnodes[node_of[p]]['children'].append(node_of[nm])

node_trs = {}
for nm in order:
    if nm in JN:
        n = JN[nm]
        node_trs[nm] = (np.array(n['t'], float), np.array(n['q'], float),
                        np.array(n['s'], float))
    else:
        node_trs[nm] = (np.zeros(3), np.array([0, 0, 0, 1.0]), np.ones(3))

# r34 sanity (row-form, r23/r24 convention): node worlds == bind worlds
def colR(q):
    x, y, z, w = np.asarray(q, float) / np.linalg.norm(q)
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T                      # row-form rotation

def Lrow(nm, q_override=None):
    t_, q_, s_ = node_trs[nm]
    if q_override is not None: q_ = q_override
    M = np.eye(4)
    M[:3, :3] = colR(q_) @ np.diag(s_)
    M[3, :3] = t_
    return M

def node_world_row(nm):
    W = {}
    def rec(x):
        if x in W: return W[x]
        p = parent_name(x)
        M = Lrow(x) @ (rec(p) if p else np.eye(4))
        W[x] = M
        return M
    return rec(nm)

worst_dp = 0.0
for b in range(31):
    W = node_world_row(joint_nodes[b])
    dp = float(np.abs(W[3, :3] - binds[b][3, :3]).max())
    worst_dp = max(worst_dp, dp)
print(f'node-worlds vs bind worlds worst dp = {worst_dp*100:.4f} cm (r34: 0.0202)')

# ---------- animations from chunk-assembled clips ----------
def clip_channels(cl):
    ts, te = cl['ts'], cl['te']
    cov = [s for s in segs if s['start'] < te and s['end'] > ts]
    ch = {}
    for c in range(78):
        acc_t = None; acc_v = None
        for s in cov:
            st = seg_streams[s['k']]
            tw = st[2 * c].astype(np.int64)
            vw = st[2 * c + 1].view('<f4')
            nt = len(tw)
            if nt == 0: continue
            m = (tw >= ts) & (tw <= te)
            if not m.any(): continue
            seg_t = tw[m]; nv = 3 if CH[c][1] == 1 else 4
            seg_v = vw.reshape(-1, nv)[:nt][m]
            if acc_t is None:
                acc_t, acc_v = seg_t, seg_v
            else:
                mg = np.concatenate([acc_t, seg_t])
                o = np.argsort(mg, kind='stable')
                acc_t = mg[o]; acc_v = np.concatenate([acc_v, seg_v])[o]
        if acc_t is None: continue
        # dedupe ticks (chunk bleed overlap)
        keep = np.concatenate([[True], np.diff(acc_t) != 0])
        ch[c] = (acc_t[keep] - ts, acc_v[keep])
    return ch, [s['k'] for s in cov]

CLIPS = [(0, '_001_idle_stand'), (5, '_007_walk'), (6, '_008_run'), (8, '_010_run_jump_start'), (460, '_461_batman_jab_countre_front_attack')]
anims = []
for ci, label in CLIPS:
    ch, covk = clip_channels(clips[ci])
    channels = []
    for c in sorted(ch):
        nm, ty = CH[c]
        bare = nm[:-5] if nm.endswith('-node') else nm
        tt, vv = ch[c]
        if ty == 5 and len(tt) >= 1 and bare in node_of:
            channels.append(dict(node=bare, path='rotation', times=(tt / 1000.0), out=vv))
        elif ty == 1 and bare == 'Bip01' and len(tt) >= 1:
            channels.append(dict(node=bare, path='translation', times=(tt / 1000.0), out=vv))
    dur = clips[ci]['te'] - clips[ci]['ts']
    print(f'{label}: clip {ci} [{clips[ci]["ts"]},{clips[ci]["te"]}] segs={covk} '
          f'tracks={len(channels)} dur={dur}ms')
    anims.append((label, channels))

# ---------- numpy FK dumps for verify ----------
def qmul(a, b):
    x1, y1, z1, w1 = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    x2, y2, z2, w2 = b[..., 0], b[..., 1], b[..., 2], b[..., 3]
    return np.stack([w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2,
                     w1*w2 - x1*x2 - y1*y2 - z1*z2], -1)

def sample_track(times, outs, t):
    if t <= times[0]: return outs[0]
    if t >= times[-1]: return outs[-1]
    hi = int(np.searchsorted(times, t))
    lo = hi - 1
    f = (t - times[lo]) / max(1e-9, times[hi] - times[lo])
    a, b = outs[lo].astype(float), outs[hi].astype(float)
    if a.size == 4:
        a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
        dd = float(np.dot(a, b))
        if dd < 0: b = -b
        if dd > 0.9995: return a + f * (b - a)
        dq = a * (1 - f) + b * f
        return dq / np.linalg.norm(dq)
    return a * (1 - f) + b * f

def fk_skinned(channels, t):
    cmap = {}
    for cd in channels:
        cmap.setdefault(cd['node'], {})[cd['path']] = cd
    W = {}
    def world(nm):
        if nm in W: return W[nm]
        p = parent_name(nm)
        t_, q_, s_ = node_trs[nm]
        t_s = t / 1000.0
        cd = cmap.get(nm, {}).get('rotation')
        q = sample_track(cd['times'], cd['out'], t_s) if cd else q_
        tr = t_
        cdt = cmap.get(nm, {}).get('translation')
        if cdt: tr = sample_track(cdt['times'], cdt['out'], t_s)
        M = np.eye(4)
        M[:3, :3] = colR(q) @ np.diag(s_)
        M[3, :3] = tr
        M = M @ (world(p) if p else np.eye(4))
        W[nm] = M
        return M
    for nm in order: world(nm)
    V = np.hstack([verts, np.ones((NV, 1))])
    M_all = np.stack([invB[b] @ world(joint_nodes[b]) for b in range(31)])
    out = np.zeros((NV, 3))
    for k in range(4):
        bk = np.clip(b4s[:, k], 0, 30)
        wk = w4s[:, k:k+1]
        Mb = M_all[bk]                      # (NV,4,4) row-form
        out += wk * np.einsum('ni,nij->nj', V, Mb)[:, :3]
    return out

import os
os.makedirs('/home/z/my-project/scripts/jsverify/s35bin', exist_ok=True)
for label, channels in anims:
    ci = dict((lab, c) for c, lab in CLIPS)[label]
    dur = clips[ci]['te'] - clips[ci]['ts']
    for f in (0.1, 0.35, 0.6, 0.85):
        t = dur * f
        pts = fk_skinned(channels, t).astype(np.float32)
        fn = f'/home/z/my-project/scripts/jsverify/s35bin/{label.split("_")[1]}_t{int(t)}.bin'
        pts.tofile(fn)
    print(f'{label}: FK dumps written')

# ---------- GLB assembly ----------
ibm_bytes = b''.join(np.asarray(invB[b], np.float32).tobytes() for b in range(31))
jindices = [node_of[joint_nodes[b]] for b in range(31)]
pos_b = verts.astype(np.float32).tobytes()
uv_b = uvs.tobytes()
wt_b = w4s.astype(np.float32).tobytes()
jn_b = b4s.astype(np.uint16).tobytes()
idx_b = ids.astype(np.uint16).tobytes()

anim_bins = []
def anim_accessors(channels, blob_off):
    sams = []
    for cd in channels:
        tb = np.asarray(cd['times'], np.float32).tobytes()
        ob = np.asarray(cd['out'], np.float32).tobytes()
        t_off = blob_off
        anim_bins.append(tb); blob_off += len(tb)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        o_off = blob_off
        anim_bins.append(ob); blob_off += len(ob)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        sams.append((t_off, len(tb), len(cd['times']), o_off, len(ob), len(cd['out']),
                     cd['out'].shape[1]))
    return sams, blob_off

blob_off = 0
sams_all = []
for label, channels in anims:
    sams, blob_off = anim_accessors(channels, blob_off)
    sams_all.append(sams)
anim_buf = b''.join(anim_bins)

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
    'asset': {'version': '2.0', 'generator': 'tdkr-s35'},
    'scene': 0, 'scenes': [{'nodes': [0, len(need)]}],
    'nodes': [], 'skins': [{'inverseBindMatrices': None, 'joints': jindices}],
    'meshes': [{'primitives': [{'attributes': {
        'POSITION': None, 'TEXCOORD_0': None, 'WEIGHTS_0': None,
        'JOINTS_0': None}, 'indices': None, 'material': 0}]}],
    'materials': [{'pbrMetallicRoughness': {'baseColorFactor': [0.75, 0.75, 0.78, 1]}}],
    'animations': [{'name': lb, 'channels': [], 'samplers': []} for lb, _ in anims],
    'accessors': [], 'bufferViews': [],
    'buffers': [{'byteLength': base + len(anim_buf)}],
}
for nm, gi in order.items():
    t, q, s = node_trs[nm]
    gnodes[gi]['translation'] = [float(x) for x in t]
    gnodes[gi]['rotation'] = [float(x) for x in q]
    gnodes[gi]['scale'] = [float(x) for x in s]
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

a_pos = add_acc(offs['pos'], len(pos_b), NV, 5126, 'VEC3')
a_uv = add_acc(offs['uv'], len(uv_b), NV, 5126, 'VEC2')
a_wt = add_acc(offs['wt'], len(wt_b), NV, 5126, 'VEC4')
a_jn = add_acc(offs['jn'], len(jn_b), NV, 5123, 'VEC4')
a_idx = add_acc(offs['idx'], len(idx_b), NIDX, 5123, 'SCALAR')
a_ibm = add_acc(offs['ibm'], len(ibm_bytes), 31, 5126, 'MAT4')
gltf['skins'][0]['inverseBindMatrices'] = a_ibm
prim = gltf['meshes'][0]['primitives'][0]
prim['attributes']['POSITION'] = a_pos
prim['attributes']['TEXCOORD_0'] = a_uv
prim['attributes']['WEIGHTS_0'] = a_wt
prim['attributes']['JOINTS_0'] = a_jn
prim['indices'] = a_idx

ANIM_BUF_BASE = base
def add_anim_acc(off_in_anim, ln, count, typ):
    bv_i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': ANIM_BUF_BASE + off_in_anim,
                                'byteLength': ln})
    ai = len(gltf['accessors'])
    gltf['accessors'].append({'bufferView': bv_i, 'componentType': 5126,
                              'count': count, 'type': typ})
    return ai

for (label, channels), sams in zip(anims, sams_all):
    g = next(a for a in gltf['animations'] if a['name'] == label)
    for cd, (t_off, t_ln, t_n, o_off, o_ln, o_n, ncomp) in zip(channels, sams):
        ti = add_anim_acc(t_off, t_ln, t_n, 'SCALAR')
        oi = add_anim_acc(o_off, o_ln, o_n, 'VEC4' if ncomp == 4 else 'VEC3')
        g['samplers'].append({'input': ti, 'output': oi, 'interpolation': 'LINEAR'})
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
open(f'{OUT}/batman_s36_anims.glb', 'wb').write(out)
print(f'wrote {OUT}/batman_s36_anims.glb ({len(out)} B)')

# rest + sample meta for three.js verify
V = np.hstack([verts, np.ones((NV, 1))])
W_rest = {}
def world_rest(nm):
    if nm in W_rest: return W_rest[nm]
    M = Lrow(nm) @ (world_rest(parent_name(nm)) if parent_name(nm) else np.eye(4))
    W_rest[nm] = M
    return M
sp_rest = np.zeros((NV, 3))
for j in range(4):
    sel_ids = np.clip(b4s[:, j], 0, 30)
    for b in range(31):
        sel = sel_ids == b
        if not sel.any(): continue
        M = invB[b] @ world_rest(joint_nodes[b])
        sp_rest[sel] += w4s[sel][:, j][:, None] * (V @ M)[sel][:, :3]
e = np.linalg.norm(sp_rest - verts, axis=1)
print(f'REST anchor: <0.1mm {int((e < 1e-4).sum())}/{NV}, mean {e.mean()*100:.4f} cm, max {e.max()*100:.4f} cm')

meta = {'rest': sp_rest.astype(np.float32).reshape(-1).tolist(), 'samples': []}
for label, channels in anims:
    ci = dict((lab, c) for c, lab in CLIPS)[label]
    dur = (clips[ci]['te'] - clips[ci]['ts']) / 1000.0
    for f in (0.1, 0.35, 0.6, 0.85):
        t = dur * f
        pts = fk_skinned(channels, t * 1000.0).astype(np.float32)
        meta['samples'].append([label, {'t': t, 'data': pts.reshape(-1).tolist()}])
json.dump(meta, open('/home/z/my-project/scripts/jsverify/s35_meta.json', 'w'))
print('wrote s35_meta.json')
