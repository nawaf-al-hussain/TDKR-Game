#!/usr/bin/env python3
"""Probe CComponentBuiltinCylinder::Load after the real 0x798f record,
and extract the engine's full 0x798f + 0x2657 read sequences."""
import sys, struct, json

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM, READERS
import s26_lnobj_harness as H

DATA = '/home/z/my-project/work/data'
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
H.build(tr)
H.install_stubs(tr)

# the 0x798f record: payload starts at 0x4e6136, Load reads 67 B ->
# extra data at 0x4e6179 (3 floats + cylinder)
REC = 0x4e6132
tr.set_cursor(REC + 4)
comp = tr.new_component()
tr.benign_fault = None
err = tr.run(0x2A7E58, [comp, STREAM])
wp_end = tr.get_cursor()
print(f'waypoint Load: err={err} end={wp_end:#x} (+{wp_end-REC-4})')

# now emulate the dispatcher's 0x798f continuation: 3 ReadFloats are in the
# case code; then BuiltinCylinder::Load(this=scratch, stream)
SCRATCH = 0x54D00000
tr.mu.mem_map(SCRATCH, 0x1000)
tr.mu.mem_write(SCRATCH, b'\x00' * 0x1000)
tr.set_cursor(wp_end)
ev0 = []
for i in range(3):
    err = tr.run(0x339B94, [STREAM])   # CMemoryStream::ReadFloat
    ev0.append(tr.get_cursor())
    print(f'  extra float {i}: -> {struct.unpack_from(">f", d, ev0[-1]-4)[0]}')
cyl_start = tr.get_cursor()
tr.benign_fault = None
err = tr.run(0x2E1000, [SCRATCH, STREAM])
cyl_end = tr.get_cursor()
print(f'cylinder Load: err={err} benign={tr.benign_fault} '
      f'end={cyl_end:#x} (+{cyl_end-cyl_start})')
print(f'TOTAL 0x798f record: {cyl_end - REC} B (walk had 71 + skips)')

ev = tr.trace.events
print('cylinder reader events:')
for a, c in ev:
    nm = READERS.get(a, hex(a))
    print(f'   {nm} @{c:#x} bytes={d[c:c+8].hex()}')

# what follows the cylinder?
print('bytes after cylinder:', d[cyl_end:cyl_end+24].hex())
print('next tid:', hex(struct.unpack_from(">i", d, cyl_end)[0]))
