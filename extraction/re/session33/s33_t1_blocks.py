#!/usr/bin/env python3
"""S33 T1: full 733-block table enumeration + _184 tail + name overlap."""
import struct, collections

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

blocks = []
o = 0x11e54
for k in range(734):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    nm = cstr(C)
    if not nm:
        break
    blocks.append((nm, A, B, o + 12 * k))

print(f'{len(blocks)} block records')
# records-per-name histogram
cnt = collections.Counter(nm for nm, A, B, _ in blocks)
h = collections.Counter(cnt.values())
print('records-per-name histogram:', dict(sorted(h.items())))
multi = [(nm, c) for nm, c in cnt.items() if c > 1]
print(f'names with >1 record: {len(multi)}')
for nm, c in sorted(multi)[:15]:
    sites = [(hex(A), B - A) for n, A, B, _ in blocks if n == nm]
    print(f'  {nm}: x{c} {sites}')

# do consecutive blocks' ranges overlap or leave gaps? sample 30
print('\ncontiguity of consecutive records (first 30):')
for i in range(min(30, len(blocks) - 1)):
    nm, A, B, _ = blocks[i]
    nm2, A2, B2, _ = blocks[i + 1]
    gap = A2 - B
    print(f'  {nm:40s} 0x{A:x}..0x{B:x} ({B-A:5d}) -> gap to next {gap:6d}')

# name overlap with clip table
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te))
clipnames = {nm for nm, ts, te in clips}
blocknames = {nm for nm, A, B, _ in blocks}
print(f'\nclips {len(clips)}, block names {len(blocknames)}')
print('block names that are also clip names:',
      len(blocknames & clipnames))
print('examples:', sorted(blocknames & clipnames)[:10])

# _184 tail: last 256 B
print('\n=== _184 block tail (0x72f0f-256..0x72f0f) ===')
A, B = 0x72bf0, 0x72f0f
for off in range(B - 256, B, 16):
    ws = [u32(off + 4 * j) for j in range(4)]
    print(f'  0x{off:x}: ' + ' '.join(f'{x:08x}' for x in ws)
          + '  | ' + ' '.join(f'{f32(off+4*j):9.4f}' for j in range(4)))
