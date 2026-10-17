#!/usr/bin/env python3
"""S32 T4 final: static-vs-fitted spec comparison + coverage."""
import json, collections

loads = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                       'session24/component_loads.json'))
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
prov = json.load(open('/home/z/my-project/download/s31_t1_provenance.json'))
provm = {e['key']: e['prov'] for e in prov['provenance']}
remaining = json.load(open('/tmp/s32_remaining_fitted.json'))
PRIORITIES = [str(x) for x in (0x729EC572, 0xF5F8CFD, 0xDFE2718, 0x2CA13C06,
                               0x37F7A8AE, 0xDDCD6C4)]

# fitted spec token sequences per class: table['components'][id] = spec
comps = tab['components']


def spec_tokens(spec):
    """flatten the fitted spec into a token list (best effort)."""
    toks = []
    if isinstance(spec, dict):
        seq = spec.get('seq') or spec.get('tokens') or spec.get('spec')
        if isinstance(seq, list):
            for t in seq:
                if isinstance(t, (list, tuple)):
                    toks.append(t[0])
                else:
                    toks.append(str(t))
            return toks, spec
    return None, spec


def norm(seq):
    """collapse loops for comparison: keep order of scalar tokens, note vars"""
    out = []
    for t in seq:
        t = str(t)
        if t in ('NEW', 'END', 'BLOCK', 'VAR'):
            out.append(t)
        else:
            out.append(t)
    return out


print('=== priority classes: static (r24 disasm) vs fitted (r21) ===')
stat_ok, stat_diff, stat_missing = [], [], []
for cid in PRIORITIES:
    cl = loads.get(hex(int(cid)))
    fit = comps.get(cid) or comps.get(str(int(cid)))
    st = cl.get('read_seq') if cl else None
    ft_flat, _ = spec_tokens(fit) if fit else (None, None)
    if st is None or ft_flat is None:
        print(f'  {cid}: static={bool(st)} fitted={bool(ft_flat)} '
              f'(class {cl.get("load_sym", "?") if cl else "?"})')
        stat_missing.append(cid)
        continue
    # compare scalar token sequences (ignore loop structure first)
    sc = collections.Counter(norm(st))
    fc = collections.Counter(norm(ft_flat))
    match = (sc == fc)
    print(f'  {cid} {cl["load_sym"].split("4Load")[0][1:]}: '
          f'{"MATCH" if match else "DIFF"}  '
          f'static counts {dict(sc)}')
    print(f'      fitted counts {dict(fc)}')
    (stat_ok if match else stat_diff).append(cid)

# how many of the 21 remaining have static sequences?
print('\n=== remaining 21: static coverage ===')
cov = 0
for cid in remaining:
    cl = loads.get(hex(int(cid)))
    if cl and cl.get('read_seq'):
        cov += 1
        fit = comps.get(cid) or comps.get(str(int(cid)))
        ft_flat, _ = spec_tokens(fit) if fit else (None, None)
        m = 'MATCH' if (ft_flat and collections.Counter(
            norm(cl['read_seq'])) == collections.Counter(norm(ft_flat))) \
            else ('DIFF' if ft_flat else 'NOFIT')
        print(f'  {cid} {cl["load_sym"].split("4Load")[0][1:]}: {m}')
    else:
        print(f'  {cid}: no static sequence in r24')
print(f'static sequences available for {cov}/21 remaining')

# final provenance tally
n_static = sum(1 for e in prov['provenance']
               if e['prov'] == 'STATIC_DISASM')
print(f'\nprovenance before: STATIC_DISASM={n_static}, FITTED_ISLAND=52')
json.dump(dict(priority=dict(ok=stat_ok, diff=stat_diff,
                             missing=stat_missing),
               remaining_static=cov),
          open('/home/z/my-project/download/s32_t4_static_vs_fitted.json',
               'w'), indent=1)
print('wrote s32_t4_static_vs_fitted.json')
