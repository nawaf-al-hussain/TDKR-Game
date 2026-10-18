#!/usr/bin/env python3
"""S35 T1b: batch segment decoder + clip assembly under the engine-derived
mapping (clips = packed-timeline windows; segments = storage chunks).
Decodes all 663 segments, assembles all 921 clips, runs the gait battery
on walk/run/idle with nulls."""
import struct, math, json, collections
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

# ---------- segment directory ----------
CNT_OFF = 0xccf4
nseg = u32a(CNT_OFF)
segarr = u32a(CNT_OFF + 4)
segs = []
for k in range(nseg):
    o = segarr + k * 0x1c
    f = [u32a(o + 4 * j) for j in range(7)]
    segs.append(dict(k=k, start=f[0], end=f[1], tbl=f[4], dist=f[5]))

# ---------- clip list ----------
def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            return ad[v:e].decode('latin1')

clips = []
for i in range(921):
    nameOff, ts, te = struct.unpack_from('<3I', ad, 0x11580 + 12 * i)
    clips.append(dict(i=i, name=cstr(nameOff), ts=ts, te=te))

# ---------- channel names (engine order) ----------
CH = []
for k in range(78):
    o = 0xb544 + k * 0x20
    sub = u32a(o + 0x10)
    nm = cstr(u32a(sub))
    ty = u32a(sub + 4)
    CH.append((nm, ty))
assert len(CH) == 78

# ---------- segment stream decode ----------
def decode_segment(seg):
    """returns list of 156 (times u32[], values f32[] flat) or error"""
    T = seg['tbl']
    nst = u32a(T)
    if not (100 <= nst <= 160):
        return None, f'bad nst {nst}'
    len0 = u32a(T + 4)
    ents = [(None, len0)]
    for j in range(1, nst):
        ents.append((u32a(T + 8 * j), u32a(T + 8 * j + 4)))
    # base candidates: TBL+ (nst+1)*8 - 4  [observed 0x4e4], off[1]+8, scan
    cands = [T + (nst + 1) * 8 - 4]
    if ents[1][0] is not None:
        cands.append(T + ents[1][0] + 8)
    for base in cands:
        streams = []
        pos = base
        ok = True
        for j, (off, ln) in enumerate(ents):
            if pos + ln > N:
                ok = False; break
            if ln % 4:
                ok = False; break
            w = np.frombuffer(ad, dtype='<u4', count=ln // 4, offset=pos)
            streams.append(w)
            pos += ln
        if not ok:
            continue
        # validate: even streams ascending ticks
        bad = 0
        for j in range(0, len(streams), 2):
            t = streams[j]
            if len(t) >= 2 and not np.all(np.diff(t.astype(np.int64)) >= 0):
                bad += 1
        if bad == 0:
            return streams, None
    return None, 'no base validated'

# decode all segments
seg_streams = {}
fails = collections.Counter()
for s in segs:
    st, err = decode_segment(s)
    if st is None:
        fails[err] += 1
    else:
        seg_streams[s['k']] = st
print(f'segments decoded: {len(seg_streams)}/{nseg}; failures: {dict(fails)}')

# ---------- assemble clips ----------
def assemble_clip(cl, pad=120):
    """gather channel keys in [ts-pad, te+pad] from covering segments"""
    ts, te = cl['ts'], cl['te']
    cov = [s for s in segs if s['start'] < te and s['end'] > ts]
    chans = [None] * 78
    nsamp = 0
    for s in cov:
        st = seg_streams.get(s['k'])
        if st is None:
            continue
        nsamp += 1
        for c in range(78):
            tw = st[2 * c].astype(np.int64)
            vw = st[2 * c + 1]
            nt = len(tw)
            if nt == 0:
                continue
            # value stream: vec3 (12/key) for type 1, quat (16/key) for type 5
            vdim = 3 if CH[c][1] == 1 else 4
            nv = len(vw) * 4 // (vdim * 4)
            n = min(nt, nv)
            m = (tw[:n] >= ts - pad) & (tw[:n] <= te + pad)
            if not m.any():
                continue
            tt = tw[:n][m]
            vf = vw.view('<f4')
            if vdim == 3:
                vv = vf.reshape(-1, 3)[:n][m]
            else:
                vv = vf.reshape(-1, 4)[:n][m]
            if chans[c] is None:
                chans[c] = (tt, vv)
            else:
                t0, v0 = chans[c]
                mg = np.concatenate([t0, tt]); ord_ = np.argsort(mg, kind='stable')
                chans[c] = (mg[ord_], np.concatenate([v0, vv])[ord_])
    return cov, chans, nsamp

# ---------- gait battery ----------
def ang(q1, q2):
    d = np.abs(np.sum(q1 * q2, axis=-1))
    return 2 * np.arccos(np.clip(d, -1, 1)) * 180 / np.pi

def chan(cl_i, name):
    cl = clips[cl_i]
    cov, chans, ns = assemble_clip(cl)
    for c, (nm, ty) in enumerate(CH):
        if nm == name + '-node' and ty == 5:
            return chans[c]
    return None

def chan_tr(cl_i, name):
    c = chan(cl_i, name)
    if c is None:
        return None
    t, v = c
    return t, v, ang(v, np.tile(v[0], (len(v), 1)))

def dom_freq(series, tick_ms=1.0):
    x = series - series.mean()
    if len(x) < 8:
        return 0.0, 0.0
    F = np.abs(np.fft.rfft(x))
    fr = np.fft.rfftfreq(len(x), d=tick_ms / 1000.0)
    if len(F) < 2:
        return 0.0, 0.0
    k = 1 + np.argmax(F[1:])
    power = F[1:].sum()
    return fr[k], F[k] / power if power > 0 else 0.0

def battery(cl_i, label):
    out = dict(clip=clips[cl_i]['name'], window=[clips[cl_i]['ts'], clips[cl_i]['te']],
               dur_ms=clips[cl_i]['te'] - clips[cl_i]['ts'])
    cov, chans, ns = assemble_clip(clips[cl_i])
    out['segments'] = [s['k'] for s in cov]
    out['nseg_found'] = ns
    # thigh travel
    for side in 'LR':
        r = chan_tr(cl_i, f'Bip01_{side}_Thigh')
        if r is None:
            out[f'{side}_thigh'] = None
            continue
        t, v, a = r
        out[f'{side}_thigh'] = dict(n=len(t), travel_max=round(float(a.max()), 1),
                                    travel_range=round(float(a.max() - a.min()), 1))
        f, pk = dom_freq(a.astype(float))
        # shuffled null for peak ratio
        rng = np.random.default_rng(7 + cl_i)
        nulls = []
        for _ in range(200):
            sh = a.astype(float).copy(); rng.shuffle(sh)
            _, pk2 = dom_freq(sh)
            nulls.append(pk2)
        out[f'{side}_thigh']['dom_freq_hz'] = round(float(f), 2)
        out[f'{side}_thigh']['peak_ratio'] = round(float(pk), 3)
        out[f'{side}_thigh']['null_peak_p95'] = round(float(np.quantile(nulls, 0.95)), 3)
    # L/R anti-phase
    lt = chan_tr(cl_i, 'Bip01_L_Thigh'); rt = chan_tr(cl_i, 'Bip01_R_Thigh')
    if lt and rt:
        # interpolate R onto L times
        tt = lt[0].astype(float)
        rv = np.interp(tt, rt[0].astype(float), rt[2].astype(float))
        cc = np.corrcoef(lt[2].astype(float), rv)[0, 1]
        out['LR_thigh_corr'] = round(float(cc), 3)
    # root vertical oscillation
    cov2, chans2, _ = assemble_clip(clips[cl_i])
    root = chans2[0]
    if root is not None:
        t, v = root
        out['root_pos_range'] = {ax: round(float(v[:, i].max() - v[:, i].min()), 3) for i, ax in enumerate('xyz')}
    # smoothness vs shuffled (per-channel angular velocity p95, mean over channels)
    vels = []
    null_vels = []
    rng = np.random.default_rng(11 + cl_i)
    for c in range(6, 78):
        if chans2[c] is None:
            continue
        tt, vv = chans2[c]
        if len(tt) < 4:
            continue
        dt = np.diff(tt.astype(float))
        da = ang(vv[1:], vv[:-1])
        okm = dt > 0
        if okm.sum() < 2:
            continue
        v = da[okm] / dt[okm] * 1000.0
        vels.append(np.quantile(v, 0.95))
        sh = vv.copy(); rng.shuffle(sh)
        da2 = ang(sh[1:], sh[:-1])
        null_vels.append(np.quantile(da2[okm] / dt[okm] * 1000.0, 0.95))
    if vels:
        out['vel_p95_med'] = round(float(np.median(vels)), 1)
        out['null_vel_p95_med'] = round(float(np.median(null_vels)), 1)
    # loop continuity: angle between first and last key (per channel, cyclic)
    wraps = []
    for c in range(6, 78):
        if chans2[c] is None:
            continue
        tt, vv = chans2[c]
        if len(tt) < 2:
            continue
        wraps.append(float(ang(vv[:1], vv[-1:])[0]))
    if wraps:
        out['wrap_med_deg'] = round(float(np.median(wraps)), 1)
        out['wrap_p10'] = round(float(np.quantile(wraps, 0.10)), 1)
    return out

print('\n=== battery: _007_walk (clip 5) ===')
b = battery(5, 'walk')
print(json.dumps(b, indent=1))
json.dump(b, open('/home/z/my-project/scripts/s35_t1_bat_walk.json', 'w'))

print('\n=== battery: _008_run (clip 6) ===')
b = battery(6, 'run')
print(json.dumps(b, indent=1))
json.dump(b, open('/home/z/my-project/scripts/s35_t1_bat_run.json', 'w'))

print('\n=== battery: _001_idle_stand (clip 0, negative control) ===')
b = battery(0, 'idle')
print(json.dumps(b, indent=1))
json.dump(b, open('/home/z/my-project/scripts/s35_t1_bat_idle.json', 'w'))
