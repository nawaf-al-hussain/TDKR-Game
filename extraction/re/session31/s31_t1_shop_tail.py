#!/usr/bin/env python3
"""S31 T1: shop tail enumeration — which record overruns table_off by 1 byte.
Replays lvc_pure.parse's record loop without the final assert, printing the
records after 0x3c00."""
import sys, json, struct, collections

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}

path = '/tmp/my-project/work/data/shop.lvc'
d = open(path, 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]
pos += 4
strings = []
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
    pos += ln

r = lvc_pure.Reader(d, strings)
dedicated = tab['dedicated']
engine_cases = tab['engine_cases']
components = tab['components']
cur = 17
rid = 0
while cur < table_off:
    rid += 1
    rec_start = cur
    tid = struct.unpack_from('>i', d, cur)[0]
    r.p = cur
    err = None
    if tid == -1:
        r.tok('i'); kind = 'skip'
    elif str(tid) in engine_cases:
        spec = engine_cases[str(tid)]
        try:
            lvc_pure.replay(spec, r, [])
        except Exception as e:
            err = f'{type(e).__name__}: {e}'
        kind = f'engine {tid:#x}'
    elif str(tid) in dedicated:
        try:
            lvc_pure.replay(dedicated[str(tid)], r, [])
        except Exception as e:
            err = f'{type(e).__name__}: {e}'
        kind = f'ded {tid:#x}'
    elif tid in templates:
        comps = templates[tid]
        r.tok('i')
        kind = f'tmpl {tid:#x}'
        for flag, ctid in comps:
            if flag:
                continue
            cstart = r.p
            ks = str(ctid)
            if ks not in components:
                err = f'NO SPEC for comp {ks}'
                break
            try:
                lvc_pure.replay(components[ks], r, [])
            except Exception as e:
                err = f'comp {ks} {type(e).__name__}: {e}'
                break
    else:
        r.tok('i'); kind = 'skip'
    end = r.p
    if rec_start >= 0x3c00 or err:
        print(f'rec {rid:4d} @{rec_start:#07x} tid {tid:#x} -> {end:#07x} '
              f'({kind}){" ERR " + err if err else ""}'
              f'{" <-- OVERUNS table " + hex(table_off) if end > table_off else ""}')
    cur = end
print(f'\nfinal cursor {cur:#x}, table_off {table_off:#x}, '
      f'distance {cur - table_off:+d} bytes')
