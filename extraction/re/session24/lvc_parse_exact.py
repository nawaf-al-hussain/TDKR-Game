#!/usr/bin/env python3
"""DETERMINISTIC LVC parser — no resync heuristics. v2 clean rewrite.

Framing sources (disasm-verified):
- Header: 'DICT' | u32be tableOffset | u8 wideFlag | u16be tag | u16be ver=3
  | u32be recordCount ; records sequential [u32be typeId][payload] until table.
- Dedicated handlers from CLevel::LoadNextObject (lnobj_full2.asm).
- Generic: CGameObjectManager::CreateObject @0x36774c walks the gol.bin
  component template list; flag==0 components Load() from the stream.
"""
import struct, json, sys, collections

GOL = '/home/z/my-project/work/TDKR-Game/extraction/re/session24/gol_templates.json'
LOADS = '/home/z/my-project/work/TDKR-Game/extraction/re/session24/component_loads.json'
gol = json.load(open(GOL))
loads = json.load(open(LOADS))
templates = {int(k, 16): [(f, t) for f, t in v] for k, v in gol['templates'].items()}
SPECIAL = {
    0x14ca79: [('B', 1), ('i', 4)] + [('f', 4)] * 9 + [('B', 1)] * 3,   # 44B
    0x152b87: [('STR', None)] + [('B', 1)] * 4,
    # CTriggerComponent::Load = CComponentTrigger::Load (i,9f,i,c,STR,i,c)
    # + CMatrix4 ctor (0 reads) + CLuaScriptManager::LoadFromBuffer (0 reads):
    # the STR interned index IS the Lua script source.
    0x37f7a8ae: [('i', 4)] + [('f', 4)] * 9 + [('i', 4), ('B', 1), ('STR', None),
                                               ('i', 4), ('B', 1)],
    # CEffectComponent::Load = CComponentBuiltinEffect::Load @0x2d7ad8
    # (STR, i, STR, c, c, c, f, f = 23B; byte-verified on a 0x2652 record)
    0x2ca13c06: [('STR', None), ('i', 4), ('STR', None), ('B', 1), ('B', 1),
                 ('B', 1), ('f', 4), ('f', 4)],
}

class Fail(Exception):
    pass

class R:
    def __init__(self, d, pos, end, strings):
        self.d, self.p, self.end = d, pos, end
        self.strings = strings
    def b(self):
        if self.p >= self.end: raise Fail('eof')
        v = self.d[self.p]; self.p += 1; return v
    def i(self):
        if self.p + 4 > self.end: raise Fail('eof')
        v = struct.unpack_from('>i', self.d, self.p)[0]; self.p += 4; return v
    def f(self):
        if self.p + 4 > self.end: raise Fail('eof')
        v = struct.unpack_from('>f', self.d, self.p)[0]; self.p += 4; return v
    def s(self):
        # DICT flag byte == 0: ReadString consumes a u32be INDEX into the
        # stream's charTable (CMemoryStream constructed with the string table).
        idx = self.i()
        if idx < -1 or idx > 100000: raise Fail(f'bad str idx {idx}')
        if idx == -1 or idx >= len(self.strings): return ''
        return self.strings[idx]
    def raw(self, k):
        if k < 0 or self.p + k > self.end: raise Fail('eof raw')
        v = self.d[self.p:self.p+k]; self.p += k; return v

def parse_0x2657(r):
    """LevelInit (banked parse_lvc.py) + TLP + GlobalIllum."""
    for _ in range(6): r.s()
    r.b()
    r.s()
    nmiss = r.i()
    for _ in range(nmiss):
        for _ in range(4): r.s()
        r.b(); r.s(); r.i()
        r.s(); r.s(); r.i()
        for _ in range(4): r.s()
        r.b()
    r.b(); r.s(); r.b()
    for _ in range(25): r.f()
    r.b()
    # CTemplateLevelProperties::Load: f, string, f, f
    r.f(); r.s(); r.f(); r.f()
    # CComponentBaseGlobalIllum::Load
    r.b(); r.i(); r.f(); r.f()
    r.raw(4); r.f(); r.f(); r.raw(4)
    np_ = r.i()
    for _ in range(np_): r.i(); r.i()
    r.b(); r.b()
    for _ in range(3): r.s()
    for _ in range(4): r.f()
    r.s()
    r.f(); r.f(); r.raw(4)
    for _ in range(3): r.f()
    r.raw(4)

def parse_generic(r, tid, out):
    tmpl = templates.get(tid)
    if tmpl is None:
        # map::operator[] default-inserts an EMPTY component list:
        # zero payload bytes for a typeId absent from gol.bin.
        k = hex(tid)
        out['counts_empty'][k] = out['counts_empty'].get(k, 0) + 1
        return
    for flag, ctid in tmpl:
        if flag != 0:
            continue
        if ctid == 0xf5f8cfd:
            # CAnimationComponent::Load = CComponentAnimated::Load @0x3bce84:
            # STR,STR,f,STR,4B,STR,i(nf), nf x [i(n), n x (STR,f)], B
            r.s(); r.s(); r.f(); r.s(); r.raw(4); r.s()
            nf = r.i()
            for _ in range(nf):
                n = r.i()
                for _ in range(n):
                    r.s(); r.f()
            r.b()
            out['comp_counts'][f'{ctid:#x}'] = out['comp_counts'].get(f'{ctid:#x}', 0) + 1
            continue
        if ctid == 0x4ab8a7cd:
            # CSmartLightComponent::Load = CComponentSmartLight::Load @0x2e30bc:
            # STR, c, f, f, c, i, c, i, i(count), count x [c,c,c,c,i,i,i,f]
            lights = []
            r.s(); r.b(); r.f(); r.f(); r.b(); r.i(); r.b(); nl = r.i()
            for _ in range(nl):
                e = [r.b(), r.b(), r.b(), r.b(), r.i(), r.i(), r.i(), r.f()]
                lights.append(e)
            out['lights'].append({'n': nl, 'lights': lights})
            out['comp_counts'][f'{ctid:#x}'] = out['comp_counts'].get(f'{ctid:#x}', 0) + 1
            continue
        if ctid == 0x2db081e2:
            # CCollisionComponent::Load @0x2230a8 (full decode):
            # 16B prefix = CComponentCollision::Load @0x2d72bc (c,c,STR,i,c,c,i)
            # then [u8 nprim][per prim: STR name, i32 triCount,
            #       triCount x (9 x f32 verts + u8 flag)][i32 n2][n2 x i32]
            pc = r.b(); pc2 = r.b(); pn = r.s(); pi = r.i(); pb = r.b(); pb2 = r.b(); pi2 = r.i()
            nprim = r.b()
            prims = []
            for _ in range(nprim):
                nm = r.s()
                tc = r.i()
                tris = []
                for _ in range(tc):
                    verts = [r.f() for _ in range(9)]
                    flg = r.b()
                    tris.append((verts, flg))
                prims.append({'name': nm, 'ntri': tc, 'tris': tris})
            n2 = r.i()
            refs = [r.i() for _ in range(n2)]
            out['collide'].append({'prefix': [pc, pc2, pn, pi, pb, pb2, pi2],
                                   'nprim': nprim, 'prims': prims, 'n2': n2, 'refs': refs})
            out['comp_counts'][f'{ctid:#x}'] = out['comp_counts'].get(f'{ctid:#x}', 0) + 1
            continue
        seq = SPECIAL.get(ctid)
        if seq is None:
            e = loads.get(f'{ctid:#010x}') or loads.get(f'{ctid:#x}')
            if not e or e.get('read_seq') is None:
                raise Fail(f'undecoded comp {ctid:#x}')
            if e.get('var'):
                raise Fail(f'comp {ctid:#x} variable reads unhandled')
            r.raw(e['fixed'])
        else:
            for kind, sz in seq:
                if kind == 'STR':
                    r.s()
                else:
                    r.raw(sz)
        out['comp_counts'][f'{ctid:#x}'] = out['comp_counts'].get(f'{ctid:#x}', 0) + 1

def parse_lvc(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'DICT'
    table_off = struct.unpack_from('>I', d, 4)[0]
    nrec_hdr = struct.unpack_from('>I', d, 13)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
        strings.append(d[pos:pos+ln].decode('utf-8', 'replace')); pos += ln
    r = R(d, 17, table_off, strings)
    out = {'records': 0, 'fail': collections.Counter(), 'fail_at': None,
           'spawn': [], 'lua': [], 'mesh': [], 'marker': [], 'collide': [], 'lights': [],
           'counts': collections.Counter(), 'counts_empty': collections.Counter(), 'comp_counts': collections.Counter()}
    while r.p < table_off:
        rec_start = r.p
        try:
            tid = r.i()
            out['records'] += 1
            out['counts'][hex(tid)] += 1
            if tid == 0x2662:  # CSpawnPointObject::Create (session-13 + handler disasm)
                r.b(); objid = r.i()
                trs = [r.f() for _ in range(9)]
                r.raw(3)
                name = r.s(); lua = r.s()
                r.raw(3); r.i()
                out['spawn'].append({'objId': objid, 'name': name, 'lua': lua, 'pos': trs[0:3]})
                if lua:
                    out['lua'].append({'objId': objid, 'name': name, 'lua': lua})
            elif tid == 0x2663:
                objid = r.i()
                trs = [r.f() for _ in range(9)]
                out['marker'].append({'objId': objid, 'pos': trs[0:3]})
            elif tid == 0x2664:
                r.i()
            elif tid == 0x2661:  # dispatcher: STR, c, f, i
                r.s(); r.b(); r.f(); r.i()
            elif tid == 0xdbbb8 or tid == 0x2669 or tid == 0x11fc6 or tid == 0x256 or tid == 0x4741:
                pass  # verified zero stream reads
            elif tid in (0x2666, 0x798f):  # dispatcher: f, f, f
                r.f(); r.f(); r.f()
            elif tid == 0x2667 or tid == 0xbba:  # CTemplateZone::Load + extra ReadInt
                r.b(); r.s(); r.f(); r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3); r.i()
            elif tid == 0x265f:  # CTemplateMetaZone::Load
                r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3); r.i(); r.i(); r.s()
            elif tid == 0x1869f:  # CTemplateBakeGroup::Load
                r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3)
                r.s(); r.f(); r.s(); r.f()
            elif tid == 0x1011:  # CZone::LoadIrradianceVolume
                r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3); r.s()
                r.raw(5); r.f(); r.b(); r.f(); r.f()
            elif tid == 0x265e:  # CComponentBase::Load only
                r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3)
            elif tid == 0x2653:  # CTemplateOccluder::Load: c,i,9f,ccc,STR,4c,f
                r.b(); r.i()
                for _ in range(9): r.f()
                r.raw(3); r.s(); r.raw(4); r.f()
            elif tid in (0x14050, 0x14051):
                r.b(); r.i()
                trs = [r.f() for _ in range(9)]
                r.raw(3)
                mesh = r.s()
                four = r.raw(4)
                out['mesh'].append({'tid': hex(tid), 'mesh': mesh, 'flags': four.hex(),
                                    'pos': trs[0:3]})
            elif tid == 0x2657:
                parse_0x2657(r)
            else:
                parse_generic(r, tid, out)
        except Fail as ex:
            out['fail'][str(ex)] += 1
            out['fail_at'] = (hex(r.p), out['records'])
            break
    out['end'] = r.p
    out['table_off'] = table_off
    out['n_hdr'] = nrec_hdr
    return out, strings

if __name__ == '__main__':
    rep, strings = parse_lvc(sys.argv[1])
    print(f"records parsed: {rep['records']} / header {rep['n_hdr']}")
    print(f"cursor end: {rep['end']:#x} / body end {rep['table_off']:#x} "
          f"({'COMPLETE' if rep['end'] == rep['table_off'] else 'INCOMPLETE'})")
    print('counts:', dict(sorted(rep['counts'].items(), key=lambda kv: -kv[1])[:16]))
    print('failures:', dict(rep['fail']), 'at', rep['fail_at'])
