#!/usr/bin/env python3
"""s53 T1 offline analysis: remaining-gap decomposition of the fixed zone render.
Inputs (produced by s53_t1_run.py + s53_t1_cpurefs.sh):
  GL  : city_slice_wt/playable/s53_gl_zone_fix1.png          (bottom-up)
  CPU : city_slice_wt/playable/s50_ref_zbuf_snap.png          (top-down, s50 zbuf+snap reference)
  per-effect CPU refs : s53_ref_<FX>.png (zbuf+snap, family-only)
Outputs: s53_t1_gap.json + s53_t1_diffmap.png (grayscale |GL-CPU|, x4 amplification, top-down)
Sign conventions:
  diff = |GL - CPU| mean-RGB bytes; coverage pixel = mean RGB > 8
  covdiff  : coverage status differs (GL XOR CPU)
  valdiff  : both covered, |diff| > 32 (values differ materially)
  family attribution: a diff pixel is attributed to family F iff exactly one family ref covers it
"""
import json, numpy as np
from PIL import Image

WT = '/tmp/my-project/work/city_slice_wt/playable/'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session53/'
FAMILIES = ['LightMapDC', 'AlphaMasking', 'SimpleAdditive', 'StandardDiffuseDC', 'other']

gl = np.asarray(Image.open(WT + 's53_gl_zone_fix1.png').convert('RGB'), np.float64)[::-1]
cpu = np.asarray(Image.open(WT + 's50_ref_zbuf_snap.png').convert('RGB'), np.float64)
assert gl.shape == cpu.shape, (gl.shape, cpu.shape)
gm = gl.mean(axis=2); rm = cpu.mean(axis=2)
d = np.abs(gm - rm)
gcm = gm > 8; rcm = rm > 8
both = gcm & rcm
covdiff = gcm ^ rcm
valdiff = both & (d > 32)
valbig = both & (d > 64)

# family label maps from per-effect CPU refs (exclusive attribution)
cov_any = np.zeros_like(gcm)
label = np.full(gm.shape, -1, np.int16)   # -1 = none/ambiguous
n_cov = np.zeros(gm.shape, np.int8)
for i, fx in enumerate(FAMILIES):
    p = WT + 's53_ref_%s.png' % fx
    try:
        f = np.asarray(Image.open(p).convert('RGB'), np.float64).mean(axis=2) > 8
    except FileNotFoundError:
        continue
    n_cov += f
    cov_any |= f
label[n_cov == 1] = -2   # marker: exactly one family (resolve below)
# resolve exclusive labels
for i, fx in enumerate(FAMILIES):
    p = WT + 's53_ref_%s.png' % fx
    try:
        f = np.asarray(Image.open(p).convert('RGB'), np.float64).mean(axis=2) > 8
    except FileNotFoundError:
        continue
    excl = f & (n_cov == 1)
    label[excl] = i

attr = {'uncovered_by_any_family_ref': int((cov_any == 0).sum()),
        'multi_family_overlap': int((n_cov > 1).sum()),
        'exclusive': int((n_cov == 1).sum())}
fam_stats = {}
for i, fx in enumerate(FAMILIES):
    m = (label == i)
    if m.sum() == 0:
        fam_stats[fx] = {'px': 0}
        continue
    fam_stats[fx] = {
        'px': int(m.sum()),
        'covdiff_px': int((m & covdiff).sum()),
        'valdiff_px': int((m & valdiff).sum()),
        'valbig_px': int((m & valbig).sum()),
        'mean_absdiff': round(float(d[m].mean()), 2),
        'gl_mean': round(float(gm[m].mean()), 2),
        'cpu_mean': round(float(rm[m].mean()), 2)}

# diff map PNG (top-down, amplified)
amp = np.clip(d * 4, 0, 255).astype(np.uint8)
Image.fromarray(amp).save(OUTDIR.replace('session53/', '') + '/session53/s53_t1_diffmap.png')

out = {
 'sign_convention': {'diff': '|GL-CPU| mean-RGB bytes; covdiff = coverage differs; valdiff = both covered & diff>32'},
 'totals': {
   'gl_cov_px': int(gcm.sum()), 'cpu_cov_px': int(rcm.sum()),
   'shared_px': int(both.sum()), 'iou': round(float(both.sum()) / max(1, (gcm | rcm).sum()), 4),
   'covdiff_px': int(covdiff.sum()),
   'covdiff_gl_only': int((gcm & ~rcm).sum()), 'covdiff_cpu_only': int((rcm & ~gcm).sum()),
   'valdiff_px': int(valdiff.sum()), 'valbig_px': int(valbig.sum()),
   'corr_shared': round(float(np.corrcoef(gm[both], rm[both])[0, 1]), 4),
   'gl_mean_shared': round(float(gm[both].mean()), 2), 'cpu_mean_shared': round(float(rm[both].mean()), 2),
   'ratio_shared': round(float(gm[both].mean() / max(rm[both].mean(), 1e-9)), 4)},
 'family_attribution': attr, 'per_family': fam_stats}
json.dump(out, open(OUTDIR + 's53_t1_gap.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
