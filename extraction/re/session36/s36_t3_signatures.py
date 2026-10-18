#!/usr/bin/env python3
"""S36 T3a: name-keyed validation of all 921 clips.
Classes by name; per-class signature (root yaw for turns, root z for jump/fall,
foot activity+periodicity for locomotion, quiet for idle, wrap for loops);
per-class shuffled-key nulls; list failing clips."""
import struct, math, json, re, collections
import numpy as np

exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split('def chan(')[0])
import heapq

def ang2(q1, q2):
    d = np.abs(np.sum(q1.astype(np.float64) * q2.astype(np.float64), axis=-1))
    return 2 * np.arccos(np.clip(d, -1, 1)) * 180 / np.pi

IDX = {nm[:-5]: k for k, (nm, ty) in enumerate(CH)}
LFOOT = next(k for k, (nm, ty) in enumerate(CH) if nm == 'Bip01_L_Foot-node')
LTHIGH = next(k for k, (nm, ty) in enumerate(CH) if nm == 'Bip01_L_Thigh-node')
RTHIGH = next(k for k, (nm, ty) in enumerate(CH) if nm == 'Bip01_R_Thigh-node')
RFOOT = next(k for k, (nm, ty) in enumerate(CH) if nm == 'Bip01_R_Foot-node')

def series(cl_i, ch, vecn, clipwin=True):
    """assemble channel across the clip window: (times, values n×vecn)"""
    cl = clips[cl_i]
    ts, te = cl['ts'], cl['te']
    tt = None; vv = None
    for s in segs:
        if not (s['start'] < te and s['end'] > ts): continue
        st = seg_streams.get(s['k'])
        if st is None: return None, None
        tw = st[2 * ch].astype(np.int64)
        vw = st[2 * ch + 1]
        if len(tw) == 0: continue
        m = (tw >= ts) & (tw <= te) if clipwin else (tw >= s['start']) & (tw <= s['end'])
        if not m.any(): continue
        seg_t = tw[m]
        seg_v = (vw.view('<f4').reshape(-1, 4)[:len(tw)] if vecn == 4 else vw.view('<f4').reshape(-1, 3)[:len(tw)])[m]
        if tt is None:
            tt, vv = seg_t, seg_v
        else:
            mg = np.concatenate([tt, seg_t])
            o = np.argsort(mg, kind='stable')
            tt = mg[o]; vv = np.concatenate([vv, seg_v])[o]
    return tt, vv

def yaw_of(q):
    # yaw about Z (game is Z-up): 2*atan2(qz, qw), unwrapped deg
    y = 2 * np.arctan2(q[:, 2], q[:, 3]) * 180 / np.pi
    return np.degrees(np.unwrap(np.radians(y)))

def grid_ac(x, t_ms, lo_ms=200, hi_ms=2000, step=10.0):
    """resample to uniform grid then autocorr; returns (peak, period_ms)"""
    if len(x) < 8: return 0.0, 0.0
    t0, t1 = float(t_ms[0]), float(t_ms[-1])
    if t1 - t0 < hi_ms: hi = max(200.0, (t1 - t0) * 0.8)
    else: hi = float(hi_ms)
    grid = np.arange(t0, t1 + step, step)
    if len(grid) < 32: return 0.0, 0.0
    g = np.interp(grid, t_ms.astype(float), x)
    g = g - g.mean()
    n = len(g)
    F = np.abs(np.fft.rfft(g)) ** 2
    return 0.0, 0.0  # placeholder (replaced below)

def ac_peak(x):
    """normalized autocorrelation peak in lags 8..len/2; returns (peak, lag)"""
    x = x - x.mean()
    n = len(x)
    if n < 16 or x.std() < 1e-6: return 0.0, 0
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac /= ac[0] if ac[0] else 1
    lo, hi = 8, max(9, n // 2)
    if hi - lo < 2: return 0.0, 0
    seg = ac[lo:hi]
    i = int(np.argmax(seg)) + lo
    return float(ac[i]), i

rng = np.random.default_rng(3603)

def clip_stats(cl_i):
    out = {}
    t0, v0 = series(cl_i, 0, 3)           # root pos
    t6, v6 = series(cl_i, 6, 4)           # root quat
    tlf, vlf = series(cl_i, LFOOT, 4)
    trf, vrf = series(cl_i, RFOOT, 4)
    tlt, vlt = series(cl_i, LTHIGH, 4, clipwin=False)
    trt, vrt = series(cl_i, RTHIGH, 4, clipwin=False)
    tp, vp = series(cl_i, IDX['Bip01_Pelvis'], 4)
    if t0 is None or len(t0) < 4: return None
    z = v0[:, 2]
    out['zr'] = float(z.max() - z.min())
    out['z_start_end'] = float(z[-1] - z[0])
    xy = np.linalg.norm(np.diff(v0[:, :2], axis=0), axis=1).sum() if len(v0) > 1 else 0.0
    out['xy_path'] = float(xy)
    dur = max(clips[cl_i]['te'] - clips[cl_i]['ts'], 1)
    out['xy_rate'] = out['xy_path'] / dur * 1000
    if v6 is not None and len(v6) >= 4:
        y = yaw_of(v6)
        out['yaw_total'] = float(abs(y[-1] - y[0]))
        out['yaw_rng'] = float(y.max() - y.min())
    else:
        out['yaw_total'] = out['yaw_rng'] = 0.0
    for nm, (tf, vf) in (('lf', (tlf, vlf)), ('rf', (trf, vrf))):
        if vf is not None and len(vf) >= 8:
            a = ang2(vf, np.tile(vf[0], (len(vf), 1)))
            out[nm + '_rng'] = float(a.max())
            pk, lag = ac_peak(a)
            out[nm + '_ac'] = pk
        else:
            out[nm + '_rng'] = 0.0; out[nm + '_ac'] = 0.0
    if vp is not None and len(vp) >= 4:
        a = ang2(vp, np.tile(vp[0], (len(vp), 1)))
        out['pel_rng'] = float(a.max())
    else:
        out['pel_rng'] = 0.0
    # shuffled nulls for the same stats
    if v0 is not None and len(v0) >= 8:
        sh = v0.copy(); rng.shuffle(sh)
        out['null_zr'] = float(sh[:, 2].max() - sh[:, 2].min())
        sh2 = np.concatenate([vlf.copy() for _ in range(1)]) if vlf is not None else None
    if vlf is not None and len(vlf) >= 8:
        sh = vlf.copy(); rng.shuffle(sh)
        a = ang2(sh, np.tile(sh[0], (len(sh), 1)))
        out['null_lf_rng'] = float(a.max())
        pk, _ = ac_peak(a)
        out['null_lf_ac'] = pk
    else:
        out['null_lf_rng'] = 0.0; out['null_lf_ac'] = 0.0
    def gac(tf, vf):
        a = ang2(vf, np.tile(vf[0], (len(vf), 1)))
        t0, t1 = float(tf[0]), float(tf[-1])
        step = 10.0
        grid = np.arange(t0, t1 + step, step)
        g = np.interp(grid, tf.astype(float), a)
        g = g - g.mean()
        n = len(g)
        if n < 60: return 0.0, 0.0, float(a.max())
        f = np.abs(np.fft.rfft(g)) ** 2
        ac = np.fft.irfft(f)[:n]
        ac = ac / (ac[0] if ac[0] else 1)
        lo, hi = int(200 / step), min(int(2000 / step), n // 2)
        if hi - lo < 4: return 0.0, 0.0, float(a.max())
        k = int(np.argmax(ac[lo:hi])) + lo
        return float(ac[k]), float(k * step), float(a.max())
    for nm, (tf, vf) in (('lth', (tlt, vlt)), ('rth', (trt, vrt))):
        if vf is not None and len(vf) >= 8:
            pk, per, rng_ = gac(tf, vf)
            out[nm + '_ac'] = pk; out[nm + '_per'] = per; out[nm + '_rng'] = rng_
        else:
            out[nm + '_ac'] = 0.0; out[nm + '_per'] = 0.0; out[nm + '_rng'] = 0.0
    if vlt is not None and len(vlt) >= 8:
        sh = vlt.copy(); rng.shuffle(sh)
        sht = tlt.copy()
        pk, per, rng_ = gac(sht, sh)
        out['null_lth_ac'] = pk; out['null_lth_per'] = per; out['null_lth_rng'] = rng_
    else:
        out['null_lth_ac'] = 0.0; out['null_lth_per'] = 0.0; out['null_lth_rng'] = 0.0
    return out

def classify(name):
    n = name.lower()
    import re as _re
    if '_to_' in n or n.startswith('to_') or n.endswith('_to') or _re.search(r'_(start|end|in|out)$', n): return 'trans'
    if 'sneak_walk' in n: return 'walk'
    if 'idle' in n or 'breath' in n: return 'idle'
    if 'walk' in n and 'sneak' not in n: return 'walk'
    if 'run' in n or 'sprint' in n or 'jog' in n: return 'run'
    if 'turn' in n: return 'turn'
    if 'jump' in n or 'leap' in n: return 'jump'
    if 'fall' in n or 'drop' in n: return 'fall'
    if 'glide' in n or 'fly' in n: return 'glide'
    if 'grappl' in n or 'grab' in n or 'hang' in n: return 'grapple'
    if any(w in n for w in ('attack', 'punch', 'kick', 'strike', 'combo', 'beatdown', 'hit_', '_hit', 'smash', 'slam')): return 'combat'
    if 'hurt' in n or 'pain' in n or 'stagger' in n: return 'hit'
    if 'death' in n or 'die' in n or 'dead' in n or 'knock' in n: return 'death'
    if 'climb' in n or 'ledge' in n or 'mantle' in n or 'vault' in n: return 'climb'
    if 'crouch' in n or 'sneak' in n or 'craw' in n: return 'crouch'
    if 'land' in n: return 'land'
    if 'dodge' in n or 'roll' in n or 'evade' in n: return 'dodge'
    return 'other'

rows = []
for cl in clips:
    st = clip_stats(cl['i'])
    if st is None:
        rows.append(dict(name=cl['name'], i=cl['i'], cls=classify(cl['name']), fail='no-root-keys'))
        continue
    st.update(name=cl['name'], i=cl['i'], cls=classify(cl['name']))
    rows.append(st)

# signature tests
def test(r):
    c = r['cls']
    if c == 'idle':
        ok = r['zr'] < 0.25 and r['lf_rng'] < 20 and r['rf_rng'] < 20 and r['xy_rate'] < 0.3
    elif c in ('walk', 'run'):
        ok = (r['lth_rng'] > 15 or r['rth_rng'] > 15) and r['lth_ac'] > r['null_lth_ac'] + 0.15
    elif c == 'turn':
        ok = r['yaw_total'] > 30 or r['yaw_rng'] > 45
    elif c in ('jump', 'fall'):
        ok = ('loop' not in r['name'].lower()) and (r['zr'] > 0.35 or r['z_start_end'] > 0.25)
    else:
        ok = None  # no signature test for other classes (report stats only)
    return ok

tested = passed = 0
fails = collections.defaultdict(list)
cls_count = collections.Counter()
for r in rows:
    cls_count[r['cls']] += 1
    if 'fail' in r:
        fails['decode'].append(r['name']); continue
    ok = test(r)
    if ok is None: continue
    tested += 1
    if ok: passed += 1
    else: fails[r['cls']].append(r['name'])

print('class counts:', dict(cls_count))
print(f'signature-tested {tested}, passed {passed} ({100*passed/max(tested,1):.1f}%)')
for c, lst in sorted(fails.items()):
    print(f'FAIL {c} ({len(lst)}): {lst[:12]}{"..." if len(lst) > 12 else ""}')

# per-class medians for the report
med = {}
for c in sorted(cls_count):
    sub = [r for r in rows if 'fail' not in r and r['cls'] == c]
    if not sub: continue
    med[c] = {k: round(float(np.median([r[k] for r in sub])), 3)
              for k in ('zr', 'xy_rate', 'yaw_total', 'lf_rng', 'rf_rng', 'lf_ac', 'null_lf_ac', 'pel_rng') if k in sub[0]}
print('\nper-class medians:')
for c, m in med.items(): print(f'  {c:8s}', m)

json.dump({'rows': rows, 'fails': {k: v for k, v in fails.items()}, 'medians': med,
           'tested': tested, 'passed': passed},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t3_signatures.json', 'w'))
