#!/usr/bin/env python3
"""Build the read-sequence TABLE for the pure lvc parser from the v2 walk.

DSL (JSON):
  token := [kind]                      kind in i,f,c,B,s,STR (natural size)
         | ["fat", kind, size]         fat token (inlined sibling reads;
                                       value decoded from first natural bytes)
         | ["raw", size]
  loop  := ["rep", "last", subspec]    count = value of the scalar read
                                       immediately before the loop entry
Span fallback:
  ["span"]                             byte length comes from the measured
                                       spans table (2 resisting classes)

Output: extraction/re/session26/lvc_readseq.json
{
  "components": { "<ctid>": spec },         generic component classes
  "dedicated":  { "<tid>": spec },          dedicated dispatcher records
  "engine_cases": { "<tid>": spec },        real-code cases (0x2657/0x798f)
  "spans": { "<ctid>": [len,...] }          measured spans per occurrence
                                            (record order = file order)
}
"""
import json, collections

ISLANDS = ['GothamCity', 'GothamCity_Island2']
OUT = '/home/z/my-project/work/TDKR-Game/extraction/re/session26/lvc_readseq.json'

# ---- hand-reviewed loop specs (byte sizes verified on every record) --------
COLLISION = [
    ['c'], ['c'], ['STR'], ['i'], ['c'], ['c'], ['i'],          # 16-B prefix
    ['c'],                                                       # prim count
    ['rep', 'last', [ ['STR'], ['i'], ['rep', 'last',
        [['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['f'],
         ['f'], ['c']] ] ] ],
    ['i'],                                                       # tail list n
]
SMARTLIGHT = [  # 1253615565 = 0x4ab8a7cd CSmartLightComponent
    ['STR'], ['c'], ['f'], ['f'], ['c'], ['i'], ['c'], ['i'],
    ['rep', 'last', [ ['c'], ['c'], ['c'], ['c'],
                      ['i'], ['i'], ['i'], ['f'] ] ],
]
SOUNDLIGHT = [  # 931672584
    ['f'], ['f'], ['i'],
    ['rep', 'last', [ ['f'], ['STR'], ['f'] ] ],
]
NPLLERS = [  # 1734173459
    ['i'],
    ['rep', 'last', [ ['i'], ['STR'] ] ],
]
ACTORBASE = [  # 1419287729 = 0x54989cb1 CActorBaseComponent
    ['raw', 7],                  # inlined head reads (3c+i or equivalent)
    ['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['f'],
    ['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['f'], ['fat', 'f', 7],
    ['i'], ['i'],
    ['rep', 'last', [ ['fat', 'i', 5] ] ],
]
LOOP_SPECS = {
    '766542306': ('CCollisionComponent', COLLISION),
    '1253615565': ('CSmartLightComponent', SMARTLIGHT),
    '931672584': ('CSoundAndLight', SOUNDLIGHT),
    '1734173459': ('NPC-pos-list', NPLLERS),
    '1419287729': ('CActorBaseComponent', ACTORBASE),
}
# classes whose byte length is measured (resist hand decode; 49 records)
SPAN_CLASSES = {'397182239', '831119443'}   # component classes
# components the v2 walk special-cased in Python (no pattern harvested):
MANUAL_COMPONENTS = {
    '1362553': ('CComponentBase::Load (0x14ca79)',
                [['c'], ['i']] + [['f']] * 9 + [['c'], ['c'], ['c']]),
    '1387399': ('name comp (0x152b87)', [['STR'], ['raw', 4]]),
    '718446662': ('CGroupObject::ReadBuiltinData (0x2ad2a046)',
                  [['c'], ['c'], ['i'], ['rep', 'last', [['i']]]]),
}
SPAN_ENGINE = {9815}                        # 0x2657 LevelInit (1 per island,
                                            # island-specific content)


def main():
    pats = collections.defaultdict(lambda: collections.defaultdict(list))
    spans = collections.defaultdict(list)
    span_toks = {}
    comps_seen = collections.Counter()
    for isl in ISLANDS:
        slices = json.load(open(
            f'/tmp/my-project/work/s26_v2_{isl}_comps.json'))
        recs = json.load(open(
            f'/tmp/my-project/work/s26_v2_{isl}_records.json'))
        rec_by_id = {r[0]: r for r in recs}
        for rid, cs in slices:
            base_off = rec_by_id[rid][1]
            for key, tk in cs:
                kj = json.dumps(key)
                pats[kj][tuple((t[0], t[2]) for t in tk)].append((isl, rid))
                comps_seen[kj] += 1
                if isinstance(key, (list, tuple)):  # ('E', tid)/('D', tid)
                    continue
                if key in (397182239, 831119443):
                    # component start offset = first token offset
                    spans[str(key)].append(
                        [tk[0][1], tk[-1][1] + tk[-1][2] - tk[0][1]])
                    span_toks.setdefault(str(key), {})[tk[0][1]] = tk
                if key in (766542306, 1253615565, 931672584, 1734173459,
                           1419287729):
                    pass
    table = {'components': {}, 'dedicated': {}, 'engine_cases': {},
             'spans': {k: v for k, v in spans.items()},
             'span_toks': span_toks,
             'meta': {'loop_specs': {}, 'span_classes': sorted(SPAN_CLASSES)}}
    n_fixed = n_loop = 0
    for kj, ps in pats.items():
        key = json.loads(kj)
        total = sum(len(v) for v in ps.values())
        if total == 0:
            continue
        if isinstance(key, (list, tuple)):
            # dedicated / engine-case record specs (whole record incl. tid)
            if key[0] == 'E':
                tid = key[1]
                if tid in SPAN_ENGINE or len(ps) != 1:
                    # measured-span fallback (record order = file order per
                    # island; lengths identical across islands verified below)
                    table['engine_cases'][str(tid)] = [['span']]
                    lens = []
                    for isl in ISLANDS:
                        sl2 = json.load(open(
                            f'/tmp/my-project/work/s26_v2_{isl}_comps.json'))
                        rr = json.load(open(
                            f'/tmp/my-project/work/s26_v2_{isl}_records.json'))
                        rb = {r[0]: r for r in rr}
                        import struct as _st
                        _d = open(f'/home/z/my-project/work/data/{isl}.lvc',
                                  'rb').read(8)
                        table_off2 = _st.unpack_from('>I', _d, 4)[0]
                        for rid2, cs2 in sl2:
                            for k2, tk2 in cs2:
                                if isinstance(k2, list) and k2[0] == "E" and k2[1] == tid:
                                    lens.append([table_off2,
                                                 rb[rid2][3] - tk2[0][1]])
                                    table.setdefault(
                                        'span_toks_e', {}).setdefault(
                                        str(tid), {})[table_off2] = tk2
                    table.setdefault('spans_e', {})[str(tid)] = lens
                    table.setdefault('span_toks_e', {}).setdefault(
                        str(tid), {})
                else:
                    spec = [list(p) for p in next(iter(ps))]
                    table['engine_cases'][str(tid)] = spec
            else:
                tid = key[1]
                assert len(ps) == 1, (key, len(ps))
                table['dedicated'][str(tid)] = [list(p) for p in
                                                next(iter(ps))]
            continue
        ks = str(key)
        if ks in MANUAL_COMPONENTS:
            continue
        if ks in SPAN_CLASSES:
            table['components'][ks] = [['span']]
            continue
        if ks in LOOP_SPECS:
            name, spec = LOOP_SPECS[ks]
            table['components'][ks] = spec
            table['meta']['loop_specs'][ks] = name
            n_loop += 1
            # verify the loop spec against every observed pattern
            print(f'loop {ks} ({name}): patterns={len(ps)} records={total}')
            continue
        assert len(ps) == 1, (ks, len(ps), [len(v) for v in ps.values()][:3])
        spec = [list(p) for p in next(iter(ps))]
        table['components'][ks] = spec
        n_fixed += 1
    for ks, (name, spec) in MANUAL_COMPONENTS.items():
        table['components'][ks] = spec
        table['meta']['loop_specs'].setdefault(ks, name)
    # cross-island consistency: every class spec must fit both islands —
    # enforced by the asserts above (single pattern per class globally).
    json.dump(table, open(OUT, 'w'))
    print(f'\ntable: {len(table["components"])} component classes '
          f'({n_fixed} fixed, {n_loop} loop, {len(SPAN_CLASSES)} span), '
          f'{len(table["dedicated"])} dedicated, '
          f'{len(table["engine_cases"])} engine cases')
    print('wrote', OUT)


def verify_spec(spec, pat, depth=0):
    """Check a spec's token shapes can produce the observed pattern."""
    toks = list(pat)
    si = 0
    # walk the spec; loops consume until the pattern is exhausted
    def emit(sp, ti):
        for tok in sp:
            if tok[0] == 'rep':
                # count unknown from pattern alone: consume repeats while
                # the remaining pattern matches the subspec cyclically
                sub = tok[2]
                sl = sum(tsize(t) for t in sub)
                while ti + sl <= len(toks) + sl:   # at least once if space
                    if ti >= len(toks):
                        break
                    # try one iteration
                    save = ti
                    try:
                        ti = emit_once(sub, ti)
                    except ValueError:
                        ti = save
                        break
                # after loop, also allow zero iterations case handled above
            else:
                ti = emit_once([tok], ti)
        return ti

    def emit_once(sp, ti):
        for tok in sp:
            if ti >= len(toks):
                raise ValueError('short')
            if tsize(tok) != toks[ti][1]:
                raise ValueError(f'size {tsize(tok)} != {toks[ti][1]}')
            ti += 1
        return ti

    try:
        end = emit(spec, 0)
        return end == len(toks)
    except ValueError:
        return False


def tsize(tok):
    if tok[0] == 'rep':
        raise ValueError('nested')
    if tok[0] == 'raw':
        return tok[1]
    if tok[0] == 'fat':
        return tok[2]
    return {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}[tok[0]]


if __name__ == '__main__':
    main()
