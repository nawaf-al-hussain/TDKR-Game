#!/usr/bin/env python3
"""S32 T1c: fixed finger parents + full residual diagnostics + CAPE scan."""
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

# r21 VERIFIED parents (from s31_t2_result.json, name-based)
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
idx = {joint_nodes[b]: b for b in range(31)}
P31 = {b: idx.get(PNAME[b], -1) for b in range(31)}

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


def qrot_row(q):
    x, y, z, w = q
    Rc = np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T


def local_mat(n):
    R = qrot_row(n['q'])
    S = np.diag(n['s'])
    M = np.eye(4)
    M[:3, :3] = R @ S
    M[3, :3] = np.array(n['t'])
    return M


def world_mat(name):
    chain = [name]
    while True:
        b = idx.get(chain[-1], None)
        p = P31[b] if (b is not None and b in P31) else -1
        pn = PNAME[chain.__len__() and b] if False else None
        # parent name: from PNAME if palette joint, else biped map
        if b is not None and b in PNAME:
            pn = PNAME[b]
        else:
            BIP = {'Bip01_Pelvis': 'Bip01', 'Bip01_Spine': 'Bip01_Pelvis',
                   'Bip01_Spine1': 'Bip01_Spine', 'Bip01_Neck': 'Bip01_Spine1',
                   'Bip01_Head': 'Bip01_Neck'}
            pn = BIP.get(chain[-1])
        if not pn:
            break
        chain.append(pn)
    chain.reverse()
    M = np.eye(4)
    for nm in chain:
        M = local_mat(JN[nm]) @ M
    return M


worlds = {b: world_mat(joint_nodes[b]) for b in range(31)}

print('=== full per-bone table: bind origin vs node world ===')
print(f'{"joint":2s} {"palette":8s} {"node":20s} '
      f'{"bind origin":>24s} {"node world":>24s} {"dist cm":>8s} {"rot deg":>8s}')
for b in range(31):
    M = worlds[b]
    d3 = float(np.linalg.norm(M[3, :3] - origins[b]))
    Rw, Rb = M[:3, :3], binds[b][:3, :3]
    c = (np.trace(Rw.T @ Rb) - 1) / 2
    ang = math.degrees(math.acos(max(-1, min(1, c))))
    print(f'{b:2d} {pal[b]:8s} {joint_nodes[b]:20s} '
          f'({origins[b][0]:7.3f},{origins[b][1]:7.3f},{origins[b][2]:7.3f}) '
          f'({M[3,0]:7.3f},{M[3,1]:7.3f},{M[3,2]:7.3f}) '
          f'{d3*100:8.1f} {ang:8.1f}')

# node t for the fingers, raw
print('\nnode local t (fingers):')
for b in (6, 7, 12, 13, 23, 24, 25, 26, 27, 28, 29, 30):
    n = JN[joint_nodes[b]]
    print(f'  {b:2d} {joint_nodes[b]:20s} t '
          f'({n["t"][0]:7.3f},{n["t"][1]:7.3f},{n["t"][2]:7.3f}) '
          f's ({n["s"][0]:.2f},{n["s"][1]:.2f},{n["s"][2]:.2f})')

# ---- residual histogram: which verts fail under node-world skinning ----
print('\n=== residual analysis (node-world skinning) ===')
V = np.hstack([verts, np.ones((N, 1))])
sp = np.zeros((N, 3))
dom = np.zeros(N, int)
for j in range(4):
    ids = np.clip(b4s[:, j], 0, 30)
    W = w4s[:, j]
    up = np.argmax(w4s, axis=1)
    for b in range(31):
        sel = ids == b
        if not sel.any():
            continue
        M = invB[b] @ worlds[b]
        P = (V[sel] @ M)[:, :3]
        sp[sel] += W[sel][:, None] * P
for i in range(N):
    js = [(w4s[i, j], b4s[i, j]) for j in range(4) if w4s[i, j] > 0]
    dom[i] = max(js)[1]
e = np.linalg.norm(sp - verts, axis=1)
print(f'  verts err<0.1cm: {(e<0.001).sum()}/1449   <1cm: {(e<0.01).sum()}'
      f'   1-10cm: {((e>=0.01)&(e<0.1)).sum()}   >10cm: {(e>=0.1).sum()}')
cnt_by = Counter()
worst_by = {}
for i in range(N):
    if e[i] >= 0.01:
        cnt_by[dom[i]] += 1
        worst_by[dom[i]] = max(worst_by.get(dom[i], 0), e[i])
print('  failing verts by dominant bone:')
for b, c in sorted(cnt_by.items(), key=lambda kv: -kv[1]):
    print(f'    {joint_nodes[b]:20s} {c:4d}  worst {worst_by[b]*100:6.1f} cm')

# ---- CAPE: scan for skin-record runs with ids < 38 ----
print('\n=== CAPE scan: skin-record-like runs (20-B [u8x4][f32x4]) ===')
cand_runs = []
i = 0x388b8
end = len(d) - 20
run_start, run_len = None, 0
while i < end:
    b4 = struct.unpack_from('<4B', d, i)
    w4 = struct.unpack_from('<4f', d, i + 4)
    if max(b4) < 38 and all(w >= 0 and w <= 1.0001 for w in w4) and \
            abs(sum(w4) - 1.0) < 0.02:
        if run_start is None:
            run_start = i
        run_len += 1
    else:
        if run_len >= 64:
            cand_runs.append((run_start, run_len))
        run_start, run_len = None, 0
    i += 20
if run_len >= 64:
    cand_runs.append((run_start, run_len))
for s, l in cand_runs:
    ids = set()
    for k in range(s, s + l * 20, 20):
        ids.update(struct.unpack_from('<4B', d, k))
    print(f'  run @0x{s:x}: {l} records, bone-id range 0..{max(ids)}, '
          f'distinct {len(ids)}')

# cape binds vs cape centroids for each run
CAPE = 0x5a210
capeB = np.array([np.array(struct.unpack_from('<16f', d, CAPE + k * 64),
                           np.float64).reshape(4, 4) for k in range(38)])
orth = max(float(np.abs(m[:3, :3] @ m[:3, :3].T - np.eye(3)).max())
           for m in capeB)
cape_bind = np.array([np.linalg.inv(m) for m in capeB])
cape_org = cape_bind[:, 3, :3]
print(f'  cape binds @0x5a210: orthonormality max {orth:.1e}; '
      f'origin spread x [{cape_org[:,0].min():.2f},{cape_org[:,0].max():.2f}] '
      f'z [{cape_org[:,2].min():.2f},{cape_org[:,2].max():.2f}]')
for s, l in cand_runs:
    cv = np.array([struct.unpack_from('<3f', d, s + k * 20 - 0) for k in range(0)])  # placeholder
    # cape vertices: try to locate a SoA f32x3 block near s
    # assume verts are NOT adjacent; use the run's own region? Instead:
    # cape skin records likely pair with a cape vertex block; search
    # backwards for plausible f32 triplets is expensive -> report later
    pass

# what is between skin end 0x388b8 and cape binds 0x5a210?
print('\nregion map 0x388b8..0x5a210: zero runs / nonzero blocks:')
z = d[0x388b8:0x5a210]
nz = np.frombuffer(z, np.uint8).reshape(-1)
blocks = []
inz = nz != 0
start = None
for i2 in range(0, len(nz), 16):
    if inz[i2:i2+16].any():
        if start is None:
            start = i2
    else:
        if start is not None and i2 - start > 32:
            blocks.append((0x388b8 + start, i2 - start))
        start = None
if start is not None:
    blocks.append((0x388b8 + start, len(nz) - start))
for off, ln in blocks[:20]:
    print(f'  nonzero block @0x{off:x} len {ln}')
print(f'  total nonzero bytes: {int(inz.sum())} of {len(nz)}')
