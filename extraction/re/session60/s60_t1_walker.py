#!/usr/bin/env python3
"""S60 T1 step 3: the template walker (engine-true), calibration + closure.
Modes:
  ENGINE-TRUE: specs = 63 GCT readers (disasm-derived; MainStoryQuests/NewShopItemProperty
               hand-verified from disasm). Templates containing no-case ids cannot be
               template-loaded by the engine (GCT default = null-deref) -> engine-cannot bucket.
  HYBRID:      no-case comps fall back to the s58 spec set (s30 lvc table + s58 overrides)
               for continuity with s58's 326/653 + 30/50 carriers + value calibration.
Nulls:
  N1 spec-permutation: engine-true specs randomly reassigned among case ids (closure must collapse)
  N2 payload-rotate:   each payload rotated by 7 bytes (closure must collapse)
Output: s60_t1_walk.json
"""
import struct, json, collections, random

GOL = '/tmp/my-project/work/data/gol.bin'
RS30 = json.load(open('/tmp/my-project/work/ghpages_mig_wt/playable/lvc_readseq_s30.json'))
S58 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session58/s58_t2_carrier_values.json'))
SPECS = json.load(open('/tmp/my-project/scripts/s60_reader_specs.json'))

HEALTH_ID, AWARE_ID = '0x0ddcd6c4', '0x6754056b'
NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4, 'STRW': 4, '2f': 8, '3f': 12, '4f': 16, 'BLKSTART': 2, 'BLKEND': 1, 'SKIPBLK': None}

# --- hand-verified patches (from disasm this session) ---
SPECS['0x5863bd59']['spec'] = ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'STR', 'STR', 'i', 'STR', 'c']]]
SPECS['0x4ca5f00e']['spec'] = [['i'], ['STR'], ['STR'], ['i'], ['i'], ['f'], ['f'], ['f'],
                               ['c'], ['c'], ['c'], ['c'], ['i'],
                               ['rep', 'last', [['c'], ['i'], ['i'], ['f'], ['f'], ['f'], ['f'],
                                                ['STR'], ['STR'], ['STR'], ['STR'], ['i'], ['c'], ['i'], ['c']]]]

def flatten(spec):
    out = []
    for t in spec:
        if isinstance(t, list):
            if t and t[0] == 'inline':
                out.extend(flatten(t[2]))
            elif t and t[0] == 'rep':
                out.append(t)
            elif t and t[0] == 'call':
                out.append(t)
            else:
                out.extend(flatten(t))
        else:
            out.append(t)
    return out

ENGINE = {}
INCOMPLETE = set()
for cid, v in SPECS.items():
    fl = flatten(v['spec'])
    if any(isinstance(t, list) and t[0] == 'call' for t in fl):
        INCOMPLETE.add(cid)
    ENGINE[cid] = fl

# gol-shape correction (TAIL-DERIVED, not engine-verifiable: no GCT case exists):
# 0x59a8390c gol/template consumption = 16 B (i,i,STR,i) vs lvc-instance 12 B (s30).
# Evidence: 167 templates leave EXACTLY +4 tail with it last; +4i flips exact 234->393.
# Consistent with the template/instance reader duality (cf. Collision 16-B template vs
# cnt-extended instance). Labelled: data-derived, two caveats stated.
GOLSHAPE = {'0x59a8390c': [['i', 4], ['i', 4], ['STR', 4], ['i', 4]]}

# s58 hybrid specs (s30 table + overrides, from s58_t2_walk.py)
s58ovr = {
    '0x5441a117': ['STR'] * 8,
    '0x3ef5108d': ['i', ['rep', 'last', ['i', 'i']]],
    '0x44c6e9e5': ['i'] + ['c'] * 6 + ['i'] * 4 + ['f'] * 3,
    '0x3e2bb040': ['i', 'i', 'f', 'i'],
    '0x54989cb1': ['c'] * 3 + ['f'] * 16 + ['c'] * 3 + ['i', 'i', ['rep', 'last', ['i', 'c']]],
    '0x592ce07c': ['c', 'f', 'f', 'c', 'f', 'f'],
    '0x40c6b80a': 'CUST',
    '0x2db081e2': ['c', 'c', 'STR', 'i', 'c', 'c', 'i'],
    '0x33702f4a': ['f'] * 5,
    HEALTH_ID: ['f', 'c', 'i', 'i'],
    AWARE_ID: ['f'] * 16,
}
HYBRID = {}
for k, v in RS30['components'].items():
    try:
        kk = '0x%08x' % int(k)
    except ValueError:
        continue
    HYBRID[kk] = v
for k, v in s58ovr.items():
    HYBRID[k] = v

class OOB(Exception):
    pass

def ri(buf, p):
    if p + 4 > len(buf):
        raise OOB()
    return struct.unpack_from('>i', buf, p)[0]

def walk_spec(toks, buf, p, end):
    """returns end pos or raises; 'last'-reps use the last numeric read as count"""
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n < 0 or n > 100000:
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
            elif len(t) == 2 and isinstance(t[0], str) and t[0] in ('raw',) and isinstance(t[1], int):
                p += t[1]
                last = 0
                continue
            elif len(t) == 2 and isinstance(t[0], str) and t[0] in NAT and isinstance(t[1], int):
                # s30 convention: [tok, nbytes] = ONE consume of nbytes
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
        if t == 'CUST':
            n = ri(buf, p); p += 4
            if n < 0 or n > 64:
                raise OOB()
            for _ in range(n):
                p += 12
                m = ri(buf, p); p += 4
                if m < 0 or m > 256:
                    raise OOB()
                p += 4 * m
            p += 8
            last = 0
            continue
        if t == 'raw16':
            p += 16
            continue
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

def parse_gol():
    d = open(GOL, 'rb').read()
    table_off = struct.unpack_from('>I', d, 4)[0]
    nrec = struct.unpack_from('>I', d, 13)[0]
    offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings = []
    for _ in range(nstr):
        l = struct.unpack_from('>i', d, pos)[0]; pos += 4
        strings.append(d[pos:pos + l].decode('latin1')); pos += l
    recs = []
    for k in range(nrec):
        ro = offs[k]
        oid = struct.unpack_from('>I', d, ro)[0]
        m = struct.unpack_from('>I', d, ro + 4)[0]
        p = ro + 8 + 4 * m
        n = struct.unpack_from('>H', d, p)[0]
        nameidx = struct.unpack_from('>I', d, p + 2)[0]
        nxt = offs[k + 1] if k + 1 < nrec else len(d)
        payload = d[p + 6 + 6 * n:nxt]
        comps = [struct.unpack_from('>IH', d, p + 6 + 6 * ci)[0] for ci in range(n)]
        flags = [struct.unpack_from('>H', d, p + 6 + 6 * ci + 4)[0] for ci in range(n)]
        recs.append((oid, strings[nameidx] if nameidx < len(strings) else '?', comps, flags, payload))
    return recs, strings

def do_walk(recs, table, rot=0, exact=False):
    ok = 0; fail = 0
    fails = []
    blockers = collections.Counter()
    engine_cannot = 0
    na = 0
    tails = collections.Counter()
    values = {}
    for oid, name, comps, flags, payload in recs:
        if rot:
            payload = payload[rot:] + payload[:rot]
        p = 0
        end = len(payload)
        if not comps:
            na += 1
            tails['empty-comps:%d' % end] += 1
            continue
        good = True
        reason = None
        vals = {}
        for cid, fl in zip(comps, flags):
            key = '0x%08x' % cid
            spec = table.get(key)
            if spec is None:
                good = False
                reason = 'nocase:%s' % key
                blockers[key] += 1
                break
            if isinstance(spec, str):
                spec = [spec]
            try:
                p2 = walk_spec(spec, payload, p, end)
            except OOB:
                good = False
                reason = '%s FAIL@%d' % (key, p)
                blockers[key] += 1
                break
            except ValueError as e:
                good = False
                reason = '%s spec:%s' % (key, e)
                blockers[key] += 1
                break
            if key == HEALTH_ID:
                try:
                    vals['health'] = struct.unpack_from('>f', payload, p)[0]
                    vals['health_start'] = p
                except Exception:
                    pass
            if key == AWARE_ID:
                try:
                    vals['aware'] = [struct.unpack_from('>f', payload, p + 4 * i)[0] for i in range(16)]
                    vals['aware_start'] = p
                except Exception:
                    pass
            p = p2
        if not good:
            if reason and reason.startswith('nocase:'):
                engine_cannot += 1
            fail += 1
            fails.append((name, hex(oid), reason))
            continue
        if p == end:
            ok += 1
            if vals:
                values[name] = vals
        elif not exact and p < end:
            # engine semantics: records are offset-table framed; unread tails allowed
            ok += 1
            tails['tail:%d' % (end - p)] += 1
            if vals:
                values[name] = vals
        else:
            fail += 1
            fails.append((name, hex(oid), 'LEN-MISMATCH %d->%d' % (p, end)))
            blockers['LEN-MISMATCH'] += 1
    return ok, fail, blockers, fails, values, engine_cannot, na, tails

recs, strings = parse_gol()
print('records: %d, string table: %d' % (len(recs), len(strings)))

# ---- ENGINE-TRUE ----
pure = [r for r in recs if all('0x%08x' % c in ENGINE for c in r[2])]
mixed = [r for r in recs if r not in pure]
ok, fail, blockers, fails, values, _, na_e, tails_e = do_walk(pure, ENGINE)
okx, failx, _, _, _, _, nax, _ = do_walk(pure, ENGINE, exact=True)
print('\nENGINE-TRUE: pure-case templates %d/%d (NA empty-comps %d); bounds-closed %d/%d; exact-closed %d/%d' % (
    len(pure), len(recs), nax, ok, len(pure), okx, len(pure)))
print('  tails:', sorted(tails_e.items())[:10])
print('  top blockers:', blockers.most_common(8))

# merged hybrid: s30 hex keys, then ENGINE (engine-true WINS), then s58 overrides
# only for classes with no GCT case (no engine reader exists)
HYBRID2 = dict(HYBRID)
for k, v in ENGINE.items():
    HYBRID2[k] = v
for k, v in s58ovr.items():
    if k not in ENGINE:
        HYBRID2[k] = v
for k, v in GOLSHAPE.items():
    HYBRID2[k] = v

# ---- HYBRID (s58 continuity) ----
okh, failh, blockh, failsh, valh, ench, nah, tailh = do_walk(recs, HYBRID2)
print('\nHYBRID: closed %d/%d (%.1f%%); engine-cannot bucket %d' % (okh, len(recs), 100.0 * okh / len(recs), ench))
print('  top blockers:', blockh.most_common(10))

# carrier values comparison vs s58
car = [k for k in S58 if k in valh]
exact_h = sum(1 for k in car if abs(valh[k].get('health', 1e9) - S58[k]['health']) < 0.001)
exact_a = sum(1 for k in car if valh[k].get('aware') is not None and
              all(abs(a - b) < 0.001 for a, b in zip(valh[k]['aware'], S58[k]['aware'])))
both = sum(1 for k in car if k in valh and abs(valh[k].get('health', 1e9) - S58[k]['health']) < 0.001
           and valh[k].get('aware') is not None and all(abs(a - b) < 0.001 for a, b in zip(valh[k]['aware'], S58[k]['aware'])))
print('\nCALIBRATION vs s58 values: carriers in both %d; health exact %d; aware exact %d; both exact %d' % (
    len(car), exact_h, exact_a, both))
diff = [(k, S58[k]['health'], valh[k].get('health')) for k in car
        if k in valh and abs(valh[k].get('health', 1e9) - S58[k]['health']) >= 0.001]
print('  health diffs:', diff[:10])

# ---- NULL N1: spec permutation ----
rng = random.Random(60)
keys = sorted(ENGINE)
vals = [ENGINE[k] for k in keys]
perm = vals[:]
rng.shuffle(perm)
PN = dict(zip(keys, perm))
okn, _, _, _, _, _, _, _ = do_walk(pure, PN)
print('\nNULL N1 (spec permutation on pure set): closed %d/%d (real: %d)' % (okn, len(pure), ok))

# ---- NULL N2: payload rotation ----
okr, _, _, _, _, _, _, _ = do_walk(pure, ENGINE, rot=7)
print('NULL N2 (payload rot-7 on pure set): closed %d/%d (real: %d)' % (okr, len(pure), ok))

okh2, failh2, blockh2, failsh2, valh2, ench2, nah2, tailh2 = do_walk(recs, HYBRID2, exact=True)
json.dump({'engine_true': {'pure': len(pure), 'ok': ok, 'of653': len(recs),
                           'exact_ok': okx, 'na_empty': nax, 'tails': dict(tails_e),
                           'n_cases': len(ENGINE), 'incomplete': sorted(INCOMPLETE)},
           'hybrid': {'ok': okh, 'of653': len(recs), 'engine_cannot': ench,
                      'exact_ok': okh2, 'tails': len(recs) - okh2 - failh2,
                      'fail': failh2, 'na_empty': nah2,
                      'tail_sizes': dict(tailh2)},
           'blockers_hybrid': blockh.most_common(20),
           'fails_hybrid': failsh[:150],
           'calibration': {'carriers_both': len(car), 'health_exact': exact_h,
                           'aware_exact': exact_a, 'both_exact': both, 'diffs': diff[:20]},
           'nulls': {'perm': okn, 'rot7': okr}},
          open('/tmp/my-project/scripts/s60_t1_walk.json', 'w'), indent=1)
print('saved s60_t1_walk.json')
