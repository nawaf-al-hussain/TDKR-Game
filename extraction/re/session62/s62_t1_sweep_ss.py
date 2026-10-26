#!/usr/bin/env python3
"""S62 T1: sweep StateSet element variants against the full closure."""
import struct, json, collections

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
E_base = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))
# rebuild base table from closure2's assembly minus StateSet special: quick approach —
# load final specs (which has the 20B variant), then try variants.
variants = {
    'fixed32': ['i'] + ['STR'] * 7,
    'elem20': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 8]] + ['STR'] * 7,
    'elem20b': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 7]] + ['STR'] * 7,
    'elem127': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 7 + ['f'] * 11 + ['i'] * 17]] + ['STR'] * 7,
    'elem129': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 9 + ['f'] * 11 + ['i'] * 17]] + ['STR'] * 7,
    'elem111': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 7 + ['f'] * 11 + ['i'] * 15]] + ['STR'] * 7,
    'elem123': ['i', ['rep', 'last', ['STR', 'i', 'i'] + ['c'] * 7 + ['f'] * 11 + ['i'] * 16]] + ['STR'] * 7,
}
NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}

def walk(toks, buf, p, end):
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
                    p = walk(t[2], buf, p, end)
                continue
            if t and t[0] == 'inline':
                p = walk(t[2], buf, p, end)
                continue
            if len(t) == 1 and t[0] in NAT:
                t = t[0]
            else:
                raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok')
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        p += sz
    return p

import copy
for name, spec in variants.items():
    T = dict(E_base)
    T['0x5441a117'] = spec
    exact = bounds = fail = 0
    for oid, tname, comps, flags, payload in recs:
        if not comps:
            continue
        p = 0; end = len(payload); ok = True
        try:
            for cid in comps:
                s = T.get('0x%08x' % cid)
                if s is None:
                    ok = False; break
                p = walk(s, payload, p, end)
        except Exception:
            ok = False
        if not ok:
            fail += 1
        elif p == end:
            exact += 1
        else:
            bounds += 1
    print(f'{name:9s}: exact {exact} pass {exact+bounds} fail {fail}')
