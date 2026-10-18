#!/usr/bin/env python3
"""S33 T1: map remaining zones; decode dialect-B block structure."""
import struct

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try:
                return d[v:e].decode('latin1')
            except Exception:
                pass
    return None

print('=== strings near 0x1e84 ===')
for p in (0x1e84, 0x1ea0, 0x1ed4, 0x1f0c, 0x1f44):
    print(f'  0x{p:x}: {cstr(p)!r}')

print('\n=== zone 0xb400..0xb53c (before groups) ===')
for off in range(0xb400, 0xb53c, 16):
    print(f'  0x{off:x}: ' + ' '.join(f'{u32(off+4*j):08x}' for j in range(4))
          + '  | ' + ' '.join(f'{f32(off+4*j):9.4f}' for j in range(4)))

print('\n=== find end of descriptor-record zone (44B chains from 0xbf04) ===')
o = 0xbf04
nrec = 0
while o + 44 <= 0x11580:
    r = [u32(o + 4 * j) for j in range(11)]
    if r[10] == 0x14ffff and r[0] == 1 and r[2] == 1 and r[4] == 6:
        nrec += 1
        o += 44
    else:
        break
print(f'  {nrec} consecutive 44-B records 0xbf04..0x{o:x}')
print(f'  zone tail @0x{o:x}:', ' '.join(f'{u32(o+4*j):08x}' for j in range(8)))

print('\n=== zone 0x140ac..0x14500 (after clip+block tables) ===')
for off in range(0x140ac, 0x14300, 16):
    print(f'  0x{off:x}: ' + ' '.join(f'{u32(off+4*j):08x}' for j in range(4)))

print('\n=== dialect-B block _187 (0x74360..0x744cf, 367 B) ===')
A, B = 0x74360, 0x744cf
for off in range(A, B, 16):
    ws = [u32(off + 4 * j) for j in range(min(4, (B - off) // 4))]
    print(f'  0x{off:x}: ' + ' '.join(f'{x:08x}' for x in ws)
          + '  | ' + ' '.join(f'{f32(off+4*j):9.4f}' for j in range(min(4, (B-off)//4))))

print('\n=== dialect-B block _184 (0x72bf0..0x72f0f, 799 B) head ===')
A, B = 0x72bf0, 0x72f0f
for off in range(A, A + 128, 16):
    ws = [u32(off + 4 * j) for j in range(4)]
    print(f'  0x{off:x}: ' + ' '.join(f'{x:08x}' for x in ws)
          + '  | ' + ' '.join(f'{f32(off+4*j):9.4f}' for j in range(4)))

print('\n=== what is at 0x53200 (after pages) .. 0x53400 ===')
for off in range(0x531f0, 0x53300, 16):
    print(f'  0x{off:x}: ' + ' '.join(f'{u32(off+4*j):08x}' for j in range(4)))

print('\n=== header @0x0..0x40 ===')
for off in range(0, 0x40, 16):
    print(f'  0x{off:x}: ' + ' '.join(f'{u32(off+4*j):08x}' for j in range(4)))
