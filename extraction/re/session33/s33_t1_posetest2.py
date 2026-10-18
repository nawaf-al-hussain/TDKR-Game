#!/usr/bin/env python3
"""S33 T1 final: robust stream walk + full pose test for _001_idle_stand."""
import struct, math, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
MD = '/tmp/my-project/work/data/batman.bdae'
ad = open(AD, 'rb').read()
md = open(MD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
u32m = lambda o: struct.unpack_from('<I', md, o)[0]

def cstr_a(v):
    if 0 < v < len(ad):
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: pass

names = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', ad, o)
    if not (w[2] and cstr_a(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr_a(w[2]))
    o += 32
pairs = [(u32a(0x53200 + 8 * k), u32a(0x53200 + 8 * k + 4)) for k in range(156)]

def ticks_ok(p, n):
    w = [u32a(p + 4 * j) for j in range(n)]
    return all(w[i] < w[i + 1] for i in range(n - 1)) and w[-1] < 2_000_000

def quats_ok(p, n, tol=8):
    good = 0
    for i in range(n):
        q = [f32a(p + 16 * i + 4 * c) for c in range(4)]
        s = sum(x * x for x in q)
        if math.isfinite(s) and abs(math.sqrt(s) - 1) < 5e-3: good += 1
    return good >= n - tol

def vecs_ok(p, n):
    for i in range(n * 3):
        x = f32a(p + 4 * i)
        if not (math.isfinite(x) and abs(x) < 100): return False
    return True

# robust walk
pos = 0x536e8
chans = {}     # bare bone name -> {time:(off,n), rot/trans:(off,n,stride)}
report = []
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    bare = nm.split('-node-')[0]
    track = nm.split('-node-')[1] if '-node-' in nm else '?'
    is_time = (k % 2 == 0)
    placed = None
    for pad in range(0, 68, 4):
        p = pos + pad
        if p + ln > len(ad): continue
        if ln == 0: placed = p; break
        if is_time:
            if ln >= 8 and ticks_ok(p, min(ln // 4, 8)) and ticks_ok(p, ln // 4):
                placed = p; break
        else:
            if ln % 16 == 0 and ln >= 0x20:
                if quats_ok(p, min(ln // 16, 6)): placed = p; break
            elif ln % 12 == 0 and ln >= 0x18:
                if vecs_ok(p, min(ln // 12, 3)): placed = p; break
            else:
                placed = p; break
    if placed is None:
        report.append((nm, 'UNPLACED', pos, ln))
        placed = pos
    key = 'time' if is_time else track
    ent = chans.setdefault(bare, {})
    ent[key] = dict(off=placed, len=ln,
                    n=ln // 4 if is_time else (ln // 16 if track == 'rotation' and ln % 16 == 0 else ln // 12))
    report.append((nm, 'T' if is_time else 'V', placed, ln))
    pos = placed + ln
print(f'walk end 0x{pos:x}')
unplaced = [r for r in report if r[1] == 'UNPLACED']
print(f'unplaced: {len(unplaced)}')
n_anim = sum(1 for nm in chans if nm.startswith('Bip01') and
             ('rot' in chans[nm] or 'trans' in chans[nm]))
print(f'animated bare bones: {n_anim}')
for nm in ('Bip01', 'Bip01_Pelvis', 'Bip01_R_Thigh', 'Bip01_R_Calf', 'Bip01_R_Foot',
           'Bip01_L_UpperArm', 'Bip01_Spine1', 'Bip01_Head'):
    if nm in chans:
        print(f'  {nm}:', {k: (hex(v["off"]), v["n"]) for k, v in chans[nm].items()})

# ---- tick spans of body channels ----
print('\ntick spans:')
for nm in ('Bip01', 'Bip01_Pelvis', 'Bip01_Spine', 'Bip01_Neck', 'Bip01_Head',
           'Bip01_L_Thigh', 'Bip01_R_Thigh', 'Bip01_L_UpperArm', 'Bip01_R_UpperArm'):
    if nm in chans and 'time' in chans[nm]:
        p, n = chans[nm]['time']['off'], chans[nm]['time']['n']
        print(f'  {nm}: [{u32a(p)}..{u32a(p + 4 * n - 4)}] n={n}')

# ================= skeleton =================
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
    nodes.append(dict(name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
by_name = {n['name']: n for n in nodes}
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
    'Bip01': None,
}
PN = {joint_nodes[b]: joint_nodes[P31[b]] for b in P31}
parent_of = dict(BIPED); parent_of.update(PN)
# CBone parents: attach to Spine1 (cape anchor); fine for plausibility tests
for i in range(47):
    nm = f'Bip01_CBone{i:02d}'
    if nm not in parent_of: parent_of[nm] = 'Bip01_Spine1'

def qnorm(q):
    q = np.array(q, float); return q / np.linalg.norm(q)

def slerp(a, b, t):
    a = qnorm(a); b = qnorm(b)
    dot = float(np.clip(np.dot(a, b), -1, 1))
    if dot < 0: b, dot = -b, -dot
    if dot > 0.9995: return qnorm(a + t * (b - a))
    th = math.acos(dot)
    return qnorm(math.sin((1-t)*th)/math.sin(th)*a + math.sin(t*th)/math.sin(th)*b)

def qmat_row(q):
    x, y, z, w = q
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

def sample(nm, kind, t_ms):
    ch = chans.get(nm, {}).get(kind)
    if ch is None: return None
    ticks = [u32a(chans[nm]['time']['off'] + 4 * j) for j in range(chans[nm]['time']['n'])]
    st = 16 if kind == 'rot' else 12
    nc = ch['n']
    p = ch['off']
    keys = [[f32a(p + st * i + 4 * c) for c in range(st // 4)] for i in range(nc)]
    if t_ms <= ticks[0]: return keys[0]
    if t_ms >= ticks[-1]: return keys[nc - 1]
    hi = next(i for i in range(1, len(ticks)) if ticks[i] >= t_ms)
    lo = hi - 1
    f = (t_ms - ticks[lo]) / max(1, ticks[hi] - ticks[lo])
    a = keys[min(lo, nc - 1)]; b = keys[min(hi, nc - 1)]
    return slerp(a, b, f) if kind == 'rot' else [a[c]*(1-f) + b[c]*f for c in range(3)]

def build_pose(t_ms, mode='abs'):
    worlds = {}
    def local(nm):
        n = by_name[nm]
        M = np.eye(4)
        q = sample(nm, 'rot', t_ms)
        R = qmat_row(q) if q is not None else qmat_row(n['q'])
        if mode == 'delta' and q is not None:
            R = R @ qmat_row(n['q'])
        tr = np.array(n['t'], float)
        if nm == 'Bip01':
            tp = sample('Bip01', 'trans', t_ms)
            if tp is not None: tr = np.array(tp, float)
        M[:3, :3] = R @ np.diag(n['s'])
        M[3, :3] = tr
        return M
    def world(nm):
        if nm in worlds: return worlds[nm]
        W = local(nm) @ (world(parent_of[nm]) if parent_of.get(nm) else np.eye(4))
        worlds[nm] = W
        return W
    for nm in BIPED:
        world(nm)
    return worlds

battery = {}
for mode in ('abs', 'delta'):
    w0 = build_pose(0, mode)
    w1 = build_pose(1000, mode)
    rig = []
    for a, b in (('Bip01_R_Thigh', 'Bip01_R_Calf'), ('Bip01_R_Calf', 'Bip01_R_Foot'),
                 ('Bip01_L_Thigh', 'Bip01_L_Calf'), ('Bip01_L_Calf', 'Bip01_L_Foot'),
                 ('Bip01_R_UpperArm', 'Bip01_R_Forearm'), ('Bip01_Spine', 'Bip01_Spine1'),
                 ('Bip01_Neck', 'Bip01_Head')):
        l0 = np.linalg.norm(w0[a][3, :3] - w0[b][3, :3])
        l1 = np.linalg.norm(w1[a][3, :3] - w1[b][3, :3])
        rig.append((a.split('_')[-1] + '/' + b.split('_')[-1], round(l0, 4), round(l1, 4)))
    def spread(w):
        out = {}
        for side in 'LR':
            sh = w[f'Bip01_{side}_Clavicle'][3, :3]
            el = w[f'Bip01_{side}_UpperArm'][3, :3]
            v = el - sh
            out[side] = round(math.degrees(math.acos(
                np.clip(np.dot(v/np.linalg.norm(v), [0, -1, 0]), -1, 1))), 1)
        return out
    battery[mode] = dict(
        root_y0=round(float(w0['Bip01'][3, 1]), 3),
        root_y1=round(float(w1['Bip01'][3, 1]), 3),
        pelvis_y0=round(float(w0['Bip01_Pelvis'][3, 1]), 3),
        foot_y0=round(float(min(w0['Bip01_L_Foot'][3, 1], w0['Bip01_R_Foot'][3, 1])), 3),
        foot_y1=round(float(min(w1['Bip01_L_Foot'][3, 1], w1['Bip01_R_Foot'][3, 1])), 3),
        feet_below_pelvis=bool(min(w0['Bip01_L_Foot'][3, 1], w0['Bip01_R_Foot'][3, 1])
                               < w0['Bip01_Pelvis'][3, 1]),
        rig=rig,
        max_len_delta_cm=round(max(abs(l1 - l0) for _, l0, l1 in rig) * 100, 2),
        arm_spread_t0=spread(w0), arm_spread_t1=spread(w1),
        head_z=round(float(w0['Bip01_Head'][3, 2]), 3),
        hand0=[round(float(x), 3) for x in w0['Bip01_R_Hand'][3, :3]],
        hand1=[round(float(x), 3) for x in w1['Bip01_R_Hand'][3, :3]],
    )
    print(f'\n== mode {mode} ==')
    for k, v in battery[mode].items():
        print(f'  {k}: {v}')

# null: shuffled quat->bone
rng = np.random.default_rng(33)
bones = [nm for nm in chans if nm in by_name and 'rot' in chans[nm]]
qs = {nm: sample(nm, 'rot', 0) for nm in bones}
sh = bones[:]; rng.shuffle(sh)
wsh = {}
def local_sh(nm):
    n = by_name[nm]
    q = qs[sh[bones.index(nm)]] if nm in bones else None
    R = qmat_row(q) if q is not None else qmat_row(n['q'])
    M = np.eye(4); M[:3, :3] = R @ np.diag(n['s']); M[3, :3] = n['t']
    return M
def world_sh(nm):
    if nm in wsh: return wsh[nm]
    W = local_sh(nm) @ (world_sh(parent_of[nm]) if parent_of.get(nm) else np.eye(4))
    wsh[nm] = W
    return W
for nm in bones: world_sh(nm)
try:
    l_sh = np.linalg.norm(wsh['Bip01_R_Thigh'][3, :3] - wsh['Bip01_R_Calf'][3, :3])
    print(f'\nNULL shuffled: R thigh len {l_sh:.3f} m (anim '
          f'{battery["abs"]["rig"][0][1]:.3f}, rest '
          f'{np.linalg.norm(by_name["Bip01_R_Thigh"]["t"]):.3f} local)')
except KeyError:
    print('\nNULL shuffled: (chain broken as expected)')
json.dump(battery, open('/home/z/my-project/scripts/s33_t1_pose.json', 'w'), indent=1)
print('wrote s33_t1_pose.json')
