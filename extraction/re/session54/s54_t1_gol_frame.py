#!/usr/bin/env python3
"""s54 T1 step 5: verify gol.bin record framing around the Glide record;
dump record offsets, check coverage, hexdump the region."""
import struct

GOL = '/tmp/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
print('table@%#x nrec=%d file=%d(%#x)' % (table_off, nrec, len(d), len(d)))

sorted_offs = sorted(o for o in offs if o != 0xFFFF and o < table_off)
print('valid offsets:', len(sorted_offs), 'min', hex(sorted_offs[0]), 'max', hex(sorted_offs[-1]))
gaps = [(hex(a), hex(b)) for a, b in zip(sorted_offs, sorted_offs[1:]) if b - a > 4000]
print('large gaps:', gaps[:10])

# offsets near the Glide record
glide_off = None
for i, off in enumerate(offs):
    if off == 0xFFFF or off >= table_off:
        continue
    p = off
    oid = struct.unpack_from('>I', d, p)[0]
    if oid == 0x7990:
        glide_off = off
        print('Glide record idx %d off %#x' % (i, off))
for o in sorted_offs:
    if abs(o - glide_off) < 0x200:
        print('  nearby rec off %#x (delta %+d)' % (o, o - glide_off))

# hexdump the region before/after glide_off
def hexdump(start, end):
    for row in range(start, end, 16):
        chunk = d[row:row + 16]
        hexs = ' '.join('%02x' % b for b in chunk)
        asci = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print('  %06x  %-47s  %s' % (row, hexs, asci))

print('\nregion around Glide record:')
hexdump(glide_off - 32, glide_off + 320)
