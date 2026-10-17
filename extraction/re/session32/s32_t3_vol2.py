#!/usr/bin/env python3
"""S32 T3e: trigger volumes with BIG-ENDIAN floats + spawn verification."""
import sys, json, struct, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}

# shape records: [3 x f32 BE extents][6 x (i32 BE 3, u32 packed)]
shapes = {}
tails = collections.Counter()
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    raw = d[off:off + 60]
    e3 = struct.unpack_from('>3f', raw, 0)
    tails[raw[12:60]] += 1
    shapes[rid] = e3
ext = np.array(list(shapes.values()))
print(f'shape extents (BE): n={len(shapes)}; tail variants {len(tails)}')
print(f'  ex [{ext[:,0].min():.2f},{ext[:,0].max():.2f}] med '
      f'{np.median(ext[:,0]):.2f}')
print(f'  ey [{ext[:,1].min():.2f},{ext[:,1].max():.2f}] med '
      f'{np.median(ext[:,1]):.2f}')
print(f'  ez [{ext[:,2].min():.2f},{ext[:,2].max():.2f}] med '
      f'{np.median(ext[:,2]):.2f}')
good = np.all((ext > 0.05) & (ext < 3000), axis=1)
print(f'  plausible extents: {good.sum()}/{len(ext)}')

# trigger records (54 B): parse RAW as [i32 BE id][9 x f32 BE][i32 BE][c][STR]
trigs = {}
for rid, off, sz in res['census'].get('938977454', []):
    off = int(off, 16)
    raw = d[off:off + sz]
    tid = tid_of.get(rid)
    i0 = struct.unpack_from('>i', raw, 0)[0]
    f9 = struct.unpack_from('>9f', raw, 4)
    i1 = struct.unpack_from('>i', raw, 40)[0]
    flag = raw[44]
    trigs[rid] = dict(tid=tid, i0=i0, f9=f9, i1=i1, flag=flag)
f0s = collections.Counter(round(t['f9'][0], 1) for t in trigs.values())
print(f'\ntrigger f9[0] (BE): {len(f0s)} distinct, top {f0s.most_common(3)}')
f45 = collections.Counter((round(t['f9'][4], 2), round(t['f9'][5], 2))
                          for t in trigs.values())
print('f9[4],f9[5] top:', f45.most_common(3))
f78 = collections.Counter((round(t['f9'][7], 2), round(t['f9'][8], 2))
                          for t in trigs.values())
print('f9[7],f9[8] (scale?) top:', f78.most_common(5))
hs = np.array([t['f9'][6] for t in trigs.values()])
print(f'f9[6] (H): [{hs.min():.2f},{hs.max():.2f}] med {np.median(hs):.2f}')
# is f9[1..3] a position? compare with object-level TRS via records offsets:
# objects with tid 9803: find their CComponentBase TRS from the census base
base = {rid: int(o, 16) for rid, o, sz in res['census'].get('1362553', [])}
n_trs = sum(1 for r in trigs if r in base)
print(f'trigger rids with C_BASE record: {n_trs}/{len(trigs)}')
# If none, use f9[1..3] directly as pos (r21's reading) and check spread
P = np.array([t['f9'][1:4] for t in trigs.values()])
print(f'f9[1:4] spread: x [{P[:,0].min():.1f},{P[:,0].max():.1f}] '
      f'y [{P[:,1].min():.1f},{P[:,1].max():.1f}] '
      f'z [{P[:,2].min():.1f},{P[:,2].max():.1f}]')
P0 = np.array([t['f9'][0:3] for t in trigs.values()])
print(f'f9[0:3] spread: x [{P0[:,0].min():.1f},{P0[:,0].max():.1f}] '
      f'y [{P0[:,1].min():.1f},{P0[:,1].max():.1f}] '
      f'z [{P0[:,2].min():.1f},{P0[:,2].max():.1f}]')

# world boxes: center (f9[0..2])? or (f9[1..3])? — decide by which lands
# closer to the ground plane of the collision soup (street z median 0)
# collision soup is in lvc space (x,y,z) with z=up (from r20 numbers)
json.dump(dict(n=len(trigs), tail_variants=len(tails),
               extents=dict(ex=[float(ext[:,0].min()), float(ext[:,0].max()),
                                float(np.median(ext[:,0]))],
                            ey=[float(ext[:,1].min()), float(ext[:,1].max()),
                                float(np.median(ext[:,1]))],
                            ez=[float(ext[:,2].min()), float(ext[:,2].max()),
                                float(np.median(ext[:,2]))]),
               plausible=float(good.mean())),
          open('/home/z/my-project/download/s32_t3_trigger_volumes.json', 'w'))
print('wrote s32_t3_trigger_volumes.json')
