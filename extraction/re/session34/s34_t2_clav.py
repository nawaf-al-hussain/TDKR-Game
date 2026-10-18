#!/usr/bin/env python3
"""S34 T2: clavicle parentage from the FILE's own node hierarchy
(childCount/firstChild), then candidate-parent test table with permuted null."""
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
    idx = len(nodes)
    nodes.append(dict(idx=idx, off=o, name=n2, alias=al, t=t, q=q, s=s,
                      childCount=u32(o + 0x38), firstChild=u32(o + 0x3c)))
    o += 0x50
print(f'{len(nodes)} node records')
# build file hierarchy: children of node i = firstChild..firstChild+childCount-1
parent = {}
for n in nodes:
    for c in range(n['childCount']):
        ci = n['firstChild'] + c
        if 0 <= ci < len(nodes):
            if ci in parent and parent[ci] != n['idx']:
                print(f'  CONFLICT node {ci} parent {parent[ci]} vs {n["idx"]}')
            parent[ci] = n['idx']
byname = {n['name']: n for n in nodes}
for nm in ('Bip01', 'Bip01_Pelvis', 'Bip01_Spine', 'Bip01_Spine1', 'Bip01_Neck',
           'Bip01_L_Clavicle', 'Bip01_R_Clavicle', 'Bip01_L_UpperArm'):
    n = byname.get(nm)
    if n is None: continue
    p = parent.get(n['idx'])
    kids = [nodes[k]['name'] for k in range(n['childCount'])
            if 0 <= n['firstChild'] + k < len(nodes)]
    print(f'{nm}: idx {n["idx"]}, parent {nodes[p]["name"] if p is not None else None}, '
          f'children ({n["childCount"]}) {kids[:8]}')

# candidate parent test: bind-derived local vs node local per candidate parent
BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])
by_alias = {n['alias']: n['name'] for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p] for p in pal]
jidx = {nm: i for i, nm in enumerate(joint_nodes)}

def qangle(a, b):
    a = np.array(a, float); b = np.array(b, float)
    a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    return math.degrees(2 * math.acos(min(1.0, abs(float(np.dot(a, b))))))

cands = ['Bip01_Spine1', 'Bip01_Spine', 'Bip01_Pelvis', 'Bip01_Neck',
         'Bip01', 'Bip01_Head']
rng = np.random.default_rng(21)
perm_joints = joint_nodes[:]
rows = []
for clav in ('Bip01_L_Clavicle', 'Bip01_R_Clavicle'):
    b = jidx[clav]
    node = byname[clav]
    for cand in cands:
        if cand not in jidx: continue
        pi = jidx[cand]
        L = binds[b] @ np.linalg.inv(binds[pi])   # bind-derived local (row form)
        dt = float(np.linalg.norm(L[3, :3] - np.array(node['t'])))
        # node local rotation vs bind-derived rotation
        R_node = np.array(node['q'], float)
        # bind-derived rotation as quat: from R_row^T (column form = standard of q)
        Rb = L[:3, :3].T
        tr = Rb[0, 0] + Rb[1, 1] + Rb[2, 2]
        if tr > 0:
            sq = math.sqrt(tr + 1) * 2
            qw = 0.25 * sq; qx = (Rb[2, 1] - Rb[1, 2]) / sq
            qy = (Rb[0, 2] - Rb[2, 0]) / sq; qz = (Rb[1, 0] - Rb[0, 1]) / sq
        else:
            qw = 0; qx = qy = qz = 0
        dq = qangle([qx, qy, qz, qw], R_node)
        rows.append((clav, cand, dt * 100, dq, cand == 'Bip01_Spine1'))
# permuted null: random parent from the 31 joints (excluding self/children)
allj = list(range(31))
nulls = []
for _ in range(500):
    b = rng.integers(31)
    pi = rng.integers(31)
    if pi == b: continue
    L = binds[b] @ np.linalg.inv(binds[pi])
    node = byname[joint_nodes[b]]
    dt = float(np.linalg.norm(L[3, :3] - np.array(node['t'])))
    Rb = L[:3, :3].T
    tr = Rb[0, 0] + Rb[1, 1] + Rb[2, 2]
    if tr > 0:
        sq = math.sqrt(tr + 1) * 2
        qw = 0.25 * sq; qx = (Rb[2, 1] - Rb[1, 2]) / sq
        qy = (Rb[0, 2] - Rb[2, 0]) / sq; qz = (Rb[1, 0] - Rb[0, 1]) / sq
    else:
        qw = 1.0; qx = qy = qz = 0
    dq = qangle([qx, qy, qz, qw], node['q'])
    nulls.append((dt * 100, dq))
print(f'\nclavicle candidate-parent table (dt in cm, dq deg):')
for clav, cand, dt, dq, is_cur in rows:
    mark = ' <= current PNAME' if is_cur else ''
    print(f'  {clav:17s} parent {cand:15s} dt={dt:8.3f} cm  dq={dq:7.3f} deg{mark}')
print(f'\npermuted null (random parent pairs, n={len(nulls)}): '
      f'dt median {np.median([n[0] for n in nulls]):.2f} cm p05 {np.percentile([n[0] for n in nulls],5):.2f} cm; '
      f'dq median {np.median([n[1] for n in nulls]):.2f} deg p05 {np.percentile([n[1] for n in nulls],5):.2f}')
# also: the 29 NON-clavicle joints with PNAME parents — their dt/dq (positive control)
PN = {}
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11,
       11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
PNAMES = {0:'Bip01_R_Calf',1:'Bip01_R_Thigh',2:'Bip01_Pelvis',3:'Bip01_L_Calf',4:'Bip01_L_Thigh',5:'Bip01_Pelvis',6:'Bip01_R_Hand',7:'Bip01_R_Hand',8:'Bip01_R_Forearm',9:'Bip01_R_UpperArm',10:'Bip01_R_Clavicle',11:'Bip01_Spine1',12:'Bip01_L_Hand',13:'Bip01_L_Hand',14:'Bip01_L_Forearm',15:'Bip01_L_UpperArm',16:'Bip01_L_Clavicle',17:'Bip01_Spine1',18:'Bip01_Neck',19:'Bip01_Spine1',20:'Bip01_Spine',21:'Bip01_Pelvis',22:'Bip01',23:'Bip01_L_Finger0',24:'Bip01_L_Finger1',25:'Bip01_L_Hand',26:'Bip01_L_Finger2',27:'Bip01_R_Finger0',28:'Bip01_R_Finger1',29:'Bip01_R_Hand',30:'Bip01_R_Finger2'}
ok_dt = []
for b, pn in PNAMES.items():
    nm = joint_nodes[b]
    if 'Clavicle' in nm: continue
    node = byname.get(nm)
    pi = jidx.get(pn)
    if node is None or pi is None: continue
    L = binds[b] @ np.linalg.inv(binds[pi])
    ok_dt.append(float(np.linalg.norm(L[3, :3] - np.array(node['t']))) * 100)
print(f'\nPOSITIVE CONTROL (29 non-clavicle joints, PNAME parents): dt median '
      f'{np.median(ok_dt):.3f} cm, max {max(ok_dt):.3f} cm')
json.dump(dict(rows=[[r[0], r[1], r[2], r[3]] for r in rows],
               null=dict(dt_median=float(np.median([n[0] for n in nulls])),
                         dt_p05=float(np.percentile([n[0] for n in nulls], 5)),
                         dq_median=float(np.median([n[1] for n in nulls]))),
               file_hierarchy={n['name']: nodes[parent[n['idx']]]['name']
                               for n in nodes if n['idx'] in parent and
                               (n['name'].startswith('Bip01'))}),
          open('/home/z/my-project/scripts/s34_t2_clav.json', 'w'))
