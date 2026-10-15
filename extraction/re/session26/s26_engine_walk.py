#!/usr/bin/env python3
"""Session 26 T1: HYBRID ENGINE WALK — the authoritative framing run.

Dedicated dispatcher cases -> run the REAL CLevel::LoadNextObject case code
(full engine call, engine reads every byte itself).
Generic records          -> replicate CreateObject's loop in Python using the
   banked gol template DB (== the natively-populated GOM map, verified on a
   sample), running each flag==0 component's REAL Load with per-component
   fault isolation (a fault truncates THAT component only, matching
   CreateObject->NULL->GCT-default => 0 reads for unknown ctids).
Unknown tids / -1        -> 4-byte skip (engine-verified: CreateObject
   default-inserts an empty vector; -1 returns 0 and the outer caller
   resumes).

Outputs (per island):
  s26_eng_<island>_records.json  [id, off, tid, end, benign, ncomp]
  s26_eng_<island>_toks.json     per-record folded read tokens
"""
import struct, json, sys, collections, time

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM, READERS, NESTING_PARENTS
import s26_lnobj_harness as H

from unicorn.arm_const import UC_ARM_REG_R0

DATA = '/home/z/my-project/work/data'
LN_OBJ = H.LN_OBJ

DEDICATED = {0x2662, 0x2661, 0xdbbb8, 0x2669, 0x2666, 0x798f, 0x4741,
             0x2667, 0xbba, 0x265f, 0x1869f, 0x1011, 0x265e, 0x2653,
             0x14050, 0x14051, 0x2657, 0x267d}
KNOWN_COMP = {0x14ca79, 0x152b87, 0x2ad2a046}


def fold(events, end, buf, strings):
    """Fold raw (reader, cursor) events into (kind, off, size, val) tokens."""
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
    H.load_gol_dict(tr, open(f'{DATA}/gol.bin', 'rb').read())
    H.populate_gom(tr)
    H.install_stubs(tr)
    tr.mu.mem_write(STREAM + 0x8, struct.pack('<I', table_off))
    tr.set_cursor(17)
    DEBUG_FIRST = int(__import__('os').environ.get('S26_DEBUG', '0'))
    _dbg = []

    walk = json.load(open(f'/tmp/my-project/work/walk_records_{island}.json'))
    walk_by_off = {r['off']: (int(r['end'], 16), r['tid']) for r in walk
                   if r['ok']}
    n_match = n_div = n_new = 0
    first_divs = []

    out_rec = open(f'/tmp/my-project/work/s26_eng_{island}_records.json', 'w')
    out_tok = open(f'/tmp/my-project/work/s26_eng_{island}_toks.json', 'w')
    out_rec.write('[')
    out_tok.write('[')
    n_recs = n_tok = 0
    cur = 17
    rid = 0
    t0 = time.time()
    stats = collections.Counter()
    tokbuf = []
    recbuf = []
    while cur < table_off:
        rid += 1
        tid = struct.unpack_from('>i', d, cur)[0]
        tr.benign_fault = None
        if tid == -1 or tid not in templates and tid not in DEDICATED:
            # engine: LoadNextObject reads tid; -1 -> return 0; unknown ->
            # CreateObject -> map default-insert empty -> 0 component reads
            end = cur + 4
            rec = [rid, cur, tid, end, None, 0]
            toks = [('i', cur, 4, tid)]
            stats[f'skip {tid & 0xFFFFFFFF:#x}' if tid != -1 else 'skip -1'] \
                += 1
        elif tid in DEDICATED:
            err = tr.run(LN_OBJ, [H.LEVEL])
            end = tr.get_cursor()
            toks = fold(tr.trace.events, end, d, strings)
            rec = [rid, cur, tid, end, tr.benign_fault, -1]
            stats[f'dedicated {tid & 0xFFFFFFFF:#x}'] += 1
        else:
            comps = templates[tid]
            toks = [('i', cur, 4, tid)]
            p = cur + 4
            ncomp = 0
            for flag, ctid in comps:
                if flag:
                    continue
                c0 = p
                if ctid == 0x152b87:
                    idx = struct.unpack_from('>i', d, p)[0]
                    nm = strings[idx] if 0 <= idx < len(strings) else None
                    toks.append(('STR', p, 4, idx if nm is None else nm))
                    toks.append(('raw', p + 4, 4, None))
                    p += 8
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
                    p = tr.get_cursor()
                    toks += fold(tr.trace.events, p, d, strings)
                ncomp += 1
            end = p
            rec = [rid, cur, tid, end, None, ncomp]
            stats[f'tmpl {tid & 0xFFFFFFFF:#x}'] += 1
        key = hex(cur)
        if key in walk_by_off:
            we, wtid = walk_by_off[key]
            if we == end:
                n_match += 1
            else:
                n_div += 1
                if len(first_divs) < 12:
                    first_divs.append((rid, key, hex(tid & 0xFFFFFFFF),
                                       wtid, hex(we), hex(end), rec[4]))
        else:
            n_new += 1
            if len(first_divs) < 12 and n_new < 6:
                first_divs.append((rid, key, hex(tid & 0xFFFFFFFF),
                                   'NEW', '-', hex(end), rec[4]))
        if rid % 500 == 0:
            print(f'    [diff] match={n_match} div={n_div} new={n_new}',
                  flush=True)
            if first_divs:
                for fd in first_divs[-4:]:
                    print('      ', fd, flush=True)
        if DEBUG_FIRST and rid <= DEBUG_FIRST:
            print(f'  rec {rid} @{cur:#x} tid={tid:#x} end={end:#x} '
                  f'benign={rec[4]} ntok={len(toks)}')
        recbuf.append(json.dumps(rec))
        tokbuf.append(json.dumps([rid, toks]))
        n_recs += 1
        n_tok += len(toks)
        cur = end
        if n_recs % 2000 == 0:
            out_rec.write(','.join(recbuf) + ',')
            out_tok.write(','.join(tokbuf) + ',')
            recbuf = []
            tokbuf = []
            print(f'... {n_recs} recs @{cur:#x} '
                  f'({n_recs/(time.time()-t0):.0f}/s) toks={n_tok}',
                  flush=True)
    out_rec.write(','.join(recbuf) + ']')
    out_tok.write(','.join(tokbuf) + ']')
    out_rec.close()
    out_tok.close()
    print(f'== {island}: {n_recs} records, end {cur:#x} / {table_off:#x} '
          f'(complete={cur == table_off}), {n_tok} tokens, '
          f'{time.time()-t0:.0f}s')
    print('header count:', nrec_hdr)
    for k, v in stats.most_common(30):
        print(f'   {k}: {v}')


if __name__ == '__main__':
    main()
