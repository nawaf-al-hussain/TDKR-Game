#!/usr/bin/env python3
"""S32 T1a: TREE-FREE BIND-SPACE TEST for batman.bdae body binds @0x30e30.

Question: are the 31 stored 64-B row-major affine matrices
  H1: bind matrices (bone-local -> mesh space at bind pose)
  H2: inverse bind matrices (mesh space -> bone-local)
Test (no node tree needed):
  - H1 bone origin in mesh space = translation (last row)
  - H2 bone origin o satisfies o*M = 0 -> o = -t * L^-1
  compare each against the per-bone skin-weighted vertex centroid.
  permuted-mapping null for each hypothesis.
Then, with the winning hypothesis:
  - derive T-pose locals: Local_T[b] = bind[b] * invBind[parent[b]]
  - check orthonormality + bone lengths (anatomical plausibility)
"""
import struct, math, json
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]


def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v:
            return d[v:e].decode('latin1')
    return None


# ---- nodes (from r21, decoded layout) ----
nodes = []
o = 0x2760
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32(o)), pool(u32(o + 4)), pool(u32(o + 8))
    if n1 is None or n2 is None or al is None:
        o += 4
        continue
    t = struct.unpack_from('<3f', d, o + 0x0c)
    q = struct.unpack_from('<4f', d, o + 0x18)
    s = struct.unpack_from('<3f', d, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s):
        o += 4
        continue
    if u32(o + 0x34) != 1 or u32(o + 0x38) > 32:
        o += 4
        continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s,
                      ccount=u32(o + 0x38), child=u32(o + 0x3c)))
    o += 0x50
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
by_name = {n['name']: n for n in nodes}

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8
joint_nodes = [by_alias[p]['name'] for p in pal]

# ---- mesh + skin ----
BASE, N, SKIN = 0x4b5c, 1449, 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
b4s, w4s = [], []
for i in range(N):
    b4s.append(struct.unpack_from('<4B', d, SKIN + i * 20))
    w4s.append(struct.unpack_from('<4f', d, SKIN + i * 20 + 4))
b4s = np.array(b4s, np.uint8)
w4s = np.array(w4s, np.float32)

# per-bone FULL-weighted centroid (all weights, not just w>=0.4)
cent_full = np.zeros((31, 3))
wsum = np.zeros(31)
for j in range(4):
    ids = b4s[:, j].astype(int)
    valid = ids < 31
    np.add.at(cent_full, ids[valid], verts[valid] * w4s[valid, j][:, None])
    np.add.at(wsum, ids[valid], w4s[valid, j])
ok = wsum > 0
cent_full[ok] /= wsum[ok][:, None]
cnt = [int(((b4s == b) & (w4s >= 0.4)).any(axis=1).sum()) for b in range(31)]

# ---- stored binds ----
BODY = 0x30e30
Ms = []
for k in range(31):
    m = np.array(struct.unpack_from('<16f', d, BODY + k * 64),
                 np.float64).reshape(4, 4)
    Ms.append(m)
Ms = np.array(Ms)

# linear-part orthonormality / det for both 3x3 readouts
print('=== stored body matrices @0x30e30: structure ===')
print('last row of each (should be [0,0,0,1] if column-conv stored,'
      ' or translation if row-conv):')
for k in range(4):
    print(f'  M[{k}] last row = {tuple(round(x,5) for x in Ms[k,3])}')
    print(f'       col3     = {tuple(round(x,5) for x in Ms[k][:,3])}')


def lin_of(m):
    """guess: upper-left 3x3 is linear, last ROW is translation (row-vector
    convention).  Verify last col ~ (0,0,0,1) or last row ~ (0,0,0,1)."""
    return m[:3, :3], m[3, :3], m[:3, 3]


orths = []
for k in range(31):
    L, trow, tcol = lin_of(Ms[k])
    orth = float(np.abs(L @ L.T - np.eye(3)).max())
    orths.append(orth)
print(f'upper-left 3x3 orthonormality max|LL^T-I|: max {max(orths):.2e}, '
      f'median {sorted(orths)[15]:.2e}')

# scale? check per-bone lengths of L columns
lens = [sorted(np.linalg.norm(Ms[k][:3, :3], axis=0)) for k in range(31)]
mx = max(l[2] for l in lens), min(l[0] for l in lens)
print(f'L column lengths: max-max {mx[0]:.6f}, min-min {mx[1]:.6f}')

# ---- hypotheses ----
rng = np.random.default_rng(31)
NPERM = 200


def perm_null(cent, origins, cnt):
    nulls = []
    for _ in range(NPERM):
        perm = rng.permutation(31)
        es = [float(np.linalg.norm(cent[b] - origins[perm[b]]))
              for b in range(31) if cnt[b] > 0]
        nulls.append(float(np.median(es)))
    return float(np.median(nulls)), float(np.percentile(nulls, 10)), \
        float(np.percentile(nulls, 90))


results = {}
for hyp, name in (('H1', 'bind (bone->mesh), origin = last row'),
                  ('H2', 'invBind (mesh->bone), origin = -t L^-1')):
    origins = np.zeros((31, 3))
    for k in range(31):
        L, trow, tcol = lin_of(Ms[k])
        if hyp == 'H1':
            origins[k] = trow
        else:
            origins[k] = -trow @ np.linalg.inv(L)
    es = {b: float(np.linalg.norm(cent_full[b] - origins[b]))
          for b in range(31) if cnt[b] > 0}
    med = float(np.median(list(es.values())))
    n50, n10, n90 = perm_null(cent_full, origins, cnt)
    results[hyp] = dict(median_cm=med * 100, null50_cm=n50 * 100,
                        null10_cm=n10 * 100, null90_cm=n90 * 100)
    print(f'\n=== {hyp}: {name} ===')
    print(f'  median centroid-vs-origin over {len(es)} used bones: '
          f'{med*100:.1f} cm   (permuted null median-of-medians {n50*100:.1f} cm,'
          f' p10 {n10*100:.1f} / p90 {n90*100:.1f})')
    for b in range(31):
        if cnt[b]:
            print(f'   joint {b:2d} {pal[b]:8s} {joint_nodes[b]:20s} '
                  f'origin ({origins[b][0]:7.3f},{origins[b][1]:7.3f},'
                  f'{origins[b][2]:7.3f})  '
                  f'cent  ({cent_full[b][0]:7.3f},{cent_full[b][1]:7.3f},'
                  f'{cent_full[b][2]:7.3f})  '
                  f'd {es[b]*100:7.1f} cm  n={cnt[b]}')

print('\n=== winning-hypothesis follow-up: T-pose locals ===')
# pick winner by median
win = min(results, key=lambda h: results[h]['median_cm'])
print(f'winner: {win}')
if win == 'H1':
    binds = Ms.copy()          # bone->mesh
else:
    binds = np.array([np.linalg.inv(Ms[k]) for k in range(31)])

# parents among the 31 palette joints (biped standard, from r21)
P31 = {1: 2, 0: 1, 3: 4, 4: 5, 6: 8, 7: 8, 8: 9, 9: 10, 10: 11, 11: 20,
       12: 14, 13: 14, 14: 15, 15: 16, 16: 17, 17: 20, 18: 19, 19: 20,
       20: 21, 21: 22, 2: 22,
       23: 7, 24: 6, 25: 14, 26: 25, 27: 10, 28: 29, 29: 8, 30: 29}
# (index -> parent index; 5=L_Thigh->2 Pelvis, 3=L_Calf->4)
P31[3] = 4
P31[5] = 2
P31[0] = 1
P31[4] = 5
P31[1] = 2

inv_binds = np.array([np.linalg.inv(binds[k]) for k in range(31)])
print('T-pose local translations (bind child x invBind parent):')
lens_b = {}
for b in range(31):
    if b in P31 and P31[b] is not None and P31[b] != b:
        loc = binds[b] @ inv_binds[P31[b]]
        p = P31[b]
        # bone vector = child origin - parent origin, in mesh space
        v = binds[b][:3, 3] - binds[p][:3, 3]
        lens_b[b] = float(np.linalg.norm(v))
        L = loc[:3, :3]
        orth = float(np.abs(L @ L.T - np.eye(3)).max())
        print(f'  joint {b:2d} {pal[b]:8s} -> {pal[p]:8s}  '
              f'local t ({loc[3,0]:7.3f},{loc[3,1]:7.3f},{loc[3,2]:7.3f})  '
              f'bone len {lens_b[b]*100:5.1f} cm  L orth {orth:.1e}')
print('\nbone length sanity: calf/thigh/foot vs upper/forearm:')
for b in (0, 1, 3, 4, 9, 15, 8, 14):
    if b in lens_b:
        print(f'  {joint_nodes[b]:20s} {lens_b[b]*100:5.1f} cm')

json.dump(dict(results=results, winner=win,
               bone_lengths_cm={joint_nodes[k]: v * 100
                                for k, v in lens_b.items()},
               bone_lengths_m={joint_nodes[k]: v for k, v in lens_b.items()}),
          open('/home/z/my-project/download/s32_t1_treefree.json', 'w'),
          indent=1)
print('\nwrote /home/z/my-project/download/s32_t1_treefree.json')
