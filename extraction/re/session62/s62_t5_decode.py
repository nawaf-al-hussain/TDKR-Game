#!/usr/bin/env python3
"""S62 T5 v2: sweep CAS candidates with the T1-note CCS (STR = u32 string-table index).
CCS = [S, i, i, c7, f10, i4, c2, i(animN), rep(animN: CAS), i(n2), rep(n2: i6,f,i2,S,i)]
(validated by hand on BatPod: c7 @0x10 = 01 01 00 00 00 00 00, f10 @0x17 = [0,0,0,0,1,1,1,0,0,20.0])
StateSet = [i(count), rep(count: CCS), S x7]."""
import struct, json

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
T = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

CAS_CANDS = {
 'c1': ['S', 'i'],
 'c2': ['S', 'i', ['rep', 'last', 'S']],
 'c3': ['S', 'i', ['rep', 'last', ['S', 'i']]],
 'c4': ['S', 'i', ['rep', 'last', 'S'], 'S', 'i', 'i', 'i', 'i'],
 'c5': ['S', 'i', ['rep', 'last', ['S', 'i']], ['rep', 'last', ['S', 'i', 'i', 'i', 'i']], 'i'],
 'c6': ['S', 'i', ['rep', 'last', ['S', 'i']], ['rep', 'last', ['S', 'i', 'i', 'i', 'i']], 'i',
        ['rep', 'last', ['S', 'i', ['rep', 'last', ['i', 'i', 'S']]]], 'i', 'i'],
 'c7': ['S', 'i', ['rep', 'last', ['S', 'i']], ['rep', 'last', ['S', 'i', 'i', 'i', 'i']], 'i',
        ['rep', 'last', ['S', 'i', ['rep', 'last', ['i', 'i', 'S']]]], 'i', 'i',
        ['rep', 'last', 'i'], ['S', 'S'], 'i', 'i', 'i'],
 'c8': ['S', 'i', ['rep', 'last', ['S', 'i']], ['rep', 'last', ['S', 'i', 'i', 'i', 'i']], 'i',
        ['rep', 'last', ['S', 'i', ['rep', 'last', ['i', 'i', 'S']]]], 'i', 'i', 'i',
        ['rep', 'last', 'i'], ['S', 'S'], 'i', 'i', 'i',
        ['rep', 'last', ['i', 'f', 'f', 'i']]],
 'c9': ['S', 'i', ['rep', 'last', ['S', 'i']], ['rep', 'last', ['S', 'i', 'i', 'i', 'i']], 'i',
        ['rep', 'last', ['S', 'i', ['rep', 'last', ['i', 'i', 'S']]]], 'i', 'i',
        ['rep', 'last', 'i'], ['S', 'S'], 'i', 'i', 'i',
        ['rep', 'last', ['i', 'f', 'f', 'i']]],
}

NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'S': 4, 'STR': 4}

class OOB(Exception):
    pass

def walk(toks, buf, p, end, path=None):
    last = 0
    for ti, t in enumerate(toks):
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk(t[2], buf, p, end)
                continue
            raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok ' + str(t))
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        p += sz
    return p

def make_ccs(cas):
    return (['S', 'i', 'i'] + ['c'] * 7 + ['f'] * 10 + ['i'] * 4 + ['c'] * 2
            + ['i', ['rep', 'last', cas]]
            + ['i', ['rep', 'last', ['i'] * 6 + ['f'] + ['i'] * 2 + ['S'] + ['i']]])

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']
res = []
for name in RESID:
    hit = [r for r in recs if r[1] == name]
    res.append((name, hit[0][2], hit[0][4]))

def try_template(comps, payload, table):
    p = 0; end = len(payload)
    for cid in comps:
        spec = table.get('0x%08x' % cid)
        if spec is None:
            return p, 'unknown comp %08x' % cid
        try:
            p = walk(spec, payload, p, end)
        except OOB:
            return p, 'OOB'
        except Exception as e:
            return p, 'err:%r' % e
    return p, None

for cname, cas in CAS_CANDS.items():
    table = dict(T)
    table['0x5441a117'] = make_ccs(cas)
    ok = 0; det = []
    for name, comps, payload in res:
        p, err = try_template(comps, payload, table)
        good = (err is None and p == len(payload))
        ok += good
        if good:
            tag = 'END'
        elif err is None:
            tag = 'bounds+%d' % (len(payload) - p)
        else:
            tag = '%s@%d/%d' % (err, p, len(payload))
        det.append('%s:%s' % (name, tag))
    print('%s: %d/6   %s' % (cname, ok, '  '.join(det)))
