#!/usr/bin/env python3
"""s51 T1a: decompose the mat73 GL-vs-Python gap: coverage vs per-pixel brightness."""
import numpy as np
from PIL import Image

W, H = 1024, 605
D = '/tmp/my-project/work/city_slice_wt/playable/'

for tag, gl, ref in [('mat73+LM', D + 's50_g_mat73.png', D + 's50_ref_mat73.png'),
                     ('mat73noLM', D + 's50_g_mat73_noLM.png', D + 's50_ref_mat73_noLM.png')]:
    try:
        G = np.asarray(Image.open(gl).convert('RGB'), np.float64)
        R = np.asarray(Image.open(ref).convert('RGB'), np.float64)
    except FileNotFoundError as e:
        print(tag, 'missing', e)
        continue
    gl_l = G.mean(axis=2)
    rf_l = R.mean(axis=2)
    # background = zero (mat-only renders start black)
    gcov = gl_l > 0
    rcov = rf_l > 0
    both = gcov & rcov
    only_g = gcov & ~rcov
    only_r = rcov & ~gcov
    print('%s: gl_cov=%d ref_cov=%d both=%d onlyGL=%d onlyRef=%d  ratio_cov=%.2f' %
          (tag, gcov.sum(), rcov.sum(), both.sum(), only_g.sum(), only_r.sum(),
           rcov.sum() / max(gcov.sum(), 1)))
    if both.sum():
        print('   mean|covered GL=%.2f ref=%.2f  ratio=%.2f' %
              (gl_l[both].mean(), rf_l[both].mean(), rf_l[both].mean() / max(gl_l[both].mean(), 1e-9)))
    if only_g.sum():
        print('   onlyGL mean=%.2f' % gl_l[only_g].mean())
    if only_r.sum():
        print('   onlyRef mean=%.2f' % rf_l[only_r].mean())
    # corr over union of coverage
    u = gcov | rcov
    a = gl_l[u]; b = rf_l[u]
    if a.std() > 0 and b.std() > 0:
        print('   corr(union)=%.4f' % np.corrcoef(a, b)[0, 1])
