#!/usr/bin/env python3
"""S35 T1d: batch all 921 clips — decode coverage + validation battery,
failures by cause; positive control _015_sneak_walk_front."""
import struct, math, json, collections
import numpy as np

exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split("print('\\n=== battery")[0])

def ang2(q1, q2):
    d = np.abs(np.sum(q1.astype(np.float64) * q2.astype(np.float64), axis=-1))
    return 2 * np.arccos(np.clip(d, -1, 1)) * 180 / np.pi

def validate_clip(cl):
    """returns dict of cheap validation stats + failure cause"""
    ts, te = cl['ts'], cl['te']
    cov = [s for s in segs if s['start'] < te and s['end'] > ts]
    if not cov:
        return dict(name=cl['name'], fail='no covering segment')
    missing = [s['k'] for s in cov if s['k'] not in seg_streams]
    if missing:
        return dict(name=cl['name'], fail=f'segment decode fail {missing}')
    # gather keys
    chans_ok = 0
    chan_tot = 0
    vels = []
    wraps = []
    rng = np.random.default_rng(cl['i'])
    null_vels = []
    tmin, tmax = None, None
    for c in range(78):
        tt = None; vv = None
        for s in cov:
            st = seg_streams[s['k']]
            tw = st[2 * c].astype(np.int64)
            vw = st[2 * c + 1]
            nt = len(tw)
            if nt == 0: continue
            m = (tw >= ts) & (tw <= te)
            if not m.any(): continue
            k = m.sum()
            seg_t = tw[m]
            seg_v = vw.view('<f4').reshape(-1, 4)[:nt][m] if CH[c][1] != 1 else vw.view('<f4').reshape(-1, 3)[:nt][m]
            if tt is None:
                tt, vv = seg_t, seg_v
            else:
                mg = np.concatenate([tt, seg_t])
                o = np.argsort(mg, kind='stable')
                tt = mg[o]; vv = np.concatenate([vv, seg_v])[o]
        chan_tot += 1
        if tt is None or len(tt) < 2:
            continue
        chans_ok += 1
        tmin = tt[0] if tmin is None else min(tmin, tt[0])
        tmax = tt[-1] if tmax is None else max(tmax, tt[-1])
        if len(tt) >= 4 and CH[c][1] != 1:
            dt = np.diff(tt.astype(float))
            da = ang2(vv[1:], vv[:-1])
            m2 = dt > 0
            if m2.sum() >= 2:
                vels.append(np.quantile(da[m2] / dt[m2] * 1000, 0.95))
                sh = vv.copy(); rng.shuffle(sh)
                null_vels.append(np.quantile(ang2(sh[1:], sh[:-1])[m2] / dt[m2] * 1000, 0.95))
            wraps.append(float(ang2(vv[:1], vv[-1:])[0]))
    if chans_ok == 0:
        return dict(name=cl['name'], fail='no keys inside window', nseg=len(cov))
    ratio = (np.median(vels) / max(np.median(null_vels), 1e-9)) if vels else None
    return dict(name=cl['name'], i=cl['i'], ts=ts, te=te, dur=te - ts, nseg=len(cov),
                segs=[s['k'] for s in cov], chan_ok=chans_ok, chan_tot=chan_tot,
                data_span=[int(tmin), int(tmax)] if tmin is not None else None,
                span_ok=bool(tmin is not None and tmin >= ts - 60 and tmax <= te + 60),
                vel_ratio=round(float(ratio), 2) if ratio else None,
                wrap_med=round(float(np.median(wraps)), 1) if wraps else None,
                empty_gap=(te - ts) - (tmax - tmin) if tmin is not None else None)

rows = []
for cl in clips:
    rows.append(validate_clip(cl))

ok = [r for r in rows if 'fail' not in r]
fails = [r for r in rows if 'fail' in r]
print(f'clips decoded: {len(ok)}/921; failed: {len(fails)}')
fc = collections.Counter(r['fail'].split()[0] for r in fails)
print('failure causes:', dict(fc))
for r in fails[:12]:
    print('  ', r)

vr = [r['vel_ratio'] for r in ok if r['vel_ratio'] is not None]
print(f'\nsmoothness ratio (real/null, lower=structured): median {np.median(vr):.3f}, '
      f'p95 {np.quantile(vr, 0.95):.3f}, >1 count {sum(1 for v in vr if v > 1)}/{len(vr)}')
wm = [r['wrap_med'] for r in ok if r['wrap_med'] is not None]
print(f'wrap med: median {np.median(wm):.1f} deg, p90 {np.quantile(wm, 0.9):.1f}')
span_ok = sum(1 for r in ok if r['span_ok'])
print(f'data span within window(+60ms): {span_ok}/{len(ok)}')
nseg_hist = collections.Counter(r['nseg'] for r in ok)
print('segments-per-clip histogram:', dict(sorted(nseg_hist.items())))
dur0 = sum(1 for r in ok if r['dur'] == 0)
print(f'zero-duration clips: {dur0}')

def conv(o):
    if isinstance(o, dict): return {k: conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    return o
json.dump(conv(rows), open('/home/z/my-project/scripts/s35_t1_batch921.json', 'w'))
print('saved s35_t1_batch921.json')

# positive control: sneak walk
print('\n=== positive control _015_sneak_walk_front (clip 13) ===')
def conv(o):
    if isinstance(o, dict): return {k: conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    return o
r = conv(rows[13])
print(json.dumps(r, indent=1))
# gait clips sanity: walk/run rows
print('\nwalk row:', json.dumps(conv(rows[5]), indent=1))
print('run row:', json.dumps(conv(rows[6]), indent=1))
