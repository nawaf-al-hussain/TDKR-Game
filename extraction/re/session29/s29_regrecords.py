#!/usr/bin/env python3
"""S29 T1: locate class registration records via known Load fn addresses."""
import struct, json
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

KNOWN_LOADS = {
    0x2018f0: 'CComponentLevelInit::Load (tid 0x2657)',
    0x2dce20: 'CComponentCinematic::Load (tid 0x2b inner)',
    0x22a368: 'CDummyComponent::Load (tid 0x10FF796)',
    0x1ffa1c: 'CTrafficSetting::Load',
    0x36cbb0: 'factory 0x54989cb1 load',
    0x394ec8: 'factory 0x6754056b load',
    0x38d828: 'factory 0x68a62e65 load',
}
def off2v(o): return o if o < 0xbbe1ec else o + 0x1000
def v2o(v): return v if v < 0xbbe1ec else v - 0x1000
def cstr_at(v, m=64):
    o = v2o(v)
    if o is None or o >= len(data): return None
    z = data.find(b'\0', o, o + m)
    s = data[o:z if z >= 0 else o + m]
    return s.decode('latin1') if all(0x20 <= c < 0x7f or c == 0 for c in s) else None

IMG = (0xa5d80, 0xc11a34)
recs = {}
for i in range(IMG[0], IMG[1] - 4, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if w in KNOWN_LOADS:
        v = off2v(i)
        recs.setdefault(w, []).append(v)
for w, vs in recs.items():
    print(f'== load fn {w:#x} {KNOWN_LOADS[w]}: {len(vs)} refs')
    for v in vs[:6]:
        words = [struct.unpack_from('<I', data, v2o(v) + k * 4)[0] for k in range(-10, 11) if 0 <= v2o(v) + k * 4 < len(data)]
        print(f'   ref@{v:#x} neighborhood:')
        for k, wd in zip(range(-10, 11), words):
            tag = ''
            cs = cstr_at(wd)
            if cs: tag = f'  STR {cs[:48]!r}'
            if wd in KNOWN_LOADS: tag += f'  <<LOAD {KNOWN_LOADS[wd]}'
            print(f'     [{k:+3d}] {v + k*4:#x}  {wd:#010x}{tag}')
