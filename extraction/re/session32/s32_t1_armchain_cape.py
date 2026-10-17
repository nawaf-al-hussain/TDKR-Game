#!/usr/bin/env python3
"""S32 T1d: arm-chain discrepancy root-cause + cape mesh parse + cape test."""
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

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]
JN = {n['name']: n for n in nodes}

# full node tree parents from childCount/firstChildPtr (r21 decode)
by_off = {n['off']: n for n in nodes}
treeparent = {}
for n in nodes:
    for k in range(n['ccount']):
        cp = u32(n['child'] + 4 * k)
        c = by_off.get(cp)
        if c is not None:
            treeparent[c['name']] = n['name']
print('tree parents for arm chain:')
for nm in ('Bip01', 'Bip01_Pelvis', 'Bip01_Spine', 'Bip01_Spine1',
           'Bip01_R_Clavicle', 'Bip01_L_Clavicle', 'Bip01_R_UpperArm',
           'Bip01_Neck', 'Bip01_Head'):
    print(f'  {nm:20s} parent={treeparent.get(nm)}')

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

BODY = 0x30e30
invB = np.array([np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                          np.float64).reshape(4, 4) for k in range(31)])
binds = np.array([np.linalg.inv(m) for m in invB])
origins = binds[:, 3, :3]


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


def world_mat(name, pmap):
    chain = [name]
    while pmap.get(chain[-1]):
        chain.append(pmap[chain[-1]])
    chain.reverse()
    M = np.eye(4)
    for nm in chain:
        if nm in JN:
            M = local_mat(JN[nm]) @ M
    return M


# ---- what parent world would the clavicle need? ----
idx = {joint_nodes[b]: b for b in range(31)}
print('\n=== required parent-world for clavicle local ===')
for side, bcl in (('R', 10), ('L', 17)):
    ncl = JN[joint_nodes[bcl]]
    Lcl = local_mat(ncl)
    need = np.linalg.inv(Lcl) @ binds[bcl]     # W_p such that Lcl @ W_p = bind
    print(f'{joint_nodes[bcl]}: required parent world t = '
          f'({need[3,0]:.4f},{need[3,1]:.4f},{need[3,2]:.4f})')
    for cand in ('Bip01', 'Bip01_Pelvis', 'Bip01_Spine', 'Bip01_Spine1',
                 'Bip01_Neck', 'Bip01_Head'):
        if cand in JN:
            Wc = world_mat(cand, PNAME)
            dd = float(np.linalg.norm(Wc[3, :3] - need[3, :3]))
            cr = (np.trace(Wc[:3, :3].T @ need[:3, :3]) - 1) / 2
            print(f'   vs {cand:16s} world t ({Wc[3,0]:.4f},{Wc[3,1]:.4f},'
                  f'{Wc[3,2]:.4f})  dt={dd*100:7.1f} cm  dR='
                  f'{math.degrees(math.acos(max(-1,min(1,cr)))):5.1f} deg')

# ---- alternative: use TREE parents for everything ----
print('\n=== worlds with TREE parents vs binds ===')
for use_tree in (False, True):
    pmap = treeparent if use_tree else {v: k for k, v in
                                        [(b, PNAME[b]) for b in PNAME]}
    errs = []
    for b in range(31):
        W = world_mat(joint_nodes[b], pmap)
        errs.append(float(np.linalg.norm(W[3, :3] - origins[b])))
    print(f'  tree={use_tree}: median {sorted(errs)[15]*100:.1f} cm  '
          f'max {max(errs)*100:.1f} cm')

# ---- raw locals: node vs bind-derived for arm chain ----
print('\n=== arm-chain locals: node record vs bind-derived ===')
for b in (10, 9, 8, 11, 6, 17):
    p = {10: 20, 9: 10, 8: 9, 11: 20, 6: 8, 17: 20}[b]
    Lb = binds[b] @ np.linalg.inv(binds[p])   # bind-derived local (row conv)
    Ln = local_mat(JN[joint_nodes[b]])
    print(f'{joint_nodes[b]:20s} parent {joint_nodes[p]}')
    print(f'  bind-local t ({Lb[3,0]:7.4f},{Lb[3,1]:7.4f},{Lb[3,2]:7.4f})  '
          f'node t ({Ln[3,0]:7.4f},{Ln[3,1]:7.4f},{Ln[3,2]:7.4f})')
    cr = (np.trace(Lb[:3, :3].T @ Ln[:3, :3]) - 1) / 2
    print(f'  local rotation delta {math.degrees(math.acos(max(-1,min(1,cr)))):.2f} deg')

# ---- cape vertex block parse @0x54d78 (21552 B) ----
print('\n=== cape block @0x54d78 ===')
off = 0x54d78
ln = 21552
blk = d[off:off + ln]
f32 = np.frombuffer(blk, np.float32)
print(f'  first 24 f32: {np.round(f32[:24], 3)}')
# hypothesis: N verts x stride S. 394 records. try S=48: 394*48=18912;
# remainder 2640 = 1320 u16 or 660 u32
for S in (48, 36, 32, 24, 44, 40):
    if ln % S == 0:
        print(f'  stride {S}: {ln//S} items')
# scan for plausable position triples: consecutive f32 in [-3,3]
vals = f32
good = np.sum((np.abs(vals) < 3) & (vals != 0))
print(f'  f32 count {len(vals)}, |v|<3 nonzero {good}')
# find offset of first plausible triple run
run = 0
best_start = None
for i in range(0, min(len(vals) - 3, 4000)):
    x, y, z = vals[i:i + 3]
    if abs(x) < 2 and abs(y) < 2 and 0 < z < 2.2:
        if run == 0:
            best_start = i
        run += 1
    else:
        if run > 50:
            break
        run = 0
print(f'  first plausible pos run starts f32 idx {best_start} '
      f'(byte {best_start*4 if best_start is not None else None}), '
      f'len {run}')
