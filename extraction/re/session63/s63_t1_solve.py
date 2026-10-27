#!/usr/bin/env python3
"""S63 T1 step 2: solve the CContainerState/CAS grammar against ALL residual payloads.
Head (82 B, code-verified): STR,i,i,c7,f,f,i,f7,c,f,i,i,i,c2,i(animN)
CAS hypothesis H5 (code-derived):
  STR, i(n1), n1*[STR, i(k1), k1*[STR,i,i,i,i]],
       i(n2), n2*[STR, i(k2), k2*[i,i,STR]],
       i(n3), n3*[i(k3),  k3*[i,i,STR,i]],
       i(n4), n4*[i(k4),  k4*[i,i,STR,STR]],
       i(n5), n5*[i(k5),  k5*[i,i,f,f,i]]
STATE tail: i(nT), nT*[i6,f,i2,STR,i]  (44 B each, code-verified in CCS::Load)
The solver parses every state in every residual template; a variant wins only if it
closes EVERY state exactly (and the trigger scriptNames land on name-like strings)."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']

def u32(b, o):
    return struct.unpack_from('>I', b, o)[0]

def f32(b, o):
    return struct.unpack_from('>f', b, o)[0]

def name_like(v):
    if v <= 0 or v >= len(strings):
        return False
    s = strings[v]
    return bool(s) and 2 <= len(s) <= 48 and all(32 <= ord(c) < 127 for c in s)

def head_ok(b, o):
    """82-B CCS head signature at offset o (name @o already checked by caller)."""
    if o + 82 > len(b):
        return False
    for k in range(7):
        if b[o + 12 + k] > 1:
            return False
    for off in (19, 23, 31, 35, 39, 43, 47, 51, 55):
        f = f32(b, o + off)
        if f != 0.0 and abs(f) > 1e7:
            return False
        if f != 0.0 and abs(f) < 1e-6:
            return False
    return True

def find_states(b, p0, p_end):
    """scan [p0, p_end) for state starts; return sorted list."""
    starts = []
    for o in range(p0, p_end - 82, 4):
        if name_like(u32(b, o)) and head_ok(b, o):
            starts.append(o)
    return starts

class ParseFail(Exception):
    pass

def parse_cas(b, p, end, variant, log):
    """CAS grammar; returns new p. variant tweaks track shapes."""
    if p + 4 > end:
        raise ParseFail('cas-str')
    v = u32(b, p)
    if not name_like(v):
        raise ParseFail('cas-animname @%d val %d' % (p, v))
    log.append('    anim=%r' % strings[v])
    p += 4
    # (nX, elem_head, track_shape) per list
    lists = variant['lists']
    for li, (elemname, track) in enumerate(lists):
        if p + 4 > end:
            raise ParseFail('cas-n%d' % li)
        n = struct.unpack_from('>i', b, p)[0]
        p += 4
        if n < 0 or n > 4096:
            raise ParseFail('cas-n%d-negative %d' % (li, n))
        if n:
            log.append('    list%d n=%d' % (li + 1, n))
        for e in range(n):
            if elemname == 'STR':
                if p + 4 > end or not name_like(u32(b, p)):
                    raise ParseFail('cas-l%d-elemname @%d' % (li, p))
                if n <= 3:
                    log.append('      e%d name=%r' % (e, strings[u32(b, p)]))
                p += 4
            elif elemname == 'i':
                p += 4
            # k count
            if p + 4 > end:
                raise ParseFail('cas-l%d-k' % li)
            k = struct.unpack_from('>i', b, p)[0]
            p += 4
            if k < 0 or k > 65536:
                raise ParseFail('cas-l%d-k-neg %d' % (li, k))
            tsz = {'Si4': 20, 'iiS': 12, 'iiSi': 16, 'iiSS': 16, 'iiffi': 20}[track]
            p += k * tsz
            if p > end:
                raise ParseFail('cas-l%d-tracks' % li)
    return p

def parse_state(b, p, end, variant, log):
    p += 82  # head (verified separately)
    if p > end:
        raise ParseFail('head')
    # animN x CAS
    animN = struct.unpack_from('>i', b, p - 4)[0]
    if animN < 0 or animN > 4096:
        raise ParseFail('animN %d' % animN)
    for a in range(animN):
        p = parse_cas(b, p, end, variant, log)
    # nT triggers
    if p + 4 > end:
        raise ParseFail('nT')
    nT = struct.unpack_from('>i', b, p)[0]
    p += 4
    if nT < 0 or nT > 65536:
        raise ParseFail('nT-neg %d' % nT)
    if nT:
        log.append('    nT=%d' % nT)
    for t in range(nT):
        p += 24 + 4 + 8  # i6, f, i2
        if p + 4 > end or not name_like(u32(b, p)):
            raise ParseFail('trig-str @%d' % p)
        if nT <= 4:
            log.append('      t%d script=%r' % (t, strings[u32(b, p)]))
        p += 4 + 4
    if p != end:
        raise ParseFail('state-end %d != %d (off %+d)' % (p, end, p - end))
    return p

VARIANT_H5 = {'lists': [('STR', 'Si4'), ('STR', 'iiS'), ('i', 'iiSi'), ('i', 'iiSS'), ('i', 'iiffi')]}
# null variants (must FAIL): wrong track shapes / wrong list order
V_NULL_TRACK = {'lists': [('STR', 'iiS'), ('STR', 'Si4'), ('i', 'iiSi'), ('i', 'iiSS'), ('i', 'iiffi')]}
V_NULL_ORDER = {'lists': [('STR', 'Si4'), ('i', 'iiSi'), ('STR', 'iiS'), ('i', 'iiSS'), ('i', 'iiffi')]}

for name in RESID:
    hit = [r for r in recs if r[1] == name][0]
    oid, tname, comps, flags, payload = hit[4], hit[1], hit[2], hit[3], hit[4]
    payload = hit[4]
    # StateSet is comp0 for all 6 (verified by the dump step); states region = [4 .. SS_end)
    # SS_end unknown (more components may follow) -> derive from state chain + STRx7 tail:
    cnt = struct.unpack_from('>i', payload, 0)[0]
    starts = find_states(payload, 4, len(payload))
    print('=' * 90)
    print('%s count=%d, head-signature starts: %d' % (name, cnt, len(starts)))
    if len(starts) < cnt:
        print('  !! fewer starts than count - report')
    # chain-parse with H5
    ok = 0
    fails = []
    sizes = []
    for variant, vname in ((VARIANT_H5, 'H5'), (V_NULL_TRACK, 'NULL-track'), (V_NULL_ORDER, 'NULL-order')):
        ok = 0
        fails = []
        for si in range(min(cnt, len(starts))):
            s0 = starts[si]
            s1 = starts[si + 1] if si + 1 < len(starts) else None
            log = []
            try:
                # state end: next start; for the LAST state try every candidate end:
                # STRx7 tail means the SS payload ends at laststate_end; the tail is 28 B
                # of name-like u32s. Scan candidate ends from s0+82 upward.
                if s1 is None:
                    lastok = None
                    for e in range(s0 + 82, len(payload) - 27):
                        try:
                            parse_state(payload, s0, e, variant, [])
                            # require the 28 B after e to be the STRx7 tail (name-like)
                            tail_ok = all(name_like(u32(payload, e + 4 * k)) or u32(payload, e + 4 * k) == 0
                                          for k in range(7))
                            if tail_ok:
                                lastok = e
                                break
                        except ParseFail:
                            continue
                    if lastok is None:
                        raise ParseFail('no end')
                    s1 = lastok
                parse_state(payload, s0, s1, variant, log)
                ok += 1
                sizes.append(s1 - s0)
            except ParseFail as e:
                fails.append((si, strings[u32(payload, s0)], str(e)))
        print('  %-11s: %d/%d states close exactly' % (vname, ok, min(cnt, len(starts))))
        for f in fails[:6]:
            print('     fail state %d %r: %s' % f)
        if vname == 'H5' and not fails:
            print('     sizes: %s' % sizes)
