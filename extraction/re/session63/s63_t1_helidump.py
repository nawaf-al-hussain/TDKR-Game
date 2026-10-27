#!/usr/bin/env python3
"""S63 T1 step 5: full annotated u32 dump of Helicopter SS payload head region."""
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
            return repr(s[:44])
        return '<str len %d>' % len(s)
    return None

for o in range(4, 904, 4):
    v = u32(payload, o)
    f = f32(payload, o)
    ann = s_of(v)
    extra = ''
    if ann is None and abs(f) < 1e7 and (f == 0 or abs(f) >= 1e-4):
        extra = ' f=%g' % f
    # head markers
    mark = ''
    rel = o - 4
    if rel == 4: mark = ' i@4'
    print('@%4d (s%4d) %10d 0x%08x %s%s%s' % (o, o - 4, v, v, ann or '', extra, mark))
