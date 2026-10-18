#!/usr/bin/env python3
"""S35 T1c: refined gait battery (FK-based, signed swing, autocorr period,
foot travel) on walk/run/idle + full 921-clip batch table."""
import struct, math, json, collections
import numpy as np

exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split("print('\\n=== battery")[0])

# ---- mini-FK for the leg chain (rest locals from batman.bdae) ----
D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v: return d[v:e].decode('latin1')

nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32(o)), pool(u32(o + 4)), pool(u32(o + 8))
    if n1 is None or n2 is None or al is None: o += 4; continue
    t = struct.unpack_from('<3f', d, o + 0x0c)
    q = struct.unpack_from('<4f', d, o + 0x18)
    s = struct.unpack_from('<3f', d, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s): o += 4; continue
    if u32(o + 0x34) != 1 or u32(o + 0x38) > 32: o += 4; continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s)); o += 0x50
JN = {n['name']: n for n in nodes}
PNAME = {'Bip01_L_Thigh': 'Bip01_Pelvis', 'Bip01_L_Calf': 'Bip01_L_Thigh',
         'Bip01_L_Foot': 'Bip01_L_Calf', 'Bip01_R_Thigh': 'Bip01_Pelvis',
         'Bip01_R_Calf': 'Bip01_R_Thigh', 'Bip01_R_Foot': 'Bip01_R_Calf',
         'Bip01_Pelvis': 'Bip01', 'Bip01': None}
CHAIN = ['Bip01', 'Bip01_Pelvis', 'Bip01_L_Thigh', 'Bip01_L_Calf', 'Bip01_L_Foot']
CHAINR = ['Bip01', 'Bip01_Pelvis', 'Bip01_R_Thigh', 'Bip01_R_Calf', 'Bip01_R_Foot']

def qmul(a, b):
    a = np.asarray(a, np.float64); b = np.asarray(b, np.float64)
    x1, y1, z1, w1 = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    x2, y2, z2, w2 = b[..., 0], b[..., 1], b[..., 2], b[..., 3]
    return np.stack([w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2,
                     w1*w2 - x1*x2 - y1*y2 - z1*z2], -1)

def qrot(q, v):
    q = np.asarray(q, np.float64); v = np.asarray(v, np.float64)
    qv = np.broadcast_to(np.append(v, 0.0), q.shape)
    qc = q * np.array([-1, -1, -1, 1])
    out = qmul(qmul(q, qv), qc)
    return out[..., :3]

def fk_leg(chans, chain):
    """world pos of each joint in chain at each key time (union grid)."""
    # gather per-node (t, quat) on a common grid = clip keys of Pelvis chain
    # use root keys as grid
    rt = chans[0][0].astype(np.int64)
    out = {}
    for nm in chain:
        ci = None
        for c, (cn, ty) in enumerate(CH):
            if cn == nm + '-node' and ty == 5:
                ci = c; break
        if ci is None or chans[ci] is None:
            return None
        t, v = chans[ci]
        out[nm] = (t.astype(np.int64), v.astype(np.float64))
    n = len(rt)
    pos = {nm: np.zeros((n, 3)) for nm in chain}
    # local translation (constant from rig) + animated rotation
    prev_p = np.zeros((n, 3)); prev_q = np.tile(JN['Bip01']['q'], (n, 1))
    for i, nm in enumerate(chain[1:], 1):
        t, v = out[nm]
        qi = np.array([v[np.searchsorted(t, rt[j] - 1) if np.searchsorted(t, rt[j] - 1) < len(v) else len(v) - 1]
                       for j in range(n)]) if len(t) else np.tile(JN[nm]['q'], (n, 1))
        wq = qmul(prev_q, qi)
        lt = np.array(JN[nm]['t'])
        off = np.array([qrot(wq[j], lt * JN[nm]['s']) for j in range(n)])
        pos[nm] = prev_p + off
        prev_p, prev_q = pos[nm], wq
    return pos

def ankle_track(chans, side):
    chain = CHAIN if side == 'L' else CHAINR
    pos = fk_leg(chans, chain)
    if pos is None: return None, None, None
    rt = chans[0][0].astype(np.int64)
    return rt.astype(float), pos[chain[4]], pos[chain[1]]

def signed_swing(chans, side):
    """thigh signed swing: forward(x?) component of knee offset angle.
    Use the knee (Calf child) world offset direction projected on forward."""
    chain = CHAIN if side == 'L' else CHAINR
    pos = fk_leg(chans, chain)
    if pos is None:
        return None
    knee = pos[chain[2]]  # thigh endpoint = knee
    hip = pos[chain[1]]
    d = knee - hip  # thigh direction over time
    # forward axis: mean direction across time defines +forward
    mean = d.mean(axis=0); mean = mean / np.linalg.norm(mean)
    fwd = mean
    up = np.array([0, 0, 1.0])
    right = np.cross(up, fwd); right /= np.linalg.norm(right)
    swing = np.arctan2(d @ right, d @ fwd) * 180 / np.pi
    return swing

def autocorr_period(x, lo_ms=200, hi_ms=2000, tick=1.0):
    x = x - x.mean()
    n = len(x)
    if n < 8:
        return None, None
    ac = np.correlate(x, x, 'full')[n - 1:]
    lags = np.arange(n) * tick
    m = (lags >= lo_ms) & (lags <= hi_ms)
    if not m.any():
        return None, None
    k = np.argmax(ac[m])
    lag = lags[m][k]
    ac0 = ac[0] or 1.0
    return float(lag), float(ac[m][k] / ac0)

def battery2(cl_i, label):
    cl = clips[cl_i]
    out = dict(clip=cl['name'], window=[cl['ts'], cl['te']], dur_ms=cl['te'] - cl['ts'])
    cov, chans, ns = assemble_clip(cl, pad=0)
    out['segments'] = [s['k'] for s in cov]
    nkeys = [len(c[0]) for c in chans if c is not None]
    out['nchan_with_keys'] = len(nkeys)
    out['keys_med'] = int(np.median(nkeys)) if nkeys else 0
    # thigh travel + ankle periodicity (uniform 10 ms grid autocorr)
    grids = {}
    thigh_sigs = {}
    # common gait frame from pelvis-chain geometry
    rt0, fL0, hL0 = ankle_track(chans, 'L')
    rt1, fR0, hR0 = ankle_track(chans, 'R')
    gaxis = None
    if fL0 is not None and fR0 is not None:
        mv = fL0.mean(axis=0) - fR0.mean(axis=0); mv[2] = 0
        if np.linalg.norm(mv) > 1e-6:
            gaxis = mv / np.linalg.norm(mv)
    for side in 'LR':
        chain = CHAIN if side == 'L' else CHAINR
        pos = fk_leg(chans, chain)
        if pos is None: continue
        hip, knee = pos[chain[1]], pos[chain[2]]
        d = knee - hip
        if gaxis is not None:
            up = np.array([0, 0, 1.0]); right = np.cross(up, gaxis)
            right /= np.linalg.norm(right)
            sig = np.degrees(np.arctan2(d @ right, d @ gaxis))
        else:
            sig = np.degrees(np.arctan2(d[:, 1], d[:, 0]))
        thigh_sigs[side] = (pos and hip is not None, sig)
    for side in 'LR':
        rt, foot, hip = ankle_track(chans, side)
        if foot is None:
            out[f'{side}_ankle'] = None; continue
        grids[side] = (rt, foot)
        # forward axis: common mean motion direction of the ankle
        d = foot - foot.mean(axis=0)
        # horizontal amplitude (perp to up) as gait signal
        horiz = d[:, :2]
        sig = np.linalg.norm(horiz, axis=1)
        tmax, tmin = rt[-1], rt[0]
        grid = np.arange(tmin, tmax + 1e-6, 10.0)
        if len(grid) < 12:
            out[f'{side}_ankle'] = dict(n_grid=len(grid)); continue
        sg = np.interp(grid, rt, sig)
        z = foot[:, 2]
        zg = np.interp(grid, rt, z)
        # autocorr period of horizontal ankle speed
        v = np.abs(np.diff(sg))
        lag, acv = autocorr_period(v - v.mean(), lo_ms=150, hi_ms=2500, tick=10.0)
        rng = np.random.default_rng(3 + cl_i)
        nulls = []
        for _ in range(200):
            sh = v.copy(); rng.shuffle(sh)
            l2, a2 = autocorr_period(sh - sh.mean(), lo_ms=150, hi_ms=2500, tick=10.0)
            nulls.append(a2 if a2 is not None else 0.0)
        out[f'{side}_ankle'] = dict(zrange=round(float(z.max() - z.min()), 3),
                                    period_ms=lag,
                                    ac=round(acv, 3) if acv else None,
                                    null_ac_p95=round(float(np.quantile(nulls, 0.95)), 3))
    # thigh periodicity on cyclic x4 series
    for side in 'LR':
        if side not in thigh_sigs: continue
        sig = thigh_sigs[side][1]
        rt, foot, hip = ankle_track(chans, side)
        if foot is None: continue
        grid = np.arange(rt[0], rt[-1] + 1e-6, 10.0)
        if len(grid) < 12: continue
        sg = np.interp(grid, rt, sig)
        cyc = np.tile(sg - sg.mean(), 4)
        trav = float(sg.max() - sg.min())
        res = dict(travel_deg=round(trav, 1), period_ms=None, ac=None, null_ac_p95=None)
        if trav > 5.0:
            lag, acv = autocorr_period(cyc, lo_ms=150, hi_ms=2600, tick=10.0)
            rng = np.random.default_rng(21 + cl_i)
            nulls = []
            for _ in range(200):
                sh = cyc.copy(); rng.shuffle(sh)
                l2, a2 = autocorr_period(sh, lo_ms=150, hi_ms=2600, tick=10.0)
                nulls.append(a2 if a2 is not None else 0.0)
            res.update(period_ms=lag, ac=round(acv, 3) if acv else None,
                       null_ac_p95=round(float(np.quantile(nulls, 0.95)), 3))
        out[f'{side}_thigh_period'] = res
    # L/R anti-phase: corr of horizontal ankle displacement components
    if 'L' in grids and 'R' in grids:
        rtL, fL = grids['L']; rtR, fR = grids['R']
        # common frame: mean motion direction of both ankles
        dL = fL - fL.mean(axis=0); dR = fR - fR.mean(axis=0)
        mvec = fL.mean(axis=0) - fR.mean(axis=0)
        mvec[2] = 0
        nrm = np.linalg.norm(mvec)
        if nrm > 1e-6:
            fwd = mvec / nrm
            aL = dL @ fwd; aR = dR @ fwd
            grid = np.arange(max(rtL[0], rtR[0]), min(rtL[-1], rtR[-1]) + 1e-6, 10.0)
            if len(grid) < 12: return out
            agL = np.interp(grid, rtL, aL); agR = np.interp(grid, rtR, aR)
            # anti-phase: min Pearson corr over lags (0..600 ms)
            best = (1.0, 0)
            for L in range(0, 61):
                if L >= len(agL): break
                c = float(np.corrcoef(agL[L:], agR[:len(agR) - L])[0, 1]) if L < len(agL) - 8 else 1.0
                if c < best[0]: best = (c, L * 10)
            out['LR_ankle_min_corr'] = round(best[0], 3)
            out['LR_ankle_min_corr_lag_ms'] = best[1]
            rng = np.random.default_rng(5 + cl_i)
            nc = []
            for _ in range(200):
                b = agL.copy(); rng.shuffle(b)
                nc.append(np.corrcoef(b, agR)[0, 1])
            out['LR_ankle_corr_null_p95'] = round(float(np.quantile(np.abs(nc), 0.95)), 3)
    # root vertical oscillation + in-place check
    root = chans[0]
    if root is not None:
        t, v = root
        out['root_range'] = {ax: round(float(v[:, i].max() - v[:, i].min()), 4) for i, ax in enumerate('xyz')}
        out['root_z_med'] = round(float(np.median(v[:, 2])), 4)
    # foot travel (FK): vertical excursion of each ankle
    for side in 'LR':
        chain = CHAIN if side == 'L' else CHAINR
        pos = fk_leg(chans, chain)
        if pos is None: continue
        foot = pos[chain[4]]
        out[f'{side}_foot_zrange'] = round(float(foot[:, 2].max() - foot[:, 2].min()), 4)
        along = foot - foot.mean(axis=0)
        fwd = None
        knee = pos[chain[2]] - pos[chain[1]]
        mf = knee.mean(axis=0); mf /= np.linalg.norm(mf)
        out[f'{side}_foot_frange'] = round(float(along @ mf).max() - (along @ mf).min(), 4) if False else round(float((along @ mf).max() - (along @ mf).min()), 4)
    # smoothness + wrap (keys within window)
    vels, nulls_v, wraps, nulls_w = [], [], [], []
    rng = np.random.default_rng(9 + cl_i)
    for c in range(6, 78):
        if chans[c] is None: continue
        tt, vv = chans[c]
        if len(tt) < 4: continue
        dt = np.diff(tt.astype(float)); da = ang(vv[1:], vv[:-1])
        m = dt > 0
        if m.sum() < 2: continue
        vels.append(np.quantile(da[m] / dt[m] * 1000, 0.95))
        sh = vv.copy(); rng.shuffle(sh)
        nulls_v.append(np.quantile(ang(sh[1:], sh[:-1])[m] / dt[m] * 1000, 0.95))
        wraps.append(float(ang(vv[:1], vv[-1:])[0]))
        i2 = rng.permutation(len(vv))
        nulls_w.append(float(ang(vv[i2[:1]], vv[i2[-1:]])[0]))
    if vels:
        out['vel_p95_med'] = round(float(np.median(vels)), 1)
        out['null_vel_p95_med'] = round(float(np.median(nulls_v)), 1)
        out['wrap_med_deg'] = round(float(np.median(wraps)), 1)
        out['null_wrap_med'] = round(float(np.median(nulls_w)), 1)
    return out

for ci, lab in ((5, 'walk'), (6, 'run'), (0, 'idle')):
    r = battery2(ci, lab)
    print(f'=== {lab} ===')
    print(json.dumps(r, indent=1))
    json.dump(r, open(f'/home/z/my-project/scripts/s35_t1_bat2_{lab}.json', 'w'))

# ---- failed segments ----
print('\n=== failed segments ===')
for s in segs:
    st, err = decode_segment(s)
    if st is None:
        T = s['tbl']
        print(f"seg{s['k']}: [{s['start']},{s['end']}) tbl=0x{T:x} nst={u32a(T)} len0={u32a(T+4)} err={err}")
