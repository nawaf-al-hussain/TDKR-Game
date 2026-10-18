#!/usr/bin/env python3
"""S34 T2b: clavicle candidate test with FIXED rotation error computation.
Separates translation match from rotation match per candidate parent."""
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
jidx = {nm: i for i, nm in enumerate(joint_nodes)}

BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])

def rot_angle_deg(Ra, Rb):
    """angle of Ra^T @ Rb (row-form pair)"""
    R = Ra.T @ Rb
    c = (np.trace(R) - 1) / 2
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def node_rot_row(q):
    x, y, z, w = q
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

cands = ['Bip01_Spine1', 'Bip01_Neck', 'Bip01_Spine', 'Bip01_Pelvis',
         'Bip01_Head', 'Bip01']
print(f'{"clavicle":18s} {"parent":15s} {"dt cm":>9s} {"dq deg":>9s}')
for clav in ('Bip01_L_Clavicle', 'Bip01_R_Clavicle'):
    b = jidx[clav]
    node = JN[clav]
    R_node = node_rot_row(node['q'])
    for cand in cands:
        pi = jidx[cand]
        L = binds[b] @ np.linalg.inv(binds[pi])
        dt = float(np.linalg.norm(L[3, :3] - np.array(node['t']))) * 100
        dq = rot_angle_deg(L[:3, :3], R_node)
        print(f'{clav:18s} {cand:15s} {dt:9.3f} {dq:9.3f}')
    print()

# axis of the rotation difference for the best translation candidate (Neck)
for clav in ('Bip01_L_Clavicle', 'Bip01_R_Clavicle'):
    b = jidx[clav]
    node = JN[clav]
    L = binds[b] @ np.linalg.inv(binds[jidx['Bip01_Neck']])
    R = L[:3, :3].T @ node_rot_row(node['q'])   # relative rotation
    c = (np.trace(R) - 1) / 2
    ang = math.acos(max(-1.0, min(1.0, c)))
    s = 2 * math.sin(ang)
    axis = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / s
    print(f'{clav}: node-vs-bind(Neck-parent) rotation {math.degrees(ang):.3f} deg '
          f'about axis {np.round(axis, 4)}')
# compare: node quat vs the R23 claim (twist about X)
