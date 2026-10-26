#!/usr/bin/env python3
"""S62 T1: brute-force the component boundary fit for Melee_Enemy_Merc's tail.
Tries NpcCombat in {34,38} and CustomizeActor start offsets; scores by sane counts
(0<=count<1000) and exact end alignment."""
import struct, json, sys

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
for oid, name, comps, flags, payload in recs:
    if name != 'Melee_Enemy_Merc':
        continue
    end = len(payload)
    NUS = {'i': 4, 'f': 4, 'c': 1, 'STR': 4, 's': 2}

    def fit_custom(start):
        """fit [i, rep(i: STR,STR,STR,i, rep(i: STR)), i, i]; return end pos or None"""
        p = start
        try:
            cnt = struct.unpack_from('>i', payload, p)[0]
        except Exception:
            return None
        if not (0 <= cnt < 64):
            return None
        p += 4
        for _ in range(cnt):
            p += 12  # STR,STR,STR
            try:
                inner = struct.unpack_from('>i', payload, p)[0]
            except Exception:
                return None
            if not (0 <= inner < 4096):
                return None
            p += 4 + 4 * inner
        if p + 8 > end:
            return None
        return p + 8

    # try each start (CustomizeActor ends 18 B before payload end: ActorSpecialFX follows)
    for st in range(427, 470):
        r = fit_custom(st)
        if r == end - 18:
            print(f'CustomizeActor start {st} fits to {end-18} (+18 B ActorSpecialFX after)')
            cnt = struct.unpack_from('>i', payload, st)[0]
            print(f'  outer count = {cnt}')
            p = st + 4
            for k in range(cnt):
                s1, s2, s3 = struct.unpack_from('>iii', payload, p)
                p += 12
                inner = struct.unpack_from('>i', payload, p)[0]
                p += 4
                strs = [struct.unpack_from('>i', payload, p + 4 * j)[0] for j in range(inner)]
                p += 4 * inner
                print(f'  elem[{k}]: STRs=({s1},{s2},{s3}) inner={inner} stridx={strs}')
            print(f'  trailing i,i = {struct.unpack_from(">ii", payload, end-8)}')
            break
    break
