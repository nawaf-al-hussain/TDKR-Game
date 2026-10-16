#!/usr/bin/env python3
"""S29 T1: runtime strings + literal-pool xrefs to find the class-id hash."""
import struct, re, json
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

RUNTIME = (0xa5d80, 0xc11a34)  # .text .. end of second LOAD (file range of loaded image)

def off2v(o): return o if o < 0xbbe1ec else o + 0x1000

# 1. all printable strings in runtime image
strings = []  # (vaddr, text)
for m in re.finditer(rb'[\x20-\x7e]{3,80}', data[RUNTIME[0]:RUNTIME[1]]):
    strings.append((off2v(RUNTIME[0] + m.start()), m.group().decode()))
print('runtime strings:', len(strings))

# keyword filter
KW = ['Cinematic', 'Dummy', 'TrafficSetting', 'LevelInit', 'Collision', 'Trigger', 'SmartLight',
      'SoundAndLight', 'Component', 'Object', 'Actor', 'Spawn', 'Waypoint', 'Zone', 'Quest']
hits = {}
for v, s in strings:
    for kw in KW:
        if kw in s:
            hits.setdefault(kw, []).append((v, s))
for kw in ['Cinematic', 'Dummy', 'TrafficSetting', 'LevelInit', 'Collision', 'Trigger', 'SmartLight', 'SoundAndLight']:
    lst = hits.get(kw, [])
    print(f'--- {kw}: {len(lst)}')
    for v, s in lst[:12]:
        print(f'   {v:#x} {s[:70]!r}')
json.dump({hex(v): s for v, s in strings}, open('/tmp/my-project/work/re29/runtime_strings.json', 'w'), indent=0)
