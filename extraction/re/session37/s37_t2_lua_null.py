#!/usr/bin/env python3
"""S37 T2: trigger volumes with an INDEPENDENT null.

Independent positions = object ids passed as ARGUMENTS in the 541 Lua scripts
(Enable/Disable/HideObject/ShowObject/HideOccluder/ShowOccluder/
SpawnObject/ObjectGetPosition/SetObjectPos...). A callee id's position is
used only when the object is known (440-trigger table). The pairing is
script-logic-driven, NOT "spawn sits at its own trigger by construction".

Metrics:
  inside-rate of independent positions vs
    A. 2,000 random collision-ground street points (new RNG)
    B. shuffled trigger positions (volumes permuted, sizes travel with
       their original trigger)
    C. spawns (positive control; expected high)
  + sensitivity: small/large split in {5,10,20}; height default in
    {10,000, 50}; rotation on/off.
"""
import json, math, re, random
import numpy as np
from collections import defaultdict

SCRIPTS = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
if isinstance(SCRIPTS, dict):
    SCRIPTS = SCRIPTS['all_scripts']
TRIGS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))
PATCH = json.load(open('/tmp/my-project/work/TDKR-Game/gh-pages/playable/patch.json'))

by_id = {t['id']: t for t in TRIGS}
print(f'triggers: {len(TRIGS)} unique ids: {len(by_id)}')

# ---- 1. extract argument ids from scripts ----
CALL_RE = re.compile(
    r'\b(Enable|Disable|HideObject|ShowObject|HideOccluder|ShowOccluder|'
    r'SpawnObject|ObjectGetPosition|SetObjectPos|MoveObject|Activate|'
    r'Deactivate|SetObjectVisible)\s*\(\s*(\d{4,})', re.I)
pairs = []
for s in SCRIPTS:
    owner = s.get('obj_id')
    for m in CALL_RE.finditer(s['script']):
        fn, arg = m.group(1), int(m.group(2))
        pairs.append((owner, fn, arg))
known = [(o, f, a) for (o, f, a) in pairs if a in by_id]
print(f'call-arg pairs: {len(pairs)}; with known position: {len(known)}; '
      f'unique callee ids with position: {len({a for _,_,a in known})}')
fncount = defaultdict(int)
for _, f, a in known:
    fncount[f] += 1
print('by function:', dict(fncount))

# ---- geometry ----
def inside(p, t, split, hdefault, use_rot):
    hx, hy, hz = t['half']
    scale = max(t.get('scale', [1, 1, 1]))
    small = scale < split
    if not small:
        return False            # large = district zones, excluded like r26
    x, y, z = p[0] - t['pos'][0], p[1] - t['pos'][1], p[2] - t['pos'][2]
    if use_rot and t.get('rot') and t['rot'][2]:
        c, s_ = math.cos(math.radians(t['rot'][2])), math.sin(math.radians(t['rot'][2]))
        x, y = c * x + s_ * y, -s_ * x + c * y
    hh = hz if hz < 100 else hdefault     # r26: height = size.z or 10,000 default
    return abs(x) <= hx and abs(y) <= hy and abs(z) <= hh + 1.0

smalls = [t for t in TRIGS if max(t.get('scale', [1, 1, 1])) < 10]
print(f'small triggers (scale<10): {len(smalls)}')

def rate(points, split=10, hdefault=10000.0, use_rot=True, vol=None):
    vol = vol if vol is not None else TRIGS
    hit = 0
    for p in points:
        if any(inside(p, t, split, hdefault, use_rot) for t in vol):
            hit += 1
    return hit / max(len(points), 1)

indep_points = [by_id[a]['pos'] for (_, _, a) in known]
indep_points = [p for p in {tuple(round(c, 3) for c in p) for p in indep_points}]
indep_points = [list(p) for p in indep_points]
print(f'independent position set: {len(indep_points)} unique positions')

# A. random street points (new RNG, r26 method: collision-ground points)
col = open('/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin', 'rb').read()
nTri = struct_unpack = None
import struct as _s
nTri = _s.unpack_from('<I', col, 4)[0]
nObj = _s.unpack_from('<I', col, 8)[0]
p = 12
nameLen = _s.unpack_from('<I', col, p)[0]; p += 4 + nameLen + nObj * 48
CT = np.frombuffer(col[p:p + nTri * 39], np.uint8).reshape(nTri, 39)
cpos = np.frombuffer(CT[:, 2:38].tobytes(), '<f4').reshape(nTri, 3, 3).astype(np.float64)
cflags = CT[:, 38].astype(np.int32)
WALKABLE = np.isin(cflags, [0, 1, 5, 6])
wtri = cpos[WALKABLE]
rng = np.random.default_rng(370)
pick = rng.integers(0, len(wtri), 4000)
bary = rng.random((4000, 3)); bary /= bary.sum(axis=1, keepdims=True)
street = (wtri[pick] * bary[:, :, None]).sum(axis=1).tolist()
street = [pt for pt in street if -1500 < pt[0] < 1500 and -2000 < pt[1] < 1500][:2000]
print(f'street null points: {len(street)}')

# C. spawns (positive control)
spawns = [s['pos'] if isinstance(s, dict) and 'pos' in s else s for s in PATCH.get('spawns', [])]
spawns = [s[:3] for s in spawns if isinstance(s, (list, tuple)) and len(s) >= 3]
print(f'spawn positive control: {len(spawns)}')

r_indep = rate(indep_points)
r_street = rate(street)
r_spawn = rate(spawns)

# B. shuffled trigger positions (positions permuted across triggers)
rnd = random.Random(371)
poslist = [t['pos'] for t in TRIGS]
perm = poslist[:]
rnd.shuffle(perm)
shuf = []
for t, np_ in zip(TRIGS, perm):
    t2 = dict(t); t2['pos'] = np_
    shuf.append(t2)
r_shuf = rate(indep_points, vol=shuf)

print('\n=== MAIN RESULT (engine model, split=10, hdefault=10000, rot on) ===')
print(f'  independent (Lua-arg) inside-rate : {r_indep:.3f}  ({int(r_indep*len(indep_points))}/{len(indep_points)})')
print(f'  random street inside-rate         : {r_street:.3f}  ({int(r_street*len(street))}/{len(street)})')
print(f'  SHUFFLED-position null            : {r_shuf:.3f}')
print(f'  spawn positive control            : {r_spawn:.3f}  ({int(r_spawn*len(spawns))}/{len(spawns)})')
if r_street > 0:
    print(f'  enrichment vs street              : {r_indep / r_street:.1f}x')

print('\n=== SENSITIVITY ===')
for split in (5, 10, 20):
    for hd in (10000.0, 50.0):
        for rot in (True, False):
            ri = rate(indep_points, split, hd, rot)
            rs = rate(street, split, hd, rot)
            print(f'  split={split:2d} hdefault={hd:7.0f} rot={int(rot)}: indep={ri:.3f} street={rs:.3f} enrich={(ri/rs if rs else float("inf")):.1f}x')

json.dump({'n_indep': len(indep_points), 'indep_rate': r_indep, 'street_rate': r_street,
           'shuffled_rate': r_shuf, 'spawn_rate': r_spawn, 'n_street': len(street),
           'n_spawns': len(spawns), 'call_pairs': len(pairs), 'known_pairs': len(known),
           'fn_count': dict(fncount)},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t2_lua_null.json', 'w'), indent=1)
print('saved s37_t2_lua_null.json')
