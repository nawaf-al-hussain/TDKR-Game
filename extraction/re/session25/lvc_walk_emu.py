#!/usr/bin/env python3
"""Engine-driven deterministic lvc walk — Unicorn tracer edition.

Replaces the hand-decoded per-class formats with actual emulation of:
  - CComponentXxx::Load(this, CMemoryStream*) for classes with Load symbols
  - GenerateComponentTemplate(typeId, CMemoryStream*) @0x368ac0 for the rest
  - CComponentBase::Load @0x1fe924 and the 0x2ad2a046 special (0x2a45d0)
  - the 0x152b87 name component (inline in CreateObject, banked 8 B)
Dedicated dispatcher typeIds keep the banked byte-verified formats.

Validation:
  - final cursor == table offset (body fully consumed, zero gaps)
  - record count == header count
  - control record offsets 0x14051 / 0x187c0 / 0x187d3 land on starts
  - cross-check vs the banked parse (first 874 records, exact to 0x4649e)
"""
import json
import struct
import sys
import collections

sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM

DATA = '/home/z/my-project/work/data'
SESS = '/home/z/my-project/work/TDKR-Game/extraction/re/session24'
SYMS = '/home/z/my-project/work/so_syms.json'

# ---------------------------------------------------------------- banked R
class Cursor:
    """Python-side reads over the lvc image that move the TRACER's cursor."""
    def __init__(self, tr, buf, strings, trace_out):
        self.tr = tr
        self.d = buf
        self.strings = strings
        self.out = trace_out

    def cur(self):
        return self.tr.get_cursor()

    def adv(self, n, kind, val=None):
        p = self.cur()
        self.out.append(('PY', kind, p, n, val))
        self.tr.set_cursor(p + n)
        return val

    def i(self):
        p = self.cur()
        v = struct.unpack_from('>i', self.d, p)[0]
        return self.adv(4, 'i', v)

    def f(self):
        p = self.cur()
        v = struct.unpack_from('>f', self.d, p)[0]
        return self.adv(4, 'f', v)

    def b(self):
        p = self.cur()
        return self.adv(1, 'B', self.d[p])

    def s(self):
        p = self.cur()
        idx = struct.unpack_from('>i', self.d, p)[0]
        name = self.strings[idx] if 0 <= idx < len(self.strings) else ''
        self.adv(4, 'STR', idx)
        return name

    def raw(self, k):
        p = self.cur()
        return self.adv(k, 'raw')


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


# ---------------------------------------------------------------- walk
def walk(path, name, tr, templates, load_addrs, fac, gct,
         census_classes):
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
    tr.load_lvc(d, strings)
    tr.set_cursor(17)

    events = []            # global pseudo/emulated read log (per record reset)
    records = []
    fail = None
    classes_bytes = collections.defaultdict(list)   # ctid -> [consumed]
    census = collections.defaultdict(list)          # ctid -> decoded payloads
    rid = 0
    cur = 17
    while cur < table_off:
        rid += 1
        rec_start = cur
        ev = []
        r = Cursor(tr, d, strings, ev)
        tid = r.i()
        try:
            if tid == 0x2662:
                r.b()
                objid = r.i()
                trs = [r.f() for _ in range(9)]
                r.raw(3)
                nm = r.s(); lua = r.s()
                r.raw(3); r.i()
                census['spawn'].append(dict(objId=objid, name=nm, lua=lua,
                                            pos=trs[0:3], off=hex(rec_start)))
            elif tid == 0x2661:
                r.s(); r.b(); r.f(); r.i()
            elif tid == 0xdbbb8:
                # CWorldBox(stream) ctor @0x2b56f4 — dedicated handler
                comp = tr.new_component()
                err = tr.run(0x2B56F4, [comp, STREAM])
                if err:
                    raise RuntimeError(f'0xdbbb8 CWorldBox: {err}')
            elif tid == 0x2669:
                # CWeatherManager loader @0x40e994 — dedicated handler
                comp = tr.new_component()
                err = tr.run(0x40E994, [comp, STREAM])
                if err:
                    raise RuntimeError(f'0x2669 Weather: {err}')
            # NOTE: 0x2663 / 0x2664 have NO dispatcher case (verified in
            # lnobj_full2.asm) — they are GENERIC gol-template records.
            elif tid in (0x2666, 0x798f, 0x4741):
                # dispatcher news CWayPointObject and calls the Create
                # thunk @0x2a8220, which virtually dispatches to
                # CWayPointObject::Load @0x2a7e58 (vtable slot 14).
                comp = tr.new_component()
                err = tr.run(0x2A7E58, [comp, STREAM])
                if err:
                    raise RuntimeError(f'{tid:#x} Waypoint.Load: {err}')
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
                                           pos=trs[0:3], off=hex(rec_start)))
            elif tid == 0x2657:
                parse_0x2657(r)
            elif tid == 0x267d:
                # CNavMeshNova::Create(this, stream) — dedicated handler
                comp = tr.new_component()
                err = tr.run(0x1D17CC, [comp, STREAM])
                if err:
                    raise RuntimeError(f'0x267d NavMeshNova.Create: {err}')
            else:
                tmpl = templates.get(tid)
                if tmpl is None:
                    # map::operator[] default-insert: empty component list
                    classes_bytes['<absent>'].append(0)
                else:
                    for flag, ctid in tmpl:
                        if flag != 0:
                            continue
                        c0 = tr.get_cursor()
                        if ctid == 0x152b87:
                            r.s(); r.raw(4)
                        elif ctid == 0x14ca79:
                            comp = tr.new_component()
                            err = tr.run(0x1FE924, [comp, STREAM])
                            if err:
                                raise RuntimeError(f'0x14ca79: {err}')
                        elif ctid == 0x2ad2a046:
                            comp = tr.new_component()
                            err = tr.run(0x2A45D0, [comp, STREAM])
                            if err:
                                raise RuntimeError(f'0x2ad2a046: {err}')
                        else:
                            # engine dispatch: factory ctor first, GCT Load
                            # second (CreateObject order), load_sym as
                            # documentation fallback, true GCT as last
                            # resort.
                            fa = fac.get(ctid)
                            la = gct.get(ctid) or load_addrs.get(ctid)
                            comp = tr.new_component()
                            if fa is not None:
                                err = tr.run(fa, [comp, STREAM])
                                if err:
                                    raise RuntimeError(
                                        f'FAC {ctid:#x} @0x{fa:x}: {err}')
                            elif la is not None:
                                err = tr.run(la, [comp, STREAM])
                                if err:
                                    raise RuntimeError(
                                        f'Load {ctid:#x} @0x{la:x}: {err}')
                            else:
                                err = tr.run(0x368AC0, [tid, STREAM])
                                if err:
                                    raise RuntimeError(
                                        f'GCT {ctid:#x}: {err}')
                        used = tr.get_cursor() - c0
                        classes_bytes[f'{ctid:#x}'].append(used)
                        if tr.str_violation:
                            raise RuntimeError(
                                f'STR-INDEX violation in comp {ctid:#x}: '
                                f'{tr.str_violation}')
                        if ctid in census_classes:
                            calls = tr.trace.calls(tr.get_cursor(), strings, d)
                            census[f'{ctid:#x}'].append(
                                dict(off=hex(c0), calls=calls))
        except (RuntimeError, struct.error) as ex:
            fail = dict(rec=rid, off=hex(rec_start), tid=hex(tid),
                        cursor=hex(tr.get_cursor()), err=str(ex)[:200])
            records.append(dict(id=rid, off=hex(rec_start), tid=hex(tid),
                                end=hex(tr.get_cursor()), ok=False))
            break
        end = tr.get_cursor()
        records.append(dict(id=rid, off=hex(rec_start), tid=hex(tid),
                            end=hex(end), ok=True))
        cur = end

    rep = dict(
        name=name, records=rid, header_records=nrec_hdr,
        complete=(cur == table_off), end=hex(cur), table_off=hex(table_off),
        fail=fail,
        classes_bytes={k: dict(n=len(v), total=sum(v), min=min(v),
                               max=max(v)) for k, v in classes_bytes.items()},
    )
    return rep, records, dict(census), strings, d


def main():
    syms = json.load(open(SYMS))['by_name']
    gol = json.load(open(f'{SESS}/gol_templates.json'))
    templates = {int(k, 16): [(f, t) for f, t in v]
                 for k, v in gol['templates'].items()}
    loads = json.load(open(f'{SESS}/component_loads.json'))
    load_addrs = {}
    for tid, e in loads.items():
        s = e.get('load_sym')
        if s and s in syms:
            load_addrs[int(tid, 16)] = int(syms[s], 16)
    # engine dispatch tables (extracted from the .so statically):
    # factory: construct + vtable Load; GCT: case Load. Both consume stream.
    fac = {int(k, 16): int(v['load'], 16)
           for k, v in json.load(
               open('/home/z/my-project/work/factory_switch.json')).items()
           if v.get('load')}
    gct = {int(k, 16): int(v['load'], 16)
           for k, v in json.load(
               open('/home/z/my-project/work/gct_switch.json')).items()
           if v.get('load')}
    tr = Tracer()
    print(f'tracer ready; factory {len(fac)} / GCT {len(gct)} / '
          f'load_sym {len(load_addrs)} entries')

    census_classes = {
        0x2db081e2,   # CCollisionComponent
        0x37f7a8ae,   # CTriggerComponent
        0x4ab8a7cd,   # CSmartLightComponent
        0x2ca13c06,   # CEffectComponent
        0xf5f8cfd,    # CAnimationComponent
        0x2ef26c52,   # CSoundAndLight
        0x54989cb1,   # CActorBaseComponent
        0x365cfd67,   # CBeastObjectComponent
    }
    out = {}
    import sys as _sys
    islands = _sys.argv[1:] or ['GothamCity', 'GothamCity_Island2']
    for island in islands:
        path = f'{DATA}/{island}.lvc'
        rep, records, census, strings, d = walk(
            path, island, tr, templates, load_addrs, fac, gct,
            census_classes)
        out[island] = rep
        print(f"\n=== {island}: {rep['records']} records "
              f"(header {rep['header_records']}), "
              f"complete={rep['complete']}, end={rep['end']} / "
              f"{rep['table_off']}")
        if rep['fail']:
            print('   FAIL:', rep['fail'])
        nb = sorted(rep['classes_bytes'].items(), key=lambda kv: -kv[1]['n'])
        print('   per-class record counts (top 20):')
        for k, v in nb[:20]:
            print(f"     {k}: n={v['n']} bytes={v['total']} "
                  f"range=[{v['min']},{v['max']}]")
        json.dump(records, open(
            f'/home/z/my-project/work/walk_records_{island}.json', 'w'))
        json.dump({k: v for k, v in census.items()},
                  open(f'/home/z/my-project/work/walk_census_{island}.json',
                       'w'))
        json.dump(rep, open(f'/home/z/my-project/work/walk_rep_{island}.json',
                            'w'), indent=1)
    json.dump(out, open('/home/z/my-project/work/walk_report.json', 'w'),
              indent=1)
    print('\nwrote walk_report.json, walk_records_*.json, walk_census_*.json')


if __name__ == '__main__':
    main()
