#!/usr/bin/env python3
"""Session 26 T1 — CORRECTED EMULATOR WALK (v2).

Architecture = round-15's walk (per-component engine Loads, Python dedicated
handlers) with two engine-verified fixes:
  0x2657 (LevelInit, 1/island): run the REAL CLevel::LoadNextObject case
       (it routes into CTemplateLevelProperties::Load) — 1,339 B, not the
       banked 1,335 B + 4-B phantom skip.
  0x798f (waypoint+collider): the dispatcher case = waypoint Load (67 B)
       + 3 ReadFloat + CComponentBuiltinCylinder::Load (45 B) — run the real
       case via LoadNextObject.  (The walk previously read only the waypoint
       and misframed each following cylinder block as 4-B float skips.)
-1 / unknown tid: 4-B skip (engine-verified: LoadNextObject returns 0 at -1
   and the outer loader re-enters; CreateObject default-inserts an empty
   template for unknown tids).

Outputs per island:
  s26_v2_<island>_records.json   [id, off, tid, end, benign, ncomp]
  s26_v2_<island>_toks.json      [id, [(kind, off, size, val), ...]]
"""
import struct, json, sys, collections, time

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM, READERS, NESTING_PARENTS
import s26_lnobj_harness as H

DATA = '/home/z/my-project/work/data'
LN_OBJ = H.LN_OBJ
ENGINE_CASE_TIDS = {0x2657, 0x798f}
DEDICATED_PY = {0x2662, 0x2661, 0xdbbb8, 0x2669, 0x2666, 0x4741, 0x2667,
                0xbba, 0x265f, 0x1869f, 0x1011, 0x265e, 0x2653, 0x14050,
                0x14051, 0x267d}


def fold(events, end, buf, strings):
    out = []
    ev = events
    n = len(ev)
    i = 0
    while i < n:
        addr, cur = ev[i]
        name = READERS.get(addr)
        if name is None:
            i += 1
            continue
        if addr in NESTING_PARENTS:
            if i + 1 < n and ev[i + 1][1] == cur and ev[i + 1][0] == 0x339914:
                i += 1
            size = (ev[i + 1][1] if i + 1 < n else end) - cur
            idx = struct.unpack_from('>i', buf, cur)[0]
            val = strings[idx] if 0 <= idx < len(strings) else None
            out.append(('STR', cur, size, idx if val is None else val))
        else:
            size = (ev[i + 1][1] if i + 1 < n else end) - cur
            if name in ('ReadInt', 'Read_intref', 'Read_uintref'):
                val = struct.unpack_from('>i', buf, cur)[0]
                kind = 'i'
            elif name in ('ReadFloat', 'Read_floatref'):
                val = struct.unpack_from('>f', buf, cur)[0]
                kind = 'f'
            elif name in ('ReadChar', 'Read_charref'):
                val = buf[cur]
                kind = 'c'
            elif name in ('ReadByte', 'Read_ucharref', 'ReadBool_ref',
                          'Read_boolref'):
                val = buf[cur]
                kind = 'B'
            elif name in ('ReadShort', 'Read_shortref', 'Read_ushortref'):
                val = struct.unpack_from('>h', buf, cur)[0]
                kind = 's'
            else:
                val = None
                kind = name
            out.append((kind, cur, size, val))
        i += 1
    return out


def parse_0x2657(r):
    for _ in range(6):
        r.s()
    r.b()
    r.s()
    nmiss = r.i()
    for _ in range(nmiss):
        for _ in range(4):
            r.s()
        r.b(); r.s(); r.i()
        r.s(); r.s(); r.i()
        for _ in range(4):
            r.s()
        r.b()
    r.b(); r.s(); r.b()
    for _ in range(25):
        r.f()
    r.b()
    r.f(); r.s(); r.f(); r.f()          # TLP
    r.b(); r.i(); r.f(); r.f()          # GlobalIllum
    r.raw(4); r.f(); r.f(); r.raw(4)
    np_ = r.i()
    for _ in range(np_):
        r.i(); r.i()
    r.b(); r.b()
    for _ in range(3):
        r.s()
    for _ in range(4):
        r.f()
    r.s()
    r.f(); r.f(); r.raw(4)
    for _ in range(3):
        r.f()
    r.raw(4)


def main():
    island = sys.argv[1] if len(sys.argv) > 1 else 'GothamCity'
    d = open(f'{DATA}/{island}.lvc', 'rb').read()
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
    gol = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/'
                         'session24/gol_templates.json'))
    templates = {int(k, 16): v for k, v in gol['templates'].items()}
    fac = {int(k, 16): int(v['load'], 16)
           for k, v in json.load(open('/home/z/my-project/work/'
                                      'factory_switch.json')).items()
           if v.get('load')}
    gct = {int(k, 16): int(v['load'], 16)
           for k, v in json.load(open('/home/z/my-project/work/'
                                      'gct_switch.json')).items()
           if v.get('load')}
    loads = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/'
                           'session24/component_loads.json'))
    syms = json.load(open('/home/z/my-project/work/so_syms.json'))['by_name']
    load_addrs = {}
    for tid, e in loads.items():
        s = e.get('load_sym')
        if s and s in syms:
            load_addrs[int(tid, 16)] = int(syms[s], 16)

    tr = Tracer()
    tr.load_lvc(d, strings)
    H.build(tr)
    # NOTE: no stubs on the main tracer — byte-for-byte walk-equivalent
    # (the walk's benign faults on Lua registration prevent global writes
    #  that otherwise change later harness behavior)
    tr.mu.mem_write(STREAM + 0x8, struct.pack('<I', table_off))
    # tracer B: pristine environment for state-polluting engine cases
    # (0x2657 LevelInit sets a global that changes later harness behavior;
    #  the real engine's own reads are proven by the walk's exact completion)
    trB = Tracer()
    trB.load_lvc(d, strings)
    H.build(trB)
    H.install_stubs(trB)
    trB.mu.mem_write(STREAM + 0x8, struct.pack('<I', table_off))

    walk = json.load(open(f'/tmp/my-project/work/walk_records_{island}.json'))
    walk_by_off = {r['off']: (int(r['end'], 16), r['tid']) for r in walk
                   if r['ok']}
    n_match = n_div = n_new = 0
    first_divs = []
    ABORT_AFTER = int(__import__('os').environ.get('S26_ABORT', '0'))

    out_rec = open(f'/tmp/my-project/work/s26_v2_{island}_records.json', 'w')
    out_tok = open(f'/tmp/my-project/work/s26_v2_{island}_toks.json', 'w')
    out_rec.write('[')
    out_tok.write('[')
    recbuf, tokbuf = [], []
    all_comp_slices = []
    n_recs = n_tok = 0
    cur = 17
    rid = 0
    t0 = time.time()
    stats = collections.Counter()
    census = collections.defaultdict(list)
    CENSUS_CLASSES = {0x2db081e2, 0x37f7a8ae, 0x4ab8a7cd, 0x2ca13c06,
                      0xf5f8cfd, 0x2ef26c52, 0x54989cb1, 0x365cfd67}
    while cur < table_off:
        rid += 1
        tid = struct.unpack_from('>i', d, cur)[0]
        tr.benign_fault = None
        toks = []
        ncomp = 0
        benign = None
        if tid == -1 or (tid not in templates and tid not in DEDICATED_PY
                         and tid not in ENGINE_CASE_TIDS):
            end = cur + 4
            toks = [('i', cur, 4, tid)]
            stats['skip'] += 1
        elif tid in ENGINE_CASE_TIDS:
            trB.set_cursor(cur)
            err = trB.run(LN_OBJ, [H.LEVEL])
            end = trB.get_cursor()
            toks = fold(trB.trace.events, end, d, strings)
            benign = trB.benign_fault
            all_comp_slices.append((rid, [(('E', tid), toks)]))
            stats[f'engine-case {tid & 0xFFFFFFFF:#x}'] += 1
        elif tid in DEDICATED_PY:
            tr.set_cursor(cur + 4)
            toks.append(('i', cur, 4, tid))
            # python-side reads that drive the tracer cursor
            class Cur:
                def __init__(s2):
                    s2.toks = toks
                def cur(s2):
                    return tr.get_cursor()
                def adv(s2, n2, kind, val=None):
                    p = tr.get_cursor()
                    toks.append((kind, p, n2, val))
                    tr.set_cursor(p + n2)
                    return val
                def i(s2):
                    p = tr.get_cursor()
                    return s2.adv(4, 'i', struct.unpack_from('>i', d, p)[0])
                def f(s2):
                    p = tr.get_cursor()
                    return s2.adv(4, 'f', struct.unpack_from('>f', d, p)[0])
                def b(s2):
                    p = tr.get_cursor()
                    return s2.adv(1, 'B', d[p])
                def s(s2):
                    p = tr.get_cursor()
                    idx = struct.unpack_from('>i', d, p)[0]
                    nm = strings[idx] if 0 <= idx < len(strings) else None
                    return s2.adv(4, 'STR', idx if nm is None else nm)
                def raw(s2, k):
                    p = tr.get_cursor()
                    return s2.adv(k, 'raw')
            r = Cur()
            if tid == 0x2662:
                r.b()
                objid = r.i()
                trs = [r.f() for _ in range(9)]
                r.raw(3)
                nm = r.s(); lua = r.s()
                r.raw(3); r.i()
                census['spawn'].append(dict(objId=objid, name=nm, lua=lua,
                                            pos=trs[0:3], off=hex(cur)))
            elif tid == 0x2661:
                r.s(); r.b(); r.f(); r.i()
            elif tid == 0xdbbb8:
                err = tr.run(0x2B56F4, [tr.new_component(), STREAM])
                end = tr.get_cursor()
                toks += fold(tr.trace.events, end, d, strings)
            elif tid == 0x2669:
                err = tr.run(0x40E994, [tr.new_component(), STREAM])
                end = tr.get_cursor()
                toks += fold(tr.trace.events, end, d, strings)
            elif tid in (0x2666, 0x4741):
                err = tr.run(0x2A7E58, [tr.new_component(), STREAM])
                end = tr.get_cursor()
                toks += fold(tr.trace.events, end, d, strings)
            elif tid in (0x2667, 0xbba):
                r.b(); r.s(); r.f(); r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3); r.i()
            elif tid == 0x265f:
                r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3); r.i(); r.i(); r.s()
            elif tid == 0x1869f:
                r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3)
                r.s(); r.f(); r.s(); r.f()
            elif tid == 0x1011:
                r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3); r.s()
                r.raw(5); r.f(); r.b(); r.f(); r.f()
            elif tid == 0x265e:
                r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3)
            elif tid == 0x2653:
                r.b(); r.i()
                for _ in range(9):
                    r.f()
                r.raw(3); r.s(); r.raw(4); r.f()
            elif tid in (0x14050, 0x14051):
                r.b(); r.i()
                trs = [r.f() for _ in range(9)]
                r.raw(3)
                mesh = r.s()
                four = r.raw(4) or b''
                census['mesh'].append(dict(tid=hex(tid), mesh=mesh,
                                           flags=four.hex(),
                                           pos=trs[0:3], off=hex(cur)))
            elif tid == 0x267d:
                err = tr.run(0x1D17CC, [tr.new_component(), STREAM])
                end = tr.get_cursor()
                toks += fold(tr.trace.events, end, d, strings)
            end = tr.get_cursor()
            all_comp_slices.append((rid, [(('D', tid), toks)]))
            stats[f'ded {tid & 0xFFFFFFFF:#x}'] += 1
        else:
            comps = templates[tid]
            toks = [('i', cur, 4, tid)]
            tr.set_cursor(cur + 4)
            p = cur + 4
            comp_slices = []
            for flag, ctid in comps:
                if flag:
                    continue
                c0 = p
                ntok0 = len(toks)
                if ctid == 0x152b87:
                    idx = struct.unpack_from('>i', d, p)[0]
                    nm = strings[idx] if 0 <= idx < len(strings) else None
                    toks.append(('STR', p, 4, idx if nm is None else nm))
                    toks.append(('raw', p + 4, 4, None))
                    p += 8
                    tr.set_cursor(p)
                elif ctid == 0x14ca79:
                    err = tr.run(0x1FE924, [tr.new_component(), STREAM])
                    p = tr.get_cursor()
                    toks += fold(tr.trace.events, p, d, strings)
                elif ctid == 0x2ad2a046:
                    err = tr.run(0x2A45D0, [tr.new_component(), STREAM])
                    p = tr.get_cursor()
                    toks += fold(tr.trace.events, p, d, strings)
                else:
                    la = fac.get(ctid) or gct.get(ctid) or \
                        load_addrs.get(ctid)
                    if la is None:
                        stats[f'ctid-skip {ctid:#x}'] += 1
                        continue
                    err = tr.run(la, [tr.new_component(), STREAM])
                    if err or tr.benign_fault:
                        import os as _os
                        with open('/tmp/my-project/work/s26_faults.txt',
                                  'a') as _f:
                            _f.write(f'{tid:#x} {ctid:#x} {p:#x} '
                                     f'{err} {tr.benign_fault}\n')
                    p = tr.get_cursor()
                    pre = len(toks)
                    toks += fold(tr.trace.events, p, d, strings)
                    if toks[pre:pre + 1] and toks[pre][1] > c0:
                        # inlined head reads produce no reader events:
                        # record the gap so the token stream stays
                        # gap-free and byte-exact
                        toks.insert(pre, ('raw', c0,
                                          toks[pre][1] - c0, None))
                    comp_slices.append((ctid, toks[pre:]))
                    if ctid in CENSUS_CLASSES:
                        census[f'{ctid:#x}'].append(
                            dict(off=hex(c0), toks=[
                                (k, o, s, v if not isinstance(v, str) or
                                 len(v) < 40 else v[:40])
                                for k, o, s, v in toks[-60:]]))
                ncomp += 1
            end = p
            comp_slices.append(('REC', [('i', cur, 4, tid)]))
            all_comp_slices.append((rid, comp_slices))
            stats[f'tmpl {tid & 0xFFFFFFFF:#x}'] += 1
        key = hex(cur)
        if key in walk_by_off:
            we, wtid = walk_by_off[key]
            if we == end:
                n_match += 1
            else:
                n_div += 1
                if len(first_divs) < 10:
                    first_divs.append((rid, key, hex(tid & 0xFFFFFFFF), wtid,
                                       hex(we), hex(end), benign, ncomp))
                    print(f'    [FIRST-DIV] {first_divs[-1]}', flush=True)
        else:
            n_new += 1
            if len(first_divs) < 10 and n_new < 4:
                first_divs.append((rid, key, hex(tid & 0xFFFFFFFF), 'NEW',
                                   '-', hex(end), benign, ncomp))
        if rid % 50 == 0:
            print(f'    [diff] m={n_match} d={n_div} n={n_new} @{cur:#x}',
                  flush=True)
            for fd in first_divs[-3:]:
                print('       ', fd, flush=True)
            if ABORT_AFTER and rid >= ABORT_AFTER:
                print('ABORT at rid'); break
        if ABORT_AFTER and rid >= ABORT_AFTER:
            break
        recbuf.append(json.dumps([rid, cur, tid, end, benign, ncomp]))
        tokbuf.append(json.dumps([rid, toks]))
        n_recs += 1
        n_tok += len(toks)
        cur = end
        if n_recs % 2000 == 0:
            out_rec.write(','.join(recbuf) + ',')
            out_tok.write(','.join(tokbuf) + ',')
            recbuf, tokbuf = [], []
            print(f'... {n_recs} recs @{cur:#x} '
                  f'({n_recs/(time.time()-t0):.0f}/s) toks={n_tok}',
                  flush=True)
    out_rec.write(','.join(recbuf) + ']')
    out_tok.write(','.join(tokbuf) + ']')
    out_rec.close()
    out_tok.close()
    json.dump(all_comp_slices,
              open(f'/tmp/my-project/work/s26_v2_{island}_comps.json', 'w'))
    json.dump({k: v for k, v in census.items()},
              open(f'/tmp/my-project/work/s26_v2_{island}_census.json', 'w'))
    print(f'== {island}: {n_recs} records, end {cur:#x}/{table_off:#x} '
          f'complete={cur == table_off}, {n_tok} tokens, {time.time()-t0:.0f}s')
    print('header count:', nrec_hdr)
    for k, v in stats.most_common(25):
        print(f'   {k}: {v}')


if __name__ == '__main__':
    main()
