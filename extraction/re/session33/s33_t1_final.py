#!/usr/bin/env python3
"""S33 T1 FINAL: decode idle_stand, oracle-select alignment/order/mode via
rest-frame match, run plausibility battery + nulls, sample t=0/t=1000."""
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

def ticks_asc(p, n):
    w = [u32a(p + 4 * j) for j in range(n)]
    return all(w[i] < w[i + 1] for i in range(n - 1)) and w[-1] < 2_000_000

# ---- placement pass ----
pos = 0x536e4
placed = []   # (name, track, off, len, n)
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    bare = nm.split('-node-')[0]
    track = nm.split('-node-')[1] if '-node-' in nm else '?'
    is_time = (k % 2 == 0)
    if is_time:
        track = '@time'
    if ln == 0:
        placed.append((nm, track, None, 0, 0)); continue
    n_iter = ln // 4 if is_time else (ln // 16 if (ln % 16 == 0 and ln >= 0x20)
                                      else ln // 12)
    found = None
    if is_time:
        for pad in range(0, 40, 4):
            p = pos + pad
            if p + ln <= len(ad) and ticks_asc(p, n_iter):
                found = p; break
    else:
        if ln % 16 == 0 and ln >= 0x20:
            for pad in (0, 4):        # quats: only two candidates
                p = pos + pad
                if p + ln <= len(ad): found = p; break
        elif ln % 12 == 0:
            found = pos
    if found is None: found = pos
    placed.append((nm, track, found, ln, n_iter))
    pos = found + ln
chans = {}
for nm, track, p, ln, n in placed:
    if p is None: continue
    key = 'time' if track == '@time' else track
    chans.setdefault(nm.split('-node-')[0], {})[key] = dict(off=p, len=ln, n=n)
nbones = sum(1 for nm in chans if nm.startswith('Bip01'))
print(f'placed {len(placed)}/156; animated Bip01 bones {nbones}; end 0x{pos:x}')

# ---- skeleton ----
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
for i in range(47):
    parent_of.setdefault(f'Bip01_CBone{i:02d}', 'Bip01_Spine1')

def qnorm(q):
    q = np.array(q, float); return q / (np.linalg.norm(q) or 1)

def qangle(a, b):
    a = qnorm(a); b = qnorm(b)
    dot = abs(float(np.dot(a, b)))
    return math.degrees(2 * math.acos(min(1.0, dot)))

def qmat_row(q):
    x, y, z, w = q
    Rc = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                   [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                   [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return Rc.T

def keys_of(nm, track):
    ch = chans[nm][track]
    st = 16 if track == 'rotation' else 12
    p = ch['off']
    return [[f32a(p + st * i + 4 * c) for c in range(st // 4)] for i in range(ch['n'])]

ticks_cache = {}
def ticks_of(nm):
    if nm not in ticks_cache:
        ch = chans[nm]['time']
        ticks_cache[nm] = [u32a(ch['off'] + 4 * j) for j in range(ch['n'])]
    return ticks_cache[nm]

# ---- oracle: rest-frame rotation error per (shift, order, mode) ----
anim_bones = [nm for nm in chans if nm in by_name and 'rotation' in chans[nm]
              and 'time' in chans[nm]]
print(f'anim bones with time+rot: {len(anim_bones)}')
results = {}
for shift in (0, 4):
    for order in ('xyzw', 'wxyz'):
        errs = []
        for nm in anim_bones:
            n = by_name[nm]
            ks = keys_of(nm, 'rotation')
            def comp(q):
                return q if order == 'xyzw' else [q[1], q[2], q[3], q[0]]
            q0 = comp(ks[0])
            if shift:
                # shifted reading: key i components rotate by one
                ks2 = [[k[1], k[2], k[3], k[0]] for k in ks]
                q0 = comp(ks2[0])
            if order == 'wxyz':
                q0 = comp(ks[0])
            # abs mode: local(t=0) = anim; delta: anim @ rest
            for mode in ('abs', 'delta'):
                pass
            qrest = n['q']
            e_abs = qangle(q0, qrest)
            # delta: anim @ rest — angle of the product vs identity
            x0, y0, z0, w0 = q0 if order == 'xyzw' else (q0[1], q0[2], q0[3], q0[0])
            xr, yr, zr, wr = qrest
            # hamilton q0*qrest
            qw_ = w0*wr - x0*xr - y0*yr - z0*zr
            e_delta = math.degrees(2 * math.acos(min(1.0, abs(qw_))))
            errs.append((nm, e_abs, e_delta))
        med_abs = float(np.median([e[1] for e in errs]))
        med_dlt = float(np.median([e[2] for e in errs]))
        results[(shift, order)] = (med_abs, med_dlt, errs)
        print(f'shift={shift} order={order}: median |abs| {med_abs:6.2f} deg, '
              f'median delta {med_dlt:6.2f} deg')
best = min(results, key=lambda k: min(results[k][:2]))
med_abs, med_dlt, errs = results[best]
mode = 'abs' if med_abs <= med_dlt else 'delta'
med = min(med_abs, med_dlt)
print(f'BEST: shift={best[0]} order={best[1]} mode={mode} median {med:.2f} deg')
worst = sorted(errs, key=lambda e: -(e[1] if mode == 'abs' else e[2]))[:6]
print('worst rest-frame bones:',
      [(e[0].replace('Bip01_', ''), round(e[1] if mode == 'abs' else e[2], 1))
       for e in worst])

# ---- final battery with winning combo ----
shift, order = best
def sample(nm, track, t_ms):
    ch = chans[nm][track]
    ticks = ticks_of(nm)
    ks = keys_of(nm, track)
    if shift and track == 'rotation':
        ks = [[k[1], k[2], k[3], k[0]] for k in ks]
    if track == 'rotation' and order == 'wxyz':
        ks = [[k[1], k[2], k[3], k[0]] for k in ks]
    if t_ms <= ticks[0]: return ks[0]
    if t_ms >= ticks[-1]: return ks[ch['n'] - 1]
    hi = next(i for i in range(1, len(ticks)) if ticks[i] >= t_ms)
    lo = hi - 1
    f = (t_ms - ticks[lo]) / max(1, ticks[hi] - ticks[lo])
    a = ks[min(lo, ch['n'] - 1)]; b = ks[min(hi, ch['n'] - 1)]
    if track == 'rotation':
        a = qnorm(a); b = qnorm(b)
        dot = float(np.dot(a, b))
        if dot < 0: b = -b
        if dot > 0.9995: return list(qnorm(a + f * (b - a)))
        th = math.acos(min(1.0, abs(dot)))
        s = math.sin(th)
        return list(math.sin((1-f)*th)/s*a + math.sin(f*th)/s*b)
    return [a[c]*(1-f) + b[c]*f for c in range(3)]

def build_pose(t_ms):
    worlds = {}
    def local(nm):
        n = by_name[nm]
        M = np.eye(4)
        if nm in chans and 'rotation' in chans[nm]:
            q = sample(nm, 'rotation', t_ms)
            R = qmat_row(q if order == 'xyzw' else (q[1], q[2], q[3], q[0]))
            if mode == 'delta':
                R = R @ qmat_row(n['q'])
        else:
            R = qmat_row(n['q'])
        tr = np.array(n['t'], float)
        if nm == 'Bip01' and 'translation' in chans.get('Bip01', {}):
            tp = sample('Bip01', 'translation', t_ms)
            if tp is not None: tr = np.array(tp, float)
        M[:3, :3] = R @ np.diag(n['s'])
        M[3, :3] = tr
        return M
    def world(nm):
        if nm in worlds: return worlds[nm]
        W = local(nm) @ (world(parent_of[nm]) if parent_of.get(nm) else np.eye(4))
        worlds[nm] = W
        return W
    for nm in BIPED: world(nm)
    return worlds

w0 = build_pose(0); w1 = build_pose(1000); w2 = build_pose(2000)
def spread(w):
    out = {}
    for side in 'LR':
        sh = w[f'Bip01_{side}_Clavicle'][3, :3]
        el = w[f'Bip01_{side}_UpperArm'][3, :3]
        v = el - sh
        out[side] = round(math.degrees(math.acos(
            np.clip(np.dot(v/np.linalg.norm(v), [0, -1, 0]), -1, 1))), 1)
    return out
rig = []
for a, b in (('Bip01_R_Thigh', 'Bip01_R_Calf'), ('Bip01_R_Calf', 'Bip01_R_Foot'),
             ('Bip01_L_Thigh', 'Bip01_L_Calf'), ('Bip01_L_Calf', 'Bip01_L_Foot'),
             ('Bip01_R_UpperArm', 'Bip01_R_Forearm'), ('Bip01_Spine', 'Bip01_Spine1'),
             ('Bip01_Neck', 'Bip01_Head')):
    ls = [round(float(np.linalg.norm(w[a][3, :3] - w[b][3, :3])), 4)
          for w in (w0, w1, w2)]
    rig.append((a.split('_', 1)[1], ls))
out = dict(
    combo=dict(shift=shift, quat_order=order, mode=mode,
               rest_median_deg=round(med, 2)),
    root_y=[round(float(w['Bip01'][3, 1]), 3) for w in (w0, w1, w2)],
    pelvis_y=[round(float(w['Bip01_Pelvis'][3, 1]), 3) for w in (w0, w1, w2)],
    foot_y=[round(float(min(w['Bip01_L_Foot'][3, 1], w['Bip01_R_Foot'][3, 1])), 3)
            for w in (w0, w1, w2)],
    arm_spread=[spread(w) for w in (w0, w1, w2)],
    rigidity=rig,
    head=[round(float(w['Bip01_Head'][3, 2]), 3) for w in (w0, w1, w2)],
    rhand=[[round(float(x), 3) for x in w['Bip01_R_Hand'][3, :3]]
           for w in (w0, w1, w2)],
)
print('\n=== BATTERY ===')
for k, v in out.items():
    print(f'  {k}: {v}')
json.dump(out, open('/home/z/my-project/scripts/s33_t1_pose_final.json', 'w'), indent=1)
print('wrote s33_t1_pose_final.json')

# ---- NULL: shuffled quat->bone assignment (rest frame should collapse) ----
rng = np.random.default_rng(34)
bones2 = [nm for nm in anim_bones if nm != 'Bip01']
qs0 = {}
for nm in bones2:
    ks = keys_of(nm, 'rotation')
    qs0[nm] = ks[0]
sh = bones2[:]; rng.shuffle(sh)
errs_null = []
for nm in bones2:
    n = by_name[nm]
    q = qs0[sh[bones2.index(nm)]]
    errs_null.append(qangle(q, n['q']))
med_null = float(np.median(errs_null))
print(f'\nNULL shuffled mapping: rest-frame median {med_null:.2f} deg '
      f'(real {med:.2f} deg, {len(bones2)} bones)')
out['null_shuffled_rest_median_deg'] = round(med_null, 2)
json.dump(out, open('/home/z/my-project/scripts/s33_t1_pose_final.json', 'w'), indent=1)
