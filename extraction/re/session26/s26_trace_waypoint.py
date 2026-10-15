#!/usr/bin/env python3
"""Run ONE real waypoint record through the engine Load, dump reader events."""
import struct, json, sys, collections

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
from lvc_tracer import Tracer, STREAM, READERS

DATA = '/home/z/my-project/work/data'

d = open(f'{DATA}/GothamCity.lvc', 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
# parse strings
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]
pos += 4
strings = []
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
    pos += ln
print(f'strings: {nstr}')

tr = Tracer()
tr.load_lvc(d, strings)

# record 2628: off=0x4e6132 tid=0x798f size=71
for rec_off, tid in ((0x4e6132, 0x798f),):
    tr.set_cursor(rec_off)
    comp = tr.new_component()
    err = tr.run(0x2A7E58, [comp, STREAM])
    end = tr.get_cursor()
    print(f'tid {tid:#x} @ {rec_off:#x}: err={err} benign={tr.benign_fault} '
          f'end={end:#x} consumed={end-rec_off}')
    ev = tr.trace.events
    print('reader events:')
    run = []
    for i, (addr, cur) in enumerate(ev):
        nxt = ev[i + 1][1] if i + 1 < len(ev) else end
        name = READERS.get(addr, hex(addr))
        run.append((name, cur, nxt - cur, d[cur:cur + min(nxt - cur, 16)].hex()))
    for name, cur, sz, hx in run:
        print(f'  {name:<16} @{cur:#x} +{sz}  {hx}')
