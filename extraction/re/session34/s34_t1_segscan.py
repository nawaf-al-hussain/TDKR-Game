#!/usr/bin/env python3
"""S34 T1: find SAnimationSegment instances in the BRES image. Scan for u32s
equal to key anchors (0x53200 stream table, 0x536e4 data, 0x53648, 0x536e4-0x9c)
and for plausible segment structs [count~157][offset][size 0xfa70]."""
import struct, json

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

anchors = {
    0x53200: 'stream table idle',
    0x536e4: 'idle data start',
    0x53648: '0x536e4-0x9c',
    0x63154: 'idle data end',
    0xfa70: 'idle total size',
}
for name_off in (0x53200, 0x53648, 0x536e4):
    pass

hits = {v: [] for v in anchors}
for o in range(0, N - 4, 4):
    w = u32a(o)
    if w in anchors:
        hits[w].append(o)
for v, lst in hits.items():
    print(f'anchor 0x{v:x} ({anchors[v]}): {len(lst)} refs at '
          f'{[hex(x) for x in lst[:12]]}')

# segment struct hunt: consecutive u32s (count, off, size) patterns
# look for 0xfa70 (total size) near 0x9c (first off) near 157/156/78 counts
print('\nstruct scan: windows where u32==157 or 156 or 78 within 0x40 of u32 0xfa70:')
cand = []
for o in range(0, N - 0x40, 4):
    if u32a(o) in (157, 156, 78):
        zone = [u32a(o + 4*j) for j in range(16)]
        if 0xfa70 in zone or 0x536e4 in zone or 0x53200 in zone:
            cand.append(o)
for o in cand[:20]:
    print(f'  @0x{o:06x}: ' + ' '.join(f'{u32a(o+4*j):x}' for j in range(14)))

# Also: search for u32 == 0x9c (first off) adjacent to 0xa8 (first len)
print('\npairs (0x9c, 0xa8) adjacent:')
for o in range(0, N - 8, 4):
    if u32a(o) == 0x9c and u32a(o + 4) == 0xa8 and abs(o - 0x53200) > 0x100:
        print(f'  @0x{o:06x}: ' + ' '.join(f'{u32a(o+4*j):x}' for j in range(10)))
