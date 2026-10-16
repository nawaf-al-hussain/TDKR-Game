#!/usr/bin/env python3
"""s27: decode the 0x2657 LevelInit span class from the two measured island
streams (GC 1339 B, I2 799 B), build a real read-sequence spec, verify
byte-exact on the islands, then apply to the other 10 levels and require
the remaining records to parse to table end (independence run v2).
"""
import collections
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lvc_pure import Reader, replay, load_table  # noqa: E402

DATA = '/home/z/my-project/work/data'
LEVELS = ['GothamCity', 'GothamCity_Island2', 'BatCave', 'Military',
          'Police_Station', 'Stadion', 'StockExchange', 'Test', 'ThePit',
          'Underground', 'l_menu', 'shop']


def build_spec_9815(t):
    """Engine-proven 0x2657 spec from CComponentLevelInit::Load @0x2018f0 +
    CTemplateLevelProperties::Load @0x2023bc (Ghidra decompiled, verified
    against both measured island streams)."""
    st = t['span_toks_e']['9815']
    streams = [st[k] for k in st]
    a = [(x[0], x[2]) for x in streams[0]]
    b = [(x[0], x[2]) for x in streams[1]]
    LI = [['i', 4]] + [['STR', 4]] * 6 + [['c', 1], ['STR', 4], ['i', 4]]
    UNIT = ([['STR', 4]] * 4 + [['c', 1], ['STR', 4], ['i', 4]]
            + [['STR', 4]] * 2 + [['i', 4]] + [['STR', 4]] * 4 + [['c', 1]])
    POST = ([['c', 1], ['STR', 4], ['c', 1]] + [['f', 4]] * 25
            + [['c', 1], ['f', 4], ['STR', 4], ['f', 4], ['f', 4]])
    # GlobalIllum block: engine-fixed; take kinds from the measured GC tail
    # (verified identical to I2's) after f@0xa8..f@0xb4
    fA = next(i for i, x in enumerate(a) if x[0] == 'f')
    gi_start = fA + 25 + 1 + 4          # f*25, c@0xa0, f,STR,f,f
    gi_end = len(a) - 1                 # final ReadInt @+0x128 excluded
    GI = [list(x) for x in a[gi_start:gi_end]]
    assert a[fA + 25][0] == 'c' and a[gi_end][0] == 'i'
    spec = (LI + [['rep', None, UNIT]] + POST
            + [list(x) for x in GI] + [['i', 4]])
    ok = verify_spec(spec, t)
    print(f"0x2657 spec built: prologue 10 + 15*count + post 3 + f*25 "
          f"+ 1 + 4 + GI {len(GI)} + 1 tokens; islands verify = {ok}")
    assert ok
    return spec


def verify_spec(spec, t):
    """Replay spec over both measured island streams; require exact match."""
    st = t['span_toks_e']['9815']
    for k, want in st.items():
        want = [tuple(x) for x in want]
        fake = Reader(b'\x00' * 4096, [])
        got = []
        # synthesize reads: replay needs real bytes; instead simulate by
        # walking the spec with the measured stream as the data source
        # -> simplest: rebuild bytes from the measured tokens and replay
        buf = bytearray()
        offs = []
        for x in want:
            offs.append(len(buf))
            v = x[3]
            if x[0] == 'STR':
                buf += struct.pack('>i', 0)   # placeholder idx
            elif x[0] == 'i':
                buf += struct.pack('>i', v if isinstance(v, int) else 0)
            elif x[0] == 's':
                buf += struct.pack('>h', v or 0)
            elif x[0] in ('c', 'B'):
                buf += bytes([v or 0])
            elif x[0] == 'f':
                buf += struct.pack('>f', v or 0.0)
            else:
                buf += b'\x00' * x[2]
        # rebuild with real string indices so STR values resolve
        fake = Reader(bytes(buf), [''] * 4)
        # patch STR indices: we need idx -> but replay only records idx;
        # compare offsets+sizes+kinds instead of values
        got = []
        p0 = fake.p
        try:
            replay([list(x) for x in spec], fake, got)
        except Exception as e:                     # noqa: BLE001
            print('  verify fail:', e)
            return False
        if len(got) != len(want):
            print(f'  verify: token count {len(got)} != {len(want)}')
            return False
        if any(g[0] != w[0] or g[2] != w[2] for g, w in zip(got, want)):
            print('  verify: kind/size mismatch')
            return False
        o0 = got[0][1]
        w0 = want[0][1]
        if ([g[1] - o0 for g in got] != [w[1] - w0 for w in want]):
            print('  verify: relative offsets mismatch')
            return False
    return True


def main():
    table, templates = load_table(HERE)
    if table['engine_cases'].get('9815') and \
            table['engine_cases']['9815'][0][0] != 'span':
        print('0x2657 spec already baked into table (session 27); skip rebuild')
        spec = table['engine_cases']['9815']
    else:
        spec = build_spec_9815(table)
        table['engine_cases']['9815'] = spec
        table.pop('spans_e', None)
        table.pop('span_toks_e', None)
    results = {}
    for lv in LEVELS:
        path = os.path.join(DATA, lv + '.lvc')
        d = open(path, 'rb').read()
        assert d[:4] == b'DICT'
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
        r = Reader(d, strings)
        toks = []
        stats = collections.Counter()
        cls_strbytes = collections.Counter()
        cls_records = collections.Counter()
        linkvals = []
        fail = None
        nrec = 0
        cur = 17
        dedicated = table['dedicated']
        engine_cases = table['engine_cases']
        components = table['components']
        spans_c = {k: dict((e[0], e[1]) for e in v)
                   for k, v in table.get('spans', {}).items()}
        span_toks = {k: {int(o): v for o, v in dd.items()}
                     for k, dd in table.get('span_toks', {}).items()}
        while cur < table_off:
            nrec += 1
            rec_start = cur
            tid = struct.unpack_from('>i', d, cur)[0]
            t0 = len(toks)
            r.p = cur
            cur_comp = [None]
            try:
                if tid == -1:
                    r.tok('i', None, toks)
                    kind = 'skip'
                elif str(tid) in engine_cases:
                    replay(engine_cases[str(tid)], r, toks)
                    kind = f'engine {tid:#x}'
                elif str(tid) in dedicated:
                    replay(dedicated[str(tid)], r, toks)
                    kind = f'ded {tid:#x}'
                elif tid in templates:
                    r.tok('i', None, toks)
                    for flag, ctid in templates[tid]:
                        if flag:
                            continue
                        ks = str(ctid)
                        if ks not in components:
                            raise RuntimeError(f'no spec for component {ks}')
                        spec_c = components[ks]
                        cstart = r.p
                        if spec_c and spec_c[0][0] == 'span':
                            stc = span_toks.get(ks, {}).get(cstart)
                            if stc is not None:
                                for tt in stc:
                                    toks.append(tuple(tt))
                                r.p += sum(x[2] for x in stc)
                            else:
                                r.raw(spans_c[ks][cstart], toks)
                        else:
                            cur_comp[0] = ks
                            replay(spec_c, r, toks)
                            cur_comp[0] = None
                        cls_records[ks] += 1
                    kind = f'tmpl {tid:#x}'
                else:
                    r.tok('i', None, toks)
                    kind = 'skip'
            except Exception as e:                     # noqa: BLE001
                fail = dict(record=nrec, offset=cur, tid=tid,
                            err=type(e).__name__, msg=str(e)[:120])
                nrec -= 1
                break
            end = r.p
            if tid in (18241, 9830, 31119):
                rt = toks[t0:t0 + 20]
                linkvals += [t[3] for j, t in enumerate(rt)
                             if 6 <= j < 18 and t[0] == 'i']
            owner = cur_comp[0]
            for tt in toks[t0:]:
                if tt[0] == 'STR' and isinstance(tt[3], str):
                    key = owner if owner else f'tid{tid:#x}'
                    cls_strbytes[key] += len(tt[3].encode()) + 1
            stats[kind] += 1
            cur = end
        complete = cur == table_off and fail is None
        # header-count hypotheses
        nway = stats.get('ded 0x4741', 0) + stats.get('ded 0x2666', 0) \
            + stats.get('engine 0x798f', 0)
        ncyl = stats.get('engine 0x798f', 0)
        real_links = sum(1 for v in linkvals if v != -1)
        uniq = sorted(set(v for v in linkvals if v != -1))
        hyps = {
            'rec+links': (nrec + real_links, nrec + real_links == nrec_hdr),
            'rec+cyl+links': (nrec + ncyl + real_links,
                              nrec + ncyl + real_links == nrec_hdr),
            'rec+uniq_targets': (nrec + len(uniq),
                                 nrec + len(uniq) == nrec_hdr),
        }
        results[lv] = dict(
            records=nrec, complete=complete, fail=fail,
            table_off=table_off, nrec_hdr=nrec_hdr, nstr=nstr, end=cur,
            stats=dict(stats), waypoints=nway, cylinders=ncyl,
            links=real_links, uniq_targets=len(uniq),
            max_link=max(linkvals) if linkvals else None,
            hyps=hyps, cls_records=dict(cls_records),
            cls_strbytes=dict(cls_strbytes))
        print(f"{lv:22s} rec={nrec:6d}/{nrec_hdr:6d} complete={complete} "
              f"end={cur:#x}/{table_off:#x} links={real_links} "
              f"uniqT={len(uniq)} maxlink="
              f"{max(linkvals) if linkvals else '-'}")
        for hname, (val, ok) in hyps.items():
            if ok:
                print(f'    HEADER-COUNT HIT: {hname} = {val}')
        if fail:
            f = fail
            print(f"    FAIL @{f['offset']:#x} rec {f['record']} "
                  f"tid {f['tid']:#x}: {f['err']} {f['msg']}")
    json.dump(results, open(os.path.join(HERE, 's27_t1_results.json'), 'w'),
              indent=1)
    json.dump(table, open(os.path.join(HERE, 'lvc_readseq.json'), 'w'),
              indent=0, separators=(',', ':'))
    print('-> s27_t1_results.json; lvc_readseq.json patched with the real '
          '0x2657 spec (span tables for 9815 removed)')


if __name__ == '__main__':
    main()
