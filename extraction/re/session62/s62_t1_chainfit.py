#!/usr/bin/env python3
"""S62 T1: chain-fit the post-Awareness components of a template.
DropCollectible = 4+8k (i + k*(i,i) per s57 page-validated reader);
NpcCombat 34; NpcSound 30; ActorBase 82+5a; ActorShadow 5; Interaction 16;
WantGen 16; CustomizeActor fitted; ActorSpecialFX 18."""
import struct

exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py')
     .read().split('recs, strings = parse_gol()')[0])

recs, strings = parse_gol()
NSTR = len(strings)

def fit_cust(payload, start, end):
    p = start
    if p + 4 > end: return None
    cnt = struct.unpack_from('>i', payload, p)[0]
    if not (0 <= cnt < 64): return None
    p += 4
    for _ in range(cnt):
        p += 12
        if p + 4 > end: return None
        inner = struct.unpack_from('>i', payload, p)[0]
        if not (0 <= inner < 4096): return None
        p += 4 + 4 * inner
    if p + 8 > end: return None
    return p + 8

for oid, name, comps, flags, payload in recs:
    if name not in ('Melee_Enemy_Merc', 'Police_Officer', 'Blake', 'Helicopter', 'Sniper'):
        continue
    end = len(payload)
    print(f'== {name} len={end}')
    # find Awareness end: walk the prefix with current final specs
    # (hardcode: prefix = everything before DropCollectible, computed by spec walk)
    # simpler: try all (start of DropCollectible, k, a) combos
    for dc_start in range(150, 340):
        for k in range(0, 5):
            dc_end = dc_start + 4 + 8 * k
            for NCS in (30, 34, 38):
                nc_end = dc_end + NCS
                ns_end = nc_end + 30
                for a in range(0, 5):
                    ab_end = ns_end + 82 + 5 * a
                    p1 = ab_end + 5 + 16 + 16
                    ca_end = fit_cust(payload, p1, end - 18)
                    if ca_end == end - 18:
                        cnt = struct.unpack_from('>i', payload, dc_start)[0]
                        ab_i2 = struct.unpack_from('>i', payload, ns_end + 78)[0]
                        mark = ' *' if (cnt == k and ab_i2 == a) else ''
                        print(f'  FIT: DC@{dc_start}(cnt={cnt},k={k}) NC={NCS} AB(a={a},i2={ab_i2}) '
                              f'CustAct@{p1}..{ca_end}{mark}')
    break
