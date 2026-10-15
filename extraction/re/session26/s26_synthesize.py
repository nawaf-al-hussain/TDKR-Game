#!/usr/bin/env python3
"""Synthesize per-class read-sequence specs from the v2 walk's component
slices. Outputs variability report + the fixed-spec draft table."""
import json, collections, struct, sys

ISLANDS = ['GothamCity', 'GothamCity_Island2']

def tok_pat(tk):
    """(kind, size) pattern of a token list."""
    return tuple((t[0], t[2]) for t in tk)

def main():
    classes = collections.defaultdict(lambda: collections.defaultdict(list))
    # classes[key][pattern] = [(island, rid, values...)]
    for isl in ISLANDS:
        slices = json.load(open(f'/tmp/my-project/work/s26_v2_{isl}_comps.json'))
        for rid, comps in slices:
            for key, tk in comps:
                classes[json.dumps(key)][tok_pat(tk)].append(
                    (isl, rid, [t[3] for t in tk][:6]))
    print(f'{"key":<22} {"#pats":>5} {"#recs":>6}  patterns (kind,size x count)')
    var_keys = []
    for key, pats in sorted(classes.items(),
                            key=lambda kv: -sum(len(v) for v in kv[1].values())):
        total = sum(len(v) for v in pats.values())
        if total < 2:
            continue
        fixed = len(pats) == 1
        if not fixed:
            var_keys.append(key)
        ps = sorted(pats.items(), key=lambda kv: -len(kv[1]))
        desc = ' | '.join(
            f'{len(v)}x[{",".join(f"{k}{s}" for k, s in p)}]'
            for p, v in ps[:3])
        print(f'{key:<22} {len(pats):>5} {total:>6}  {desc[:110]}')
    print(f'\nvariable classes: {len(var_keys)}')
    json.dump(var_keys, open('/tmp/my-project/work/s26_var_classes.json', 'w'))
    # dump full pattern examples for variable classes
    out = {}
    for key in var_keys:
        pats = classes[key]
        out[key] = {','.join(f'{k}{s}' for k, s in p): v[:3]
                    for p, v in pats.items()}
    json.dump(out, open('/tmp/my-project/work/s26_var_patterns.json', 'w'),
              indent=1)
    # also dump singletons (rare classes) for completeness
    singles = {k: [[list(p), v[:2]] for p, v in pats.items()]
               for k, pats in classes.items()
               if sum(len(v) for v in pats.values()) == 1}
    json.dump(singles, open('/tmp/my-project/work/s26_single_classes.json',
                            'w'), indent=1)
    print('wrote s26_var_patterns.json, s26_single_classes.json')

if __name__ == '__main__':
    main()
