#!/usr/bin/env python3
"""S64 T1 step 4: test the code-derived SlowMotion element shape.
The CAS disasm (0x3b61ec list count, 0x3b62a0 per-element k, track loop
0x3b63e4..0x3b6468 = i,i,f,f,i + 2 ldrb, RETURN at 0x3b6494) shows NO
per-element trailing int. The s63 spec has one. Run the closure with the
param removed and compare; also try param-after-list (per-list, not per-elem)
for completeness."""
import struct, json, copy

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py'
exec(open(SRC).read().split('recs, strings = parse_gol()')[0])

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
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json'))

SS = '0x5441a117'

def find_l5(spec):
    """return the list5 block: ['i', ['rep','last',[ ... ]]] inside the CAS body"""
    state = spec[1][2]           # CCS: ['i', ['rep','last',[STATE]], 'STR'x7]
    cas = state[28][2]           # CAS body list
    return cas, state

def variants():
    spec = copy.deepcopy(E[SS])
    cas = spec[1][2][28][2]
    # CAS body: [STR, l1, l2, l3, l4, l5] where l5 = ['i', ['rep','last', ELEM]]
    l5 = cas[10]                 # ['i', ['rep','last', ['i', [rep tracks], 'i']]]
    rep = l5[1]
    elem = rep[2]                # ['i', ['rep','last',[...]], 'i']
    # v0: s63 spec (with per-element param)
    yield 's63-param', copy.deepcopy(spec)
    # v1: code-exact (no per-element param)
    s1 = copy.deepcopy(spec)
    c1 = s1[1][2][28][2]
    e1 = c1[10][2]               # ['i', ['rep','last',[tracks]], 'i']
    assert e1[0] == 'i' and e1[2] == 'i', e1
    del e1[2]                    # -> ['i', ['rep','last',[tracks]]]
    yield 'no-param', s1
    # v2: param moved to per-list level (CAS body trailing 'i' after the l5 rep)
    s2 = copy.deepcopy(spec)
    c2 = s2[1][2][28][2]
    e2 = c2[10][2]
    del e2[2]
    c2.insert(11, 'i')
    yield 'param-after-list', s2

def do_walk(table):
    exact = bounds = fail = na = 0
    fails = []
    tails = {}
    for oid, name, comps, flags, payload in recs:
        if not comps:
            na += 1
            continue
        p = 0; end = len(payload); reason = None
        try:
            for cid in comps:
                spec = table.get('0x%08x' % cid)
                if spec is None:
                    reason = 'nocase'; break
                p = walk_spec(spec, payload, p, end)
        except OOB:
            reason = 'OOB'
        except ValueError as e:
            reason = 'err:%s' % str(e)[:30]
        if reason:
            fail += 1
            fails.append(name)
        elif p == end:
            exact += 1
        else:
            bounds += 1
            tails['t%d' % (end - p)] = tails.get('t%d' % (end - p), 0) + 1
    return exact, bounds, fail, na, fails, tails

for label, spec in variants():
    T = dict(E); T[SS] = spec
    ex, bo, fa, na, fails, tails = do_walk(T)
    print('[%s] exact %d/653  pass %d  fail %d  na %d' % (label, ex, ex + bo, fa, na))
    print('   fails(%d): %s' % (len(fails), fails[:14]))
    print('   tails:', dict(sorted(tails.items(), key=lambda kv: -kv[1])[:6]))
