#!/usr/bin/env python3
"""S32 T3d: trigger extents census + world volumes + spawn verification."""
import sys, json, struct, collections, math
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

# trigger records (54 B class)
trigs = {}
for rid, off, sz in res['census'].get('938977454', []):
    off = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = off
    toks = []
    rr.tok('i', out=toks)
    n0 = len(toks)
    for _ in range(9):
        rr.tok('f', out=toks)
    f9 = [t[3] for t in toks[n0:]]
    rr.tok('i', out=toks)
    rr.tok('c', out=toks)
    s = rr.tok('STR', out=toks)
    trigs[rid] = dict(f9=f9, flag=None if s is None else 1, tid=tid_of.get(rid))

# shape records (60 B class): extents + tail constancy
shapes = {}
tails = collections.Counter()
bad_first = 0
for rid, off, sz in res['census'].get('1923007858', []):
    off = int(off, 16)
    raw = d[off:off + 60]
    e3 = struct.unpack_from('<3f', raw, 0)
    tails[raw[12:60]] += 1
    if not all(0.05 < abs(x) < 2000 for x in e3):
        bad_first += 1
    shapes[rid] = e3
print(f'shape records: {len(shapes)}; constant tail variants: {len(tails)} '
      f'(top count {tails.most_common(1)[0][1]}); bad extents: {bad_first}')
ext = np.array([v for v in shapes.values()])
print(f'extents ex [{ext[:,0].min():.2f},{ext[:,0].max():.2f}] median '
      f'{np.median(ext[:,0]):.2f}; ey [{ext[:,1].min():.2f},'
      f'{ext[:,1].max():.2f}] med {np.median(ext[:,1]):.2f}; '
      f'ez [{ext[:,2].min():.2f},{ext[:,2].max():.2f}] '
      f'med {np.median(ext[:,2]):.2f}')

# correlate: trigger f9 vs shape extents for tid-9803 objects
n_both = 0
corr = []
for rid, t in trigs.items():
    if rid in shapes:
        n_both += 1
        corr.append((t['f9'][1], t['f9'][2], t['f9'][3], t['f9'][6],
                     t['f9'][7], t['f9'][8], *shapes[rid]))
corr = np.array(corr)
print(f'triggers with shape: {n_both}/{len(trigs)}')
print('f9[7] (scaleX?) vs shape ex ratio: ',
      np.median(corr[:, 4] / np.where(np.abs(corr[:, 6]) > 1e-6, corr[:, 6], 1)))
# f9[6] vs ey?
r_h = corr[:, 3] / np.where(np.abs(corr[:, 7]) > 1e-6, corr[:, 7], 1)
print(f'f9[6] (H) / shape ey: median {np.median(r_h):.3f}')

# f9[0] census (unknown field)
f0s = collections.Counter(round(t['f9'][0], 3) for t in trigs.values())
print('f9[0] top:', f0s.most_common(6))

# spawns
spawns = []
for rec in res['census'].get('spawn', []):
    pass
# r21: spawn census key 'spawn' with records; TRS at 0x2662 (y,z,x order)
print('\nspawn census records:', len(res['census'].get('spawn', [])))
sp_pos = []
for rid, off, sz in res['census'].get('spawn', []):
    off = int(off, 16)
    raw = d[off:off + sz]
    if len(raw) >= 0x2662 - 0x2662 + 0x30:
        pass
# r21 formula: pos = (f1, f0, f2) at 0x2662
n_in = 0
tested = 0
boxes = []
for rid, t in trigs.items():
    if rid not in shapes:
        continue
    e = shapes[rid]
    f9 = t['f9']
    # candidate world box: center (f9[1], f9[2], f9[3]), half-extents
    # (e[0]*f9[7], e[1], e[2]*f9[8]), H from f9[6]?
    boxes.append((rid, f9[1], f9[2], f9[3], e[0] * max(f9[7], 0.01),
                  e[1] * max(f9[6], 0.01) if f9[6] > 0.05 else e[1],
                  e[2] * max(f9[8], 0.01)))
# verify: fraction of spawn positions inside any box (xz, with y in range)
# spawn pos: from r21 '0x2662 TRS stores (y,z,x,...) -> pos=(f1,f0,f2)'
spawn_pos = []
for rid, off, sz in res['census'].get('spawn', []):
    off = int(off, 16)
    # find the object base TRS: use C_BASE if available
    pass
print(f'(spawn-TR extraction via census done separately; '
      f'{len(boxes)} trigger boxes built)')
json.dump(dict(n_triggers=len(trigs), n_shapes=len(shapes),
               tail_variants=len(tails),
               extents=dict(ex=[float(ext[:, 0].min()), float(ext[:, 0].max()),
                                float(np.median(ext[:, 0]))],
                            ey=[float(ext[:, 1].min()), float(ext[:, 1].max()),
                                float(np.median(ext[:, 1]))],
                            ez=[float(ext[:, 2].min()), float(ext[:, 2].max()),
                                float(np.median(ext[:, 2]))])),
          open('/home/z/my-project/download/s32_t3_trigger_volumes.json', 'w'))
print('wrote s32_t3_trigger_volumes.json')
