#!/usr/bin/env python3
"""S63 T1 step 6: state1 of Helicopter (starts payload[138]) - annotate its CAS content."""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

def u32(b, o):
    return struct.unpack_from('>I', b, o)[0]

def f32(b, o):
    return struct.unpack_from('>f', b, o)[0]

hit = [r for r in recs if r[1] == 'Helicopter'][0]
payload = hit[4]

def s_of(v):
    if v < len(strings):
        s = strings[v]
        if s and len(s) <= 60 and all(32 <= ord(c) < 127 or c == '\n' for c in s):
            return repr(s[:46])
        return '<str len%d>' % len(s)
    return None

S0 = 138
for k in range(0, 120):
    o = S0 + 4 * k
    if o + 4 > len(payload):
        break
    v = u32(payload, o)
    f = f32(payload, o)
    ann = s_of(v)
    extra = ''
    if ann is None and abs(f) < 1e7 and (f == 0 or abs(f) >= 1e-4):
        extra = ' f=%g' % f
    mark = ''
    rel = o - S0
    if rel == 82: mark = ' <<< CAS animName'
    if rel == 78: mark = ' <<< animN'
    if rel in (4, 8): mark = ' <<< i@head'
    print('s1+%4d (abs%4d) %10d 0x%08x %s%s%s' % (rel, o, v, v, ann or '', extra, mark))
