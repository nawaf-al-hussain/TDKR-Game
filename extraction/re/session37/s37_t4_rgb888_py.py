#!/usr/bin/env python3
"""S37 T4.2b: Batman DIFFUSE (RGB888, no mips) -> python decode to RGBA;
write the source strip for the JS decoder to compare pixel-by-pixel."""
import zipfile, struct, json
import numpy as np

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
off, size = ents['chara_Batman_DIFFUSE.tga']
w, h = struct.unpack_from('<II', d, off + 4)
data = d[off + 52:off + size]
assert len(data) == w * h * 3, (len(data), w, h)
rgb = np.frombuffer(data, np.uint8).reshape(h, w, 3)
rgba = np.dstack([rgb, np.full((h, w), 255, np.uint8)])
print(f'Batman DIFFUSE: {w}x{h} RGB888; mean {rgb.reshape(-1,3).mean(0).round(1)} '
      f'std {rgb.reshape(-1,3).std(0).round(1)}')
# plausibility: distinct colors
uc = len(np.unique(rgb.reshape(-1, 3), axis=0))
print('distinct colors:', uc, f'({100*uc/(w*h):.2f}% of pixels)')
rgba.tofile('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_batman_diffuse_py.bin')
open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_batman_diffuse_src.bin', 'wb').write(data)
json.dump({'w': w, 'h': h}, open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_batman_diffuse_meta.json', 'w'))
print('saved py decode + source strip for JS compare')
