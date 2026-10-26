#!/usr/bin/env python3
"""S62 T1 step 3: closure with HAND-DERIVED reader sequences (engine-disasm, zero fitted rules).
Fixes vs s61 auto specs (all verified against libKRHP.so disassembly this session):
  0x365cfd67 BeastObjectComponent : + second STR            (0x2e1e8c: 2x ReadString)
  0x59a8390c BeastObjectCompGlobal: [i,i] -> [i,i,STR]      (0x2e1fb0: tail ReadString)
  0x592ce07c SurveillanceCam      : + tail STR              (0x2e4e98)
  0x4de3f7c4 VehicleSoundEvents   : 10 STR -> 9 STR         (0x205458)
  0x0116a6fa Trail                : std::fill decoded       (0x2e5318: i, rep(c,STR,STR,f6))
  0x40c6b80a CustomizeActor       : SkinSets ctor decoded   (0x3bf688: i,rep(STR,STR,STR,i,rep STR),i,i)
  0x2c9a0e3f MuzzleFlash          : loop + tail decoded     (0x3c2a48)
  0x4ab8a7cd SmartLight           : color loop decoded      (0x2e30bc)
  + s60 hand-verified MainStoryQuests / NewShopItemProperty (unchanged)
Nulls: spec permutation, payload rot-7. Output: s62_t1_closure.json"""
import struct, json, collections, random

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E, INC = build(SPECS_RAW)

# ---- S62 HAND-DERIVED (engine disasm) ----
F = {}
F['0x365cfd67'] = ['f'] * 4 + ['STR'] + ['f'] * 4 + ['STR']
F['0x59a8390c'] = ['i', 'i', 'STR']
F['0x592ce07c'] = ['f'] * 7 + ['i', 'f', 'i', 'i', 'i', 'f', 'f', 'STR']
F['0x4de3f7c4'] = ['STR'] * 9 + ['f', 'f']
F['0x6a204677'] = ['STR'] * 9 + ['f', 'f']          # same reader 0x205458 (2nd id on it)
F['0x0116a6fa'] = ['i', ['rep', 'last', ['c', 'STR', 'STR'] + ['f'] * 6]]
F['0x40c6b80a'] = ['i', ['rep', 'last', ['STR', 'STR', 'STR', 'i', ['rep', 'last', ['STR']]]], 'i', 'i']
F['0x4a04f065'] = ['i', ['rep', 'last', ['STR', 'STR', 'STR', 'i', ['rep', 'last', ['STR']]]], 'i', 'i']
F['0x2c9a0e3f'] = ['STR', 'i', ['rep', 'last', ['STR']], 'STR'] + ['c'] * 5 + ['f'] * 4 + ['i'] * 3
F['0x4ab8a7cd'] = ['STR', 'c', 'f', 'f', 'c', 'i', 'c', 'i',
                   ['rep', 'last', ['c', 'c', 'c', 'c', 'i', 'i', 'i', 'f']]]
# s60/s61 hand-verified (kept, unchanged)
F['0x5863bd59'] = ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'STR', 'STR', 'i', 'STR', 'c']]]
F['0x4ca5f00e'] = ['i', 'STR', 'STR', 'i', 'i', 'f', 'f', 'f', 'c', 'c', 'c', 'c', 'i',
                   ['rep', 'last', ['c', 'i', 'i', 'f', 'f', 'f', 'f', 'STR', 'STR', 'STR',
                                    'STR', 'i', 'c', 'i', 'c']]]
for k, v in F.items():
    E[k] = flatten(v)

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
            reason = 'err:%s' % str(e)[:40]
        except Exception as e:
            reason = 'exc:%s' % str(e)[:40]
        if reason:
            fail += 1
            fails.append({'oid': hex(oid), 'name': name, 'reason': reason})
        elif p == end:
            exact += 1
        else:
            bounds += 1
            tails['tail:%d' % (end - p)] += 1
    r = {'exact': exact, 'bounds': bounds, 'fail': fail, 'na': na,
         'tails': dict(tails.most_common(12))}
    if want_fails:
        r['fails'] = fails
    return r

res = {}
r = do_walk(recs, E, want_fails=True)
res['S62_ENGINE'] = r
print(f"[S62 engine-derived, 0 fitted] exact {r['exact']}/653 ({100*r['exact']/653:.1f}%) "
      f"bounds+exact {(r['exact']+r['bounds'])}/653 fail {r['fail']} na {r['na']}")
print('   tails:', r['tails'])
print('   fails:', [(f['name'], f['reason']) for f in r['fails'][:20]])

# nulls
random.seed(61)
ids = [k for k in E]
perm = ids[:]
random.shuffle(perm)
t2 = dict(zip(ids, [E[k] for k in perm]))
r = do_walk(recs, t2)
res['NULL_PERM'] = {'exact': r['exact'], 'bounds': r['exact'] + r['bounds']}
print(f"[NULL-perm] exact {r['exact']} (real {res['S62_ENGINE']['exact']})")
r = do_walk(recs, E, rot=7)
res['NULL_ROT7'] = {'exact': r['exact'], 'bounds': r['exact'] + r['bounds']}
print(f"[NULL-rot7] exact {r['exact']}")

json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_closure.json', 'w'), indent=1)
print('saved')
