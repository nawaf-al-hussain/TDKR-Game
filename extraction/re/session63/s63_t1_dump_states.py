#!/usr/bin/env python3
"""S63 T1 step 1: dump per-state bytes for the 6 residual StateSet templates.
State boundaries via the state-name index runs (table written in read order ->
state names are consecutive table entries). For every u32 in a state, show the
resolved string if it is a valid name-like index -> the S-position net."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()
T = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json'))

RESID = ['BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive']

def name_like(s):
    return bool(s) and 2 <= len(s) <= 48 and all(32 <= ord(c) < 127 for c in s)

def u32(buf, off):
    return struct.unpack_from('>I', buf, off)[0]

for name in RESID:
    hit = [r for r in recs if r[1] == name]
    if not hit:
        print(name, ': NOT FOUND'); continue
    oid, tname, comps, flags, payload = hit[0]
    end = len(payload)
    # walk pre-StateSet components
    p = 0
    ss_idx = None
    for ci, cid in enumerate(comps):
        if cid == 0x5441a117:
            ss_idx = ci
            break
        spec = T.get('0x%08x' % cid)
        if spec is None:
            print(name, ': unknown comp %08x idx %d' % (cid, ci)); break
        try:
            # simple flat walk (no nested containers expected before SS in these 6)
            q = p
            for tok in spec:
                sz = {'i': 4, 'f': 4, 'c': 1, 's': 2, 'STR': 4}[tok]
                if isinstance(tok, list):
                    raise ValueError('nested pre-SS')
                q += sz
            # NOTE: flat sum only valid if no rep; check
            p = q
        except Exception as e:
            print(name, ': pre-SS walk failed for %08x: %r' % (cid, e)); break
    else:
        pass
    if ss_idx is None:
        print(name, ': StateSet not reached'); continue
    ss = payload[p:]
    print('=' * 90)
    print('%s  StateSet payload @comp%d, %d B (template payload %d B)' % (name, ss_idx, len(ss), end))
    cnt = struct.unpack_from('>i', ss, 0)[0]
    print('  count =', cnt)
    tail = 7 * 4
    idx0 = u32(ss, 4)
    print('  state0 name idx =', idx0, repr(strings[idx0]) if idx0 < len(strings) else '?')
    # state-name candidates: idx0..idx0+cnt-1
    wanted = {idx0 + k for k in range(cnt)}
    starts = []
    off = 4
    while off + 4 <= len(ss) - tail:
        v = u32(ss, off)
        if v in wanted:
            starts.append(off)
            if len(starts) == cnt:
                break
        off += 4
    print('  state starts:', ['%d(0x%x)' % (o, o) for o in starts],
          'names:', [repr(strings[u32(ss, o)])[:40] for o in starts])
    if len(starts) != cnt:
        print('  !! start count mismatch')
        continue
    states_end = len(ss) - tail
    # tail strings
    tailstrs = [strings[u32(ss, states_end + 4 * k)] if u32(ss, states_end + 4 * k) < len(strings) else '?'
                for k in range(7)]
    print('  tail STRx7:', [t[:28] for t in tailstrs])
    for si, s0 in enumerate(starts):
        s1 = starts[si + 1] if si + 1 < len(starts) else states_end
        chunk = ss[s0:s1]
        print('  --- state %d: [%d..%d) size=%d name=%r' % (si, s0, s1, len(chunk), strings[u32(ss, s0)]))
        # annotate u32s
        ann = []
        for o in range(0, len(chunk) - 3, 1):
            if o % 4 == 0:
                v = u32(chunk, o)
                if v < len(strings) and name_like(strings[v]):
                    ann.append('+%d:STR(%d)=%r' % (o, v, strings[v][:34]))
        print('    STR-net:', ann if ann else '(none)')
        hx = chunk.hex()
        for r in range(0, min(len(hx), 200 * 2), 48):
            print('    %04d: %s' % (r // 2, ' '.join(hx[r + j:r + j + 8] for j in range(0, min(48, len(hx) - r), 8))))
