#!/usr/bin/env python3
"""s45 T1a step 4: resolve sampler-name strings + find mat73's texture binding.

Steps: read all name-pool strings referenced by rec73 blocks; establish the
ordinal of gothamcity_roads_details.tga in (a) image pool, (b) tga list; then
search that ordinal value in the rec73 target neighborhoods (u16/u32).
"""
import struct, io, zipfile
import numpy as np

def load_bres():
    P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
    raw = open(P, 'rb').read()
    return zipfile.ZipFile(io.BytesIO(raw)).read('little_endian_not_quantized.bdae')

bres = load_bres()
u16 = np.frombuffer(bres, '<u2', len(bres) // 2)
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)

def cstr(off):
    try:
        e = bres.index(b'\0', off)
        return bres[off:e].decode('ascii', 'replace')
    except Exception:
        return '<bad>'

names = [0x18a70, 0x18a7c, 0x18a9c, 0x18aa8, 0x18ae4, 0x18b14, 0x18b20, 0x18b3c,
         0x18b84, 0x18eac, 0x19180, 0x19198, 0x18ad0, 0x18af8, 0x18b58]
print('=== name pool strings ===')
for n in names:
    print(f'  {n:#x}: {cstr(n)!r}')

# image pool: triples {image_name,len,tga_name} at 0x171ec+ ; ptr table @0x22d04
# rebuild ordered list from the pointer table: two pointers per image (image, tga)
print('\n=== image ptr table walk @0x22d04 ===')
imgs = []
for k in range(300):
    off = 0x22d04 + k * 8
    p1 = int(u32[off // 4]); p2 = int(u32[off // 4 + 1])
    if not (0x1000 < p1 < len(bres) and 0x1000 < p2 < len(bres)):
        break
    imgs.append((cstr(p1), cstr(p2)))
print('entries:', len(imgs))
for i, (a, b) in enumerate(imgs):
    if 'roads_details' in b or i in (54, 55, 56, 57):
        print(f'  [{i}] image={a!r} tga={b!r}')

# ordinal of roads_details
ordi = [i for i, (a, b) in enumerate(imgs) if 'roads_details' in b]
print('roads_details image-pool ordinal:', ordi)

# also walk the raw triple area at 0x171ec for an ordered tga list
# triple format from s44: {image_name, len, tga_name} - find pointer triples near 0x22d04 alt table
# Instead: scan the u16 view of rec73 target region 0x3f000..0x41000 for the ordinal value
if ordi:
    V = ordi[0]
    seg16 = u16[0x3f000 // 2:0x41000 // 2]
    hits = np.where(seg16 == V)[0]
    print(f'u16=={V} in 0x3f000..0x41000: {len(hits)} at {[hex(0x3f000 + h * 2) for h in hits[:12]]}')
    seg32 = u32[0x3f000 // 4:0x41000 // 4]
    hits3 = np.where(seg32 == V)[0]
    print(f'u32=={V} in 0x3f000..0x41000: {len(hits3)} at {[hex(0x3f000 + h * 4) for h in hits3[:12]]}')
    # also 56
    h56 = np.where(seg16 == 56)[0]
    print(f'u16==56 in 0x3f000..0x41000: {len(h56)} at {[hex(0x3f000 + h * 2) for h in h56[:12]]}')
    h56b = np.where(seg32 == 56)[0]
    print(f'u32==56 in 0x3f000..0x41000: {len(h56b)} at {[hex(0x3f000 + h * 4) for h in h56b[:12]]}')
