#!/usr/bin/env python3
"""S34 T1d: run half-cycle mirror test + FK pose battery (pelvis/foot heights,
joint limits) at several times; no bone-length test (per rules)."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

def qangle(a, b):
    a = np.array(a, float); b = np.array(b, float)
    a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    return math.degrees(2 * math.acos(min(1.0, abs(float(np.dot(a, b))))))

# run channels
T = 0x0b2818
pairs = [(u32a(T+8*k), u32a(T+8*k+4)) for k in range(156)]
base = T + 156*8 + 4
ch = {}
pos = base
for kk, (off, ln) in enumerate(pairs):
    c = kk // 2
    if kk % 2 == 0:
        n = ln // 4
        ch.setdefault(c, {})['ticks'] = [u32a(pos + 4*j) for j in range(n)]
    else:
        if ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            ch.setdefault(c, {})['quat'] = [[f32a(pos+16*i+4*cc) for cc in range(4)] for i in range(m)]
        elif ln % 12 == 0:
            ch.setdefault(c, {})['vec3'] = [[f32a(pos+12*i+4*cc) for cc in range(3)] for i in range(ln // 12)]
    pos += ln

names = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))['names']
def by_name(bare, kind):
    for c in ch:
        nm = names[c] if c < len(names) else ''
        if nm == f'{bare}-node-{kind}': return c
    return None

# half-cycle mirror: L(t) vs mirrored R(t+333ms)
HALF = 333
errs = []
for c in ch:
    if 'quat' not in ch[c] or len(ch[c]['quat']) < 4: continue
    nm = names[c] if c < len(names) else ''
    if '-node-rotation' not in nm: continue
    bare = nm.split('-node-')[0]
    if '_L_' not in bare: continue
    rc = by_name(bare.replace('_L_', '_R_'), 'rotation')
    if rc is None: continue
    tsL, ksL = ch[c]['ticks'], ch[c]['quat']
    tsR, ksR = ch[rc]['ticks'], ch[rc]['quat']
    for i, t in enumerate(tsL):
        t2 = t + HALF
        j = min(range(len(tsR)), key=lambda x: abs(tsR[x] - t2))
        if abs(tsR[j] - t2) > 60: continue
        mr = np.array(ksR[j]) * np.array([-1, -1, 1, 1])
        errs.append(qangle(ksL[i], mr))
print(f'run L/R half-cycle({HALF}ms) mirror: {len(errs)} samples, '
      f'median {np.median(errs):.2f} deg (same-index was 18.20, null 14.11)')

# ---- FK pose battery (no bone-length test) ----
# skeleton from batman.bdae (same as r23)
MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
u32m = lambda o: struct.unpack_from('<I', md, o)[0]
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
    ql = math.sqrt(sum(x*x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s): o += 4; continue
    if u32m(o + 0x34) != 1 or u32m(o + 0x38) > 32: o += 4; continue
    nodes.append(dict(name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
by_name_m = {n['name']: n for n in nodes}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = md[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
by_alias = {n['alias']: n['name'] for n in nodes if n['alias'].startswith('Bone')}
joint_nodes = [by_alias[p] for p in pal]
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11,
       11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
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
    'Bip01': None,
}
PN = {joint_nodes[b]: joint_nodes[P31[b]] for b in P31}
parent_of = dict(BIPED); parent_of.update(PN)
for i in range(47):
    parent_of.setdefault(f'Bip01_CBone{i:02d}', 'Bip01_Spine1')

def qmat_row(q):
    x, y, z, w = q
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

def sample(c, t_ms, kind):
    ts = ch[c]['ticks']; ks = ch[c][kind]
    if t_ms <= ts[0]: return ks[0]
    if t_ms >= ts[-1]: return ks[-1]
    hi = next(i for i in range(1, len(ts)) if ts[i] >= t_ms)
    lo = hi - 1
    f = (t_ms - ts[lo]) / max(1, ts[hi] - ts[lo])
    a, b = np.array(ks[lo]), np.array(ks[hi])
    if kind == 'quat':
        a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
        d = float(np.dot(a, b))
        if d < 0: b = -b
        if d > 0.9995: return a + f * (b - a)
        th = math.acos(min(1.0, abs(d)))
        s = math.sin(th)
        return math.sin((1-f)*th)/s*a + math.sin(f*th)/s*b
    return a*(1-f) + b*f

def pose(t_ms):
    worlds = {}
    def local(nm):
        n = by_name_m[nm]
        M = np.eye(4)
        c = by_name(nm, 'rotation')
        if c is not None:
            q = sample(c, t_ms, 'quat')
            M[:3, :3] = qmat_row(q)
        else:
            M[:3, :3] = qmat_row(n['q'])
        tr = np.array(n['t'], float)
        if nm == 'Bip01':
            c0 = by_name('Bip01', 'translation')
            if c0 is not None:
                tr = np.array(sample(c0, t_ms, 'vec3'), float)
        M[:3, :3] = M[:3, :3] @ np.diag(n['s'])
        M[3, :3] = tr
        return M
    def world(nm):
        if nm in worlds: return worlds[nm]
        W = local(nm) @ (world(parent_of[nm]) if parent_of.get(nm) else np.eye(4))
        worlds[nm] = W
        return W
    for nm in BIPED: world(nm)
    return worlds

# battery over the run cycle
print('\nFK battery over run (Z-up world):')
rows = []
for t in range(13899, 15601, 100):
    w = pose(t)
    pel = float(w['Bip01_Pelvis'][3, 2])
    fL = float(w['Bip01_L_Foot'][3, 2]); fR = float(w['Bip01_R_Foot'][3, 2])
    hd = float(w['Bip01_Head'][3, 2])
    rows.append((t, round(pel, 3), round(fL, 3), round(fR, 3), round(hd, 3)))
for r in rows:
    print(f'  t={r[0]}: pelvis z={r[1]}, footL z={r[2]}, footR z={r[3]}, head z={r[4]}')
pel = [r[1] for r in rows]; fL = [r[2] for r in rows]; fR = [r[3] for r in rows]
print(f'pelvis z: min {min(pel)}, max {max(pel)}, amplitude {max(pel)-min(pel):.3f} m')
print(f'footL z: min {min(fL)}, max {max(fL)}; footR: min {min(fR)}, max {max(fR)}')
print(f'feet anti-phase corr: {np.corrcoef(fL, fR)[0,1]:.2f} (expect negative)')
lo_f = sum(1 for a, b in zip(fL, fR) if (a > 0.3) != (b > 0.3))
print(f'foot-contact alternation: {lo_f}/{len(fL)} samples exactly one foot high')

# joint limits: fraction of keys with per-axis local angle < 120 deg from rest
lim_ok = lim_n = 0
worst = []
for c in ch:
    if 'quat' not in ch[c]: continue
    nm = names[c] if c < len(names) else ''
    bare = nm.split('-node-')[0]
    n = by_name_m.get(bare)
    if n is None: continue
    for k in ch[c]['quat']:
        a = qangle(k, n['q'])
        lim_n += 1
        if a < 170: lim_ok += 1
        worst.append((a, bare))
worst.sort(reverse=True)
print(f'\njoint-limit plausibility: {lim_ok}/{lim_n} keys within 170 deg of any rest '
      f'(worst: {worst[0][0]:.1f} deg at {worst[0][1]}, {worst[1][0]:.1f} at {worst[1][1]})')
