#!/usr/bin/env python3
"""s45 T1a step 8: batch_info-as-texture-binding hypothesis test.

For known materials, get (diffuse_ordinal, lightmap_ordinal) from the compiled
image table via source.dae names, then scan the material's 196-byte batch_info
record for those byte values. Success = both values present at CONSISTENT slot
positions across materials; failure = model refuted.
"""
import numpy as np, io, zipfile, json

# --- image ordinal lookup from compiled table
P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)

def cstr(off):
    if not (0 < off < len(bres)):
        return ''
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > 120:
        return ''
    return bres[off:e].decode('ascii', 'replace')

IMG = 0x22a9c
tga2ord = {}
for i in range(176):
    a = IMG + i * 12
    tga = cstr(int(u32[a // 4 + 2]))
    tga2ord.setdefault(tga, i)

mats = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/mat_tex_GothamCity.json'))['mats']

# --- batch_info
bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
stride = int(np.frombuffer(bi[:4], '<u4')[0])
M = (len(bi) - 4) // stride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, stride)
print(f'batch_info: stride {stride}, M {M}')

tests = []
for m in (72, 73, 74, 90, 157, 302, 156, 2, 3, 250):
    mm = mats[m]
    d = tga2ord.get(mm['DiffuseMap'] or '')
    l = tga2ord.get(mm['LightMap'] or '')
    rec = recs[m]
    dpos = [int(j) for j in np.where(rec == (d if d is not None else 999))[0]] if d is not None else []
    lpos = [int(j) for j in np.where(rec == (l if l is not None else 999))[0]] if l is not None else []
    tests.append((m, mm['DiffuseMap'], d, dpos[:6], mm['LightMap'], l, lpos[:6]))
    print(f"mat {m:3d} diff={str(mm['DiffuseMap'])[:34]:34s} ord={d} slots={dpos[:6]}  light={str(mm['LightMap'])[:30]:30s} ord={l} slots={lpos[:6]}")

# verdict: do the diffuse/lightmap ordinals appear in their records at all?
hit_d = sum(1 for t in tests if t[3])
hit_l = sum(1 for t in tests if t[6])
print(f'\ndiffuse ordinal present in record: {hit_d}/{len(tests)}   lightmap ordinal present: {hit_l}/{len(tests)}')
