#!/usr/bin/env python3
"""S36 T3a2: FK-based gait battery for ALL walk/run/sneak clips (81), reusing
the r35 FK machinery (signed thigh swing, 10-ms grid autocorr, anti-phase)."""
import struct, math, json
import numpy as np

exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split('def chan(')[0])
# pull in r35 battery FK helpers
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session35/s35_t1_battery.py').read()
exec(src.split('def battery2(')[0])

def grid_ac(sig, rt, lo_ms=200, hi_ms=2000, step=10.0):
    t0, t1 = rt[0], rt[-1]
    if t1 - t0 < 400: return None, None, None
    grid = np.arange(t0, t1 + step, step)
    g = np.interp(grid, rt, sig)
    g = g - g.mean()
    s = g.std()
    if s < 1e-6: return None, None, None
    n = len(g)
    ac = np.correlate(g, g, 'full')[n - 1:]
    ac /= ac[0] if ac[0] else 1
    lags = np.arange(n) * step
    m = (lags >= lo_ms) & (lags <= hi_ms) & (lags <= (t1 - t0) * 0.95)
    if not m.any(): return None, None, None
    idx = np.where(m)[0]
    k = idx[np.argmax(ac[idx])]
    return float(lags[k]), float(ac[k]), float(s)

rng = np.random.default_rng(3607)
results = []
for cl in clips:
    n = cl['name'].lower()
    cls = None
    if 'walk' in n: cls = 'walk'
    elif 'run' in n or 'sprint' in n or 'jog' in n: cls = 'run'
    if cls is None: continue
    cov0 = [s for s in segs if s['start'] < cl['te'] and s['end'] > cl['ts']]
    lo = min(s['start'] for s in cov0); hi = max(s['end'] for s in cov0)
    cl2 = dict(cl); cl2['ts'] = lo; cl2['te'] = hi
    cov, chans, ns = assemble_clip(cl2, pad=0)
    rt0, fL, hL = ankle_track(chans, 'L')
    rt1, fR, hR = ankle_track(chans, 'R')
    if fL is None or fR is None:
        results.append(dict(name=cl['name'], cls=cls, fail='fk-missing')); continue
    row = dict(name=cl['name'], cls=cls)
    # foot z amplitude (travel)
    row['footz_L'] = round(float(fL[:, 2].max() - fL[:, 2].min()), 3)
    row['footz_R'] = round(float(fR[:, 2].max() - fR[:, 2].min()), 3)
    # thigh swing periodicity
    sL = signed_swing(chans, 'L'); sR = signed_swing(chans, 'R')
    perL, acL, sLs = grid_ac(sL, rt0) if sL is not None else (None,) * 3
    perR, acR, sRs = grid_ac(sR, rt1) if sR is not None else (None,) * 3
    row['perL'] = perL; row['acL'] = None if acL is None else round(acL, 3)
    row['perR'] = perR; row['acR'] = None if acR is None else round(acR, 3)
    # anti-phase at half period
    anti = None; anti0 = None
    # ankle X (forward) position corr at zero lag
    grid = np.arange(max(rt0[0], rt1[0]), min(rt0[-1], rt1[-1]), 10.0)
    if len(grid) >= 40:
        aL = np.interp(grid, rt0, fL[:, 0]); aR = np.interp(grid, rt1, fR[:, 0])
        if aL.std() > 1e-4 and aR.std() > 1e-4:
            c0 = np.corrcoef(aL, aR)[0, 1]
            anti0 = round(float(c0), 3)
            if perL:
                gRs = np.interp(grid - perL / 2, grid, aR)
                if gRs.std() > 1e-4:
                    anti = round(float(np.corrcoef(aL, gRs)[0, 1]), 3)
    row['anti'] = anti; row['anti0'] = anti0
    # shuffled null: shuffle L swing keys
    if sL is not None and len(sL) >= 8:
        sh = sL.copy(); rng.shuffle(sh)
        _, acN, _ = grid_ac(sh, rt0)
        row['null_ac'] = None if acN is None else round(acN, 3)
    else:
        row['null_ac'] = None
    results.append(row)

ok = 0; tested = 0; fails = []
for r in results:
    if 'fail' in r: fails.append((r['name'], r['fail'])); continue
    if r['acL'] is None: fails.append((r['name'], 'no-period')); continue
    tested += 1
    good = (r['acL'] > max((r['null_ac'] or 0) + 0.1, 0.3) and r['footz_L'] > 0.12
            and ((r['anti0'] is not None and r['anti0'] < -0.5) or (r['anti'] is not None and r['anti'] > 0.5)))
    if good: ok += 1
    else: fails.append((r['name'], f"acL={r['acL']} null={r['null_ac']} footz={r['footz_L']} anti={r['anti']}"))
print(f'FK gait battery: {ok}/{tested} pass ({100*ok/max(tested,1):.1f}%), fk-missing {sum(1 for r in results if "fail" in r)}')
from collections import Counter
print('fail causes:', Counter(c for _, c in fails).most_common(8))
for n_, c in fails[:14]: print('  ', n_, c)
json.dump({'results': results, 'ok': ok, 'tested': tested, 'fails': fails},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t3_gaitfk.json', 'w'))
