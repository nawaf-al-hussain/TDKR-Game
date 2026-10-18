#!/usr/bin/env python3
"""S33 T1: find engine code referencing magic 0x14FFFF / stride constants."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
print(f'.so size {len(d)}')

def find_all(pat, limit=40):
    out, i = [], 0
    while len(out) < limit:
        i = d.find(pat, i)
        if i < 0: break
        out.append(i)
        i += 1
    return out

# literal-pool words (little-endian)
for val, name in ((0x0014ffff, 'magic 0x14FFFF'),
                  (0x000c0000, 'stride<<16 0x0C0000 (vec3)'),
                  (0x00100000, 'stride<<16 0x100000 (vec4)'),
                  (0x00000044, '44')):
    hits = find_all(struct.pack('<I', val))
    print(f'{name}: {len(hits)} hits in file')
    for h in hits[:20]:
        print(f'  0x{h:x}')

# also as bytes pattern in .text (ARM literal pools live in .text)
print('\nsearch aligned words only in 0x0..0xbbe1ec:')
for val, name in ((0x0014ffff, 'magic'), (0x000c0000, 'vec3stride'), (0x00100000, 'vec4stride')):
    pat = struct.pack('<I', val)
    hits = find_all(pat, 100)
    aligned = [h for h in hits if h % 4 == 0 and h < 0xbbe1ec]
    print(f'{name}: total {len(hits)}, in-text aligned {len(aligned)}: '
          + ' '.join(f'0x{h:x}' for h in aligned[:24]))
