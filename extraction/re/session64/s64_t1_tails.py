#!/usr/bin/env python3
"""S64 T1 step 6: tail analysis. Dump the leftover bytes for every bounds-pass
template grouped by tail size; check for a common trailer value."""
import struct, json, collections

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py'
exec(open(SRC).read().split('recs, strings = parse_gol()')[0])

def walk_spec(toks, buf, p, end):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk_spec(t[2], buf, p, end)
                continue
            if t and t[0] == 'call':
                raise ValueError('call')
            if t and t[0] == 'inline':
                p = walk_spec(t[2], buf, p, end)
                continue
            if len(t) == 1 and isinstance(t[0], str) and t[0] in NAT:
                t = t[0]
            elif len(t) == 2 and isinstance(t[0], str) and t[0] in NAT and isinstance(t[1], int):
                if p + t[1] > end:
                    raise OOB()
                p += t[1]
                last = 0
                continue
            elif len(t) >= 3 and t[0] == 'fat':
                for _ in range(t[2]):
                    p = walk_spec([t[1]], buf, p, end)
                last = 0
                continue
            else:
                raise ValueError('tok %r' % (t,))
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok %r' % (t,))
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
        p += sz
    return p

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_final_specs.json'))

def sv(idx):
    if 0 <= idx < len(strings):
        v = strings[idx]
        if isinstance(v, bytes):
            v = v.decode('latin1')
        return str(v)[:24]
    return None

bytail = collections.defaultdict(list)
for oid, name, comps, flags, payload in recs:
    if not comps:
        continue
    p = 0; end = len(payload)
    try:
        for cid in comps:
            spec = E.get('0x%08x' % cid)
            if spec is None:
                p = None; break
            p = walk_spec(spec, payload, p, end)
    except Exception:
        p = None
    if p is not None and p != end:
        bytail[end - p].append((name, comps[-1], payload[p:end], end))

for tail in sorted(bytail):
    entries = bytail[tail]
    print('== tail %d B, n=%d' % (tail, len(entries)))
    if tail <= 24:
        vals = collections.Counter()
        for name, lastc, tb, end in entries:
            u = struct.unpack('>I', tb.ljust(4, b'\0')[:4])[0] if len(tb) >= 4 else struct.unpack('>I', tb + b'\0' * (4 - len(tb)))[0]
            s = sv(u)
            vals[(tb.hex(), s)] += 1
        for (hx, s), n in vals.most_common(6):
            print('   %dx %s %s' % (n, hx, repr(s) if s else ''))
        names = [e[0] for e in entries][:8]
        print('   names:', names)
