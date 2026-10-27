#!/usr/bin/env python3
"""S62 T1 step 4: FULL closure with corrected id->reader assignments.
Table = s61 byte-sequences REASSIGNED by reader function (108 ids)
      + 44 hand-derived specs (this session's disasm).
Zero fitted rules. Nulls: spec-permutation + payload rot-7.
Output: s62_t1_closure.json + s62_t1_final_specs.json"""
import struct, json, collections, random

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

# engine-true rep semantics override: count<=0 skips the loop (cmp r6,#0; ble skip)
def walk_spec(toks, buf, p, end):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk_spec(t[2], buf, p, end)
                continue
            if t and t[0] == 'call':
                raise ValueError('call')
            if t and t[0] == 'inline':
                p = walk_spec(t[2], buf, p, end)
                continue
            if len(t) == 1 and isinstance(t[0], str) and t[0] in NAT:
                t = t[0]
            elif len(t) == 2 and isinstance(t[0], str) and t[0] in NAT and isinstance(t[1], int):
                if p + t[1] > end:
                    raise OOB()
                p += t[1]
                last = 0
                continue
            elif len(t) >= 3 and t[0] == 'fat':
                for _ in range(t[2]):
                    p = walk_spec([t[1]], buf, p, end)
                last = 0
                continue
            else:
                raise ValueError('tok %r' % (t,))
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok %r' % (t,))
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
        p += sz
    return p

recs, strings = parse_gol()
specs61 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
plan = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_specplan.json'))

# reader addr -> spec tokens (from s61, keyed by reader func)
by_reader = {}
for k, v in specs61.items():
    by_reader[int(v['reader'], 16)] = v['spec']

# hand-derived (this session; reader func -> tokens)
D = {
    0x2e3e50: [],                                            # Dummy
    0x3c0938: ['i'] + ['f'] * 20 + ['i'],                    # Glide
    0x3bba48: ['f', 'f', 'f'],                               # ActorsCollision
    0x1ff0b0: ['i', 'c', 'f', 'f', 'f', 'i', 'i', 'i', 'i', 'i', 'i', 'STR', 'f', 'c'],  # TrafficRoad
    0x2e1298: ['f'] * 4 + ['i'] + ['f'] * 9 + ['i'] + ['STR'] * 5 + ['f'] * 4,           # BatpodHandle
    0x2d79ec: ['STR'],                                       # Motion (tail-call ReadString)
    0x3bce84: ['STR', 'STR', 'f', 'c', 'c', 'c', 'c', 'STR', 'i',
               ['rep', 'last', ['i', ['rep', 'last', ['STR', 'f']]]], 'c'],               # Animated
    0x3be2ac: ['i'] + ['f'] * 7 + ['i'] * 10 + ['f'] * 5 + ['STR'] * 9 + ['c', 'f', 'f', 'i'],  # Batarang
    0x2051fc: ['i', 'c', 'c', 'c', 'c'],                     # VehicleGraphics
    0x205d00: ['i', 'i', ['rep', 'last', ['i', 'i', 'i', 'i', 'i']]],                      # CharXPLevels
    0x2d90fc: [],                                            # RunScript
    0x2d9008: ['c', 'c', 'c', 'c', 'f', 'f', 'i', 'i', 'f'], # HasLight
    0x202000: ['c', 'i', 'f', 'f', 'c', 'c', 'c', 'c', 'f', 'f', 'c', 'c', 'c', 'c', 'i',
               ['rep', 'last', ['i', 'i', 'c', 'c', 'STR', 'STR', 'STR', 'f', 'f', 'f', 'f',
                                'STR', 'f', 'f', 'c', 'c', 'c', 'c', 'f', 'f', 'f',
                                'c', 'c', 'c', 'c']]],      # BaseGlobalIllum
    0x2d86e4: ['c', 'i', 'c', 'i', 'i', 'i', 'i', 'STR', 'STR', 'STR', 'STR'],             # Collectible
    0x2e67cc: ['c', 'c'],                                    # BuiltinGroup
    0x3be7a0: [],                                            # BuiltinColors
    0x2d7ad8: ['STR', 'i', 'STR', 'c', 'c', 'c', 'f', 'f'],  # BuiltinEffect
    0x1feb64: ['i', 'i', 'i', 'STR', 'i', ['rep', 'last', ['STR', 'STR', 'i']]],           # SoundAndLight
    0x1ff69c: ['i'],                                         # TrafficSemaphore
    0x3c0fdc: ['STR', 'f'],                                  # LazyLoad
    0x204a18: ['i', 'STR', 'STR', 'i', 'f', 'STR', 'STR', 'i', 'f'],                       # VehicleState
    0x2e0bcc: ['i'] + ['f'] * 8 + ['i', 'c', 'STR', 'i', 'c'],                             # Trigger
    0x3c425c: ['f', 'f', 'f'],                               # ZombieConverter
    0x2027d0: ['f', 'STR', 'i', 'i', 'c', 'STR', 'i', 'i', 'c'],                           # NpcSound
    0x2018f0: ['STR'] * 6 + ['c', 'STR', 'i'] + ['STR'] * 4 + ['c', 'STR', 'i'] + ['STR'] * 5 + ['c', 'c', 'STR', 'c'] + ['f'] * 23 + ['c'],  # LevelInit
    0x3bdbec: ['i', 'i', 'i', 'f', 'i', 'f', 'f', 'i', 'i', 'f'],                          # AIController
    0x3bed64: ['i', 'i', 'i', 'i', 'f'],                     # BuiltinTerrain
    0x2e080c: ['STR'] * 4 + ['i'] * 6 + ['f', 'i', 'STR'],   # MiniGameObject
    0x3c0c1c: ['f', 'c'] + ['f'] * 23,                       # KombatCameraParams
    0x2e24b0: ['c', 'c', 'c', 'c', 'f', 'c', 'i', 'f', 'i', 'f', 'f', 'c', 'f', 'f', 'f', 'i'],  # Beast_Spot
    0x3c2818: ['i', ['rep', 'last', ['f', 'f', 'f']]],       # MorphValueList
    0x3b8e9c: ['i', ['rep', 'last', [
        'STR', 'i', 'i', 'c', 'c', 'c', 'c', 'c', 'c', 'c',
        'f', 'f', 'i', 'f', 'f', 'f', 'f', 'f', 'f', 'f',
        'c', 'f', 'i', 'i', 'i', 'c', 'c', 'i',
        ['rep', 'last', ['STR',
            'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', ['STR', 'i', 'i', 'i', 'i']]]],
            'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', ['i', 'i', 'STR', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'STR', 'i', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'f', 'f', 'i', 'c', 'c']], 'i']]]],
        'i', ['rep', 'last', ['i', 'i', 'i', 'i', 'i', 'i', 'f', 'i', 'i', 'STR', 'i']]]],
        ] + ['STR'] * 7,                       # StateSet: s63 engine-true nested (CCS 82-B head + 5 CAS lists + triggers)
    0x200ecc: ['i', 'STR', 'STR', 'STR', 'i', 'i', 'STR', 'c', 'c', 'c'],                  # Quest_Parameters
    0x3bdf78: ['c', 'f', 'f', 'c', 'f', 'f'],                # ActorSpecialEffects
    0x1ff270: ['i', 'c', 'f', 'f', 'f'] + ['i'] * 9,         # TrafficCrossroad
    0x3beb0c: ['f', 'f', 'f'],                               # BuiltinIrradianceVolume
    0x2e2a8c: ['i', 'i', 'STR'],                             # DropActors
    0x3c07d8: ['i', 'f', 'f', 'i', 'i'],                     # GadgetZoom
    0x3c1100: ['f', 'f', 'c', 'c', 'c', 'c', 'f', 'f', 'f', 'f'],                          # LevelGlobalIllum
    0x3c3330: ['c', 'i', 'f', 'i', 'f'],                     # Pendulum_Movement
    0x2e0d78: ['f', 'f', 'f'] + ['i', 'c', 'c', 'c', 'c'] * 6,                             # BuiltinBox
    0x3c3448: ['i', 'STR'],                                  # Pendulum_Properties
    0x3bf038: ['f'] * 8 + ['i'] * 3 + ['STR', 'STR', 'i', 'i', 'f', 'c'] + ['f'] * 3,      # CameraParams
    0x3c2eb8: ['f'] * 8 + ['i'] * 3 + ['c'] * 16,            # NpcGlobals
    # previously derived (blockers)
    0x2e1fb0: ['i', 'i', 'STR'],                             # BeastObjectComponentGlobal
    0x2e1e8c: ['f'] * 4 + ['STR'] + ['f'] * 4 + ['STR'],     # BeastObjectComponent
    0x2e4e98: ['f'] * 7 + ['i', 'f', 'i', 'i', 'i', 'f', 'f', 'STR'],                      # SurveillanceCam
    0x205458: ['STR'] * 9 + ['f', 'f'],                      # VehicleSoundEvents
    0x2e5318: ['i', ['rep', 'last', ['c', 'STR', 'STR'] + ['f'] * 6]],                     # Trail
    0x3bf688: ['i', ['rep', 'last', ['STR', 'STR', 'STR', 'i', ['rep', 'last', ['STR']]]], 'i', 'i'],  # CustomizeActor
    0x3c2a48: ['STR', 'i', ['rep', 'last', ['STR']], 'STR'] + ['c'] * 5 + ['f'] * 4 + ['i'] * 3,       # MuzzleFlash
    0x2e30bc: ['STR', 'c', 'f', 'f', 'c', 'i', 'c', 'i', ['rep', 'last', ['c', 'c', 'c', 'c', 'i', 'i', 'i', 'f']]],  # SmartLight
    0x3bbb68: ['f'] * 16,                                  # Awareness (16 ReadFloat, NO int)
    0x2e3940: ['i', ['rep', 'last', ['STR']]],             # Dummies (fill loop reads STR/elem)
    0x2e3500: ['i', 'STR', 'STR', 'STR', 'STR', 'STR', 'c', 'c', 'STR'],                   # Destroyable (+ tail STR)
    0x3baee0: ['c'] * 7 + ['f'] * 16 + ['c'] * 3 + ['i', 'i', ['rep', 'last', ['i', 'c']]],  # ActorBase (+ rep 5B/elem)
    0x2e27b8: ['i', ['rep', 'last', ['i', 'i']]],          # DropCollectible (s57 page-validated + count data)
    # (s63: duplicate flat StateSet entry removed - nested engine-true spec above)
    # s60 hand-verified
    0x3c18e0: ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'STR', 'STR', 'i', 'STR', 'c']]],         # MissionsList
    0x202ae4: ['i', 'STR', 'STR', 'i', 'i', 'f', 'f', 'f', 'c', 'c', 'c', 'c', 'i',
               ['rep', 'last', ['c', 'i', 'i', 'f', 'f', 'f', 'f', 'STR', 'STR', 'STR',
                                'STR', 'i', 'c', 'i', 'c']]],  # NewShopItemProperty
}

# ids the island scan missed (mov rX,#imm8 low-half compares) — readers verified:
FALLBACK = {
    '0x0116a6fa': D[0x2e5318],                   # Trail (derived this session)
    '0x0ddcd6c4': specs61['0x0ddcd6c4']['spec'], # Health (s60 hand-verified, engine @137)
    '0x222500f6': specs61['0x222500f6']['spec'], # TheBatHandle
    '0x365cfd67': D[0x2e1e8c],                   # BeastObjectComponent (derived this session)
}

# assemble: start from s61 specs reassigned by reader, then override with derived
E = {}
for nk, (r, sym) in plan['reassign'].items():
    E[nk] = flatten(by_reader[int(r, 16)])
derived = 0
for r, toks in D.items():
    nk = '0x%08x' % 0  # placeholder
    # find all ids that map to this reader
    for cid, c in plan['reassign'].items():
        if int(c[0], 16) == r:
            E[cid] = flatten(toks)
            derived += 1
    # ids in need_derive with this reader
    for cid, c in plan['need_derive'].items():
        if int(c[0], 16) == r:
            E[cid] = flatten(toks)
            derived += 1

print(f'table: {len(E)} ids ({derived} spec assignments from {len(D)} hand-derived readers)')
for nk, toks in FALLBACK.items():
    E[nk] = flatten(toks)
print('after fallback:', len(E), 'ids')

def do_walk(recs_, table, rot=0, want_fails=False):
    exact = bounds = fail = na = 0
    fails = []
    tails = collections.Counter()
    for oid, name, comps, flags, payload in recs_:
        if rot:
            payload = payload[rot:] + payload[:rot]
        if not comps:
            na += 1
            continue
        p = 0; end = len(payload); reason = None
        try:
            for cid in comps:
                key = '0x%08x' % cid
                spec = table.get(key)
                if spec is None:
                    reason = 'nocase:%s' % key; break
                p = walk_spec(spec, payload, p, end)
        except OOB:
            reason = 'OOB'
        except ValueError as e:
            reason = 'err:%s' % str(e)[:36]
        except Exception as e:
            reason = 'exc:%s' % str(e)[:36]
        if reason:
            fail += 1
            fails.append({'oid': hex(oid), 'name': name, 'reason': reason})
        elif p == end:
            exact += 1
        else:
            bounds += 1
            tails['tail:%d' % (end - p)] += 1
    r = {'exact': exact, 'bounds': bounds, 'fail': fail, 'na': na,
         'tails': dict(tails.most_common(14))}
    if want_fails:
        r['fails'] = fails
    return r

r = do_walk(recs, E, want_fails=True)
res = {'S62_ENGINE': r}
print(f"[S63 nested-StateSet] exact {r['exact']}/653 ({100*r['exact']/653:.1f}%) "
      f"pass {(r['exact']+r['bounds'])}/653 ({100*(r['exact']+r['bounds'])/653:.1f}%) fail {r['fail']} na {r['na']}")
print('tails:', r['tails'])
print('fails:', [(f['name'], f['reason'][:40]) for f in r['fails'][:25]])

random.seed(61)
ids = [k for k in E]
perm = ids[:]
random.shuffle(perm)
t2 = dict(zip(ids, [E[k] for k in perm]))
r2 = do_walk(recs, t2)
res['NULL_PERM'] = {'exact': r2['exact'], 'pass': r2['exact'] + r2['bounds']}
print(f"[NULL-perm] exact {r2['exact']} (real {r['exact']})")
r3 = do_walk(recs, E, rot=7)
res['NULL_ROT7'] = {'exact': r3['exact'], 'pass': r3['exact'] + r3['bounds']}
print(f"[NULL-rot7] exact {r3['exact']}")

# S63 NULL: swap the CAS list2/list3 track shapes inside the StateSet spec (wrongly ordered)
_ss = E['0x5441a117']
def _swap_ss(spec):
    import copy
    s = copy.deepcopy(spec)
    state = s[1][2]
    cas = state[28][2]          # ['rep','last',[CAS-body]] -> CAS-body
    l2 = cas[2]; l3 = cas[4]    # list2 block, list3 block
    cas[2], cas[4] = l3, l2
    return s
E2 = dict(E); E2['0x5441a117'] = _swap_ss(E['0x5441a117'])
r_ss = do_walk([r for r in recs if r[1] in ('BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive')], E2, want_fails=True)
res['NULL_SS_SWAP'] = {'exact': r_ss['exact'], 'pass': r_ss['exact'] + r_ss['bounds'],
                       'fails': [f['name'] for f in r_ss.get('fails', [])]}
print('[NULL-ss-swap] exact %d pass %d fails %s (content templates must break)' % (
    r_ss['exact'], r_ss['exact'] + r_ss['bounds'], res['NULL_SS_SWAP']['fails']))

json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_closure.json', 'w'), indent=1)
json.dump({k: v for k, v in E.items()},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json', 'w'), indent=1)
print('saved')
