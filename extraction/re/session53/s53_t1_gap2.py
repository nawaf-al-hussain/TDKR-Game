#!/usr/bin/env python3
"""s53 T1 per-effect gap analysis (final).
Label maps: flat zbuf+snap per-family renders (s53_lab_<FX>.png, geometry-only).
Assignment: pixels covered by several family labels (3.2%) go to the SMALLER family first
(priority order AlphaMasking, StandardDiffuseDC, SimpleAdditive, other, LightMapDC).
Per-effect corr = Pearson r of per-pixel mean RGB between the GL zone dump (fix=1) and the
s50 CPU zbuf+snap reference, over {label==fx} AND both-covered. Same restriction for the
WRONGLM dump = per-effect calibration (the metric must move for LightMapDC).
Sign conventions: corr 1 = agreement; ratio = GL/CPU covered-mean; wronglm must lower corr."""
import json, numpy as np
from PIL import Image

WT = '/tmp/my-project/work/city_slice_wt/playable/'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session53/'
FAM = ['AlphaMasking', 'StandardDiffuseDC', 'SimpleAdditive', 'other', 'LightMapDC']  # priority order

gl = np.asarray(Image.open(WT + 's53_gl_zone_fix1.png').convert('RGB'), np.float64)[::-1]
cpu = np.asarray(Image.open(WT + 's50_ref_zbuf_snap.png').convert('RGB'), np.float64)
glw = np.asarray(Image.open(WT + 's53_gl_zone_wronglm.png').convert('RGB'), np.float64)[::-1]
gm = gl.mean(axis=2); rm = cpu.mean(axis=2); gwm = glw.mean(axis=2)
gcm = gm > 8; rcm = rm > 8
both = gcm & rcm
d = np.abs(gm - rm)

label = np.full(gm.shape, -1, np.int16)
ncov = np.zeros(gm.shape, np.int8)
for i, fx in enumerate(FAM):
    a = np.asarray(Image.open(WT + 's53_lab_%s.png' % fx).convert('RGB'), np.float64).mean(axis=2) > 8
    ncov += a
    m = a & (label < 0)
    label[m] = i
overlap_px = int((ncov > 1).sum())

out = {'sign_convention': {'corr': 'Pearson r per-pixel mean RGB, label AND both-covered',
                           'ratio': 'GL/CPU covered-mean within the label',
                           'calibration': 'wronglm dump must lower corr for LightMapDC labels; small families may be n-limited'},
        'overlap_px': overlap_px, 'per_effect': {}}
for i, fx in enumerate(FAM):
    m = (label == i) & both
    rec = {'label_px': int((label == i).sum())}
    if m.sum() > 20:
        a = gm[m]; b = rm[m]; w = gwm[m]
        rec.update({'n': int(m.sum()),
                    'gl_mean': round(float(a.mean()), 2), 'cpu_mean': round(float(b.mean()), 2),
                    'ratio': round(float(a.mean() / max(b.mean(), 1e-9)), 4),
                    'corr': round(float(np.corrcoef(a, b)[0, 1]), 4),
                    'wronglm_corr': round(float(np.corrcoef(w, b)[0, 1]), 4),
                    'wronglm_ratio': round(float(w.mean() / max(b.mean(), 1e-9)), 4),
                    'valdiff_px': int((m & (d > 32)).sum())})
    else:
        rec['n'] = int(m.sum()); rec['note'] = 'n too small for corr'
    out['per_effect'][fx] = rec
    print(fx, rec, flush=True)

# the covdiff/valdiff totals (same as s53_t1_gap.json, kept for one-file convenience)
out['totals'] = {'shared_px': int(both.sum()), 'iou': round(float(both.sum()) / max(1, (gcm | rcm).sum()), 4),
                 'corr_shared': round(float(np.corrcoef(gm[both], rm[both])[0, 1]), 4),
                 'covdiff_px': int((gcm ^ rcm).sum()), 'valdiff_px': int((both & (d > 32)).sum())}
json.dump(out, open(OUTDIR + 's53_t1_pereffect.json', 'w'), indent=1)
print('saved', OUTDIR + 's53_t1_pereffect.json')
