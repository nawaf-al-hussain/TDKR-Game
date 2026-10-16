#!/usr/bin/env python3
"""S29 T1: find SSO-inline registration records: tag bytes + id nearby."""
import struct, re
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

TAGS = [b'Cinematic\x00', b'Trigger\x00', b'Steammer\x00', b'CamEvent\x00', b'WantedManager\x00',
        b'Dummy\x00', b'Collision\x00', b'SmartLight\x00', b'LevelInit\x00', b'TrafficSetting\x00']
KNOWN_IDS = {0x17AC851F: 'CCinematicComponent', 0x10FF796: 'CDummyComponent', 0x2B: 'tid 0x2b',
             0x2657: 'CComponentLevelInit', 0x798F: 'waypoint', 0x2651: 'zone',
             0x2EE3: 'triggerLua', 0x264B: 'triggerLua2', 0x2666: 'wp2', 0x4741: 'wp3'}
# add factory switch ids
fac = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/factory_switch.json')) if False else None
import json
fac = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/factory_switch.json'))
for k in fac:
    KNOWN_IDS[int(k, 16)] = f'factory {k}'

def off2v(o): return o if o < 0xbbe1ec else o + 0x1000
def cstr_at(v, m=40):
    o = v if v < 0xbbe1ec else v - 0x1000
    if o is None or o >= len(data) or o < 0: return None
    z = data.find(b'\0', o, o + m)
    s = data[o:z if z >= 0 else o + m]
    if not all(0x20 <= c < 0x7f or c == 0 for c in s): return None
    return s.decode('latin1')

for tag in TAGS:
    name = tag[:-1].decode()
    hits = [m.start() for m in re.finditer(re.escape(tag), data[:0xc11a34])]
    in_relro = [h for h in hits if h >= 0xbbe930]
    print(f'== {name!r}: {len(hits)} total, {len(in_relro)} in data.rel.ro/data {[hex(off2v(h)) for h in in_relro[:6]]}')
    for h in in_relro:
        v = off2v(h)
        # scan +-0x40 words for known ids
        for k in range(-16, 17):
            o = h + k * 4
            if 0 <= o < len(data) - 4:
                w = struct.unpack_from('<I', data, o)[0]
                if w in KNOWN_IDS:
                    print(f'   @{v:#x} [{k:+3d}w] {KNOWN_IDS[w]} ({w:#x})')
