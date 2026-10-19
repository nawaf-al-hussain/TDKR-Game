#!/usr/bin/env python3
"""S38 T1a: DEFINITIVE numpy FK truth — correct units + verified convention.

Fixes vs s37_t3_slerp.py:
  (1) UNIT BUG: fk_mode divided t by 1000 although channel times are SECONDS
      (Bip01 translation times run 0..5.0 s) — s37's truth sampled only the
      first 5 ms of each clip. Here: sample in seconds directly.
  (2) Convention: keeps the s36 pipeline convention M_all = invB @ world with
      row-vector einsum, which is ALGEBRAICALLY IDENTICAL to three.js
      (W_bone @ ibm) @ v (verified this session: numpy world matrices are the
      exact transposes of three.js matrixWorld; row-form composition inverts
      the same way). Do NOT "fix" it to world @ invB — that breaks the
      equivalence for posed bones.
Writes 50-ms dumps for the three.js fresh-state check.
"""
import numpy as np, json, os

SRC = open('/home/z/my-project/scripts/s36_t3_export.py').read()
head = SRC.split('# ---------- GLB assembly ----------')[0]
g = {'__name__': 's38_ctx'}
exec(head, g)

def sample_track(times, outs, t):
    if t <= times[0]: return outs[0].astype(float)
    if t >= times[-1]: return outs[-1].astype(float)
    hi = int(np.searchsorted(times, t)); lo = hi - 1
    f = (t - times[lo]) / max(1e-9, times[hi] - times[lo])
    a, b = outs[lo].astype(float), outs[hi].astype(float)
    if a.size != 4:
        return a * (1 - f) + b * f
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

def fk(channels, t):
    """t in SECONDS. Row-form convention (see docstring)."""
    cmap = {}
    for cd in channels:
        cmap.setdefault(cd['node'], {})[cd['path']] = cd
    W = {}
    parent_name = g['parent_name']; node_trs = g['node_trs']; order = g['order']
    def world(nm):
        if nm in W: return W[nm]
        p = parent_name(nm)
        t_, q_, s_ = node_trs[nm]
        cd = cmap.get(nm, {}).get('rotation')
        q = sample_track(cd['times'], cd['out'], t) if cd else q_
        tr = t_
        cdt = cmap.get(nm, {}).get('translation')
        if cdt: tr = sample_track(cdt['times'], cdt['out'], t)
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

OUT = '/home/z/my-project/scripts/jsverify/s38_truth'
os.makedirs(OUT, exist_ok=True)
summary = {}
for label, channels in g['anims']:
    tt = [cd['times'] for cd in channels if cd['path'] == 'translation' and cd['node'] == 'Bip01']
    dur = float(tt[0][-1]) if tt else max(float(cd['times'][-1]) for cd in channels if len(cd['times']))
    ts = np.arange(0.0, dur + 1e-9, 0.05)  # 50 ms grid, SECONDS
    dumps = {f't{int(round(t*1000))}': fk(channels, t).astype(np.float32) for t in ts}
    np.savez(f'{OUT}/{label}.npz', ts=ts.astype(np.float32), **dumps)
    summary[label] = {'dur_s': dur, 'n_dumps': len(dumps)}
    print(label, summary[label])
json.dump(summary, open('/home/z/my-project/scripts/s38/s38_t1_truth2_report.json', 'w'), indent=1)
print('saved s38_truth (SECONDS-grid, verified convention)')
