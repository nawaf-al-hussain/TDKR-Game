#!/usr/bin/env python3
"""S62 T5 v3: locate state-name string indexes in the residual payloads -> exact state
boundaries; read the strings; diff consecutive states to derive the CCS/CAS layout."""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
print('string table entries:', len(strings))

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']
for name in RESID:
    hit = [r for r in recs if r[1] == name][0]
    payload = hit[4]
    n = struct.unpack_from('>i', payload, 0)[0]
    print('=' * 70)
    print(name, 'states(count)=', n, 'payload', len(payload))
    # scan u32 values that look like string-table indexes of state-ish names
    hits = []
    for off in range(0, len(payload) - 3, 1):
        v = struct.unpack_from('>I', payload, off)[0]
        if 0 < v < len(strings):
            s = strings[v]
            if s and all(32 <= ord(c) < 127 for c in s[:24]) and len(s) >= 2:
                hits.append((off, v, s))
    # cluster: report all, we look for the sequential run
    for off, v, s in hits[:60]:
        print('  @%04x idx=%d (0x%x) %r' % (off, v, v, s[:40]))
