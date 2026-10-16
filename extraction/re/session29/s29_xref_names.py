#!/usr/bin/env python3
"""S29 T1: neighborhood dump + literal-pool xrefs for class-name candidates."""
import struct, re, json, sys
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

def off2v(o): return o if o < 0xbbe1ec else o + 0x1000
def v2o(v): return v if v < 0xbbe1ec else v - 0x1000
def cstr_at(v, m=90):
    o = v2o(v)
    if o is None or o >= len(data): return None
    z = data.find(b'\0', o, o + m)
    return data[o:z if z >= 0 else o + m].decode('latin1')

ANCHORS = {
    'CinematicComponent.cpp': 0xb3af28, 'DummyComponent.cpp': 0xb38acc,
    'CollisionComponent.cpp': 0xb386c8, 'TriggerComponent.cpp': 0xb397a8,
    'TrafficSetting.cpp': 0xb35df4,
}
# also find LevelInit path
for m in re.finditer(rb'[\x20-\x7e]{3,120}', data[0xa5d80:0xbbe1ec]):
    s = m.group().decode()
    if 'LevelInit' in s or ('Component' in s and s.endswith('.cpp')):
        v = off2v(0xa5d80 + m.start())
        if s.endswith('.cpp'):
            ANCHORS.setdefault(s.split('\\')[-1], v)

print('=== neighborhoods (strings within +-0xC0) ===')
for name, v in sorted(ANCHORS.items()):
    print(f'--- {name} @ {v:#x}')
    lo, hi = v - 0xC0, v + 0xC0
    o = v2o(lo)
    for m in re.finditer(rb'[\x20-\x7e]{3,90}', data[o:o + (hi - lo)]):
        sv = lo + m.start()
        print(f'    {sv:#x}  {m.group().decode()[:80]!r}')

# 2. literal pool xrefs: search loaded image for u32 LE == string vaddr
def xrefs(vaddr):
    pat = struct.pack('<I', vaddr)
    res = []
    start = 0
    while True:
        i = data.find(pat, start, 0xc11a34)
        if i < 0: break
        res.append(off2v(i))
        start = i + 1
    return res

print('\n=== literal-pool xrefs ===')
XREF = {}
for name, v in sorted(ANCHORS.items()):
    xs = xrefs(v)
    XREF[name] = [hex(x) for x in xs]
    print(f'{name} @ {v:#x}: {[hex(x) for x in xs]}')
json.dump(XREF, open('/tmp/my-project/work/re29/name_xrefs.json', 'w'), indent=1)
