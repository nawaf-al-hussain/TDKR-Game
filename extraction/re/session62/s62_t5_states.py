#!/usr/bin/env python3
"""S62 T5 v4: pin the CCS fixed head via Helicopter's 13 states.
- find the 13 state-name indexes (sequential string idx run) -> state boundaries
- per-state sizes; the fixed head = common prefix of all state payloads (after names)
- print head bytes; then per-state: the bytes after the common prefix = counts region"""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])
recs, strings = parse_gol()

hit = [r for r in recs if r[1] == 'Helicopter'][0]
payload = hit[4]
n = struct.unpack_from('>i', payload, 0)[0]
print('count =', n, 'payload', len(payload))

# state0 name @4; find the OTHER state starts by scanning for u32 string indexes whose
# strings look like state names AND whose offsets are plausible state starts
starts = [4]
for off in range(8, len(payload) - 3):
    v = struct.unpack_from('>I', payload, off)[0]
    if v < len(strings):
        s = strings[v]
        if s and 2 <= len(s) <= 40 and all(32 <= ord(c) < 127 for c in s):
            # state starts follow a state END; check: bytes before should complete state_{k-1}
            starts.append(off)
# deduce: real state starts = offsets o where the walk of state_{k-1} lands exactly; use
# the sequential-index trick instead: state names tend to be consecutive table entries
seq = [off for off in range(4, len(payload) - 3)
       if struct.unpack_from('>I', payload, off)[0] in range(0x0fc0, 0x0fe0)]
print('sequential idx hits:', ['%x' % o for o in seq][:40])

# try: state starts = 4 + cumulative sizes; sizes unknown. Use the name idx sequence:
# the state names' indexes in TABLE ORDER: collect the idx at each candidate start
cands = {}
for off in seq:
    v = struct.unpack_from('>I', payload, off)[0]
    cands[off] = (v, strings[v])
for off, (v, s) in sorted(cands.items()):
    print('  @%04x idx=%d %r' % (off, v, s[:36]))
