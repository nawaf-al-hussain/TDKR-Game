#!/usr/bin/env python3
"""S32 T1b: node-local convention search + bind-pose reproduction + CAPE.

1. Node worlds under 8 conventions vs bind origins (gold reference, tree-free).
2. Bind-pose reproduction: skinned = sum w (v invBind bind) over 1449 verts,
   mean/max error, shuffled-weights null.
3. Rest-pose test with best node convention: skinned = sum w (v invBind world).
4. CAPE: locate cape skin records + vertices, repeat H2 test with cape binds.
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

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]

P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10,
       10: 11, 11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20,
       18: 19, 19: 20, 20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25,
       27: 10, 28: 29, 29: 8, 30: 29}

# ---- stored invBinds ----
BODY = 0x30e30
invB = []
for k in range(31):
    m = np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                 np.float64).reshape(4, 4)
    invB.append(m)
invB = np.array(invB)                    # row-vector conv, mesh->bone
binds = np.array([np.linalg.inv(m) for m in invB])   # bone->mesh, t in last row
origins = binds[:, 3, :3]                # bone origins in mesh space (T-pose)

# full-weighted centroids
BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20) for i in range(N)],
               np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
                for i in range(N)], np.float64)
cent = np.zeros((31, 3))
wsum = np.zeros(31)
for j in range(4):
    ids = b4s[:, j]
    ok = (ids >= 0) & (ids < 31) & (w4s[:, j] > 0)
    np.add.at(cent, ids[ok], verts[ok] * w4s[ok, j][:, None])
    np.add.at(wsum, ids[ok], w4s[ok, j])
okm = wsum > 0
cent[okm] /= wsum[okm][:, None]

# ---- 1. node convention search ----
def qrot_row(q, conv):
    x, y, z, w = q
    if conv == 'wxyz':
        x, y, z, w = q[1], q[2], q[3], q[0]
    if conv.endswith('_conj'):
        x, y, z = -x, -y, -z
    # column-conv R, then transpose for row conv
    Rc = np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T                             # row-vector rotation


def local_mat(n, conv, order):
    R = qrot_row(n['q'], conv)
    s = np.array(n['s'])
    S = np.diag(s)
    L = R @ S if order == 'RS' else S @ R
    M = np.eye(4)
    M[:3, :3] = L
    M[3, :3] = np.array(n['t'])            # row-conv translation
    return M


# parents for full chains (biped standard on Bip01 names)
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
# override with the palette-index tree where both are palette joints
PN = {joint_nodes[b]: joint_nodes[P31[b]] for b in P31}
parent_of = dict(BIPED)
parent_of.update(PN)


def world_mat(name, conv, order):
    chain = [name]
    while parent_of.get(chain[-1]):
        chain.append(parent_of[chain[-1]])
    chain.reverse()
    M = np.eye(4)
    for nm in chain:
        n = by_name[nm]
        M = local_mat(n, conv, order) @ M
    return M


print('=== 1. node convention search (vs bind origins) ===')
best = None
for conv in ('xyzw', 'xyzw_conj', 'wxyz', 'wxyz_conj'):
    for order in ('RS', 'SR'):
        errs = []
        for b in range(31):
            if b not in P31:
                continue
            M = world_mat(joint_nodes[b], conv, order)
            errs.append(float(np.linalg.norm(M[3, :3] - origins[b])))
        med = float(np.median(errs))
        tag = f'{conv:11s} {order}'
        print(f'  {tag}: median {med*100:6.1f} cm  max {max(errs)*100:6.1f}')
        if best is None or med < best[1]:
            best = ((conv, order), med, errs)
(convB, orderB), medB, errsB = best
print(f'  BEST: {convB} {orderB}  median {medB*100:.1f} cm  '
      f'max {max(errsB)*100:.1f} cm')
# null: permuted mapping under best convention
rng = np.random.default_rng(32)
n50s = []
worlds_best = {b: world_mat(joint_nodes[b], convB, orderB) for b in range(31)}
for _ in range(200):
    perm = rng.permutation(31)
    es = [float(np.linalg.norm(
        worlds_best[b][3, :3] - origins[perm[b]]))
        for b in range(31) if b in P31]
    n50s.append(float(np.median(es)))
print(f'  permuted-mapping null: median-of-medians '
      f'{sorted(n50s)[100]*100:.1f} cm (200 trials)')

# linear-part agreement: angle between world R and bind rotation
angs = []
for b in range(31):
    if b not in P31:
        continue
    Rw = worlds_best[b][:3, :3]
    Rb = binds[b][:3, :3]
    c = (np.trace(Rw.T @ Rb) - 1) / 2
    angs.append(math.degrees(math.acos(max(-1, min(1, c)))))
print(f'  rotation-part angle world-vs-bind: median '
      f'{sorted(angs)[len(angs)//2]:.1f} deg  max {max(angs):.1f} deg')

# ---- 2. bind-pose reproduction ----
print('\n=== 2. bind-pose reproduction (body, 1449 verts) ===')
V = np.hstack([verts, np.ones((N, 1))])          # row vectors
skin_pos = np.zeros((N, 3))
for i in range(N):
    acc = np.zeros(4)
    for j in range(4):
        b, w = int(b4s[i, j]), float(w4s[i, j])
        if b < 31 and w != 0.0:
            acc = acc + w * (V[i] @ invB[b] @ binds[b])
    skin_pos[i] = acc[:3]
err = np.linalg.norm(skin_pos - verts, axis=1)
print(f'  mean {err.mean()*100:.4f} cm  median {np.median(err)*100:.4f} cm  '
      f'max {err.max()*100:.4f} cm  (p99 {np.percentile(err,99)*100:.4f})')

# shuffled-weights null: permute weights within each record
rng2 = np.random.default_rng(33)
null_max, null_mean = [], []
for trial in range(20):
    sp = np.zeros((N, 3))
    wperm = np.array([rng2.permutation(w4s[i]) for i in range(N)])
    for j in range(4):
        ids = np.clip(b4s[:, j], 0, 30)
        W = wperm[:, j]
        # accumulate: v invB[b] bind[b] per vertex -- vectorize per bone
        for b in range(31):
            sel = ids == b
            if not sel.any():
                continue
            M = invB[b] @ binds[b]
            P = (V[sel] @ M)[:, :3]
            sp[sel] += W[sel][:, None] * P
    e = np.linalg.norm(sp - verts, axis=1)
    null_max.append(e.mean())
nulls_sorted = sorted(null_max)
print(f'  shuffled-weights null (20 trials): mean err '
      f'{float(np.mean(null_max))*100:.1f} cm  '
      f'(min {nulls_sorted[0]*100:.1f}, max {nulls_sorted[-1]*100:.1f})')

# ---- 3. rest-pose test with best node convention ----
print('\n=== 3. rest-pose test (node worlds, best convention) ===')
sp2 = np.zeros((N, 3))
for j in range(4):
    ids = np.clip(b4s[:, j], 0, 30)
    W = w4s[:, j]
    for b in range(31):
        sel = ids == b
        if not sel.any():
            continue
        M = invB[b] @ worlds_best[b]
        P = (V[sel] @ M)[:, :3]
        sp2[sel] += (W[sel][:, None] * P)
e2 = np.linalg.norm(sp2 - verts, axis=1)
print(f'  skinned(node default) vs unskinned mesh: mean {e2.mean()*100:.2f} cm'
      f'  median {np.median(e2)*100:.2f}  max {e2.max()*100:.2f} cm')
print('  -> if ~0: node default pose == bind pose (mesh authored in rest pose)')
print('  -> if large: mesh is in a different pose than node defaults')
# per-bone distance node-world vs bind origin
d_nb = {b: float(np.linalg.norm(worlds_best[b][3, :3] - origins[b]))
        for b in P31}
print('  per-bone node-vs-bind-origin distance (top 8):')
for b, v in sorted(d_nb.items(), key=lambda kv: -kv[1])[:8]:
    print(f'    {joint_nodes[b]:20s} {v*100:6.1f} cm')
print('  ... (median %.1f cm)' % (sorted(d_nb.values())[len(d_nb)//2]*100))

# arm angle numbers (bind origins vs node worlds)
def ang(v1, v2):
    c = v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return math.degrees(math.acos(max(-1, min(1, c))))

for side, ua, fa, ha in (('R', 10, 9, 8), ('L', 16, 15, 14)):
    shoulder = origins[P31[ua]] if False else None
    # mesh-space arm chain from bind origins: clavicle->upperarm->forearm->hand
    cl, up, fo, ha_o = origins[P31[ua] if False else
                               {10: 11, 16: 17}[ua]], \
        origins[ua], origins[fa], origins[ha]
    up_vec = fo - up
    hor = math.degrees(math.atan2(-up_vec[2], abs(up_vec[0])))
    print(f'  {side} upper-arm (bind): elbow-shoulder '
          f'({up_vec[0]:.3f},{up_vec[1]:.3f},{up_vec[2]:.3f}) '
          f'= {hor:.1f} deg below horizontal')
    wup = worlds_best[ua][3, :3]
    wfo = worlds_best[fa][3, :3]
    wup_vec = wfo - wup
    hor2 = math.degrees(math.atan2(-wup_vec[2], abs(wup_vec[0])))
    print(f'  {side} upper-arm (node):  elbow-shoulder '
          f'({wup_vec[0]:.3f},{wup_vec[1]:.3f},{wup_vec[2]:.3f}) '
          f'= {hor2:.1f} deg below horizontal')

json.dump(dict(
    best_conv=[convB, orderB], node_vs_bind_median_cm=medB * 100,
    node_vs_bind_max_cm=max(errsB) * 100,
    perm_null_cm=sorted(n50s)[100] * 100,
    rot_angle_median_deg=sorted(angs)[len(angs) // 2],
    bindpose_err_cm=dict(mean=float(err.mean() * 100),
                         median=float(np.median(err) * 100),
                         max=float(err.max() * 100)),
    shuffled_null_mean_cm=float(np.mean(null_max) * 100),
    rest_err_cm=dict(mean=float(e2.mean() * 100),
                     median=float(np.median(e2) * 100),
                     max=float(e2.max() * 100)),
    per_bone_node_vs_bind_cm={joint_nodes[b]: v * 100
                              for b, v in d_nb.items()},
), open('/home/z/my-project/download/s32_t1_bindpose.json', 'w'), indent=1)
print('\nwrote /home/z/my-project/download/s32_t1_bindpose.json')
