#!/usr/bin/env python3
"""s51 T1f: gradient-probe analysis, LM-free version (raw texel coords)."""
import numpy as np
from PIL import Image

WT = '/tmp/my-project/work/city_slice_wt/playable/'
gl = np.load(WT + 's51_g_mat73_gradnolm.npy')
ref = np.asarray(Image.open(WT + 's51_ref_mat73_gradnolm.png').convert('RGB'), np.float64)
T = 512
gtx, gty = gl[..., 0] / 2.0, gl[..., 1] / 2.0
rtx, rty = ref[..., 0] / 2.0, ref[..., 1] / 2.0
both = (gl.mean(axis=2) > 8) & (ref.mean(axis=2) > 8)
print('shared:', both.sum())
for nm, a in (('ref ty', rty[both]), ('gl ty', gty[both]), ('ref tx', rtx[both]), ('gl tx', gtx[both])):
    print('%s: mean %.1f med %.1f p10 %.1f p90 %.1f' % (nm, a.mean(), np.median(a), *np.percentile(a, [10, 90])))

def wrapdiff(a, b, T=512):
    d = a - b
    return (d + T / 2) % T - T / 2

ty_r, ty_g, tx_r, tx_g = rty[both], gty[both], rtx[both], gtx[both]
print('identical |d| med: tx %.1f ty %.1f' % (np.median(np.abs(wrapdiff(tx_g, tx_r))),
                                              np.median(np.abs(wrapdiff(ty_g, ty_r)))))
A = np.stack([ty_r, np.ones_like(ty_r)], axis=1)
sol, *_ = np.linalg.lstsq(A, ty_g, rcond=None)
print('fit ty_g = %.4f * ty_r + %.1f' % (sol[0], sol[1]))
A2 = np.stack([tx_r, np.ones_like(tx_r)], axis=1)
sol2, *_ = np.linalg.lstsq(A2, tx_g, rcond=None)
print('fit tx_g = %.4f * tx_r + %.1f' % (sol2[0], sol2[1]))
# correlation of coordinates
print('corr(tx_g, tx_r) %.3f  corr(ty_g, ty_r) %.3f' % (np.corrcoef(tx_g, tx_r)[0, 1], np.corrcoef(ty_g, ty_r)[0, 1]))
