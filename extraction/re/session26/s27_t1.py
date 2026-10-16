#!/usr/bin/env python3
"""s27 T1: independence run (all 12 game_config.gla levels), header-count
test (records + real waypoint links == header count?), Lua script union.

Reuses lvc_pure's Reader/replay + the banked read-sequence tables.
Per-record try/except: a failure blocks the rest of the file (no safe
resync without record framing); the blocking class is reported.
"""
import collections
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lvc_pure import Reader, replay, load_table  # noqa: E402

TABLE_DIR = HERE
DATA = '/home/z/my-project/work/data'
LEVELS = ['GothamCity', 'GothamCity_Island2', 'BatCave', 'Military',
          'Police_Station', 'Stadion', 'StockExchange', 'Test', 'ThePit',
          'Underground', 'l_menu', 'shop']

WAYPOINT_TIDS = {18241, 9830, 31119}   # 0x4741, 0x2666, 0x798f
# the 12 link slots = token positions 6..17 within the 20-token waypoint head
LINK_POS = set(range(6, 18))


def parse_level(path, table, templates):
    d = open(path, 'rb').read()
    assert d[:4] == b'DICT', 'bad magic'
    table_off = struct.unpack_from('>I', d, 4)[0]
    nrec_hdr = struct.unpack_from('>I', d, 13)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', d, pos)[0]
        pos += 4
        strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
        pos += ln

    dedicated = table['dedicated']
    engine_cases = table['engine_cases']
    components = table['components']
    spans_c = {k: dict((e[0], e[1]) for e in v)
               for k, v in table.get('spans', {}).items()}
    span_toks = {k: {int(o): v for o, v in dd.items()}
                 for k, dd in table.get('span_toks', {}).items()}
    spans_e = {k: dict((t, l) for t, l in v)
               for k, v in table.get('spans_e', {}).items()}
    span_toks_e = {k: {int(o): v for o, v in dd.items()}
                   for k, dd in table.get('span_toks_e', {}).items()}

    r = Reader(d, strings)
    toks = []
    stats = collections.Counter()
    cls_records = collections.Counter()      # component class -> record count
    cls_strbytes = collections.Counter()     # component class -> str bytes
    ded_strbytes = collections.Counter()     # dedicated tid -> str bytes
    links_total = 0
    n_way = 0
    n_cyl = 0
    fail = None
    nrec = 0
    cur = 17
    while cur < table_off:
        nrec += 1
        rec_start = cur
        tid = struct.unpack_from('>i', d, cur)[0]
        t0 = len(toks)
        r.p = cur
        try:
            if tid == -1:
                r.tok('i', None, toks)
                kind = 'skip'
            elif str(tid) in engine_cases:
                spec = engine_cases[str(tid)]
                if spec and spec[0][0] == 'span':
                    st = span_toks_e.get(str(tid), {}).get(table_off)
                    if st is not None:
                        for t in st:
                            toks.append(tuple(t))
                        r.p += sum(t[2] for t in st)
                    else:
                        r.raw(spans_e[str(tid)][table_off], toks)
                else:
                    replay(spec, r, toks)
                kind = f'engine {tid:#x}'
            elif str(tid) in dedicated:
                replay(dedicated[str(tid)], r, toks)
                kind = f'ded {tid:#x}'
            elif tid in templates:
                comps = templates[tid]
                r.tok('i', None, toks)
                for flag, ctid in comps:
                    if flag:
                        continue
                    ks = str(ctid)
                    if ks not in components:
                        raise RuntimeError(
                            f'no spec for component {ks}')
                    spec = components[ks]
                    cstart = r.p
                    if spec and spec[0][0] == 'span':
                        st = span_toks.get(ks, {}).get(cstart)
                        if st is not None:
                            for t in st:
                                toks.append(tuple(t))
                            r.p += sum(t[2] for t in st)
                        else:
                            r.raw(spans_c[ks][cstart], toks)
                    else:
                        replay(spec, r, toks)
                    cls_records[ks] += 1
                kind = f'tmpl {tid:#x}'
            else:
                r.tok('i', None, toks)
                kind = 'skip'
        except (RuntimeError, KeyError, Exception) as e:
            fail = dict(record=nrec, offset=cur, tid=tid,
                        err=type(e).__name__, msg=str(e)[:120])
            nrec -= 1
            break
        end = r.p
        # waypoint link census
        if tid in WAYPOINT_TIDS:
            n_way += 1
            rec_toks = toks[t0:]
            if tid == 31119:
                n_cyl += 1
            nlink = sum(1 for j, t in enumerate(rec_toks[:20])
                        if j in LINK_POS and t[0] == 'i' and t[3] != -1)
            links_total += nlink
        # STR byte census
        for t in toks[t0:]:
            if t[0] == 'STR' and isinstance(t[3], str):
                if str(tid) in dedicated or str(tid) in engine_cases:
                    ded_strbytes[f'{tid:#x}'] += len(t[3].encode()) + 1
                else:
                    # attribute to the component class: re-walk is costly;
                    # attribute at record level via templates? keep per-record
                    cls_strbytes[f'rec{tid:#x}'] += len(t[3].encode()) + 1
        stats[kind] += 1
        cur = end
    complete = (cur == table_off) and fail is None
    return dict(records=nrec, complete=complete, fail=fail,
                table_off=table_off, nrec_hdr=nrec_hdr, nstr=nstr,
                end=cur, stats=dict(stats), links=links_total,
                waypoints=n_way, cylinders=n_cyl,
                ded_strbytes=dict(ded_strbytes),
                rec_strbytes=dict(cls_strbytes),
                cls_records=dict(cls_records))


def main():
    table, templates = load_table(TABLE_DIR)
    out = {}
    for lv in LEVELS:
        p = os.path.join(DATA, lv + '.lvc')
        res = parse_level(p, table, templates)
        hc_test = None
        if res['complete']:
            for hyp, add in (('rec+links', res['links']),
                             ('rec+cyl+links',
                              res['links'] + res['cylinders'])):
                if res['records'] + add == res['nrec_hdr']:
                    hc_test = hyp
        res['header_count_test'] = hc_test
        out[lv] = res
        print(f"{lv:22s} rec={res['records']:6d}/{res['nrec_hdr']:6d} "
              f"complete={res['complete']} end={res['end']:#x}/"
              f"{res['table_off']:#x} links={res['links']} "
              f"way={res['waypoints']} cyl={res['cylinders']} "
              f"hc_test={hc_test}")
        if res['fail']:
            f = res['fail']
            print(f"    FAIL @{f['offset']:#x} rec {f['record']} "
                  f"tid {f['tid']:#x}: {f['err']} {f['msg']}")
    json.dump(out, open(os.path.join(HERE, 's27_t1_results.json'), 'w'),
              indent=1)
    print('-> s27_t1_results.json')


if __name__ == '__main__':
    main()
