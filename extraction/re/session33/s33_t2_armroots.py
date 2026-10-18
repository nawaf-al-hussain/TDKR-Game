#!/usr/bin/env python3
"""S33 T2a: the 4 arm-root node records — scale signs, mirroring; and the
T1 idle t=0 rotation vs node rest vs bind-derived local for these bones."""
import struct, math, json
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
AD = '/tmp/my-project/work/data/batman_anims.bdae'
md = open(MD, 'rb').read()
ad = open(AD, 'rb').read()
u32m = lambda o: struct.unpack_from('<I', md, o)[0]
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]

def pool(v):
    if 0x868 <= v < 0x22d8:
        e = md.find(b'\0', v)
        if e >= v: return md[v:e].decode('latin1')

nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32m(o)), pool(u32m(o + 4)), pool(u32m(o + 8))
    if n1 is None or n2 is None or al is None: o += 4; continue
    t = struct.unpack_from('<3f', md, o + 0x0c)
    q = struct.unpack_from('<4f', md, o + 0x18)
    s = struct.unpack_from('<3f', md, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s): o += 4; continue
    if u32m(o + 0x34) != 1 or u32m(o + 0x38) > 32: o += 4; continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
by_name = {n['name']: n for n in nodes}
print(f'{len(nodes)} nodes')

# --- the 4 arm-root records ---
for nm in ('Bip01_L_Clavicle', 'Bip01_R_Clavicle',
           'Bip01_L_UpperArm', 'Bip01_R_UpperArm',
           'Bip01_L_Forearm', 'Bip01_R_Forearm'):
    n = by_name[nm]
    print(f'{nm}: t={[round(x,4) for x in n["t"]]} q={[round(x,4) for x in n["q"]]} '
          f's={[round(x,4) for x in n["s"]]} det(R@S)={np.linalg.det(np.array(n["s"]) * np.eye(3)):.4f}')

# --- bind-derived locals for the arm chain (from stored inverse binds) ---
u32 = u32m
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = md[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11,
       11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', md, BODY + k * 64), np.float64).reshape(4, 4)
                 for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])

def parent_idx(b):
    return P31.get(b)

def bind_local(b):
    Wb = binds[b]
    p = parent_idx(b)
    Wp = binds[p] if p is not None else np.eye(4)
    return Wb @ np.linalg.inv(Wp)   # row-vector: child_local = Wb * inv(Wp)

def decompose(M):
    R = M[:3, :3]
    t = M[3, :3]
    # polar-ish: assume no shear; extract per-axis via column norms? use SVD
    U, S, Vt = np.linalg.svd(R)
    return t, U @ Vt, S

print('\nbind-derived locals vs node records (arm chain):')
for b in range(31):
    nm = joint_nodes[b]
    if not any(x in nm for x in ('Clavicle', 'UpperArm', 'Forearm', 'Spine1', 'Neck')):
        continue
    L = bind_local(b)
    t, R, sv = decompose(L)
    n = by_name[nm]
    tn = np.array(n['t'])
    # angle between node quat R and bind R
    def qmat_row(q):
        x, y, z, w = q
        Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                       [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                       [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
        return Rc.T
    Rn = qmat_row(n['q'])
    ang = math.degrees(math.acos(min(1, max(-1, (np.trace(Rn @ R.T) - 1) / 2))))
    print(f'  {nm:22s} node t={[round(x,4) for x in tn]} bindL t={[round(x,4) for x in t]} '
          f'ang={ang:6.2f} sv={[round(x,3) for x in sv]}')

# --- T1 idle t=0 rotations for the arm chain vs node rest ---
# reload T1 decode quickly (reuse placement logic inline, minimal)
import subprocess
print('\nT1 idle t=0 arm rotations vs node rest:')
exec(open('/home/z/my-project/scripts/s33_t1_final.py').read().split("# ---- oracle")[0])
for nm in ('Bip01_L_Clavicle', 'Bip01_R_Clavicle', 'Bip01_L_UpperArm',
           'Bip01_R_UpperArm', 'Bip01_L_Forearm', 'Bip01_R_Forearm'):
    if nm not in chans or 'rotation' not in chans[nm]:
        print(f'  {nm}: no anim channel'); continue
    ks = keys_of(nm, 'rotation')
    q0 = ks[0]
    n = by_name[nm]
    e = qangle(q0, n['q'])
    print(f'  {nm}: t=0 quat {[round(x,4) for x in q0]} vs node rest '
          f'{[round(x,4) for x in n["q"]]} angle {e:.2f} deg, keys={len(ks)}')
