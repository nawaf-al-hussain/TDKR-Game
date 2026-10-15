#!/usr/bin/env python3
"""Prove pure-parser == engine-walk equivalence on every record of both
islands: identical record boundaries AND identical token streams."""
import json, sys, struct

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TABLE_DIR = '/home/z/my-project/work/TDKR-Game/extraction/re/session26'
DATA = '/home/z/my-project/work/data'


def main():
    table, templates = lvc_pure.load_table(TABLE_DIR)
    gr = gm = tr = gt = 0
    for isl in ('GothamCity', 'GothamCity_Island2'):
        v2_recs = json.load(open(
            f'/tmp/my-project/work/s26_v2_{isl}_records.json'))
        v2_toks = json.load(open(
            f'/tmp/my-project/work/s26_v2_{isl}_toks.json'))
        v2_by_off = {r[1]: r for r in v2_recs}
        tok_by_id = {t[0]: [tuple(x) for x in t[1]] for t in v2_toks}
        toks = []
        res = lvc_pure.parse(f'{DATA}/{isl}.lvc', table, templates,
                             tokens_out=toks)
        precs = res['records']
        # map pure tokens to records via offsets
        bounds = [(r[1], r[3], r[0]) for r in precs]
        bi = 0
        by_id = {}
        cur_toks = []
        for t in toks:
            while bi < len(bounds) and t[1] >= bounds[bi][1]:
                by_id[bounds[bi][2]] = cur_toks
                cur_toks = []
                bi += 1
            cur_toks.append(t)
        if bi < len(bounds):
            by_id[bounds[bi][2]] = cur_toks
        n_match = n_tok = 0
        divs = []
        for rid, off, tid, end, kind in precs:
            v2r = v2_by_off.get(off)
            if v2r and v2r[3] == end:
                n_match += 1
            elif len(divs) < 6:
                divs.append(('REC', rid, hex(off), hex(tid & 0xFFFFFFFF),
                             hex(end), hex(v2r[3]) if v2r else 'NEW'))
            pt = by_id.get(rid, [])
            vt = tok_by_id.get(rid, [])
            if pt == vt:
                n_tok += 1
            elif len(divs) < 6:
                for j in range(min(len(pt), len(vt))):
                    if pt[j] != vt[j]:
                        divs.append(('TOK', rid, j, pt[j], vt[j]))
                        break
                else:
                    divs.append(('TOKLEN', rid, len(pt), len(vt)))
        gr += len(precs)
        gm += n_match
        tr += len(precs)
        gt += n_tok
        print(f"{isl}: {len(precs)} records, boundaries {n_match}/{len(precs)}"
              f", complete={precs[-1][3] == res['table_off']}, "
              f"token-streams {n_tok}/{len(precs)}")
        for dv in divs[:4]:
            print('   ', dv)
    print(f'\nEQUIVALENCE: {gm}/{gr} record boundaries exact; '
          f'{gt}/{tr} record token-streams exact (incl. values)')


if __name__ == '__main__':
    main()
