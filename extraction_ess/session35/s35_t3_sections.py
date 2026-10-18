#!/usr/bin/env python3
"""S35 T3f: sequential decode with resync — map section boundaries in the
cell region; each section = run of valid 15-B cells."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
GS = 0x5a4e6
NV = 30905
nrec_total = (N - GS) // 15

def valid_cell(off):
    v = struct.unpack_from('>7H', d, off)
    if not all(x < NV for x in v[:3]):
        return False
    for x in v[3:6]:
        if not (x == 65535 or x < 80000):
            return False
    if v[6] > 8192:
        return False
    return True

sections = []
off = GS
k = 0
while off + 15 <= N:
    if valid_cell(off):
        run_start = off
        run_k = 0
        while off + 15 <= N and valid_cell(off):
            off += 15
            run_k += 1
        sections.append((run_start, run_k))
    else:
        off += 1  # slide byte-wise to resync

print(f'sections: {len(sections)}; total cells {sum(s[1] for s in sections)} / {nrec_total}')
for s in sections[:12]:
    print(f'  start 0x{s[0]:x} cells {s[1]}')
print('  ...')
for s in sections[-4:]:
    print(f'  start 0x{s[0]:x} cells {s[1]}')
gaps = [(sections[i][0] + sections[i][1] * 15, sections[i+1][0]) for i in range(len(sections)-1)]
print(f'\ngaps between sections: {len(gaps)}')
for g0, g1 in gaps[:12]:
    print(f'  0x{g0:x}..0x{g1:x} = {g1-g0} B: {d[g0:min(g1, g0+32)].hex()}')
