#!/usr/bin/env python3
"""S31 T1.4b: MINIMAL faithful distillation for s26_build_table.py.

The builder consumes, per class key (pooled across both islands):
  - the set of distinct (kind,size) patterns with counts (for the
    len(ps)==1 assert and the loop-spec printout)
  - the single winning pattern's full token shape (stored into the table)
  - for span classes (cine 397182239, traffic 831119443): per-occurrence
    [start,size] + per-instance tokens (reproduces spans/span_toks)
  - for the 0x2657 engine case: per-island [start,size] + tokens
So we store full pattern JSON only where the builder actually stores it
(globally single-pattern, non-loop, non-span, non-manual classes); for
multi-pattern classes we keep SHA+count only (content never used).
"""
import json, collections, hashlib

OUT = ('/tmp/my-project/work/TDKR-Game/extraction/re/session26/'
       's26_v2_walk_patterns.json')
ISLANDS = ['GothamCity', 'GothamCity_Island2']
SPAN_CLASSES = (397182239, 831119443)
SPAN_ENGINE = 9815
LOOP_CLASSES = {766542306, 1253615565, 931672584, 1734173459, 1419287729}
MANUAL = {1362553, 1387399, 718446662}

pats = collections.defaultdict(lambda: collections.defaultdict(int))
spans = collections.defaultdict(list)
span_toks = collections.defaultdict(dict)
spans_e, span_toks_e = {}, {}
per_island_counts = {}

for isl in ISLANDS:
    slices = json.load(open(f'/tmp/my-project/work/s26_v2_{isl}_comps.json'))
    recs = json.load(open(f'/tmp/my-project/work/s26_v2_{isl}_records.json'))
    rec_by_id = {r[0]: r for r in recs}
    cnt = collections.Counter()
    for rid, cs in slices:
        for key, tk in cs:
            kj = json.dumps(key)
            pat = json.dumps([[t[0], t[2]] for t in tk])
            pats[kj][pat] += 1
            cnt[kj] += 1
            if isinstance(key, (list, tuple)):
                if key[0] == 'E' and key[1] == SPAN_ENGINE:
                    import struct as _st
                    _d = open(f'/tmp/my-project/work/data/{isl}.lvc',
                              'rb').read(8)
                    toff = _st.unpack_from('>I', _d, 4)[0]
                    start = tk[0][1]
                    spans_e.setdefault(str(SPAN_ENGINE), {})[str(toff)] = \
                        [start, rec_by_id[rid][3] - start]
                    span_toks_e.setdefault(str(SPAN_ENGINE), {})[str(toff)] = tk
                continue
            try:
                k = int(key) if isinstance(key, str) else key
            except ValueError:
                continue
            if k in SPAN_CLASSES:
                start = tk[0][1]
                spans[str(k)].append([start, tk[-1][1] + tk[-1][2] - start])
                span_toks[str(k)][str(start)] = tk
    per_island_counts[isl] = cnt

# minimize: full pattern only where needed
out_pats = {}
for kj, ps in pats.items():
    keep_full = (len(ps) == 1)
    try:
        kint = json.loads(kj)
        is_int = isinstance(kint, int)
    except Exception:
        is_int = False
    if is_int and (kint in LOOP_CLASSES or kint in MANUAL
                   or kint in SPAN_CLASSES):
        keep_full = False
    if keep_full:
        pat = next(iter(ps))
        out_pats[kj] = {'count': next(iter(ps.values())),
                        'pattern': json.loads(pat)}
    else:
        out_pats[kj] = {'count': sum(ps.values()),
                        'sha1': {hashlib.sha1(p.encode()).hexdigest()[:12]: c
                                 for p, c in ps.items()}}

out = {'patterns': out_pats,
       'per_island_counts': {isl: dict(c)
                             for isl, c in per_island_counts.items()},
       'spans': dict(spans), 'span_toks': dict(span_toks),
       'spans_e': spans_e, 'span_toks_e': span_toks_e}
json.dump(out, open(OUT, 'w'))
import os
print('wrote', OUT, f'{os.path.getsize(OUT)/1e6:.2f} MB')
