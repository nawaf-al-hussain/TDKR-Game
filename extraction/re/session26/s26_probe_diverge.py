#!/usr/bin/env python3
"""Probe the divergent records: 0x264b @0x15f1 and 0x1872d @0x49710."""
import struct, json, sys

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM, READERS
from s26_lnobj_harness import (build, load_gol_dict, populate_gom, DATA,
                               LN_OBJ, LEVEL)

d = open(f'{DATA}/GothamCity.lvc', 'rb').read()
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
tr = Tracer()
tr.load_lvc(d, strings)
build(tr)
load_gol_dict(tr, open('/home/z/my-project/work/data/gol.bin', 'rb').read())
populate_gom(tr)
import s26_lnobj_harness as H
H.install_stubs(tr)

for off in (0x15f1, 0x49710):
    tid = struct.unpack_from('>i', d, off)[0]
    tr.set_cursor(off)
    err = tr.run(LN_OBJ, [LEVEL])
    end = tr.get_cursor()
    print(f'\n=== record @{off:#x} tid={tid:#x} engine_end={end:#x} '
          f'(+{end-off}) err={err} benign={tr.benign_fault}')
    # reader events
    ev = tr.trace.events
    agg = []
    for i, (addr, cur) in enumerate(ev):
        nxt = ev[i + 1][1] if i + 1 < len(ev) else end
        name = READERS.get(addr, hex(addr))
        agg.append((name, cur, nxt - cur))
    # compress consecutive same-reader runs
    comp = []
    for name, cur, sz in agg:
        if comp and comp[-1][0] == name and comp[-1][2] == sz and \
                comp[-1][3] + sz == cur:
            comp[-1][1] += 1
            comp[-1][3] = cur
        else:
            comp.append([name, 1, sz, cur])
    for name, cnt, sz, last in comp:
        print(f'   {name:<15} x{cnt:<4} +{sz}')
    # gol template for this tid
    gol = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/'
                         'session24/gol_templates.json'))
    t = gol['templates'].get(hex(tid & 0xFFFFFFFF))
    print(f'   template: {t}')
    print(f'   name: {gol["names"].get(hex(tid & 0xFFFFFFFF))}')
