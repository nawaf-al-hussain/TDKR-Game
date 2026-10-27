#!/usr/bin/env python3
"""S63 T1 step 8: search the CAS track-shape combination that closes ALL 6 residual SS payloads.
Element heads: list1/2 = [STR, k]; list3/4/5 = [k]. Track shape candidates per list.
A combo wins only if SS walk lands and the remaining components close the payload exactly."""
import struct, json, itertools, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
T = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

class OOB(Exception):
    pass

NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}
REC = {r[1]: r for r in recs}

def walk_spec(toks, buf, p, end, depth=0):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000 or depth > 12:
                    raise OOB('rep-n %d' % n)
                for _ in range(n):
                    p = walk_spec(t[2], buf, p, end, depth + 1)
                continue
            raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok')
        if p + sz > end:
            raise OOB('field @%d' % p)
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
        p += sz
    return p

TRIG = ['i'] * 6 + ['f', 'i', 'i', 'STR', 'i']
HEAD = ['STR', 'i', 'i'] + ['c'] * 7 + ['f', 'f', 'i'] + ['f'] * 7 + ['c', 'f', 'i', 'i', 'i', 'c', 'c', 'i']

SHAPES = {
    1: [('STR', 'i', 'i', 'i', 'i')],
    2: [('i', 'i', 'STR', 'c'), ('i', 'i', 'STR'), ('STR', 'i', 'i', 'c'), ('i', 'i', 'i', 'i')],
    3: [('i', 'i', 'STR', 'i', 'c'), ('i', 'i', 'STR', 'i'), ('i', 'i', 'STR', 'c'), ('STR', 'STR', 'i', 'i', 'c')],
    4: [('i', 'i', 'STR', 'STR', 'c'), ('i', 'i', 'STR', 'STR'), ('i', 'i', 'STR', 'i', 'c'), ('STR', 'STR', 'i', 'i', 'c')],
    5: [('i', 'i', 'f', 'f', 'i'), ('i', 'i', 'f', 'f', 'i', 'c'), ('i', 'i', 'i', 'i', 'i')],
}

def make_statespec(shapes):
    CAS = ['STR']
    for li in (1, 2, 3, 4, 5):
        elem = (['STR', 'i'] if li in (1, 2) else ['i']) + [['rep', 'last', list(shapes[li])]]
        CAS += ['i', ['rep', 'last', elem]]
    STATE = HEAD + [['rep', 'last', CAS], 'i', ['rep', 'last', TRIG]]
    return ['i', ['rep', 'last', STATE]] + ['STR'] * 7

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']

def ss_walk(name, spec):
    payload = REC[name][4]
    try:
        return walk_spec(spec, payload, 0, len(payload))
    except (OOB, ValueError) as e:
        return None

def walk_rest(name, ss_end):
    hit = REC[name]
    comps, payload = hit[2], hit[4]
    p = ss_end
    end = len(payload)
    try:
        for cid in comps[1:]:
            spec = T.get('0x%08x' % cid)
            if spec is None:
                return False
            p = walk_spec(spec, payload, p, end)
        return p == end
    except (OOB, ValueError):
        return False

best = []
keys = [1, 2, 3, 4, 5]
combos = list(itertools.product(*[SHAPES[k] for k in keys]))
print('combos:', len(combos))
for ci, combo in enumerate(combos):
    shapes = dict(zip(keys, combo))
    spec = make_statespec(shapes)
    ends = {}
    okall = True
    for name in RESID:
        e = ss_walk(name, spec)
        ends[name] = e
        if e is None:
            okall = False
            break
    if okall:
        full = all(walk_rest(n, ends[n]) for n in RESID)
        best.append((shapes, dict(ends), full))
        print('CLOSE-SS combo:', {k: '+'.join(v) for k, v in shapes.items()},
              'ends:', ends, 'full-closure:', full)
    if ci % 50 == 0:
        print('  ..%d/%d' % (ci, len(combos)), flush=True)
print('total SS-closing combos:', len(best))
