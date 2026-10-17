#!/usr/bin/env python3
"""S30 T1: validate the static CTrafficSetting::Load spec (@0x1ffa1c,
ret @0x1ffeb4) against the 15 banked spans (tid 0x3189E053 = 831119443)."""
import json, struct, glob

SPEC = [
    ['i'], ['c'], ['f'], ['f'], ['f'], ['STR'],
    ['f'], ['f'], ['f'], ['f'], ['f'], ['f'],
    ['i'],
    ['rep', 'last', [['i'], ['i'], ['i']]],
    ['i'],
    ['rep', 'last', [
        ['i'], ['i'], ['i'],
        ['rep', 'last', [['STR'], ['f']]],
        ['i'],
    ]],
]
NAT = {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}


class Abort(Exception):
    pass


class Reader:
    def __init__(self, data, p):
        self.d = data; self.p = p; self.fields = []

    def tok(self, kind, out=None):
        size = NAT[kind]
        off = self.p
        b = self.d[self.p:self.p + size]
        self.p += size
        val = struct.unpack_from('>i', b, 0)[0] \
            if kind in ('i', 'STR') else \
            (struct.unpack_from('>f', b, 0)[0] if kind == 'f' else b[0])
        self.fields.append(val)
        if out is not None:
            out.append((kind, off, size, val))


def replay(spec, r, out, limit=None):
    i = 0
    while i < len(spec):
        if limit is not None and r.p > limit:
            raise Abort()
        tok = spec[i]
        if tok[0] == 'rep':
            cnt = r.fields[-1]
            if cnt < 0 or cnt > 100000:
                raise Abort()
            for _ in range(cnt):
                replay(tok[2], r, out, limit)
                if limit is not None and r.p > limit:
                    raise Abort()
            i += 1
        else:
            r.tok(tok[0], out)
            i += 1


def island_strings(data):
    table_off = struct.unpack_from('>I', data, 4)[0]
    pos = table_off
    n = struct.unpack_from('>i', data, pos)[0]; pos += 4
    out = []
    for _ in range(n):
        ln = struct.unpack_from('>i', data, pos)[0]; pos += 4
        out.append(data[pos:pos + ln].decode('utf-8', 'replace')); pos += ln
    return out


tab = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                     'session26/lvc_readseq.json'))
spans = tab['spans']['831119443']
toks = tab['span_toks']['831119443']
lvcs, strs = {}, {}
for f in glob.glob('/tmp/my-project/work/data/*.lvc'):
    isl = f.rsplit('/', 1)[1][:-4]
    lvcs[isl] = open(f, 'rb').read()
    strs[isl] = island_strings(lvcs[isl])

npass = nfail = 0
fails = []
for off, size in spans:
    best = None
    for isl, data in lvcs.items():
        if off + size > len(data):
            continue
        r = Reader(data, off)
        out = []
        try:
            replay(SPEC, r, out, limit=off + size)
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
        (g[3] == b[3] or (g[0] == 'STR' and (g[3] >= 0 and g[3] < len(strs[isl]) and strs[isl][g[3]] == b[3])))
        for g, b in zip(out, btoks))
    if ok:
        npass += 1
    else:
        nfail += 1
        for k, (g, b) in enumerate(zip(out, btoks)):
            gv = (strs[isl][g[3]] if 0 <= g[3] < len(strs[isl]) else g[3]) if g[0] == 'STR' else g[3]
            if g[0] != b[0] or g[2] != b[2] or g[1] != b[1] or gv != b[3]:
                fails.append((off, size, f'{isl} diff@{k}: banked '
                              f'{b[:3]}={str(b[3])[:16]} vs spec '
                              f'{g[:3]}={str(gv)[:16]}'))
                break
        else:
            fails.append((off, size, f'{isl} len {len(out)} vs {len(btoks)}'))
print(f'CTrafficSetting static spec vs {len(spans)} banked instances:')
print(f'  PASS {npass} / {npass + nfail}')
for f in fails[:6]:
    print('  FAIL', f)
