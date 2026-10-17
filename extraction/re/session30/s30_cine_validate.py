#!/usr/bin/env python3
"""S30 T1a: CCinematicComponent spec derived STATICALLY from disassembly
(CComponentCinematic::Load @0x2dce20 .. ret @0x2ddf8c,
 CContainerTracksAnimatedObject::Load @0x2d9118 .. last read @0x2d93b8).

Spec (stream order; every count read immediately before its loop):
  head: [i dur][c][f][c]
  sec1: [i n1] + n1 x { [i X][i cnt] + cnt x [i][i][i][i] }
        (outer 16-B elem = {i head, vector<i32x4>}; reader sites
         0x2dd0a0/0x2dd0b0 + 0x2dd130/.13c/.14c/.158)
  sec2: [i n2] + n2 x { [i cnt] + cnt x [i][i][STR][c] }
        (16-B elem {i,i,char*,bool}; sites 0x2dd76c, 0x2dd968/.980/.994/.99c)
  sec3: [i n3] + n3 x { [i cnt] + cnt x [i][i][STR] }
        (12-B elem {i,i,char*}; sites 0x2dda98/0x2ddcc4/.ce0/.cf4)
  sec4: [i n4] + n4 x { [STR][i cnt] + cnt x [i][i][f x6] }
        (outer 16-B {char*, vector}, inner 32-B keys;
         sites 0x2ddd20, 0x2ddac: STR 0x2dddc0 + i 0x2dddc8,
         keys 0x2dde78/.e84 + f x6 0x2dde94..0x2dded0)
  sec5: [i n5] + n5 x CContainerTracksAnimatedObject::Load @0x2d9118:
           [i A]                                  (0x2d9134)
           [i B] + B x [STR][i][f][i][i]          (0x2d9140; 0x14-B elems,
                                                   sites 0x2d91ec/.1f4/.200/.20c/.218)
           [i C] + C x { [STR][i cnt] + cnt x [f][f][f][i][i] }
                                                   (0x2d922c; 16-B elems @r7+0x10,
                                                   0x14-B keys; 0x2d92c8/.2d0 +
                                                   0x2d9350/.368/.374/.380/.38c)
           [i D]                                  (0x2d93b8; count read only,
                                                   16-B vector built from memory,
                                                   NO further stream reads)
RET @0x2ddf8c. All code after 0x2ddfa0 in the dump = vector slow paths /
cleanup (no readers), verified by full-spine scan.
"""
import json, struct, sys

CCINEMATIC = [
    ['i'], ['c'], ['f'], ['c'],
    ['i'],
    ['rep', 'last', [
        ['i'], ['i'],
        ['rep', 'last', [['i'], ['i'], ['i'], ['i']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['i'],
        ['rep', 'last', [['i'], ['i'], ['STR'], ['c']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['i'],
        ['rep', 'last', [['i'], ['i'], ['STR']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['STR'], ['i'],
        ['rep', 'last', [['i'], ['i'], ['f'], ['f'], ['f'],
                         ['f'], ['f'], ['f']]],
    ]],
    ['i'],
    ['rep', 'last', [
        # --- CContainerTracksAnimatedObject::Load @0x2d9118 (ret 0x2dad20)
        ['i'],                                   # A   0x2d9134
        ['i'],                                   # B   0x2d9140
        ['rep', 'last', [['STR'], ['i'], ['f'], ['i'], ['i']]],
        ['i'],                                   # C   0x2d922c
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # D   0x2d93b8
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['STR'], ['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # E   0x2d9ac8
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # F   0x2d9c50
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['i'], ['i'], ['STR']]],
        ]],
        ['i'],                                   # G   0x2da33c
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['STR'], ['i'], ['i'], ['STR'], ['c']]],
        ]],
        ['i'],                                   # H   0x2dab0c
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['i'], ['i'], ['STR'], ['STR'], ['c'],
                             ['f'], ['c'], ['c']]],
        ]],
    ]],
]

NAT = {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}


class Reader:
    def __init__(self, data, p):
        self.d = data
        self.p = p
        self.fields = []

    def tok(self, kind, out=None):
        size = NAT[kind]
        off = self.p
        b = self.d[self.p:self.p + size]
        self.p += size
        if kind == 'STR':
            val = struct.unpack_from('>i', b, 0)[0]
        elif kind == 'i':
            val = struct.unpack_from('>i', b, 0)[0]
        elif kind == 'f':
            val = struct.unpack_from('>f', b, 0)[0]
        else:
            val = b[0]
        self.fields.append(val)
        if out is not None:
            out.append((kind, off, size, val))


class Abort(Exception):
    pass


def replay(spec, r, out, limit=None):
    i = 0
    n = len(spec)
    while i < n:
        if limit is not None and r.p > limit:
            raise Abort()
        tok = spec[i]
        k = tok[0]
        if k == 'rep':
            count = r.fields[-1]
            if count < 0 or count > 100000:
                raise Abort()
            sub = tok[2]
            for _ in range(count):
                replay(sub, r, out, limit)
                if limit is not None and r.p > limit:
                    raise Abort()
            i += 1
        else:
            r.tok(k, out)
            i += 1


def island_strings(data):
    """Extract the lvc string pool (header at table offset, like lvc_pure)."""
    table_off = struct.unpack_from('>I', data, 4)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', data, pos)[0]
    pos += 4
    out = []
    for _ in range(nstr):
        ln = struct.unpack_from('>i', data, pos)[0]
        pos += 4
        out.append(data[pos:pos + ln].decode('utf-8', 'replace'))
        pos += ln
    return out


def main():
    tab = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/'
                         're/session26/lvc_readseq.json'))
    spans = tab['spans']['397182239']          # [(off, size)] in file order
    toks = tab['span_toks']['397182239']
    import glob
    lvcs = {}
    strs = {}
    for f in glob.glob('/tmp/my-project/work/data/*.lvc'):
        isl = f.rsplit('/', 1)[1][:-4]
        lvcs[isl] = open(f, 'rb').read()
        strs[isl] = island_strings(lvcs[isl])
    npass = nfail = 0
    fails = []
    for off, size in spans:
        # spans are file-absolute per island; find the right file by
        # re-deriving: try each island, spec must end exactly at off+size
        best = None
        for isl, data in lvcs.items():
            if off + size > len(data):
                continue
            r = Reader(data, off)
            out = []
            try:
                replay(CCINEMATIC, r, out, limit=off + size)
            except (Abort, struct.error, IndexError):
                continue
            if r.p == off + size:
                best = (isl, out)
                break
        if best is None:
            nfail += 1
            fails.append((off, size, 'no island frames exactly'))
            continue
        isl, out = best
        btoks = toks[str(off)]
        ok = len(out) == len(btoks) and all(
            g[0] == b[0] and g[2] == b[2] and g[1] == b[1] and
            (g[3] == b[3] or (g[0] == 'STR' and
                              (g[3] >= 0 and g[3] < len(strs[isl]) and strs[isl][g[3]] == b[3])))
            for g, b in zip(out, btoks))
        if ok:
            npass += 1
        else:
            nfail += 1
            for k, (g, b) in enumerate(zip(out, btoks)):
                gv = (strs[isl][g[3]] if 0 <= g[3] < len(strs[isl]) else g[3]) if g[0] == 'STR' else g[3]
                if g[0] != b[0] or g[2] != b[2] or g[1] != b[1] or gv != b[3]:
                    fails.append((off, size, f'{isl} first diff @{k}: '
                                  f'banked {b[:3]}={str(b[3])[:20]} vs '
                                  f'spec {g[:3]}={str(gv)[:20]}'))
                    break
            else:
                fails.append((off, size, f'{isl} len {len(out)} vs {len(btoks)}'))
    print(f'CCinematicComponent static spec vs 96 banked instances:')
    print(f'  PASS {npass} / {npass + nfail}')
    for f in fails[:12]:
        print('  FAIL', f)
    return npass, nfail


if __name__ == '__main__':
    main()
