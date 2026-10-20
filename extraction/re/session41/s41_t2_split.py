#!/usr/bin/env python3
"""S41 T2: manually parse the embedded ZIP inside a PK_SPLIT entry."""
import struct, zipfile, sys, io
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import read_archive

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d, ents = read_archive(Z, 'actors_tex.gla')
# find Collectible_graffiti and one more split entry
splits = [(n, o, s) for (n, o, s) in ents if d[o:o+2] == b'PK']
print('PK_SPLIT entries in actors_tex:', len(splits), [x[0] for x in splits][:6])

for name, off, size in splits[:2]:
    print(f'\n=== {name} (entry {size} B)')
    buf = d[off:off + size]
    pos = 0
    members = []
    while pos + 30 <= len(buf) and buf[pos:pos+4] == b'PK\x03\x04':
        ver, flags, method, t, dt, crc, comp, uncomp, nlen, xlen = struct.unpack_from('<HHHHHIIIHH', buf, pos + 4)
        nm = buf[pos+30:pos+30+nlen].decode('latin1')
        data = buf[pos+30+nlen+xlen: pos+30+nlen+xlen+comp]
        members.append((nm, method, comp, uncomp, bytes(data)))
        pos += 30 + nlen + xlen + comp
    print('trailing bytes after local members:', len(buf) - pos, 'next sig:', buf[pos:pos+4])
    for nm, method, comp, uncomp, data in members:
        print(f'  member {nm!r} method={method} comp={comp} uncomp={uncomp}')
        if method == 8:
            try:
                import zlib
                inf = zlib.decompress(data, -15)
                print(f'    inflated {len(inf)} B; first 16: {inf[:16].hex()}')
                if uncomp <= 8:
                    print('    content:', inf)
            except Exception as e:
                print('    inflate failed:', e)
        else:
            print(f'    stored content: {data[:40]!r}')
