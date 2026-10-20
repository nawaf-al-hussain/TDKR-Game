#!/usr/bin/env python3
"""S41 T2 recon: ZIP_SPLIT structure, RGB565/888/8888 layout calibration vs
deployed JPGs, mip-chain size semantics."""
import struct, zipfile, sys, io
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
ARCHS = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
         'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
         'l_policestation_tex.gla']

tot = 0
classes = {}
split_sample = None
samples = {}
for arch in ARCHS:
    d, ents = read_archive(Z, arch)
    for (name, off, size) in ents:
        tot += 1
        hdr = d[off:off + 52]
        if len(hdr) < 8:
            classes.setdefault('short', []).append((arch, name, size)); continue
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', hdr, 0)
        if hdr[:2] == b'PK':
            classes.setdefault('PK_SPLIT', []).append((arch, name, size, dsz))
            if split_sample is None:
                split_sample = (arch, name, off, size, d[off:off + 96])
            continue
        if hs != 52:
            classes.setdefault(f'hs{hs}', []).append((arch, name, size)); continue
        classes.setdefault(f'bpp{bpp}', []).append((arch, name, wid, hgt, mips, flags, dsz, size))
        if f'bpp{bpp}' not in samples or len(samples[f'bpp{bpp}']) < 3:
            samples.setdefault(f'bpp{bpp}', []).append((arch, name, off, wid, hgt, mips, flags, dsz, size))

print('total entries:', tot)
for k, v in sorted(classes.items()):
    print(f'{k}: {len(v)}')
print('\n--- ZIP_SPLIT sample:')
arch, name, off, size, raw = split_sample
print(arch, name, 'entry size', size)
print('first 96 bytes:', raw[:64].hex())
print('as text:', raw[:64])
# embedded zip: list members via zipfile on the slice
try:
    import zipfile as zf2
    emb = zf2.ZipFile(io.BytesIO(d[off:off + size]))
    print('embedded members:', emb.namelist())
    for n2 in emb.namelist():
        info = emb.getinfo(n2)
        print('  member', n2, 'size', info.file_size, 'compress', info.compress_type)
except Exception as e:
    print('embedded zip parse failed:', e)

print('\n--- non-ETC1 samples (arch,name,off,w,h,mips,flags,dsz,size):')
for k, v in samples.items():
    if k == 'bpp4': continue
    for row in v: print(k, row)

print('\n--- mip semantics (ETC1 samples: dsz vs sum-of-chain vs entry-size):')
for (arch, name, off, wid, hgt, mips, flags, dsz, size) in samples.get('bpp4', [])[:3]:
    w2, h2 = wid, hgt
    chain = 0
    lv = 0
    sizes = []
    while lv < mips and w2 > 0 and h2 > 0:
        s = ((w2 + 3) // 4) * ((h2 + 3) // 4) * 8
        sizes.append(s); chain += s
        w2 = max(1, w2 // 2); h2 = max(1, h2 // 2); lv += 1
    print(f'{name} {wid}x{hgt} mips={mips} dsz={dsz} chain={chain} entry={size} avail={size-52} sizes[:4]={sizes[:4]}')
