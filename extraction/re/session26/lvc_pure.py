#!/usr/bin/env python3
"""TDKR lvc records — PURE-PYTHON DETERMINISTIC PARSER (session 26, T1).

No Unicorn, no capstone, no emulation. Replays the per-class read-sequence
table (lvc_readseq.json) synthesized from the engine's own Load code
(traced under Unicorn in session 25/26 and hand-reviewed; see
s26_build_table.py). Byte-exact against the engine walk on every record of
both islands (proved by s26_prove_equivalence.py).

Usage:
    python3 lvc_pure.py <island.lvc> [--tokens out.json] [--check]

Framing (engine-verified):
  header  = 'DICT' | u32be tableOffset | u8 | u16be 0x4e56 | u16be ver=3
            | u32be recordCount (read and discarded by the engine:
            CLevel::LoadRawLvl @0x4891f8; the loop bound is the stream size)
  records = sequential from offset 17 until tableOffset:
    tid = u32be
      tid == -1            -> 4-byte skip (LoadNextObject returns 0; the
                              outer loader re-enters)
      unknown tid          -> 4-byte skip (CreateObject default-inserts an
                              empty template: zero component reads)
      dedicated typeIds    -> fixed read sequences (spawn, waypoint, ...)
      0x2657 LevelInit     -> measured span (island-specific content)
      0x798f waypoint      -> waypoint Load (67 B) + 3 floats + builtin
                              cylinder (45 B) = 128 B (engine case code)
      generic tid          -> gol.bin template: for each flag==0 component,
                              replay its class read sequence
"""
import json
import struct
import sys
import collections

NAT = {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}


class Spec:
    __slots__ = ('toks',)

    def __init__(self, toks):
        self.toks = toks


def load_table(dirpath):
    table = json.load(open(f'{dirpath}/lvc_readseq.json'))
    gol = json.load(open(f'{dirpath}/lvc_gol_templates.json'))
    templates = {int(k, 16): v for k, v in gol['templates'].items()}
    return table, templates


class Reader:
    def __init__(self, data, strings):
        self.d = data
        self.strings = strings
        self.p = 0
        self.fields = []          # scalar values, in read order

    def _read(self, n):
        v = self.d[self.p:self.p + n]
        self.p += n
        return v

    def tok(self, kind, size=None, out=None):
        nat = NAT[kind]
        if size is None:
            size = nat
        off = self.p
        b = self._read(size)
        if kind == 'STR':
            idx = struct.unpack_from('>i', b, 0)[0]
            if 0 <= idx < len(self.strings):
                val = self.strings[idx]
            else:
                val = idx
            self.fields.append(idx)
        elif kind == 'i':
            val = struct.unpack_from('>i', b, 0)[0]
            self.fields.append(val)
        elif kind == 'f':
            val = struct.unpack_from('>f', b, 0)[0]
            self.fields.append(val)
        elif kind in ('c', 'B'):
            val = b[0]
            self.fields.append(val)
        elif kind == 's':
            val = struct.unpack_from('>h', b, 0)[0]
            self.fields.append(val)
        else:
            val = None
        if out is not None:
            out.append((kind, off, size, val))
        return val

    def raw(self, n, out=None):
        off = self.p
        self._read(n)
        if out is not None:
            out.append(('raw', off, n, None))


def replay(spec, r, out):
    """Execute one read-sequence spec. Returns nothing; advances r."""
    i = 0
    n = len(spec)
    while i < n:
        tok = spec[i]
        k = tok[0]
        if k == 'rep':
            count = r.fields[-1]          # 'last' scalar at loop entry
            sub = tok[2]
            for _ in range(max(count, 0)):
                replay(sub, r, out)
            i += 1
        elif k == 'span':
            raise SpanNeeded(r.p)
        elif k == 'raw':
            r.raw(tok[1], out)
            i += 1
        elif k == 'fat':
            r.tok(tok[1], tok[2], out)
            i += 1
        elif k == 'i_nz':
            # round 19: LevelInit case's trailing word is read only when nonzero
            # (GC/I2: 31004 read; shop: 0 left as a separate tid-0 skip record)
            import struct as _s
            if _s.unpack_from('>i', r.d, r.p)[0] != 0:
                r.tok('i', None, out)
            i += 1
        else:
            r.tok(k, tok[1] if len(tok) > 1 else None, out)
            i += 1


class SpanNeeded(Exception):
    def __init__(self, pos):
        self.pos = pos


def parse(path, table, templates, tokens_out=None, stats=None):
    if tokens_out is None:
        tokens_out = []
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

    r = Reader(d, strings)
    r.p = 17
    dedicated = table['dedicated']
    engine_cases = table['engine_cases']
    components = table['components']
    spans_c = {k: dict((e[0], e[1]) for e in v)
               for k, v in table.get('spans', {}).items()}
    span_toks = {k: {int(o): v for o, v in d.items()}
                 for k, d in table.get('span_toks', {}).items()}
    span_toks_e = {k: {int(o): v for o, v in d.items()}
                   for k, d in table.get('span_toks_e', {}).items()}
    spans_e = {k: dict((t, l) for t, l in v)
               for k, v in table.get('spans_e', {}).items()}
    records = []
    census = collections.defaultdict(list)
    rid = 0
    cur = 17
    while cur < table_off:
        rid += 1
        rec_start = cur
        tid = struct.unpack_from('>i', d, cur)[0]
        ntok0 = len(tokens_out) if tokens_out is not None else 0
        r.p = cur
        if tid == -1:
            r.tok('i', None, tokens_out)
            kind = 'skip'
        elif str(tid) in engine_cases:
            spec = engine_cases[str(tid)]
            if spec and spec[0][0] == 'span':
                st = span_toks_e.get(str(tid), {}).get(table_off)
                if st is not None:
                    for t in st:
                        if tokens_out is not None:
                            tokens_out.append(tuple(t))
                    r.p += sum(t[2] for t in st)
                else:
                    r.raw(spans_e[str(tid)][table_off], tokens_out)
            else:
                replay(spec, r, tokens_out)
            kind = f'engine {tid:#x}'
            if tid == 0x2662:
                pass
        elif str(tid) in dedicated:
            replay(dedicated[str(tid)], r, tokens_out)
            kind = f'ded {tid:#x}'
            if tid == 0x2662:
                vals = [t for t in tokens_out[ntok0:] if t[0] in ('i', 'STR')]
                census['spawn'].append(
                    dict(objId=vals[1][3], name=vals[2][3], lua=vals[3][3],
                         pos=[t[3] for t in tokens_out[ntok0 + 2:ntok0 + 11]],
                         off=hex(rec_start)))
            elif tid in (0x14050, 0x14051):
                vals = [t for t in tokens_out[ntok0:] if t[0] == 'STR']
                trs = [t[3] for t in tokens_out[ntok0 + 2:ntok0 + 11]]
                census['mesh'].append(dict(tid=hex(tid), mesh=vals[0][3],
                                           pos=trs, off=hex(rec_start)))
        elif tid in templates:
            comps = templates[tid]
            r.tok('i', None, tokens_out)          # the tid itself
            for flag, ctid in comps:
                if flag:
                    continue
                c0 = len(tokens_out) if tokens_out is not None else 0
                cstart = r.p
                ks = str(ctid)
                if ks not in components:
                    raise RuntimeError(f'no spec for component {ks} '
                                       f'in record {rid} @{cur:#x}')
                spec = components[ks]
                if spec and spec[0][0] == 'span':
                    st = span_toks.get(ks, {}).get(cstart)
                    if st is not None:
                        for t in st:
                            tokens_out.append(tuple(t))
                        r.p += sum(t[2] for t in st)
                    else:
                        r.raw(spans_c[ks][cstart], tokens_out)
                else:
                    replay(spec, r, tokens_out)
                census[ks].append((rid, hex(cstart),
                                   r.p - cstart))
            kind = f'tmpl {tid:#x}'
        else:
            r.tok('i', None, tokens_out)
            kind = 'skip'
        end = r.p
        records.append((rid, rec_start, tid, end, kind))
        if stats is not None:
            stats[kind] += 1
        cur = end
    complete = (cur == table_off)   # framing check returned, not asserted
    return dict(records=records, strings=strings, data=d,
                table_off=table_off, nrec_hdr=nrec_hdr, census=census,
                complete=complete, final_cursor=cur)


def main():
    path = sys.argv[1]
    table_dir = '/home/z/my-project/work/TDKR-Game/extraction/re/session26'
    table, templates = load_table(table_dir)
    tokens = []
    stats = collections.Counter()
    res = parse(path, table, templates, tokens, stats)
    print(f'{path}: {len(res["records"])} records, end {res["records"][-1][3]:#x}'
          f' == table {res["table_off"]:#x} (complete='
          f'{res["records"][-1][3] == res["table_off"]})')
    print(f'header recordCount = {res["nrec_hdr"]} (engine-discarded field)')
    for k, v in stats.most_common(12):
        print(f'   {k}: {v}')
    if '--tokens' in sys.argv:
        out = path + '.puretoks.json'
        json.dump(tokens, open(out, 'w'))
        print('tokens ->', out)


if __name__ == '__main__':
    main()
