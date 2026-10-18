#!/usr/bin/env python3
"""S34 T1c: (a) idle mirror-symmetry control, (b) sliding-window loop-wrap
scan over run segment to locate the 666-ms clip subrange (with null)."""
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

def load_seg(table, nent=None):
    if nent is None:
        nent = 0
        while nent < 200:
            off, ln = u32a(table + 8*nent), u32a(table + 8*nent + 4)
            if ln == 0 or ln > 0x4000 or off > 0x20000 or ln % 4: break
            nent += 1
    pairs = [(u32a(table+8*k), u32a(table+8*k+4)) for k in range(nent)]
    ch = {}
    pos = None
    for extra in (0, 4, 8, 12):
        base = table + nent*8 + extra
        p = base; ok = 0
        for kk, (off, ln) in enumerate(pairs):
            if ln == 0: continue
            if kk % 2 == 0:
                n = ln // 4
                w = [u32a(p + 4*j) for j in range(n)]
                if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2e6: break
            else:
                if ln % 16 == 0 and ln >= 0x20:
                    if not all(0.95 < math.sqrt(sum(f32a(p+16*i+4*c)**2 for c in range(4))) < 1.05
                               for i in range(ln // 16)): break
                elif ln % 12 == 0:
                    if any(abs(f32a(p+12*i+4*c)) > 1e5 for i in range(ln // 12) for c in range(3)): break
                else: break
            ok += 1; p += ln
        if ok == len([1 for o, l in pairs if l]):
            pos = base; break
    for kk, (off, ln) in enumerate(pairs):
        c = kk // 2
        if ln == 0: continue
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
    return ch, pos

names = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))['names']

# ---- (a) idle mirror control ----
idle = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
IDLE_T = 0x53200
# rebuild idle channels from the validated contiguous layout
ipairs = idle['pairs']
ch_i = {}
pos = 0x536e4
for kk, (off, ln) in enumerate(ipairs):
    c = kk // 2
    if ln == 0: pos += 0; continue
    if kk % 2 == 0:
        n = ln // 4
        ch_i.setdefault(c, {})['ticks'] = [u32a(pos + 4*j) for j in range(n)]
    else:
        if ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            ch_i.setdefault(c, {})['quat'] = [[f32a(pos+16*i+4*cc) for cc in range(4)] for i in range(m)]
        elif ln % 12 == 0:
            ch_i.setdefault(c, {})['vec3'] = [[f32a(pos+12*i+4*cc) for cc in range(3)] for i in range(ln // 12)]
    pos += ln

def mirror_err(ch, names):
    out = []
    for c in ch:
        if 'quat' not in ch[c] or len(ch[c]['quat']) < 2: continue
        nm = names[c] if c < len(names) else ''
        if '-node-rotation' not in nm: continue
        bare = nm.split('-node-')[0]
        if '_L_' not in bare: continue
        mir = bare.replace('_L_', '_R_')
        rc = next((c2 for c2 in ch if (names[c2] if c2 < len(names) else '').startswith(mir + '-node-')), None)
        if rc is None: continue
        kL = np.array(ch[c]['quat']); kR = np.array(ch[rc]['quat'])
        n = min(len(kL), len(kR))
        mr = kR[:n] * np.array([-1, -1, 1, 1])
        out.append(np.median([qangle(kL[i], mr[i]) for i in range(n)]))
    return out

e_idle = mirror_err(ch_i, names)
print(f'idle L/R mirror: {len(e_idle)} pairs, median {np.median(e_idle):.2f} deg, '
      f'<10deg {sum(1 for x in e_idle if x < 10)}/{len(e_idle)}')

# ---- (b) run sliding-window loop wrap ----
ch_r, rbase = load_seg(0x0b2818)
qc = [c for c in ch_r if 'quat' in ch_r[c] and len(ch_r[c]['quat']) > 4]
t_all = ch_r[0]['ticks']
lo, hi = t_all[0], t_all[-1]
print(f'\nrun segment ticks {lo}..{hi} ({hi-lo} ms); scanning 666-ms windows')
best = []
for start in range(lo, hi - 666, 17):
    end = start + 666
    errs = []
    for c in qc:
        ts = ch_r[c]['ticks']; ks = ch_r[c]['quat']
        i0 = next((i for i, t in enumerate(ts) if t >= start), None)
        i1 = next((i for i in range(len(ts)-1, -1, -1) if ts[i] <= end), None)
        if i0 is None or i1 is None or i1 <= i0: continue
        errs.append(qangle(ks[i0], ks[i1]))
    if errs:
        best.append((float(np.median(errs)), start))
best.sort()
print('top-5 wrap windows (median first-vs-last deg, start_ms):')
for e, s in best[:5]:
    print(f'  start {s}: {e:.2f} deg')
rng = np.random.default_rng(11)
nulls = []
for _ in range(300):
    s = rng.integers(lo, hi - 666)
    end = int(s) + 666
    errs = []
    for c in qc[:20]:
        ts = ch_r[c]['ticks']; ks = ch_r[c]['quat']
        i0 = next((i for i, t in enumerate(ts) if t >= s), None)
        i1 = next((i for i in range(len(ts)-1, -1, -1) if ts[i] <= end), None)
        if i0 is None or i1 is None or i1 <= i0: continue
        errs.append(qangle(ks[i0], ks[i1]))
    if errs: nulls.append(float(np.median(errs)))
print(f'null random 666-ms windows: median {np.median(nulls):.2f} deg, '
      f'p05 {np.percentile(nulls, 5):.2f}')
