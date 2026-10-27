#!/usr/bin/env python3
"""S63 T1 step 7: field-exact verbose walk of a StateSet payload with the H5 grammar.
Prints every field read with offset/value/resolved-string so divergence is visible."""
import struct, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

def u32(b, o):
    return struct.unpack_from('>i', b, o)[0]

def s_of(v):
    if 0 <= v < len(strings):
        s = strings[v]
        return repr(s[:40])
    return None

NAME = sys.argv[1] if len(sys.argv) > 1 else 'Helicopter'
MAXF = int(sys.argv[2]) if len(sys.argv) > 2 else 400
hit = [r for r in recs if r[1] == NAME][0]
payload = hit[4]
print('%s payload %d B; strings[90]=%s strings[29]=%s strings[4044]=%s' % (
    NAME, len(payload), s_of(90), s_of(29), (strings[4044][:40] if len(strings) > 4044 else '?')))

p = 0
cnt = u32(payload, p)
print('SS count=%d @0' % cnt)
p += 4
for st in range(cnt):
    s0 = p
    print('--- state %d @%d' % (st, s0))
    def rd(kind, rel):
        global p
        o = p
        if kind == 'i':
            v = u32(payload, o)
            print('  @%4d i    = %11d %s' % (o - s0, v, s_of(v) or ''))
        elif kind == 'f':
            v = struct.unpack_from('>f', payload, o)[0]
            print('  @%4d f    = %g' % (o - s0, v))
        elif kind == 'c':
            v = payload[o]
            print('  @%4d c    = %d' % (o - s0, v))
        elif kind == 'STR':
            v = u32(payload, o)
            print('  @%4d STR  = %11d %s' % (o - s0, v, s_of(v) or ''))
        p += {'i': 4, 'f': 4, 'c': 1, 'STR': 4}[kind]
        return v
    # head
    rd('STR', 0)
    rd('i', 0)
    rd('i', 0)
    for k in range(7):
        rd('c', 0)
    rd('f', 0)
    rd('f', 0)
    rd('i', 0)
    for k in range(7):
        rd('f', 0)
    rd('c', 0)
    rd('f', 0)
    rd('i', 0)
    rd('i', 0)
    rd('i', 0)
    rd('c', 0)
    rd('c', 0)
    animN = rd('i', 0)
    print('  animN=%d -> CAS x%d' % (animN, animN))
    if animN > 4000 or p > len(payload):
        print('  !! animN insane, stop'); break
    for a in range(animN):
        an = rd('STR', 0)
        for li in range(5):
            n = rd('i', 0)
            if n:
                print('  CAS%d list%d n=%d' % (a, li + 1, n))
            if n < 0 or n > 5000:
                print('  !! n insane'); p = None; break
            for e in range(min(n, 6)):
                if li in (0, 1):
                    rd('STR', 0)
                else:
                    rd('i', 0)
                k = rd('i', 0)
                if k:
                    print('    e%d k=%d tracks:' % (e, k))
                if k < 0 or k > 5000:
                    print('    !! k insane'); p = None; break
                for t in range(min(k, 4)):
                    if li == 0:
                        rd('STR', 0); rd('i', 0); rd('i', 0); rd('i', 0); rd('i', 0)
                    elif li == 1:
                        rd('i', 0); rd('i', 0); rd('STR', 0)
                    elif li == 2:
                        rd('i', 0); rd('i', 0); rd('STR', 0); rd('i', 0)
                    elif li == 3:
                        rd('i', 0); rd('i', 0); rd('STR', 0); rd('STR', 0)
                    else:
                        rd('i', 0); rd('i', 0); rd('f', 0); rd('f', 0); rd('i', 0)
                # skip remaining tracks silently
                for t in range(max(0, min(k, 5000) - 4)):
                    p += {0: 20, 1: 12, 2: 16, 3: 16, 4: 20}[li]
                if p is None:
                    break
            if n > 6:
                sz = {0: None, 1: None, 2: None, 3: None, 4: None}
                print('    ... %d more elems SKIPPED-BLIND' % (n - 6))
                # cannot skip blindly without sizes; bail out of this list
                p = None
                break
            if p is None:
                break
        if p is None:
            break
    if p is None:
        print('  (stopped: cannot skip large lists blindly)')
        break
    nT = rd('i', 0)
    print('  nT=%d' % nT)
    for t in range(nT):
        for kk in range(6):
            rd('i', 0)
        rd('f', 0)
        rd('i', 0)
        rd('i', 0)
        rd('STR', 0)
        rd('i', 0)
    if p - s0 > MAXF and st >= 2:
        pass
print('walked to p=%d' % p)
