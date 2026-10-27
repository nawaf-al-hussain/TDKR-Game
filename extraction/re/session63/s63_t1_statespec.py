#!/usr/bin/env python3
"""S63 T1 step 3: nested StateSet spec, validated standalone on the 6 residual templates.
Walk: SS comp0 with the nested grammar, then comps[1:] with final_specs -> exact end required.
Variants for the 5 CAS lists are tested systematically; a variant wins only if ALL 6 close."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
T = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

class OOB(Exception):
    pass

NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}

def walk_spec(toks, buf, p, end, path=''):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB('rep-n %d @%d %s' % (n, p, path))
                for k in range(n):
                    try:
                        p = walk_spec(t[2], buf, p, end, path + '/%d.%d' % (len(path), k))
                    except OOB as e:
                        raise OOB('%s[rep%d.%d] %s' % (path, len(path), k, e))
                continue
            raise ValueError('tok %r' % (t,))
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok %r' % (t,))
        if p + sz > end:
            raise OOB('field %s @%d end %d' % (t, p, end))
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
        p += sz
    return p

TRIG = ['i', 'i', 'i', 'i', 'i', 'i', 'f', 'i', 'i', 'STR', 'i']

def make_statespec(v):
    l1, l2, l3, l4, l5 = v
    def lst(elem, track):
        return ['rep', 'last', [elem, 'i', ['rep', 'last', track]]]
    CAS = ['STR'] + ['i'] + [x for l in v for x in (
        ['rep', 'last', l[0] and ['STR', 'i', ['rep', 'last', l[1]]] if l[0] == 'STR'
         else ['i', ['rep', 'last', l[1]]]])]
    # rebuild explicitly for clarity
    CAS = (['STR', 'i'] + [['rep', 'last', ['STR', 'i', ['rep', 'last', v[0][1]]]]] if False else None)
    CAS = ['STR',
           'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', v[0]]]],
           'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', v[1]]]],
           'i', ['rep', 'last', ['i', ['rep', 'last', v[2]]]],
           'i', ['rep', 'last', ['i', ['rep', 'last', v[3]]]],
           'i', ['rep', 'last', ['i', ['rep', 'last', v[4]]]]]
    STATE = (['STR', 'i', 'i'] + ['c'] * 7 + ['f', 'f', 'i'] + ['f'] * 7 + ['c', 'f', 'i', 'i', 'i', 'c', 'c', 'i']
             + [['rep', 'last', CAS]]
             + ['i', ['rep', 'last', TRIG]])
    return ['i', ['rep', 'last', STATE]] + ['STR'] * 7

V_H5 = (['STR', 'i', 'i', 'i', 'i'], ['i', 'i', 'STR'], ['i', 'i', 'STR', 'i'],
        ['i', 'i', 'STR', 'STR'], ['i', 'i', 'f', 'f', 'i'])

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']

def try_template(payload, spec, verbose=False):
    """walk SS comp0 from 0; return (ss_end, error_or_None)."""
    try:
        p = walk_spec(spec, payload, 0, len(payload), 'SS')
        return p, None
    except (OOB, ValueError) as e:
        return None, str(e)

def walk_rest(name, payload, ss_end):
    """walk comps[1:] with final_specs; returns (ok, detail)."""
    hit = [r for r in recs if r[1] == name][0]
    comps = hit[2]
    p = ss_end
    end = len(payload)
    for cid in comps[1:]:
        spec = T.get('0x%08x' % cid)
        if spec is None:
            return False, 'nocase %08x @%d' % (cid, p)
        try:
            p = walk_spec(spec, payload, p, end, '%08x' % cid)
        except (OOB, ValueError) as e:
            return False, 'comp %08x @%d: %s' % (cid, p, str(e)[:60])
    return (p == end), 'p=%d end=%d' % (p, end)

results = {}
for name in RESID:
    hit = [r for r in recs if r[1] == name][0]
    payload = hit[4]
    cnt = struct.unpack_from('>i', payload, 0)[0]
    spec = make_statespec(V_H5)
    ss_end, err = try_template(payload, spec)
    print('%-16s count=%-4d SS walk: %s' % (name, cnt, ('END @%d' % ss_end) if ss_end is not None else 'FAIL: %s' % str(err)[:110]))
    if ss_end is not None:
        ok, detail = walk_rest(name, payload, ss_end)
        print('     rest: %s (%s)' % (ok, detail))
        results[name] = ok
    else:
        results[name] = False

print()
print('V_H5 verdict:', 'ALL CLOSE' if all(results.values()) else 'open: %s' % [k for k, v in results.items() if not v])
