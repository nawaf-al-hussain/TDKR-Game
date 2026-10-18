#!/usr/bin/env python3
"""S34 T2: end-to-end rig check with corrected clavicle parent (Neck).
If all 31 node worlds == bind worlds, the r22 '4-record override' disappears.
Also fix the dq display and verify the full skinning from raw node records."""
import struct, math, json
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
    nodes.append(dict(name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
JN = {n['name']: n for n in nodes}
by_alias = {n['alias']: n['name'] for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p] for p in pal]

# corrected parent map: r23 PNAME with clavicles -> Neck
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
BIPED = {
    'Bip01_Pelvis': 'Bip01', 'Bip01_Spine': 'Bip01_Pelvis',
    'Bip01_Spine1': 'Bip01_Spine', 'Bip01_Neck': 'Bip01_Spine1',
    'Bip01_Head': 'Bip01_Neck',
    'Bip01_L_Thigh': 'Bip01_Pelvis', 'Bip01_L_Calf': 'Bip01_L_Thigh',
    'Bip01_L_Foot': 'Bip01_L_Calf', 'Bip01_R_Thigh': 'Bip01_Pelvis',
    'Bip01_R_Calf': 'Bip01_R_Thigh', 'Bip01_R_Foot': 'Bip01_R_Calf',
    'Bip01_L_UpperArm': 'Bip01_L_Clavicle',
    'Bip01_L_Forearm': 'Bip01_L_UpperArm', 'Bip01_L_Hand': 'Bip01_L_Forearm',
    'Bip01_R_UpperArm': 'Bip01_R_Clavicle',
    'Bip01_R_Forearm': 'Bip01_R_UpperArm', 'Bip01_R_Hand': 'Bip01_R_Forearm',
    'Bip01_L_Finger0': 'Bip01_L_Hand', 'Bip01_L_Finger01': 'Bip01_L_Finger0',
    'Bip01_L_Finger1': 'Bip01_L_Hand', 'Bip01_L_Finger11': 'Bip01_L_Finger1',
    'Bip01_L_Finger2': 'Bip01_L_Hand', 'Bip01_L_Finger21': 'Bip01_L_Finger2',
    'Bip01_R_Finger0': 'Bip01_R_Hand', 'Bip01_R_Finger01': 'Bip01_R_Finger0',
    'Bip01_R_Finger1': 'Bip01_R_Hand', 'Bip01_R_Finger11': 'Bip01_R_Finger1',
    'Bip01_R_Finger2': 'Bip01_R_Hand', 'Bip01_R_Finger21': 'Bip01_R_Finger2',
}
pname_of = {joint_nodes[b]: PNAME[b] for b in PNAME}
def parent_name(nm):
    if nm in pname_of: return pname_of[nm]
    if nm in BIPED: return BIPED[nm]
    return None

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

def world(nm):
    chain = [nm]
    while parent_name(chain[-1]): chain.append(parent_name(chain[-1]))
    chain.reverse()
    M = np.eye(4)
    for x in chain:
        if x in JN: M = local_row(JN[x]) @ M
    return M

BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])

print('node world vs bind world (row-form, position error cm / rot error deg):')
worst_p = worst_r = 0
per = []
for b in range(31):
    nm = joint_nodes[b]
    W = world(nm)
    dp = float(np.linalg.norm(W[3, :3] - binds[b][3, :3])) * 100
    Rn = W[:3, :3].T @ binds[b][:3, :3]
    ang = math.degrees(math.acos(min(1.0, (np.trace(Rn) - 1) / 2)))
    per.append((nm, dp, ang))
    worst_p = max(worst_p, dp); worst_r = max(worst_r, ang)
for nm, dp, ang in per:
    flag = ' <-- ' if dp > 0.01 or ang > 0.01 else ''
    print(f'  {nm:22s} dp={dp:8.4f} cm  dr={ang:7.3f} deg{flag}')
print(f'\nWORST: dp {worst_p:.4f} cm, dr {worst_r:.4f} deg')
print('clavicles:', [(nm, round(dp, 4), round(ang, 4)) for nm, dp, ang in per
                    if 'Clavicle' in nm])

# full skinning from raw node records (no overrides) vs stored verts
BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80) for i in range(N)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20) for i in range(N)], np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4) for i in range(N)])
V = np.hstack([verts, np.ones((N, 1))])
W = {b: world(joint_nodes[b]) for b in range(31)}
sp = np.zeros((N, 3))
for j in range(4):
    sel_ids = np.clip(b4s[:, j], 0, 30)
    for b in range(31):
        sel = sel_ids == b
        if not sel.any(): continue
        M = invB[b] @ W[b]
        sp[sel] += w4s[sel][:, j][:, None] * (V[sel] @ M)[:, :3]
e = np.linalg.norm(sp - verts, axis=1)
print(f'\nSKIN from raw node records (corrected parent, NO overrides): '
      f'exact<0.1mm {int((e < 1e-4).sum())}/1449, mean {e.mean()*100:.4f} cm, '
      f'max {e.max()*100:.4f} cm')
json.dump(dict(per_joint=[[nm, dp, ang] for nm, dp, ang in per],
               skin_exact=int((e < 1e-4).sum()), skin_max_cm=float(e.max()*100)),
          open('/home/z/my-project/scripts/s34_t2_rigfix.json', 'w'))
