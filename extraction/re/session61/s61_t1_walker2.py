#!/usr/bin/env python3
"""S61 T1 step 20: ENGINE-TRUE closure over ALL 653 templates with the FULL 120-reader
spec set (s61_reader_specs.json, every gol id now has an engine-resolved GCT case).
Modes: RAW (auto-extracted specs) / PATCHED (+ MainStoryQuests + NewShopItemProperty
hand-verified disasm specs) / GOLSHAPE (+ the labelled 0x59a8390c 16-B template shape).
Nulls: N1 spec-permutation, N2 payload-rotate-7.
Output: s61_t1_walk2.json"""
import struct, json, collections, random

GOL = '/home/z/my-project/work/data/gol.bin'
SPECS_RAW = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))

NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4, 'STRW': 4, '2f': 8, '3f': 12, '4f': 16}

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

def build(raw):
    E = {}
    INCOMPLETE = set()
    for cid, v in raw.items():
        kk = '0x%08x' % int(cid, 16)
        fl = flatten(v['spec'])
        if any(isinstance(t, list) and t[0] == 'call' for t in fl):
            INCOMPLETE.add(kk)
        E[kk] = fl
    return E, INCOMPLETE

PATCHED = dict(SPECS_RAW)
PATCHED['0x5863bd59']['spec'] = ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'STR', 'STR', 'i', 'STR', 'c']]]
PATCHED['0x4ca5f00e']['spec'] = [['i'], ['STR'], ['STR'], ['i'], ['i'], ['f'], ['f'], ['f'],
                                 ['c'], ['c'], ['c'], ['c'], ['i'],
                                 ['rep', 'last', [['c'], ['i'], ['i'], ['f'], ['f'], ['f'], ['f'],
                                                  ['STR'], ['STR'], ['STR'], ['STR'], ['i'], ['c'], ['i'], ['c']]]]
GOLSHAPE_SPEC = [['i'], ['i'], ['STR'], ['i']]
GOLSHAPE_ID = '0x59a8390c'

class OOB(Exception):
    pass

def walk_spec(toks, buf, p, end):
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
        comps = [struct.unpack_from('>I', d, p + 6 + 6 * ci)[0] for ci in range(n)]
        flags = [struct.unpack_from('>H', d, p + 6 + 6 * ci + 4)[0] for ci in range(n)]
        recs.append((oid, strings[nameidx] if nameidx < len(strings) else '?', comps, flags, payload))
    return recs, strings

def do_walk(recs, table, rot=0):
    exact = 0; bounds = 0; fail = 0; na = 0
    fails = []
    blockers = collections.Counter()
    tails = collections.Counter()
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
        try:
            for cid in comps:
                key = '0x%08x' % cid
                spec = table.get(key)
                if spec is None:
                    good = False
                    reason = 'nocase:%s' % key
                    blockers[key] += 1
                    break
                if isinstance(spec, str):
                    spec = [spec]
                p = walk_spec(spec, payload, p, end)
        except OOB:
            good = False
            reason = 'OOB'
        except ValueError as e:
            good = False
            reason = 'incomplete:%s' % e
        except Exception as e:
            good = False
            reason = 'err:%s' % e
        if not good:
            fail += 1
            fails.append({'oid': hex(oid), 'name': name, 'reason': reason})
        elif p == end:
            exact += 1
        else:
            bounds += 1
            tails['tail:%d' % (end - p)] += 1
    return {'exact': exact, 'bounds': bounds, 'fail': fail, 'na': na,
            'blockers': dict(blockers.most_common(20)), 'tails': dict(tails.most_common(12)),
            'fails': fails[:80]}

recs, strings = parse_gol()
E_raw, INC_raw = build(SPECS_RAW)
E_pat, INC_pat = build(PATCHED)

res = {}
for label, table in (('RAW', E_raw), ('PATCHED', E_pat)):
    r = do_walk(recs, table)
    r['incomplete_specs'] = sorted(INC_raw if label == 'RAW' else INC_pat)
    res[label] = r
    print(f"[{label}] exact {r['exact']}/653 bounds {r['exact']+r['bounds']}/653 fail {r['fail']} na {r['na']}")
    print('   blockers:', dict(list(r['blockers'].items())[:10]))

# GOLSHAPE variant: PATCHED + 0x59a8390c template shape (overrides auto spec)
table = dict(E_pat)
table['0x%08x' % int(GOLSHAPE_ID, 16)] = flatten(GOLSHAPE_SPEC)
r = do_walk(recs, table)
res['GOLSHAPE'] = r
print(f"[GOLSHAPE] exact {r['exact']}/653 bounds {r['exact']+r['bounds']}/653 fail {r['fail']} na {r['na']}")
print('   blockers:', dict(list(r['blockers'].items())[:10]))

# Nulls on the GOLSHAPE table
import copy
random.seed(61)
ids = [k for k in table]
perm = ids[:]
random.shuffle(perm)
t2 = dict(zip(ids, [table[k] for k in perm]))
r = do_walk(recs, t2)
res['NULL_PERM'] = {'exact': r['exact'], 'bounds': r['exact'] + r['bounds']}
print(f"[NULL-perm] exact {r['exact']} bounds {r['exact']+r['bounds']}")
r = do_walk(recs, table, rot=7)
res['NULL_ROT7'] = {'exact': r['exact'], 'bounds': r['exact'] + r['bounds']}
print(f"[NULL-rot7] exact {r['exact']} bounds {r['exact']+r['bounds']}")

json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walk2.json', 'w'), indent=1)
print('saved')
