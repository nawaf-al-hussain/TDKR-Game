#!/usr/bin/env python3
"""s45 T1a step 5: full annotated dump of rec73's pointer graph + image array bounds."""
import numpy as np, io, zipfile

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)
f32 = np.frombuffer(bres, '<f4', len(bres) // 4)
u16 = np.frombuffer(bres, '<u2', len(bres) // 2)

def cstr(off):
    if not (0 < off < len(bres)):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e - off > 96 or e == off:
        return None
    s = bres[off:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def dump(a, b, label):
    print(f'--- {label} {a:#x}..{b:#x} ---')
    for off in range(a, b, 4):
        v = int(u32[off // 4])
        s = cstr(v)
        note = f" -> {s!r}" if s else ''
        fv = float(f32[off // 4])
        if not s and 1e-4 < abs(fv) < 1e6:
            note += f'  f={fv:.5g}'
        # small int annotation
        if not s and 0 < v < 4096:
            note += f'  i={v}'
        print(f'  {off:#07x}: {v:#010x}{note}')

# image triple array: find exact start by scanning back from image50's proven triple
print('=== S3/S4 boundary region 0x22a60..0x22ac0 ===')
dump(0x22a60, 0x22ac0, 'img array start hunt')
# rec73 full span: from slot13 target to slot17 target end
dump(0x3fc00, 0x3fd40, 'rec73 block A region')
dump(0x3fe00, 0x3fec0, 'rec73 block B region')
