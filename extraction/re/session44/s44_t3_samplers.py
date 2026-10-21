#!/usr/bin/env python3
"""s44 T3a: hunt the per-material sampler records in little_endian_not_quantized.bdae.

Known anchors (s43): texture name pool @0x1c704+, tga<->image triples @0x229b4+,
shader reflection {name,type,slot,0xffff} @0x36c78, effect defs @0x23e2c/0x2cd60,
uniform/sampler name pool @0x18b40+. Missing: the per-material records binding
sampler slots to texture indices + uv scale/offset.

Strategy:
1. Enumerate candidate texture-index words: u16/u32 values in [0,176) at high
   density -> find the record array(s).
2. For each candidate region, estimate the record stride by autocorrelation of
   "value < 176" hits; check count ~ 305/307 (or a small multiple: samplers per
   material).
3. Read float pairs inside the records (scale/offset candidates in [0,8]).
"""
import struct, io, zipfile, json
import numpy as np

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity_materials.bdae' or nm.endswith('materials.bdae'):
        print('member:', nm, s)
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        bres = Z.read('little_endian_not_quantized.bdae')
        break
else:
    bres = None
    print('materials member not found in this gla; trying direct file')
if bres is None:
    bres = open('/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae', 'rb').read()
    bres = zipfile.ZipFile(io.BytesIO(bres)).read('little_endian_not_quantized.bdae')
print('bres size:', len(bres))

# texture universe names from s43 (176) — rebuild from the pool at 0x1c704 region:
# just take the count 176 as the index bound.
NT = 176
b = np.frombuffer(bres, np.uint8)
u16 = np.frombuffer(bres, '<u2', len(bres) // 2)
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)

def density_runs(vals, bound, minrun, stride=1):
    ok = vals < bound
    # find runs of dense hits
    runs = []
    start = None
    gap = 0
    for i in range(len(ok)):
        if ok[i]:
            if start is None:
                start = i
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap > 64:
                    if i - gap - start >= minrun:
                        runs.append((start, i - gap))
                    start = None
    if start is not None and len(ok) - start >= minrun:
        runs.append((start, len(ok)))
    return runs

print('\n=== u16 dense regions (values < 176, runs >= 200) ===')
runs16 = density_runs(u16, NT, 200)
for a, bb in runs16[:24]:
    print(f'  u16 region {hex(a*2)}..{hex(bb*2)}  len {bb-a}')

print('\n=== u32 dense regions ===')
runs32 = density_runs(u32, NT, 150)
for a, bb in runs32[:24]:
    print(f'  u32 region {hex(a*4)}..{hex(bb*4)}  len {bb-a}')

# stride estimate inside the best u16 regions: autocorrelation of hits
def stride_guess(vals, a, bb):
    seg = (vals[a:bb] < NT).astype(np.int8)
    best = []
    for s in range(2, 65):
        if len(seg) <= s:
            break
        score = np.mean(seg[s:] & seg[:-s])
        best.append((score, s))
    best.sort(reverse=True)
    return best[:4]

for a, bb in runs16[:6]:
    print(f'  u16 region {hex(a*2)} len {bb-a}: stride candidates {stride_guess(u16, a, bb)}')
for a, bb in runs32[:6]:
    print(f'  u32 region {hex(a*4)} len {bb-a}: stride candidates {stride_guess(u32, a, bb)}')

json.dump({'u16_runs': [[int(a * 2), int(bb * 2)] for a, bb in runs16[:24]],
           'u32_runs': [[int(a * 4), int(bb * 4)] for a, bb in runs32[:24]]},
          open('/home/z/my-project/scripts/s44_t3_bres_runs.json', 'w'))
