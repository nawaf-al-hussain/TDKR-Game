#!/usr/bin/env python3
"""S39b: dump PVR container region, locate true mip0, render endpoint image."""
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
body = d[off:off + size]

print('=== region [40, 340) hexdump (16B rows) ===')
for r in range(40, 340, 16):
    row = body[r:r + 16]
    print(f'{r:4d}: ' + ' '.join(f'{b:02x}' for b in row))

# candidate mip0 offsets: try 52 and 310 (0x136)
w = h = 256
for base in (52, 310):
    m = np.frombuffer(body[base:base + 32768], np.uint8).reshape(-1, 8)
    A = m[:, 0:3].reshape(64, 64, 3).astype(np.int16)
    dx = np.abs(np.diff(A, axis=1)).mean(); dy = np.abs(np.diff(A, axis=0)).mean()
    img = np.repeat(np.repeat(A.astype(np.uint8), 4, 0), 4, 1)
    s = img.astype(float).reshape(32, 8, 32, 8, 3).mean((1, 3)).mean(2)
    chars = ' .:-=+*#%@'
    print(f'== base {base}: endpoint dx={dx:.2f} dy={dy:.2f}')
    for r in range(0, 32, 2):
        print(''.join(chars[min(9, int(s[r, c] / 26))] for c in range(32)))
    Image.fromarray(img).save(f'/tmp/endpointA_base{base}.png')
