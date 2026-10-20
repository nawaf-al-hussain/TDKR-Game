#!/usr/bin/env python3
"""S39b: render endpoint-A image + dump .tga header to validate geometry."""
import struct, zipfile
import numpy as np
from PIL import Image

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
print('entry off', hex(off), 'size', size)
hdr = d[off:off + 64]
print('header hex:', ' '.join(f'{b:02x}' for b in hdr))
w, h = struct.unpack_from('<II', d, off + 4)
print('w,h @+4 =', w, h)
for extra in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48):
    vals = struct.unpack_from('<4I', d, off + extra)
    print(f'  +{extra}: {[hex(v) for v in vals]}')
body = d[off + 52: off + 52 + size] if size < 100000 else d[off + 52: off + 52 + 100000]
print('bytes after +52 available:', len(d) - off - 52, 'expected mip0 32768; size-sizeof(hdr)?', size - 52)

mip0 = np.frombuffer(d[off + 52:off + 52 + 32768], np.uint8).reshape(-1, 8)
A = mip0[:, 0:3].reshape(h // 4, w // 4, 3)
img = np.repeat(np.repeat(A, 4, axis=0), 4, axis=1)
Image.fromarray(img.astype(np.uint8)).save('/tmp/endpointA_256.png')
s = img.reshape(32, 8, 32, 8, 3).mean((1, 3)).mean(3)
chars = ' .:-=+*#%@'
print('endpoint-A image (block colors):')
for r in range(0, 32, 2):
    print(''.join(chars[min(9, int(s[r, c] / 26))] for c in range(32)))

# also try: data starting at +48 or +56, in case 52 is off
for delta in (48, 56):
    m = np.frombuffer(d[off + delta:off + delta + 32768], np.uint8).reshape(-1, 8)
    Ae = m[:, 0:3].reshape(h // 4, w // 4, 3)
    img2 = np.repeat(np.repeat(Ae, 4, 0), 4, 1)
    dx1 = np.abs(np.diff(A.astype(np.int16), axis=1)).mean()
    print(f'delta {delta}: endpoint xsmooth={dx1:.2f}')
dx = np.abs(np.diff(A.astype(np.int16), axis=1)).mean()
dy = np.abs(np.diff(A.astype(np.int16), axis=0)).mean()
print(f'endpoint smooth @52: dx={dx:.2f} dy={dy:.2f}')
