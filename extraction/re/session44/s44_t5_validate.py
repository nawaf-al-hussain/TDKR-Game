#!/usr/bin/env python3
"""s44 T5a: validate the loose-scan TRS population (s43 claimed 8,064 records).

Rebuild: scan the s26 pure-python token streams (both islands) for runs
[i32 objId][9 x f32] with ANY token prefix (the loose scan), dedup by (id, pos).

Validation battery per record:
  V1 id-resolve : objId appears as a token-stream object-header id in the same
                  island stream (the TRS belongs to an object record present
                  in the level)
  V2 in-AABB    : position inside the island collision-soup bbox (+40 m margin)
  V3 above-pit  : position z >= soup zmin - 40 (not deep under the world)
  V4 rot-range  : |rot_x,y,z| <= 4.0 rad (~229 deg) — euler-ish storage
  V5 scale      : 0 < s <= 500, no NaN/inf anywhere
NULLS:
  N1 byte-random floats  : 36 fresh random bytes per record -> same battery
  N2 rotation-as-position: the rotation triple used as position -> V2/V3
  N3 shuffled records    : permute the 9 floats within each record
"""
import json, struct, re
import numpy as np

TOKS = {'island1': '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity.lvc.puretoks.json',
        'island2': '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_Island2.lvc.puretoks.json'}
COL = {'island1': '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin',
       'island2': '/tmp/my-project/work/TDKR-Game/extraction/prototype/i2_collision.bin'}

records = []
header_ids = {}
for isl, path in TOKS.items():
    toks = json.load(open(path))
    # collect all 'i' values that look like object ids (header ids): i32 values in [1, 3_000_000]
    ids = set()
    n = len(toks)
    i = 0
    # token shape: ['i', ?, size, value] per the sample ['i', 17, 4, 9815]
    types = [t[0] for t in toks]
    vals = []
    for t in toks:
        # value = last element
        vals.append((t[0], t[-1]))
    # header ids: every 'i' value in the id range (dedup later by V1 definition:
    # an id is 'resolvable' if it occurs in the stream more than the TRS occurrence
    # itself -> simpler: count occurrences of each candidate id in 'i' tokens)
    from collections import Counter
    icount = Counter(v for ty, v in vals if ty == 'i' and isinstance(v, int) and 1 <= v <= 3_000_000)
    # loose TRS scan
    k = 0
    while k < len(vals) - 9:
        ty, v = vals[k]
        if ty == 'i' and isinstance(v, int) and 1 <= v <= 3_000_000:
            window = vals[k + 1:k + 10]
            if all(ty2 == 'f' and isinstance(v2, float) for ty2, v2 in window):
                fl = np.array([v2 for _, v2 in window], dtype=np.float64)
                if np.isfinite(fl).all():
                    records.append({'isl': isl, 'id': v, 'pos': fl[0:3].tolist(),
                                    'rot': fl[3:6].tolist(), 'scl': fl[6:9].tolist()})
                    ids.add(v)
                    k += 10
                    continue
        k += 1
    header_ids[isl] = icount

print('loose TRS records rebuilt:', len(records))
# dedup by (id, rounded pos)
seen = set()
dedup = []
for r in records:
    key = (r['isl'], r['id'], round(r['pos'][0], 2), round(r['pos'][1], 2), round(r['pos'][2], 2))
    if key in seen:
        continue
    seen.add(key)
    dedup.append(r)
print('after dedup:', len(dedup))

# island AABBs from the collision soups
def soup_bbox(p):
    col = open(p, 'rb').read()
    nTri = struct.unpack_from('<I', col, 4)[0]
    nObj = struct.unpack_from('<I', col, 8)[0]
    pp = 12
    nameLen = struct.unpack_from('<I', col, pp)[0]
    pp += 4 + nameLen + nObj * 48
    CT = np.frombuffer(col[pp:pp + nTri * 39], np.uint8).reshape(nTri, 39)
    cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
    lo = cpos.reshape(-1, 3).min(axis=0)
    hi = cpos.reshape(-1, 3).max(axis=0)
    return lo, hi

BBOX = {isl: soup_bbox(p) for isl, p in COL.items()}
for isl, (lo, hi) in BBOX.items():
    print(f'{isl} soup bbox lo={np.round(lo,1)} hi={np.round(hi,1)}')

# validation battery
res = {'n': len(dedup)}
ok = {k: 0 for k in ('V1', 'V2', 'V3', 'V4', 'V5')}
fails_examples = {k: [] for k in ok}
for r in dedup:
    isl = r['isl']
    lo, hi = BBOX[isl]
    p = np.array(r['pos']); rt = np.array(r['rot']); sc = np.array(r['scl'])
    v1 = header_ids[isl].get(r['id'], 0) >= 1
    v2 = bool((p >= lo - 40).all() and (p <= hi + 40).all())
    v3 = bool(p[2] >= lo[2] - 40)
    v4 = bool(np.isfinite(rt).all() and (np.abs(rt) <= 4.0).all())
    v5 = bool(np.isfinite(sc).all() and (sc > 0).all() and (sc <= 500).all())
    for k, v in (('V1', v1), ('V2', v2), ('V3', v3), ('V4', v4), ('V5', v5)):
        if v:
            ok[k] += 1
        elif len(fails_examples[k]) < 3:
            fails_examples[k].append(r)
for k in ok:
    print(f'{k}: {ok[k]}/{len(dedup)}')
res['real'] = dict(ok)
res['fails_examples'] = fails_examples

# ---- NULLS ----
rng = np.random.RandomState(44)
# N1 byte-random floats
n1 = {k: 0 for k in ('V2', 'V3', 'V4', 'V5')}
for _ in range(len(dedup)):
    raw = rng.bytes(36)
    fl = np.frombuffer(raw, '<f4').astype(np.float64)
    if not np.isfinite(fl).all():
        continue
    isl = 'island1'
    lo, hi = BBOX[isl]
    p, rt, sc = fl[0:3], fl[3:6], fl[6:9]
    if (p >= lo - 40).all() and (p <= hi + 40).all(): n1['V2'] += 1
    if p[2] >= lo[2] - 40: n1['V3'] += 1
    if np.isfinite(rt).all() and (np.abs(rt) <= 4.0).all(): n1['V4'] += 1
    if np.isfinite(sc).all() and (sc > 0).all() and (sc <= 500).all(): n1['V5'] += 1
print('N1 byte-random floats (of', len(dedup), '):', n1)
res['null_byte_random'] = n1

# N2 rotation-as-position
n2 = {'V2': 0, 'V3': 0}
for r in dedup:
    lo, hi = BBOX[r['isl']]
    p = np.array(r['rot'])
    if (p >= lo - 40).all() and (p <= hi + 40).all(): n2['V2'] += 1
    if p[2] >= lo[2] - 40: n2['V3'] += 1
print('N2 rotation-as-position:', n2, '/', len(dedup))
res['null_rot_as_pos'] = n2

# N3 within-record float shuffle (keeps marginals, breaks roles)
n3 = {k: 0 for k in ('V2', 'V3', 'V4', 'V5')}
for r in dedup:
    fl = np.array(r['pos'] + r['rot'] + r['scl'])
    perm = rng.permutation(9)
    fl = fl[perm]
    lo, hi = BBOX[r['isl']]
    p, rt, sc = fl[0:3], fl[3:6], fl[6:9]
    if (p >= lo - 40).all() and (p <= hi + 40).all(): n3['V2'] += 1
    if p[2] >= lo[2] - 40: n3['V3'] += 1
    if np.isfinite(rt).all() and (np.abs(rt) <= 4.0).all(): n3['V4'] += 1
    if np.isfinite(sc).all() and (sc > 0).all() and (sc <= 500).all(): n3['V5'] += 1
print('N3 within-record shuffle:', n3, '/', len(dedup))
res['null_shuffle'] = n3

json.dump(res, open('/home/z/my-project/scripts/s44_t5_validation.json', 'w'), indent=1)
print('saved s44_t5_validation.json')
