#!/usr/bin/env python3
"""S37 T3b: attribute the three.js residual error with numbers.

- rebuild the 5 exported anims' channels exactly as s36_t3_export.py
- FK in TWO interpolation modes: nlerp (s36's sample_track) vs true slerp
- per-anim, 10-ms grid: max/mean |fk_slerp - fk_nlerp| over the 1449 skinned
  verts; correlate worst t with the steepest adjacent-key angular velocity
- write fk_slerp dumps (50-ms subset, ascending times) for the three.js
  forward-only fresh-state cross-check
"""
import numpy as np, json, os, re

SRC = open('/home/z/my-project/scripts/s36_t3_export.py').read()
head = SRC.split('# ---------- GLB assembly ----------')[0]
g = {'__name__': 's37_t3_slerp_ctx'}
exec(head, g)
fk_skinned = g['fk_skinned']
sample_track = g['sample_track']
qmul = g['qmul']
anims = g['anims']
anims = [(l, c) for l, c in anims]

def qmul_scalar(a, b):
    x1, y1, z1, w1 = a; x2, y2, z2, w2 = b
    return np.array([w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2,
                     w1*w2 - x1*x2 - y1*y2 - z1*z2])

def sample_slerp(times, outs, t):
    if t <= times[0]: return outs[0].astype(float)
    if t >= times[-1]: return outs[-1].astype(float)
    hi = int(np.searchsorted(times, t)); lo = hi - 1
    f = (t - times[lo]) / max(1e-9, times[hi] - times[lo])
    a = outs[lo].astype(float); b = outs[hi].astype(float)
    if a.size != 4:
        return a * (1 - f) + b * f          # translation / scale: linear
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    dd = float(np.dot(a, b))
    if dd < 0.0:
        b = -b; dd = -dd
    if dd > 0.9995:
        r = a + f * (b - a)
        return r / np.linalg.norm(r)
    th = np.arccos(np.clip(dd, -1, 1))
    s = np.sin(th)
    r = (np.sin((1 - f) * th) / s) * a + (np.sin(f * th) / s) * b
    return r / np.linalg.norm(r)

def fk_mode(channels, t, sampler):
    cmap = {}
    for cd in channels:
        cmap.setdefault(cd['node'], {})[cd['path']] = cd
    W = {}
    parent_name = g['parent_name']; node_trs = g['node_trs']; order = g['order']
    def world(nm):
        if nm in W: return W[nm]
        p = parent_name(nm)
        t_, q_, s_ = node_trs[nm]
        t_s = t / 1000.0
        cd = cmap.get(nm, {}).get('rotation')
        q = sampler(cd['times'], cd['out'], t_s) if cd else q_
        tr = t_
        cdt = cmap.get(nm, {}).get('translation')
        if cdt: tr = sampler(cdt['times'], cdt['out'], t_s)
        M = np.eye(4)
        M[:3, :3] = g['colR'](q) @ np.diag(s_)
        M[3, :3] = tr
        M = M @ (world(p) if p else np.eye(4))
        W[nm] = M
        return M
    for nm in order: world(nm)
    verts = g['verts']; NV = g['NV']; invB = g['invB']; joint_nodes = g['joint_nodes']
    b4s = g['b4s']; w4s = g['w4s']
    V = np.hstack([verts, np.ones((NV, 1))])
    M_all = np.stack([invB[b] @ world(joint_nodes[b]) for b in range(31)])
    out = np.zeros((NV, 3))
    for k in range(4):
        bk = np.clip(b4s[:, k], 0, 30)
        wk = w4s[:, k:k + 1]
        Mb = M_all[bk]
        out += wk * np.einsum('ni,nij->nj', V, Mb)[:, :3]
    return out

def steepest_omega(channels):
    """max adjacent-key angular velocity (deg/s) across quat channels"""
    best = 0.0
    for cd in channels:
        if cd['path'] != 'rotation': continue
        tt, vv = cd['times'], cd['out']
        for i in range(len(tt) - 1):
            a = vv[i].astype(float); b = vv[i + 1].astype(float)
            a /= np.linalg.norm(a); b /= np.linalg.norm(b)
            if float(np.dot(a, b)) < 0: b = -b
            ang = np.degrees(2 * np.arccos(np.clip(abs(float(np.dot(a, b))), 0, 1)))
            dt = max(tt[i + 1] - tt[i], 1e-6)
            best = max(best, ang / dt)
    return best

os.makedirs('/home/z/my-project/scripts/jsverify/s37_fk', exist_ok=True)
report = {}
for label, channels in anims:
    dur = None
    tt = [cd['times'] for cd in channels if cd['path'] == 'translation' and cd['node'] == 'Bip01']
    if tt:
        dur = float(tt[0][-1])
    else:
        durs = [float(cd['times'][-1]) for cd in channels if len(cd['times'])]
        dur = max(durs)
    grid = np.arange(0.0, dur + 1e-9, 0.01)
    dmax = 0.0; dsum = 0.0; dt_worst = 0.0; n = 0
    dumps = []
    for t in grid:
        ps = fk_mode(channels, t, sample_slerp)
        pn = fk_mode(channels, t, sample_track)
        d = np.linalg.norm(ps - pn, axis=1) * 100.0  # cm
        dmax = max(dmax, float(d.max())); dsum += float(d.mean()); n += 1
        if float(d.max()) > dt_worst:
            dt_worst = float(d.max())
        if abs(t * 1000 % 50) < 5:  # 50-ms subset for three.js
            dumps.append((t, ps))
    fn_dump = f'/home/z/my-project/scripts/jsverify/s37_fk/{label}.npz'
    np.savez(fn_dump, ts=np.array([t for t, _ in dumps]),
             **{f't{int(round(t*1000))}': ps.astype(np.float32) for t, ps in dumps})
    report[label] = {'dur_ms': int(dur * 1000), 'slerp_vs_nlerp_max_cm': round(dmax, 4),
                     'slerp_vs_nlerp_mean_cm': round(dsum / n, 4),
                     'steepest_omega_deg_s': round(steepest_omega(channels), 1)}
    print(label, report[label])
json.dump(report, open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t3_slerp.json', 'w'), indent=1)
print('saved s37_t3_slerp.json + dumps for three.js check')
