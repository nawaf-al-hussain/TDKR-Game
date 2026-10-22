#!/usr/bin/env python3
"""s51 T1i: check mip chain presence in shipped PVR textures (Roads0 etc.)."""
import struct, io, zipfile
import numpy as np

BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
ld = open(TEXGLA, 'rb').read()
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

# IMG table (N=176 @0x22a9c, 12B entries) -> names; find Roads0 + the mat73 diffuse + LightMapSampler
IMG_BASE, IMG_N = 0x22a9c, 176
imgs = [(int(w32[(IMG_BASE + i * 12) // 4]), int(w32[(IMG_BASE + i * 12 + 8) // 4])) for i in range(IMG_N)]
names = {}
for i in range(IMG_N):
    nm = cstr(imgs[i][1])
    if nm: names[nm] = i
print('img names sample:', [n for n in list(names)[:12]])
want = [n for n in names if any(k in n.lower() for k in ('roads', 'lightmap', 'htmap'))]
print('roads/lm names:', sorted(want)[:24])

# texture gla member lookup (same as s50 pyref tex_member)
def tex_member(wantname):
    # s50 logic: scan gla for member headers - replicate minimal version
    # members: 4B name-ptr? Use the known s50 approach: brute scan 8-byte aligned headers
    # simpler: the tex gla layout used before: [off=?,...] — reuse s50's exact code path
    raise NotImplementedError

# Instead of re-deriving, reuse s50 pyref functions by import
import importlib.util, sys, argparse
sys.argv = ['x']
spec = importlib.util.spec_from_file_location('pyref', '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_pyref.py')
# pyref runs argparse on import - can't. Read its tex_member source and exec the functions only.
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_pyref.py').read()
ns = {'__name__': 't1i'}
lines = src.splitlines(True)
keep = []
skip_until = None
for i, ln in enumerate(lines):
    if ln.startswith('ap = argparse') or ln.startswith('args = ap'):
        continue
    keep.append(ln)
code = ''.join(keep)
# stop execution at the first statement that does heavy work: find marker 'segdata = []'
cut = code.index('segdata = []')
code = code[:cut]
exec(compile(code, 'pyref_head', 'exec'), ns)
tm = ns['tex_member']

for nm in ['Roads0', 'Roads1', 'LightMapSampler', 'gothamcity_roads_details']:
    if nm not in names and nm != 'gothamcity_roads_details':
        print(nm, ': not in img table names'); continue
    u = tm(nm)
    if u is None:
        print(nm, ': no member'); continue
    try:
        parts = ns['unwrap_split'](u)
        key = 'rgb.pvr' if 'rgb.pvr' in parts else 'rgb'
        pvr = parts[key]
    except Exception as e:
        print(nm, ': unwrap err', e); continue
    # PVR3 header: ver(4) flags(4) pixfmt(8) colourspace(4) chdepth(4) order... h(4) w(4) mips(4)
    if pvr[:4] != b'PVR\x03':
        print(nm, ': not PVR3:', pvr[:4])
        continue
    h, w, mips = struct.unpack_from('<3I', pvr, 24 + 8)  # after 8B ver + 4B flags + 8B pixfmt = offset 24
    # precisely: 0 ver,4 flags,8..16 pixfmt,16 colourspace,20 chdepth,24 order?,28 h,32 w,36 mips
    fields = struct.unpack_from('<10I', pvr, 0)
    hh, ww, mipcount = fields[7], fields[8], fields[9]
    print('%-26s PVR3 %dx%d mips=%d size=%d' % (nm, ww, hh, mipcount, len(pvr)))
    if mipcount > 1:
        # compute total size for mips to sanity check
        total = 8 + sum(max(1, (ww >> l) // 4) * max(1, (hh >> l) // 4) * 8 for l in range(mipcount))
        print('   expected etc1 size (8B/block): %d' % total)
