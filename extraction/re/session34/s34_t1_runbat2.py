#!/usr/bin/env python3
"""S34 T1b: run channel semantics check + validation battery with nulls."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

T = 0x0b2818
pairs = [(u32a(T+8*k), u32a(T+8*k+4)) for k in range(156)]
base = T + 156*8 + 4
ch = {}
pos = base
for kk, (off, ln) in enumerate(pairs):
    is_time = (kk % 2 == 0)
    c = kk // 2
    if is_time:
        n = ln // 4
        ch.setdefault(c, {})['ticks'] = [u32a(pos + 4*j) for j in range(n)]
    else:
        if ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            ch.setdefault(c, {})['quat'] = [[f32a(pos+16*i+4*cc) for cc in range(4)] for i in range(m)]
        elif ln % 12 == 0:
            m = ln // 12
            ch.setdefault(c, {})['vec3'] = [[f32a(pos+12*i+4*cc) for cc in range(3)] for i in range(m)]
    pos += ln

# channel census
mism = [(c, len(ch[c]['ticks']), len(ch[c].get('quat', ch[c].get('vec3', []))))
        for c in ch if len(ch[c]['ticks']) != len(ch[c].get('quat', ch[c].get('vec3', [])))]
print('mismatched channels:', mism)

# ch0 = root translation? print range per axis
v0 = np.array(ch[0]['vec3'])
print('ch0 vec3 (root?): first', v0[0], 'last', v0[-1])
print('  min', v0.min(0), 'max', v0.max(0))
print('  y range', v0[:,1].min(), v0[:,1].max())

# which channels are vec3
vecc = [c for c in ch if 'vec3' in ch[c]]
print('vec3 channels:', vecc)

# loop wrap: quat channel first vs last key angle
def qangle(a, b):
    a = np.array(a); b = np.array(b)
    a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    d = abs(float(np.dot(a, b)))
    return math.degrees(2*math.acos(min(1.0, d)))

qc = [c for c in ch if 'quat' in ch[c] and len(ch[c]['quat']) > 2]
wrap_errs = [qangle(ch[c]['quat'][0], ch[c]['quat'][-1]) for c in qc]
print(f'\nloop wrap first-vs-last key: median {np.median(wrap_errs):.2f} deg, '
      f'max {max(wrap_errs):.2f}, <5deg: {sum(1 for e in wrap_errs if e < 5)}/{len(wrap_errs)}')
# NULL: random pairs
rng = np.random.default_rng(7)
null_errs = []
for _ in range(2000):
    c = qc[rng.integers(len(qc))]
    i, j = rng.integers(len(ch[c]['quat']), size=2)
    null_errs.append(qangle(ch[c]['quat'][i], ch[c]['quat'][j]))
print(f'NULL random key pairs: median {np.median(null_errs):.2f} deg '
      f'(real first-last {np.median(wrap_errs):.2f})')

# temporal smoothness: angular velocity between consecutive keys vs shuffled
vel = []
for c in qc:
    ks = ch[c]['quat']; ts = ch[c]['ticks']
    for i in range(len(ks)-1):
        dt = max(1, ts[i+1]-ts[i])
        vel.append(qangle(ks[i], ks[i+1]) / dt * 1000)
vel = np.array(vel)
print(f'\nangular velocity: median {np.median(vel):.1f} deg/s, p95 {np.percentile(vel,95):.1f}, '
      f'max {vel.max():.1f}')
sh = []
for c in qc:
    ks = ch[c]['quat']; ts = ch[c]['ticks']
    idx = list(range(len(ks))); rng.shuffle(idx)
    for i in range(len(ks)-1):
        dt = max(1, ts[i+1]-ts[i])
        sh.append(qangle(ks[idx[i]], ks[idx[i+1]]) / dt * 1000)
sh = np.array(sh)
print(f'NULL shuffled-key velocity: median {np.median(sh):.1f} deg/s, '
      f'p95 {np.percentile(sh,95):.1f} (real p95 {np.percentile(vel,95):.1f}, '
      f'ratio {np.percentile(sh,95)/max(1e-9,np.percentile(vel,95)):.1f}x)')

# L/R symmetry: mirror channel pairs (L_*/R_* by idle name order)
names = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))['names']
def cname(c): return names[c] if c < len(names) else f'?{c}'
sym_errs = []
pairs_lr = []
for c in qc:
    nm = cname(c)
    if '-node-rotation' not in nm: continue
    bare = nm.split('-node-')[0]
    if '_L_' in bare:
        mir = bare.replace('_L_', '_R_')
        rc = next((c2 for c2 in qc if cname(c2).startswith(mir + '-node-')), None)
        if rc: pairs_lr.append((c, rc))
for c, rc in pairs_lr:
    kL = np.array(ch[c]['quat']); kR = np.array(ch[rc]['quat'])
    n = min(len(kL), len(kR))
    if not n: continue
    mir = kR[:n] * np.array([-1, -1, 1, 1])   # biped mirror conjugation (-x,-y,z,w) on xyzw
    errs = [qangle(kL[i], mir[i]) for i in range(n)]
    sym_errs.append(np.median(errs))
print(f'\nL/R mirror symmetry ({len(sym_errs)} pairs): median {np.median(sym_errs):.2f} deg, '
      f'<10deg {sum(1 for e in sym_errs if e < 10)}/{len(sym_errs)}')
rng2 = np.random.default_rng(8)
nul2 = []
for _ in range(500):
    c, rc = pairs_lr[rng2.integers(len(pairs_lr))]
    kL = np.array(ch[c]['quat']); kR = np.array(ch[rc]['quat'])
    n = min(len(kL), len(kR))
    s = rng2.integers(n)
    nul2.append(qangle(kL[s], kR[s] * np.array([-1, -1, 1, 1])))
print(f'NULL unpaired L-R at same index: median {np.median(nul2):.2f} deg')

json.dump(dict(wrap_median=float(np.median(wrap_errs)),
               wrap_lt5=sum(1 for e in wrap_errs if e < 5), nq=len(wrap_errs),
               vel_p95=float(np.percentile(vel, 95)),
               null_vel_p95=float(np.percentile(sh, 95)),
               sym_median=float(np.median(sym_errs)), npairs=len(sym_errs),
               null_sym=float(np.median(nul2))),
          open('/home/z/my-project/scripts/s34_t1_runbattery.json', 'w'))
print('\nwrote s34_t1_runbattery.json')
