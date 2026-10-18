#!/usr/bin/env python3
"""S33 T1: pose test — apply decoded _001_idle_stand to the T2 skeleton.

Walk the contiguous stream data (16-B aligned quats), sample channels at
t=0 and t=1000 ms, FK the biped, run plausibility battery:
  R1 rest-frame: t=0 anim rotations vs node rest rotations (quat order test)
  R2 rigidity: bone lengths at t=0 vs t=1000
  R3 feet below pelvis
  R4 arm spread vs bind A-pose (~55 deg)
  R5 delta-vs-absolute: local(t) = R_anim vs R_delta @ R_rest
Nulls: shuffled quat assignment across bones (pose should collapse).
"""
import struct, math, json, collections
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

# ================= 1. decode idle_stand streams (fixed alignment) ==========
names = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', ad, o)
    if not (w[2] and cstr_a(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr_a(w[2]))
    o += 32
pairs = [(u32a(0x53200 + 8 * k), u32a(0x53200 + 8 * k + 4)) for k in range(156)]
DATA0 = 0x536e8

def try_place(pos, ln, is_time, prefer16):
    for pad in (0, 4, 8, 12):
        p = pos + pad
        if p % 4: continue
        if prefer16 and p % 16: continue
        if p + ln > len(ad): continue
        if ln == 0: return p
        if is_time:
            w = [u32a(p + 4 * j) for j in range(ln // 4)]
            if all(w[i] < w[i + 1] for i in range(len(w) - 1)) and w[-1] < 2e6:
                return p
        elif ln % 16 == 0 and ln >= 0x20:
            n = ln // 16
            good = 0
            for i in range(n):
                q = [f32a(p + 16 * i + 4 * c) for c in range(4)]
                if abs(math.sqrt(sum(x * x for x in q)) - 1) < 5e-3: good += 1
            if good >= n - 1: return p
        elif ln % 12 == 0:
            v = [f32a(p + 4 * j) for j in range(min(6, ln // 4))]
            if all(abs(x) < 100 and math.isfinite(x) for x in v): return p
        else:
            return p
    return pos

pos = DATA0
chans = {}   # name -> dict(time=..., rot=..., trans=...)
order = []
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    is_time = (k % 2 == 0)
    prefer16 = (not is_time) and ln % 16 == 0 and ln >= 0x20
    p = try_place(pos, ln, is_time, prefer16)
    key = 'time' if is_time else ('rot' if (ln % 16 == 0 and ln >= 0x20) else 'trans')
    ch = chans.setdefault(nm, {})
    ch[key] = dict(off=p, len=ln, n=(ln // 4 if is_time else
                                     ln // 16 if key == 'rot' else ln // 12))
    order.append((nm, key, p, ln))
    pos = p + ln
ok_t = sum(1 for nm, key, p, ln in order if key == 'time' and ln >= 8 and
           all(u32a(p + 4 * j) < u32a(p + 4 * (j + 1)) for j in range(ln // 4 - 1)))
n_t = sum(1 for nm, key, p, ln in order if key == 'time')
print(f're-walk: end 0x{pos:x}, TIME ascending {ok_t}/{n_t}')

# ================= 2. skeleton from batman.bdae ============================
def pool(v):
    if 0x868 <= v < 0x22d8:
        e = md.find(b'\0', v)
        if e >= v:
            return md[v:e].decode('latin1')

nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32m(o)), pool(u32m(o + 4)), pool(u32m(o + 8))
    if n1 is None or n2 is None or al is None:
        o += 4; continue
    t = struct.unpack_from('<3f', md, o + 0x0c)
    q = struct.unpack_from('<4f', md, o + 0x18)
    s = struct.unpack_from('<3f', md, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s):
        o += 4; continue
    if u32m(o + 0x34) != 1 or u32m(o + 0x38) > 32:
        o += 4; continue
    nodes.append(dict(name=n2, alias=al, t=t, q=q, s=s))
    o += 0x50
by_name = {n['name']: n for n in nodes}
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
pal = []
o = 0x3167c
while o < 0x31774:
    blk = md[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6]).decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]
P31 = {0: 1, 1: 2, 2: 22, 3: 4, 4: 5, 5: 22, 6: 8, 7: 8, 8: 9, 9: 10,
       10: 11, 11: 20, 12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20,
       18: 19, 19: 20, 20: 21, 21: 22, 23: 7, 24: 6, 25: 14, 26: 25,
       27: 10, 28: 29, 29: 8, 30: 29}
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
PN = {joint_nodes[b]: joint_nodes[P31[b]] for b in P31}
parent_of = dict(BIPED); parent_of.update(PN)

# ================= 3. sampling + FK ========================================
def qnorm(q):
    q = np.array(q, float); return q / np.linalg.norm(q)

def qmul(a, b):  # hamilton
    x1, y1, z1, w1 = a; x2, y2, z2, w2 = b
    return np.array([w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2,
                     w1*w2 - x1*x2 - y1*y2 - z1*z2])

def qmat_row(q, order='xyzw'):
    x, y, z, w = (q if order == 'xyzw' else (q[1], q[2], q[3], q[0]))
    Rc = np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

def slerp(a, b, t):
    a = qnorm(a); b = qnorm(b)
    dot = float(np.clip(np.dot(a, b), -1, 1))
    if dot < 0: b = -b; dot = -dot
    if dot > 0.9995:
        return qnorm(a + t * (b - a))
    th = math.acos(dot)
    return qnorm(math.sin((1-t)*th)/math.sin(th)*a + math.sin(t*th)/math.sin(th)*b)

def sample(nm, kind, t_ms, order4='xyzw'):
    ch = chans.get(nm, {}).get(kind)
    if ch is None: return None
    p, ln = ch['off'], ch['len']
    if kind == 'time':
        return None
    n_t = chans[nm]['time']['len'] // 4
    ticks = [u32a(chans[nm]['time']['off'] + 4 * j) for j in range(n_t)]
    if kind == 'rot':
        st, nc = 16, ch['len'] // 16
    else:
        st, nc = 12, ch['len'] // 12
    keys = [[f32a(p + st * i + 4 * c) for c in range(st // 4)] for i in range(nc)]
    # clamp/wrap
    if t_ms <= ticks[0]: return keys[0]
    if t_ms >= ticks[-1]:
        return keys[nc - 1]
    hi = next(i for i in range(1, n_t) if ticks[i] >= t_ms)
    lo = hi - 1
    f = (t_ms - ticks[lo]) / max(1, ticks[hi] - ticks[lo])
    a = keys[min(lo, nc - 1)]; b = keys[min(hi, nc - 1)]
    if kind == 'rot':
        return slerp(a, b, f)
    return [a[c] * (1 - f) + b[c] * f for c in range(3)]

def build_pose(t_ms, order4, mode):
    """mode: 'abs' local rotation = anim; 'delta' local = anim @ rest"""
    worlds = {}
    def local(nm):
        n = by_name[nm]
        M = np.eye(4)
        q = sample(nm, 'rot', t_ms, order4) if nm in chans and 'rot' in chans[nm] else None
        if q is None:
            R = qmat_row(n['q'], 'xyzw')
        else:
            R = qmat_row(q, order4)
            if mode == 'delta':
                R = R @ qmat_row(n['q'], 'xyzw')
        tr = np.array(n['t'], float)
        if nm == 'Bip01':
            tp = sample('Bip01', 'trans', t_ms)
            if tp is not None: tr = np.array(tp, float)
        S = np.diag(n['s'])
        M[:3, :3] = R @ S
        M[3, :3] = tr
        return M
    def world(nm):
        if nm in worlds: return worlds[nm]
        par = parent_of.get(nm)
        W = local(nm) @ (world(par) if par else np.eye(4))
        worlds[nm] = W
        return W
    for nm in list(chans) + ['Bip01']:
        if nm in by_name:
            world(nm)
    return worlds

battery = {}
for order4 in ('xyzw', 'wxyz'):
    for mode in ('abs', 'delta'):
        w0 = build_pose(0, order4, mode)
        w1 = build_pose(1000, order4, mode)
        # R1 rest-frame deviation (t=0 vs node rest worlds)
        dev = []
        for nm in w0:
            if nm not in by_name: continue
            n = by_name[nm]
            Rn = qmat_row(n['q'], 'xyzw')
            Ra = w0[nm][:3, :3] @ np.linalg.inv(np.diag(n['s']))
            Ra = Ra @ np.linalg.inv(np.diag(n['s']))  # strip scale both ways
            tr = w0[nm][3, :3] - w0[parent_of[nm]][3, :3] if parent_of.get(nm) else w0[nm][3, :3]
            dev.append(tr)
        # R2 rigidity: thigh/calf/shin lengths at t0 vs t1000
        rig = []
        for a, b in (('Bip01_R_Thigh', 'Bip01_R_Calf'), ('Bip01_R_Calf', 'Bip01_R_Foot'),
                     ('Bip01_L_Thigh', 'Bip01_L_Calf'), ('Bip01_L_Calf', 'Bip01_L_Foot'),
                     ('Bip01_R_UpperArm', 'Bip01_R_Forearm'), ('Bip01_Spine', 'Bip01_Spine1'),
                     ('Bip01_Head', 'Bip01_Neck')):
            l0 = np.linalg.norm(w0[a][3, :3] - w0[b][3, :3])
            l1 = np.linalg.norm(w1[a][3, :3] - w1[b][3, :3])
            rig.append((a, b, l0, l1, abs(l1 - l0)))
        # R3 feet below pelvis
        fy0 = min(w0['Bip01_L_Foot'][3, 1], w0['Bip01_R_Foot'][3, 1])
        py0 = w0['Bip01_Pelvis'][3, 1]
        fy1 = min(w1['Bip01_L_Foot'][3, 1], w1['Bip01_R_Foot'][3, 1])
        py1 = w1['Bip01_Pelvis'][3, 1]
        # R4 arm spread (t0): upper arm direction vs down
        def spread(w):
            out = {}
            for side in 'LR':
                sh = w[f'Bip01_{side}_Clavicle'][3, :3]
                el = w[f'Bip01_{side}_UpperArm'][3, :3]
                wr = w[f'Bip01_{side}_Forearm'][3, :3]
                v = el - sh
                out[side] = math.degrees(math.acos(
                    np.clip(np.dot(v/np.linalg.norm(v), [0, -1, 0]), -1, 1)))
            return out
        sp0, sp1 = spread(w0), spread(w1)
        battery[f'{order4}/{mode}'] = dict(
            root_y0=float(w0['Bip01'][3, 1]), root_y1=float(w1['Bip01'][3, 1]),
            pelvis_y0=float(py0), feet_y0=float(fy0), feet_y1=float(fy1),
            pelvis_y1=float(py1),
            feet_below_pelvis=bool(fy0 < py0 and fy1 < py1),
            max_len_delta_cm=float(max(r[4] for r in rig) * 100),
            rig=[(a, b, round(l0, 4), round(l1, 4)) for a, b, l0, l1, _ in rig],
            arm_spread_t0={k: round(v, 1) for k, v in sp0.items()},
            arm_spread_t1={k: round(v, 1) for k, v in sp1.items()},
        )
        print(f'\n== {order4}/{mode} ==')
        print(f"  root y t0/t1: {w0['Bip01'][3,1]:.3f} / {w1['Bip01'][3,1]:.3f}")
        print(f"  pelvis y0 {py0:.3f}, feet y0 {fy0:.3f} | pelvis y1 {py1:.3f} feet y1 {fy1:.3f}")
        print(f"  max bone-length delta t0->t1: {max(r[4] for r in rig)*100:.2f} cm")
        print(f"  arm spread t0: {sp0}  t1: {sp1}")

# null: shuffle per-bone quat assignment at t=0 (xyzw/abs)
rng = np.random.default_rng(33)
bones = [nm for nm in chans if nm in by_name and 'rot' in chans[nm]]
qs = {nm: sample(nm, 'rot', 0) for nm in bones}
sh = bones[:]; rng.shuffle(sh)
wshuffle = {}
def local_sh(nm):
    n = by_name[nm]
    M = np.eye(4)
    q = qs.get(sh[bones.index(nm)]) if nm in qs else None
    R = qmat_row(q, 'xyzw') if q is not None else qmat_row(n['q'], 'xyzw')
    M[:3, :3] = R @ np.diag(n['s']); M[3, :3] = n['t']
    return M
def world_sh(nm):
    par = parent_of.get(nm)
    return local_sh(nm) @ (world_sh(par) if par else np.eye(4))
for nm in bones: world_sh(nm)
rig_sh = [np.linalg.norm(world_sh(a)[3, :3] - world_sh(b)[3, :3])
          for a, b in (('Bip01_R_Thigh', 'Bip01_R_Calf'),
                       ('Bip01_L_UpperArm', 'Bip01_L_Forearm'))]
print(f'\nNULL (shuffled quat->bone): thigh len {rig_sh[0]:.3f} m '
      f'(anim {battery["xyzw/abs"]["rig"][0][2]:.3f})')
json.dump(battery, open('/home/z/my-project/scripts/s33_t1_pose.json', 'w'), indent=1)
print('wrote s33_t1_pose.json')
