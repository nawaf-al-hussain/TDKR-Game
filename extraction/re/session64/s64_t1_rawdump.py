#!/usr/bin/env python3
"""S64 T1 step 3: raw u32/string dump around the divergence state."""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

def sv(idx):
    if 0 <= idx < len(strings):
        v = strings[idx]
        if isinstance(v, bytes):
            v = v.decode('latin1')
        return str(v)[:28]
    return None

def dump(name_target, lo, hi):
    hit = [r for r in recs if r[1] == name_target][0]
    payload = hit[4]
    print('==== %s [%d:%d] of %d' % (name_target, lo, hi, len(payload)))
    p = lo
    while p + 4 <= min(hi, len(payload)):
        v = struct.unpack_from('>I', payload, p)[0]
        f = struct.unpack_from('>f', payload, p)[0]
        note = ''
        s = sv(v)
        if s is not None:
            note = 'STR %r' % s
        elif v == 0xffffffff:
            note = '-1'
        if abs(f) > 1e-6 and abs(f) < 1e8:
            note += ' f=%.4g' % f
        print('  %6d  %08x  %s' % (p, v, note))
        p += 4

dump('Enemy_Melee_Movement', 316, 480)
dump('Batman_30_Combat_Strike1', 340, 480)
