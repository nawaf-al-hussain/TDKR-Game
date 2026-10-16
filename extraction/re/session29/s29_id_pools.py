#!/usr/bin/env python3
"""S29 T1: literal-pool hunt for component ids in .text + map ldr refs."""
import struct, json
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
TEXT = (0xa5d80, 0xac2490)

ID_TARGETS = {
    0xC69A6A7: 'UNK_Underground_ThePit', 0x2AD64F3D: 'UNK_ThePit', 0x3377F0E: 'UNK_Military',
    0x2657: 'LevelInit(tid)', 0x17AC851F: 'CCinematicComponent', 0x10FF796: 'CDummyComponent',
    0x798F: 'waypoint', 0x2B: 'CinematicObject', 0x2666: 'wpLua', 0x3377: 'lo3377', 0x6A7: 'lo6a7',
}

def arm_ldr_target(ins_addr, w):
    """decode ARM ldr rX,[pc,#imm] -> pool addr (ARM: pc = ins+8)"""
    if (w & 0x0F100000) not in (0x04100000,): return None
    if (w & 0x000F0000) >> 16 != 15: return None  # rn = pc
    imm12 = w & 0xFFF
    up = (w >> 23) & 1
    return ins_addr + 8 + imm12 if up else ins_addr + 8 - imm12

pool_hits = {}
for i in range(TEXT[0], TEXT[1] - 4, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if w in ID_TARGETS:
        pool_hits.setdefault(w, []).append(i)
for w, locs in sorted(pool_hits.items(), key=lambda kv: -len(kv[1])):
    print(f'{ID_TARGETS[w]} ({w:#x}): {len(locs)} pool words')
    for p in locs[:10]:
        # find ARM ldr referencing pool addr p (align p to 4)
        refs = []
        for back in range(4, 0x1200, 4):
            ia = p - back
            if ia < TEXT[0]: break
            wi = struct.unpack_from('<I', data, ia)[0]
            t = arm_ldr_target(ia, wi)
            if t == p:
                refs.append(ia)
        print(f'    pool {p:#x}: ldr refs {[hex(r) for r in refs[:4]]}')
json.dump({hex(w): [hex(p) for p in ls] for w, ls in pool_hits.items()},
          open('/tmp/my-project/work/re29/id_pool_hits.json', 'w'), indent=1)
