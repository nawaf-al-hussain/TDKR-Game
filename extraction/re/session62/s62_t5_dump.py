#!/usr/bin/env python3
"""S62 T5: dump the StateSet component payload of the 6 residual templates
(BatPod, Helicopter, Helicopter_Bane, Military_Heli, Test_Object, TheBatDrive).
The closure fails ONLY on these (count>0 StateSet). Data-driven decode of
CContainerState::Load / CContainerStateAnimation::Load from the payload bytes."""
import struct, json, sys
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session61')

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
T = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

NAT = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}

class OOB(Exception):
    pass

def walk(toks, buf, p, end):
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
                    p = walk(t[2], buf, p, end)
                continue
            raise ValueError('tok')
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok ' + str(t))
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
        elif t == 'c':
            last = buf[p]
        p += sz
    return p

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']

def hexdump(buf, p0, width=16, maxrows=28):
    rows = []
    for off in range(0, min(len(buf) - p0, maxrows * width), width):
        a = p0 + off
        chunk = buf[a:a + width]
        hx = ' '.join('%02x' % b for b in chunk)
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        rows.append('%04x  %s  %s' % (a, hx.ljust(width * 3 - 1), asc))
    return '\n'.join(rows)

def u32s(buf, p0, n):
    return [struct.unpack_from('>I', buf, p0 + 4 * i)[0] for i in range(n)]

for name in RESID:
    hit = [r for r in recs if r[1] == name]
    if not hit:
        print(name, ': NOT FOUND'); continue
    oid, tname, comps, flags, payload = hit[0]
    end = len(payload)
    # walk components until the StateSet one
    p = 0
    ss_idx = None
    for ci, cid in enumerate(comps):
        spec = T.get('0x%08x' % cid)
        if spec is None:
            print(name, ': unknown comp %08x at idx %d, p=%d' % (cid, ci, p)); break
        if cid == 0x5441a117:
            ss_idx = ci
            break
        try:
            p = walk(spec, payload, p, end)
        except Exception as e:
            print(name, ': pre-SS comp %08x walk failed at p=%d (%r)' % (cid, p, e)); break
    print('=' * 78)
    print('%s oid=%08x comps=%s payload=%d B' % (name, oid, ['%08x' % c for c in comps], end))
    if ss_idx is None:
        print('  (StateSet component not reached)'); continue
    print('  StateSet at comp #%d, payload offset p=%d, remaining=%d B (pre-walk used the flat spec? no - dumped raw)' % (ss_idx, p, end - p))
    print(hexdump(payload, p))
    print('  u32 BE view:', u32s(payload, p, 14))
