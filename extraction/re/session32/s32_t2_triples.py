#!/usr/bin/env python3
"""S32 T2c: decode the per-clip channel triples (start,end,name)."""
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

clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te, o + 12 * len(clips)))

# triples start right after the clip table
print('=== triples right after clip table ===')
o = 0x11e54
for k in range(10):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    nm = cstr(C)
    span = B - A
    # interpretation dump
    ticks = [u32(A + 4 * j) for j in range(4)] if span < 4096 else []
    vals = [round(f32(A + 4 * j), 4) for j in range(4)] if span < 4096 else []
    print(f'  triple {k}: A=0x{A:x} B=0x{B:x} (span {span} B) C=0x{C:x} '
          f'name={nm!r}')
    print(f'     as u32: {ticks}   as f32: {vals}')
# how many triples until something breaks?
n = 0
o = 0x11e54
while True:
    A, B, C = u32(o), u32(o + 4), u32(o + 8)
    if not (A < B < len(d) and cstr(C)):
        break
    n += 1
    o += 12
print(f'\ncontiguous plausible triples: {n} (ends @0x{o:x})')
# sample names along the way
o = 0x11e54
seen_names = []
for k in range(0, min(n, 4000), 1):
    C = u32(o + 12 * k + 8)
    nm = cstr(C)
    if nm and (not seen_names or seen_names[-1][1] != nm):
        seen_names.append((k, nm))
print('first 15 distinct names with triple index:')
for k, nm in seen_names[:15]:
    print(f'  triple {k}: {nm!r}')
print('...')
for k, nm in seen_names[-6:]:
    print(f'  triple {k}: {nm!r}')
