#!/usr/bin/env python3
"""T2: batman.bdae structure — BRES sections, mesh block, streams, indices."""
import struct, json, sys

BDAE = '/home/z/my-project/work/actors/batman.bdae'
d = open(BDAE, 'rb').read()
print(f'batman.bdae: {len(d)} B, magic {d[:4]}')
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
i32 = lambda o: struct.unpack_from('<i', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

ver = u16(4)
n_sections = u16(6)
print(f'ver=0x{ver:x} sections={n_sections}')

# find section names by scanning for known strings
for name in (b'BATMAN-mesh', b'CAPE-mesh', b'Bip01', b'-mesh-skin',
             b'-mesh', b'-skin', b'BATMAN'):
    idx = 0
    hits = []
    while True:
        i = d.find(name, idx)
        if i < 0:
            break
        hits.append(i)
        idx = i + 1
        if len(hits) > 6:
            break
    print(f'{name.decode()}: {hits[:6]}')

# the session-15 BRES layout: strings near the start; section table after
# dump the first 0x200 bytes as words for structure
print('\nhead words:')
for o in range(0, 0x80, 16):
    row = [f'{u32(o + k):08x}' for k in range(0, 16, 4)]
    print(f'  {o:04x}: {" ".join(row)}')
# strings?
print('\nbytes 0x20..0x120 as text:')
seg = d[0x20:0x120]
print(' ', seg[:64])
