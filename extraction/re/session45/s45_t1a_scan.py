#!/usr/bin/env python3
"""s45 T1a: structural scan of little_endian_not_quantized.bdae for per-material sampler records.

Anchors from s43/s44: 176 textures, 305 dae materials, mat73 diffuse = image56
(gothamcity_roads_details.tga), u32-dense back region 0x23308..0x6f164,
effect defs 0x23e2c/0x2cd60, image ptr table ~0x22d04.

Probes:
  A. GL enum search (0x2901 REPEAT, 0x812F CLAMP_TO_EDGE, 0x2900 CLAMP,
     0x2600/0x2601 filters, 0x2703 LINEAR_MIPMAP_LINEAR) both endians.
  B. Fine u32 density map of the back region (windows of 16 u32, >=12 hits <176).
  C. Record-stride autocorrelation inside dense regions.
  D. 305x10 f32 table search (consecutive plausible floats).
  E. mat73 anchor: all offsets where u16/u32 == 56 in dense regions, with
     neighborhood structure (is 56 preceded/followed by stable patterns?).
"""
import struct, io, zipfile, json
import numpy as np

def load_bres():
    for P in ('/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae',
              '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'):
        try:
            raw = open(P, 'rb').read()
            if raw[:2] == b'PK':
                return zipfile.ZipFile(io.BytesIO(raw)).read('little_endian_not_quantized.bdae')
            # gla member container
            _, idxsz, tabsz, n = struct.unpack('>IIII', raw[:16])
            pool = raw[16 + n * 16:idxsz]
            for i in range(n):
                o, s, no, _ = struct.unpack('>IIII', raw[16 + i * 16:16 + i * 16 + 16])
                nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
                if nm == 'GothamCity_materials.bdae':
                    return zipfile.ZipFile(io.BytesIO(raw[o:o + s])).read('little_endian_not_quantized.bdae')
        except FileNotFoundError:
            continue
    raise SystemExit('no source found')

bres = load_bres()
print('bres size:', len(bres), hex(len(bres)))
NT = 176  # texture universe
NM = 305  # dae materials

# --- A. GL enum search
enums = {'GL_REPEAT': 0x2901, 'GL_CLAMP': 0x2900, 'GL_CLAMP_TO_EDGE': 0x812F,
         'GL_MIRRORED_REPEAT': 0x8370, 'GL_NEAREST': 0x2600, 'GL_LINEAR': 0x2601,
         'GL_NEAREST_MIPMAP_NEAREST': 0x2700, 'GL_LINEAR_MIPMAP_NEAREST': 0x2701,
         'GL_NEAREST_MIPMAP_LINEAR': 0x2702, 'GL_LINEAR_MIPMAP_LINEAR': 0x2703}
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)
be32 = np.frombuffer(bres, '>u4', len(bres) // 4)
for name, v in enums.items():
    le = np.where(u32 == v)[0]
    be = np.where(be32 == v)[0]
    if len(le) or len(be):
        print(f'{name} {hex(v)}: LE x{len(le)} at {[hex(x*4) for x in le[:10]]}'
              f'  BE x{len(be)} at {[hex(x*4) for x in be[:10]]}')

# --- B. fine u32 density in back region
lo, hi = 0x23308, min(0x6f164, len(bres))
w = (hi - lo) // 4
vals = u32[lo // 4:hi // 4]
small = (vals < NT)
win = 16
nwin = len(small) // win
dens = small[:nwin * win].reshape(nwin, win).sum(1)
th = np.where(dens >= 12)[0]
if len(th):
    # group consecutive windows into regions
    groups = []
    s = th[0]; p = th[0]
    for t in th[1:]:
        if t == p + 1:
            p = t
        else:
            groups.append((s, p)); s = p = t
    groups.append((s, p))
    print(f'\nback-region dense sub-regions (>=12/16 u32 < {NT}):')
    for a, b in groups[:40]:
        print(f'  {hex(lo + a * 64)}..{hex(lo + b * 64 + 64)}  ({(b - a + 1) * 64} B)')

# --- C. stride autocorrelation on 'small' indicator inside the biggest dense area
def autocorr(ind, maxlag=80):
    best = []
    n = len(ind)
    for lag in range(2, maxlag + 1):
        agree = np.mean(ind[lag:] == ind[:-lag])
        best.append((agree, lag))
    best.sort(reverse=True)
    return best[:6]

for a, b in groups[:6]:
    seg = small[(a * 16):(b + 1) * 16]
    if len(seg) > 400:
        print(f'autocorr in {hex(lo + a * 64)}..{hex(lo + b * 64 + 64)}:', 
              [(f'lag {l} ({l*4}B)', round(ag, 3)) for ag, l in autocorr(seg)])

# --- D. 305x10 float table
f32 = np.frombuffer(bres, '<f4', len(bres) // 4)
plaus = np.isfinite(f32) & ((np.abs(f32) < 16) | (f32 == 0))
win = 10 * 40  # 40 records worth
nwin = len(plaus) - win
hits = np.convolve(plaus.astype(np.int32), np.ones(win, dtype=np.int32), 'valid')
best = np.argsort(hits)[-6:][::-1]
print('\ntop plausible-float windows (380 floats):')
for i in best:
    if hits[i] > win * 0.8:
        print(f'  {hex(i*4)}: {hits[i]}/{win}')

# --- E. mat73 anchor: u32==56 offsets inside back region
fiftysix = np.where((u32[lo//4:hi//4] == 56))[0]
print(f'\nu32==56 in back region: {len(fiftysix)} hits')
# histogram of gaps between consecutive hits
if len(fiftysix) > 10:
    gaps = np.diff(fiftysix) * 4
    import collections
    common = collections.Counter(gaps).most_common(8)
    print('  most common gaps (bytes):', [(g, c) for g, c in common])
    print('  first hits at:', [hex(lo + h * 4) for h in fiftysix[:16]])
