#!/usr/bin/env python3
"""s46 T1: full annotated dump of the technique/setparam/value-struct regions
for nodes 73 and 70, to establish the TRUE compiled schema."""
import io, zipfile
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(bres)
u32 = np.frombuffer(bres, '<u4', NB // 4)
f32 = np.frombuffer(bres, '<f4', NB // 4)
u16 = np.frombuffer(bres, '<u2', NB // 2)

def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > maxn:
        return None
    s = bres[off:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

IMG_BASE, IMG_N = 0x22a9c, 176
imgs = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    imgs.append((int(w[0]), int(w[2])))  # name_ptr, tga_ptr
img_map = {}
for i, (nm, tg) in enumerate(imgs):
    img_map[nm] = ('imgname', i)
    img_map[tg] = ('tga', i)

def ann(v):
    parts = []
    s = cstr(v)
    if s:
        parts.append(f'"{s}"')
    if v in img_map:
        parts.append(f'<<{img_map[v][0]}{img_map[v][1]}>>')
    if 0 < v < NB:
        # in-file pointer: peek one u32
        t = int(u32[v // 4])
        s2 = cstr(t)
        if s2:
            parts.append(f'->"{s2}"')
        elif v in img_map:
            pass
    fv = float(f32[min(v // 4, len(f32) - 1)]) if v >= 4 else 0.0
    if not parts and 1e-4 < abs(fv) < 1e6:
        parts.append(f'f={fv:.5g}')
    return (' [' + ' '.join(parts) + ']') if parts else ''

def dump(a, b, label):
    print(f'--- {label} {a:#x}..{b:#x} ---')
    for off in range(a, b, 4):
        v = int(u32[off // 4])
        print(f'  {off:#07x}: {v:#010x}{ann(v)}')

if __name__ == '__main__':
    # node70 lists: setparam {0x3f8e0?, ...} -> recompute from node words
    BASE, REC = 0x23308, 260
    for i in (70, 73):
        a = BASE + i * REC
        ws = [int(u32[(a + k * 4) // 4]) for k in range(REC // 4)]
        print(f'node {i}: tech=({ws[13]:#x},{ws[14]}) setparam=({ws[15]:#x},{ws[16]}) '
              f'rstate=({ws[17]:#x},{ws[18]}) eff={cstr(ws[63])!r}')
    print()
    dump(0x3f8e0, 0x3fc9c, 'node70 setparam+values (setparam list @0x3f8e0? x?)')
    dump(0x3fc9c, 0x3ffc0, 'node73 technique list 0x3fc9c x3 + setparam 0x3fe0c x2 + values')
