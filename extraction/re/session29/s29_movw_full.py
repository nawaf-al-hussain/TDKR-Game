#!/usr/bin/env python3
"""S29 T1: full ARM MOVW/MOVT pair scan; hunt 0xC69A6A7 / 0x2AD64F3D / 0x3377F0E and ALL id-like pairs."""
import struct, json
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
TEXT = (0xa5d80, 0xac2490)

TARGETS = {0xC69A6A7: 'UNKNOWN_Underground_ThePit', 0x2AD64F3D: 'UNKNOWN_ThePit', 0x3377F0E: 'UNKNOWN_Military'}
KNOWN = {0x2657: 'LevelInit', 0x2B: 'CinematicObject', 0x798F: 'waypoint', 0x2666: 'wpLua',
         0x10FF796: 'CDummyComponent', 0x17AC851F: 'CCinematicComponent', 0x2AD64F3D: '?', 0xC69A6A7: '?', 0x3377F0E: '?'}

events = []  # (addr, rd, val16, kind)
for i in range(TEXT[0], TEXT[1] - 4, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if (w & 0x0FF00000) == 0x03000000:      # MOVW
        imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
        rd = (w >> 12) & 0xF
        events.append((i, rd, imm16, 'W'))
    elif (w & 0x0FF00000) == 0x04000000:    # MOVT
        imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
        rd = (w >> 12) & 0xF
        events.append((i, rd, imm16, 'T'))
print('total MOVW/MOVT events:', len(events))

# pair: same rd, W then T within 0x40 bytes
pairs = {}
lastW = {}
for a, rd, v, k in events:
    if k == 'W':
        lastW[rd] = (a, v)
    else:
        if rd in lastW:
            aw, vw = lastW[rd]
            if 0 < a - aw <= 0x40:
                val = (v << 16) | vw
                pairs.setdefault(val, []).append((aw, a, rd))
print('formed pairs:', len(pairs))
hits = {}
for val, locs in pairs.items():
    if val in TARGETS:
        hits[val] = locs
        print(f'TARGET {TARGETS[val]} ({val:#x}): {len(locs)} sites -> {[(hex(a),hex(b)) for a,b in locs[:8]]}')
# also dump distribution of pair values that match known ids
for val, locs in pairs.items():
    if val in KNOWN and val not in TARGETS:
        print(f'known {KNOWN[val]} ({val:#x}): {len(locs)} sites')
json.dump({hex(v): [(hex(a), hex(b), r) for a, b, r in ls] for v, ls in pairs.items()},
          open('/tmp/my-project/work/re29/movw_pairs.json', 'w'), indent=0)
