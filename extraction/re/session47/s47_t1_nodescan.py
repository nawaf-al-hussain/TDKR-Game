#!/usr/bin/env python3
"""s47 T1 FINAL: scan the whole compiled DB for value-node patterns
{X, 0xff, 0xff, 0xff, 0xff, 0xffffffff} (u32 x6). X = image index (0..175)
means a REAL binding; X = 0xffffffff (-1) means 'no image' (postLoadProcess
writes 0 -> constructImage skipped). Also verify the s46 walk population:
all 651 sampler setparam value nodes across the 307 materials."""
import io, zipfile, json
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
u32 = np.frombuffer(LE, '<u4', NB // 4)

FF = 0x000000ff
TERM = 0xffffffff
hits_real, hits_none = [], []
for k in range(NB // 4 - 6):
    if int(u32[k]) == TERM and all(int(u32[k - j]) == FF for j in (1, 2, 3, 4)):
        x = int(u32[k - 5])
        if x == TERM:
            hits_none.append(k * 4 - 20)
        elif 0 <= x < 176:
            hits_real.append((k * 4 - 20, x))
print('value nodes with real image index (0..175):', len(hits_real), hits_real[:12])
print('value nodes with -1 (none):', len(hits_none))
# node pattern may also appear with fewer/more ff words; try 4-word ff run only
runs = 0
for k in range(NB // 4 - 4):
    if all(int(u32[k + j]) == FF for j in range(4)):
        runs += 1
print('raw 4x-0xff u32 runs:', runs)

# verify s46 walk: all sampler value nodes -1
d = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session46/s46_t1_setparam_walk.json'))
tot = sam = none_cnt = real = 0
for mat in d:
    for prm in mat.get('params', []):
        if prm.get('type') == 13:
            tot += 1
            v2w = prm.get('v2_words')
            if v2w and v2w[5] == 4294967295:
                none_cnt += 1
            elif v2w and v2w[5] < 176:
                real += 1
            else:
                sam += 1
print(f's46 walk sampler setparams: total {tot}, node==-1 {none_cnt}, node<176 {real}, other {sam}')

# the ff*16B payload semantics: sampler value node = {idx, 4x0xff} + terminal
# for node 73 bytes: 0x3fe6c holds -1 (LightMap), 0x3fe88 holds -1 (DiffuseMap)
for a in (0x3fe6c, 0x3fe88):
    print(hex(a), [hex(int(u32[(a + j) // 4])) for j in (0, 4, 8, 12, 16, 20)])
