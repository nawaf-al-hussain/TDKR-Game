#!/usr/bin/env python3
"""S32 T1e: CONSOLIDATED bind-pose numbers + CAPE solve + bridge dump.

Facts established so far (to be re-derived cleanly here):
- stored 31 matrices @0x30e30 = inverse binds in MESH space (tree-free test)
- node worlds (correct parents): legs/spine/head EXACT; arm chain off
- discrepancy localized to Clavicle + UpperArm node locals
- cape: 394 skin records @0x5ad64 (ids 0..37), binds @0x5a210,
  vertex block candidate @0x54d78 (21552 B; 394x48 + 2640 u16 idx?)
"""
import struct, math, json
import numpy as np
from collections import Counter

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


def local_mat(n):
    M = np.eye(4)
    M[:3, :3] = qrot_row(n['q']) @ np.diag(n['s'])
    M[3, :3] = np.array(n['t'])
    return M


def world_mat(name, override=None):
    chain = [name]
    while parent_name(chain[-1]):
        chain.append(parent_name(chain[-1]))
    chain.reverse()
    M = np.eye(4)
    for nm in chain:
        if override and nm in override:
            M = override[nm] @ M
        elif nm in JN:
            M = local_mat(JN[nm]) @ M
    return M


BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])
origins = binds[:, 3, :3]

BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20) for i in range(N)],
               np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
                for i in range(N)], np.float64)
V = np.hstack([verts, np.ones((N, 1))])

out = {}

# ---- A. node worlds vs binds: final numbers ----
worlds = {b: world_mat(joint_nodes[b]) for b in range(31)}
pos_err = {b: float(np.linalg.norm(worlds[b][3, :3] - origins[b]))
           for b in range(31)}
rot_err = {}
for b in range(31):
    c = (np.trace(worlds[b][:3, :3].T @ binds[b][:3, :3]) - 1) / 2
    rot_err[b] = math.degrees(math.acos(max(-1, min(1, c))))
exact_bones = [b for b in range(31) if pos_err[b] < 0.002 and rot_err[b] < 0.1]
arm_bones = [b for b in range(31) if b not in exact_bones]
print(f'=== A. node worlds vs stored binds ===')
print(f'  exact bones ({len(exact_bones)}): '
      f'{[joint_nodes[b] for b in exact_bones]}')
print(f'  off bones ({len(arm_bones)}): '
      f'{[(joint_nodes[b], round(pos_err[b]*100,1), round(rot_err[b],2)) for b in arm_bones]}')
out['pos_err_cm'] = {joint_nodes[b]: pos_err[b] * 100 for b in range(31)}
out['rot_err_deg'] = {joint_nodes[b]: rot_err[b] for b in range(31)}

# ---- B. rest-pose skinning with node worlds + proper shuffled null ----
def skin(world_map, wmat=None):
    sp = np.zeros((N, 3))
    W = w4s if wmat is None else wmat
    for j in range(4):
        ids = np.clip(b4s[:, j], 0, 30)
        Wj = W[:, j]
        for b in range(31):
            sel = ids == b
            if not sel.any():
                continue
            M = invB[b] @ world_map[b]
            sp[sel] += Wj[sel][:, None] * (V[sel] @ M)[:, :3]
    return sp


sp_node = skin(worlds)
e_node = np.linalg.norm(sp_node - verts, axis=1)
n_exact = int((e_node < 1e-3).sum())
print(f'\n=== B. rest-pose skinning (node worlds) ===')
print(f'  exact (<0.1 cm): {n_exact}/1449   0.1-1cm: '
      f'{int(((e_node>=0.001)&(e_node<0.01)).sum())}   '
      f'>1cm: {int((e_node>=0.01).sum())}   max {e_node.max()*100:.1f} cm  '
      f'mean {e_node.mean()*100:.2f} cm')
dom = np.zeros(N, int)
for i in range(N):
    js = [(w4s[i, j], int(b4s[i, j])) for j in range(4) if w4s[i, j] > 0]
    dom[i] = max(js)[1]
fail_by = Counter(dom[i] for i in range(N) if e_node[i] >= 0.001)
print(f'  failing verts touch ONLY exact bones? ', end='')
only_exact = sum(1 for i in range(N) if e_node[i] >= 0.001
                 and all(int(b) in exact_bones for b in b4s[i] if b < 31))
print(f'{only_exact} (expect 0)')

# shuffled-weights null on the SAME node worlds
rng = np.random.default_rng(34)
nulls = []
for _ in range(20):
    wp = np.array([rng.permutation(w4s[i]) for i in range(N)])
    e = np.linalg.norm(skin(worlds, wp) - verts, axis=1)
    nulls.append(float(e.mean()))
nulls.sort()
print(f'  shuffled-weights null: mean-err median {nulls[10]*100:.1f} cm '
      f'(min {nulls[0]*100:.1f} max {nulls[-1]*100:.1f}) '
      f'vs real {e_node.mean()*100:.2f} cm')
out['rest_skinning'] = dict(
    exact=int(n_exact), n_1cm=int((e_node >= 0.01).sum()),
    max_cm=float(e_node.max() * 100), mean_cm=float(e_node.mean() * 100),
    null_mean_median_cm=nulls[10] * 100)

# ---- C. bind-aligned rig: override clavicle+upperarm with bind locals ----
override = {}
for b in arm_bones:
    p = PNAME[b]
    pi = idx.get(p, -1)
    L = binds[b] @ (np.linalg.inv(binds[pi]) if pi >= 0 else np.eye(4))
    override[joint_nodes[b]] = L
worlds_fix = {b: world_mat(joint_nodes[b], override) for b in range(31)}
pf = {b: float(np.linalg.norm(worlds_fix[b][3, :3] - origins[b]))
      for b in range(31)}
print(f'\n=== C. bind-aligned rig (override clavicle+upperarm locals) ===')
print(f'  max pos err after fix: {max(pf.values())*100:.4f} cm')
sp_fix = skin(worlds_fix)
e_fix = np.linalg.norm(sp_fix - verts, axis=1)
print(f'  skinning after fix: exact {int((e_fix<1e-3).sum())}/1449  '
      f'max {e_fix.max()*100:.4f} cm  mean {e_fix.mean()*100:.4f} cm')
out['fixed_rig'] = dict(max_pos_err_cm=float(max(pf.values()) * 100),
                        skin_max_cm=float(e_fix.max() * 100),
                        skin_mean_cm=float(e_fix.mean() * 100))

# ---- D. bridge dump @0x30614 ----
print('\n=== D. u16 bridge @0x30614 (first 64) ===')
br = [struct.unpack_from('<H', d, 0x30614 + 2 * i)[0] for i in range(64)]
print(' ', br)
vals = set()
for i in range(841):
    vals.add(struct.unpack_from('<H', d, 0x30614 + 2 * i)[0])
print(f'  distinct {len(vals)}, min {min(vals)}, max {max(vals)}')
out['bridge'] = dict(first64=br, distinct=len(vals), max=int(max(vals)))

# ---- E. CAPE: parse vertex block, tree-free test, node check ----
print('\n=== E. CAPE ===')
CAPE, CSKIN, CN = 0x5a210, 0x5ad64, 394
cape_inv = np.array([np.array(struct.unpack_from('<16f', d, CAPE + k * 64),
                              np.float64).reshape(4, 4) for k in range(38)])
cape_bind = np.array([np.linalg.inv(m) for m in cape_inv])
cape_org = cape_bind[:, 3, :3]
cb4 = np.array([struct.unpack_from('<4B', d, CSKIN + i * 20)
                for i in range(CN)], np.int64)
cw4 = np.array([struct.unpack_from('<4f', d, CSKIN + i * 20 + 4)
                for i in range(CN)], np.float64)
# vertex block hypothesis: 394 x 48 B @0x54d78, pos at +0
VOFF = 0x54d78
cverts = np.array([struct.unpack_from('<3f', d, VOFF + i * 48)
                   for i in range(CN)])
print(f'  cape verts (stride-48 hypothesis): x [{cverts[:,0].min():.2f},'
      f'{cverts[:,0].max():.2f}] y [{cverts[:,1].min():.2f},'
      f'{cverts[:,1].max():.2f}] z [{cverts[:,2].min():.2f},'
      f'{cverts[:,2].max():.2f}]')
# normals at +12?
cn = np.array([struct.unpack_from('<3f', d, VOFF + i * 48 + 12)
               for i in range(CN)])
nl = np.linalg.norm(cn, axis=1)
print(f'  +12 f32x3 norm: median {np.median(nl):.3f} '
      f'(1.0 => normals; ~0 => garbage)')
# cape centroids (full weights) vs cape bind origins
ccent = np.zeros((38, 3))
cwsum = np.zeros(38)
for j in range(4):
    ids = cb4[:, j]
    ok = (ids >= 0) & (ids < 38) & (cw4[:, j] > 0)
    np.add.at(ccent, ids[ok], cverts[ok] * cw4[ok, j][:, None])
    np.add.at(cwsum, ids[ok], cw4[ok, j])
okm = cwsum > 0
ccent[okm] /= cwsum[okm][:, None]
es = [float(np.linalg.norm(ccent[b] - cape_org[b])) for b in range(38)
      if cwsum[b] > 0]
print(f'  tree-free H2 (cape bind origins vs centroids): median '
      f'{sorted(es)[len(es)//2]*100:.1f} cm over {len(es)} bones')
# permuted null
rng2 = np.random.default_rng(35)
nn = []
for _ in range(200):
    pm = rng2.permutation(38)
    nn.append(float(np.median([float(np.linalg.norm(ccent[b] - cape_org[pm[b]]))
                               for b in range(38) if cwsum[b] > 0])))
nn.sort()
print(f'  permuted null: median-of-medians {nn[100]*100:.1f} cm')

# cape node worlds: find CBone nodes
cbone_nodes = [n for n in nodes if n['name'].startswith('CBone')]
print(f'  CBone-named nodes in bdae: {len(cbone_nodes)}')
print('  names sample:', [n['name'] for n in cbone_nodes[:8]])
# cape palette names? look for strings near 0x5a1b8 (88 B block)
blk = d[0x5a1b8:0x5a210]
print(f'  0x5a1b8 block: {blk[:40].hex()} ... ascii attempt: '
      f'{bytes(b if 32<=b<127 else 46 for b in blk[:48]).decode()}')

json.dump(out, open('/home/z/my-project/download/s32_t1_consolidated.json',
                    'w'), indent=1)
print('\nwrote s32_t1_consolidated.json')
