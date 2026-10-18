#!/usr/bin/env python3
"""S35 T1a9: find the in-file containers: {count, array} pairs for the
segment directory (656, 0xcd00) and clip list (921, 0x11580), plus the
0x20-stride clip entry array. Dump clip entry fields."""
import struct

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

def find_pair(count, arr, limit=20):
    hits = []
    pat = struct.pack('<II', count, arr)
    start = 0
    while True:
        i = ad.find(pat, start)
        if i < 0 or len(hits) >= limit: break
        hits.append(i)
        start = i + 1
    return hits

h_seg = find_pair(656, 0xcd00)
print('segment container {656, 0xcd00} at:', [f'0x{x:x}' for x in h_seg])
h_clip = find_pair(921, 0x11580)
print('cliplist container {921, 0x11580} at:', [f'0x{x:x}' for x in h_clip])
# clip array: 921 entries x 0x20; count 921 with unknown array ptr -> search count only
h921 = []
start = 0
while True:
    i = ad.find(struct.pack('<I', 921), start)
    if i < 0: break
    h921.append(i); start = i + 1
print(f'count==921 occurrences: {len(h921)}: {[f"0x{x:x}" for x in h921[:10]]}')
for i in h921[:6]:
    arr = u32a(i + 4)
    if 0 < arr < N:
        print(f'  0x{i:x}: count 921, array 0x{arr:x}')
        # dump first 4 entries (0x20 stride)
        for e in range(4):
            o = arr + e * 0x20
            vals = [u32a(o + 4 * k) for k in range(8)]
            print(f'    entry{e} @0x{o:x}: ' + ' '.join(f'{v:9d}' for v in vals) + '  hex: ' + ' '.join(f'{v:08x}' for v in vals))
