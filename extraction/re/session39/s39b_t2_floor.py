#!/usr/bin/env python3
"""S39b: (1) pure-data mip floor: LUT-inverse endpoint images ds2-vs-mip1 RMSE.
(2) contrast-stretched ASCII of the morton 'same' decode -> gargoyle visible?
(3) byte3 full histogram + joint stats with A/mod.
"""
import struct, zipfile, json
import numpy as np
from PIL import Image

RE = '/tmp/my-project/work/TDKR-Game/extraction/re'
GA = np.array([0, 16, 33, 49, 66, 82, 99, 115, 140, 156, 173, 189, 206, 222, 239, 255])
BA = np.array([0, 33, 74, 107, 156, 189, 222, 255])
A4 = np.array([0, 34, 68, 102, 136, 170, 204, 238, 255, 255, 255, 255, 255, 255, 255, 255])

def inv_lut(lut, val):
    # nearest LUT entry for each 0..255 value
    lut8 = np.array(lut, np.int16)
    idx = np.argmin(np.abs(lut8[None, :] - np.arange(256)[:, None]), axis=1)
    return idx[np.clip(val, 0, 255)]

z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/actors_tex.gla')
n = struct.unpack_from('>I', d, 12)[0]
pool = 16 + n * 16
ents = {}
for i in range(n):
    o = 16 + i * 16
    off, size, nameOff = struct.unpack_from('>3I', d, o)
    nb = pool + nameOff
    e = d.index(b'\0', nb)
    ents[d[nb:e].decode('latin1')] = (off, size)
off, size = ents['GC_StockExchange_Gargoyle.tga']
mip0 = np.frombuffer(d[off + 52:off + 52 + 32768], np.uint8).reshape(-1, 8)
mip1 = np.frombuffer(d[off + 52 + 32768:off + 52 + 40960], np.uint8).reshape(-1, 8)

# (1) pure-data floor: invert LUTs on endpoint bytes, ds2 vs mip1
A0 = mip0[:, 0:3].reshape(64, 64, 3)
A1 = mip1[:, 0:3].reshape(32, 32, 3)
r0 = inv_lut(GA, A0[..., 0]); g0 = inv_lut(GA, A0[..., 1]); b0 = inv_lut(BA, A0[..., 2])
r1 = inv_lut(GA, A1[..., 0]); g1 = inv_lut(GA, A1[..., 1]); b1 = inv_lut(BA, A1[..., 2])
ds = np.stack([r0, g0, b0], -1).astype(np.float64)
ds = ds.reshape(32, 2, 32, 2, 3).mean((1, 3))
ref = np.stack([r1, g1, b1], -1).astype(np.float64)
rmse_pure = float(np.sqrt(((ds - ref) ** 2).mean()))
print(f'(1) PURE-DATA mip floor (LUT-inverse endpoints): RMSE={rmse_pure:.2f}')
ds888 = A0.astype(np.float64).reshape(32, 2, 32, 2, 3).mean((1, 3))
print(f'    raw-888 endpoints ds2-vs-mip1: RMSE={np.sqrt(((ds888 - A1) ** 2).mean()):.2f}')

# (2) render the morton 'same' decode with contrast stretch
img = np.asarray(Image.open(f'{RE}/session39/s39b_best_same_morton.png').convert('L')).astype(float)
lo, hi = np.percentile(img, [2, 98])
st = np.clip((img - lo) / max(hi - lo, 1) * 255, 0, 255)
chars = ' .:-=+*#%@'
s = st.reshape(32, 8, 32, 8).mean((1, 3))
print('(2) decoded (morton, B=A) contrast-stretched:')
for r in range(0, 32, 2):
    print(''.join(chars[min(9, int(s[r, c] / 26))] for c in range(32)))
Image.fromarray(st.astype(np.uint8)).save(f'{RE}/session39/s39b_best_same_stretch.png')

# endpoint image stretched too
e0 = A0.mean(2).astype(float)
lo, hi = np.percentile(e0, [2, 98])
st2 = np.clip((e0 - lo) / max(hi - lo, 1) * 255, 0, 255)
s2 = st2.reshape(32, 2, 32, 2).mean((1, 3))
print('    endpoint-A image stretched:')
for r in range(0, 32, 2):
    print(''.join(chars[min(9, int(s2[r, c] / 26))] for c in range(32)))

# (3) byte3 histogram + joint stats
b3 = mip0[:, 3]
vals, cnts = np.unique(b3, return_counts=True)
print('(3) byte3: unique', len(vals), 'top:', sorted(zip(cnts, vals), reverse=True)[:12])
modw = mip0[:, 4:8]
print('    P(flags) vs A-grey corr:', np.corrcoef(b3.astype(float), A0[..., 0].astype(float).ravel())[0, 1].round(3))
nzero = int((mip0[:, 4:8] == 0).all(1).sum())
nff = int((mip0[:, 4:8] == 255).all(1).sum())
print('    blocks with mod==0:', nzero, ' mod==FF..:', nff, 'of', len(mip0))
