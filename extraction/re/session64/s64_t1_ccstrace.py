#!/usr/bin/env python3
"""S64 T1 step 2: hand-rolled STATE-LEVEL tracer for the nested StateSet spec.
Logs per state: name (resolved), head fields, animN, list1..5 counts and
element counts, trigger count - so the exact divergence point is visible."""
import struct, json

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

TARGETS = ['Batman_30_Combat_Strike1', 'Batman_01_Movement', 'Enemy_Melee_Movement',
           'Batman_02_Flying', 'Enemy_Melee_Hurt', 'Batman_39_Combat_CounterStrike']

def s(idx):
    if 0 <= idx < len(strings):
        v = strings[idx]
        if isinstance(v, bytes):
            v = v.decode('latin1')
        return str(v)[:32]
    return '<%d>' % idx

class Die(Exception):
    pass

def trace(name_target):
    hit = [r for r in recs if r[1] == name_target][0]
    oid, tname, comps, flags, payload = hit[0], hit[1], hit[2], hit[3], hit[4]
    end = len(payload)
    print('==== %s payload %d B' % (tname, end))
    p = [0]

    def rd(fmt, sz, what):
        if p[0] + sz > end:
            raise Die('%s at %d: need %d, only %d left' % (what, p[0], sz, end - p[0]))
        v = struct.unpack_from(fmt, payload, p[0])[0]
        p[0] += sz
        return v

    def ri(what):
        return rd('>i', 4, 'i:' + what)

    def rf(what):
        return rd('>f', 4, 'f:' + what)

    def rc(what):
        return rd('>B', 1, 'c:' + what)

    def rstr(what):
        v = ri(what)
        return v, s(v)

    try:
        nstates = ri('CCS count')
        print('  CCS states: %d @%d' % (nstates, p[0]))
        for st in range(nstates):
            sbase = p[0]
            sidx, sname = rstr('state%d name' % st)
            f1 = ri('f1'); f2 = ri('f2')
            c7 = [rc('c%d' % k) for k in range(7)]
            ff1 = rf('ff1'); ff2 = rf('ff2')
            hi = ri('head-i')
            f7 = [rf('f%d' % k) for k in range(7)]
            hc = rc('head-c')
            hf = rf('head-f')
            i1 = ri('i1'); i2 = ri('i2'); i3 = ri('i3')
            cc1 = rc('cc1'); cc2 = rc('cc2')
            animN = ri('animN')
            print('  state %d @%d name=%r f1=%d f2=%d ff=(%.3f,%.3f) hi=%d f7[0]=%.3f hc=%d hf=%.3f i=(%d,%d,%d) cc=(%d,%d) animN=%d'
                  % (st, sbase, sname, f1, f2, ff1, ff2, hi, f7[0], hc, hf, i1, i2, i3, cc1, cc2, animN))
            # CAS
            for a in range(animN):
                abase = p[0]
                aidx, aname = rstr('anim%d name' % a)
                # list1: STR, i k, k x (STR,i,i,i,i)
                l1n = ri('l1 count')
                l1el = []
                for e in range(l1n):
                    en, _ = rstr('l1e%d' % e)
                    k = ri('l1e%d k' % e)
                    for t in range(k):
                        tn, _ = rstr('l1e%d t%d' % (e, t))
                        ri('x'); ri('x'); ri('x'); ri('x')
                    l1el.append((en, k))
                # list2: STR, i k, k x (i,i,STR,c)
                l2n = ri('l2 count')
                for e in range(l2n):
                    en, _ = rstr('l2e%d' % e)
                    k = ri('l2e%d k' % e)
                    for t in range(k):
                        ri('x'); ri('x'); rstr('x'); rc('x')
                # list3: i, k, k x (i,i,STR,i,c)
                l3n = ri('l3 count')
                for e in range(l3n):
                    k = ri('l3e%d k' % e)
                    for t in range(k):
                        ri('x'); ri('x'); rstr('x'); ri('x'); rc('x')
                # list4: i, k, k x (i,i,STR,STR,c)
                l4n = ri('l4 count')
                for e in range(l4n):
                    k = ri('l4e%d k' % e)
                    for t in range(k):
                        ri('x'); ri('x'); rstr('x'); rstr('x'); rc('x')
                # list5: i count, i param?, count x (i,i,f,f,i,c,c), i param?
                l5n = ri('l5 count')
                for e in range(l5n):
                    k = ri('l5e%d k' % e)
                    for t in range(k):
                        ri('x'); ri('x'); rf('x'); rf('x'); ri('x'); rc('x'); rc('x')
                    l5p = ri('l5e%d param' % e)
                print('    anim %d @%d %r l1=%d%s l2=%d l3=%d l4=%d l5=%d end=%d'
                      % (a, abase, aname, l1n, l1el, l2n, l3n, l4n, l5n, p[0]))
            # triggers: spec = [i,i,i,i,i,i, f, i,i, STR, i] = 44 B
            nT = ri('trig count')
            for t in range(nT):
                iA = ri('t%d a1' % t); iB = ri('t%d a2' % t); iC = ri('t%d a3' % t)
                iD = ri('t%d a4' % t); iE = ri('t%d a5' % t); iF = ri('t%d a6' % t)
                f = rf('t%d f' % t)
                b = ri('t%d b' % t); c = ri('t%d c' % t)
                tn, tnv = rstr('t%d str' % t)
                d = ri('t%d d' % t)
            print('    trig n=%d end=%d' % (nT, p[0]))
        # 7 strings after states
        tail = [rstr('tail%d' % k)[1] for k in range(7)]
        print('  tail strings:', tail)
        print('  END p=%d (payload %d) %s' % (p[0], end, 'EXACT' if p[0] == end else 'LEFTOVER %d' % (end - p[0])))
    except Die as e:
        print('  DIE @%d: %s' % (p[0], e))
        print('  hex at die:', payload[p[0]:p[0] + 40].hex())
        print('  hex -24:', payload[max(0, p[0] - 24):p[0]].hex())

for t in TARGETS:
    trace(t)
    print()
