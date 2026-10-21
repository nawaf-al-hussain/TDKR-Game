#!/usr/bin/env python3
"""s47 T1 step G: decode node 73's compiled technique/profile region and
hunt for image references (indices 0..175 or pointers into the image table)
in sampler/newparam value positions. Node 73 anchor: authoring table binds
DiffuseMap -> roads_details (image56) and LightMap -> Roads0 (image6)."""
import io, zipfile, struct
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
u32 = np.frombuffer(LE, '<u4', NB // 4)
u16 = np.frombuffer(LE, '<u2', NB // 2)

def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = LE.find(b'\0', off)
    if e < 0 or e == off or e - off > maxn:
        return None
    s = LE[off:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

# image table
IMG_BASE, IMG_N = 0x22a9c, 176
imgs = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    imgs.append((i, int(w[0]), int(w[2])))
img_by_name = {}
for i, nm, tg in imgs:
    img_by_name[nm] = i
    img_by_name[tg] = i
print('images 0..3:', [(i, cstr(nm), cstr(tg)) for i, nm, tg in imgs[:4]])
print('image56:', cstr(imgs[56][1]), '/', cstr(imgs[56][2]),
      '| image6:', cstr(imgs[6][1]), '/', cstr(imgs[6][2]))

# node 73 record
BASE, REC = 0x23308, 260
a73 = BASE + 73 * REC
ws = [int(u32[(a73 + k * 4) // 4]) for k in range(REC // 4)]
print('node73 words[0..20]:', [hex(x) for x in ws[:21]])
print('node73 eff name:', cstr(ws[63]))

def ann(v):
    s = cstr(v)
    if s:
        return f'"{s}"'
    if v in img_by_name:
        i = img_by_name[v]
        return f'<IMG{i}:{cstr(imgs[i][1])}>'
    return ''

def dump(a, b, label):
    print(f'--- {label} {a:#x}..{b:#x} ---')
    for off in range(a, b, 4):
        v = int(u32[off // 4])
        f = struct.unpack('<f', struct.pack('<I', v))[0]
        extra = ann(v)
        fs = f' (f={f:.4g})' if extra == '' and 1e-4 < abs(f) < 1e6 else ''
        print(f'  {off:#07x}: {v:#010x}{extra}{fs}')

# technique list region of node 73: ws[13]=(0x3fc9c,3)
dump(0x3fc9c, 0x3fe0c, 'node73 techniques x3 + setparam x2')
