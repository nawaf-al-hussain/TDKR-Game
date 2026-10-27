#!/usr/bin/env python3
"""S63 T1 step 4: annotate Helicopter/Test_Object state contents to solve CAS track shapes."""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

def u32(b, o):
    return struct.unpack_from('>I', b, o)[0]

def nm(v):
    if 0 < v < len(strings):
        s = strings[v]
        if s and 2 <= len(s) <= 48 and all(32 <= ord(c) < 127 for c in s):
            return repr(s[:40])
    return None

hit = [r for r in recs if r[1] == 'Helicopter'][0]
payload = hit[4]
print('Helicopter payload', len(payload), 'B; strings[224]=%r strings[6]=%r' % (strings[224][:40], strings[6][:40]))

# state starts: u32 == 75 ('Idle') or in [0x0fcc, 0x0fcc+15]
cands = []
for o in range(4, len(payload) - 3, 4):
    v = u32(payload, o)
    if v == 75 or 0x0fcc <= v <= 0x0fdc:
        cands.append((o, v, nm(v)))
for o, v, s in cands[:40]:
    print('  @%5d idx=%5d %s' % (o, v, s))
