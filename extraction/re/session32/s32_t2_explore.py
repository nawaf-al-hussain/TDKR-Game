#!/usr/bin/env python3
"""S32 T2a: explore the anim file descriptor-zone structures."""
import struct

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]
print(f'file size {len(d):x}')

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 80:
            try:
                return d[v:e].decode('latin1')
            except Exception:
                pass
    return None

# clip table
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te))
print(f'clips: {len(clips)}; first 10: {[c[0] for c in clips[:10]]}')

# named groups @0xb53c
print('\nnamed groups @0xb53c:')
groups = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if not (w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1):
        break
    groups.append(w)
    o += 32
print(f'  {len(groups)} groups; first 6:')
for w in groups[:6]:
    print(f'    {cstr(w[2])!r:34s} w=({w[0]:.3g},{w[1]}) tOff={w[4]:#x} '
          f'vOff={w[6]:#x} w7={w[7]:#x}')
names = [cstr(w[2]) for w in groups]
print('  distinct tracks:', sorted({n.split("-node-")[-1] for n in names}))
print('  distinct bones:', sorted({n.split("-node-")[0] for n in names})[:8],
      '... total', len({n.split('-node-')[0] for n in names}))

# dump a descriptor record chain: group 0 (which?)
print('\ngroup0 tOff region:')
t0 = groups[0][4]
for k in range(12):
    off = t0 + 44 * k
    print(f'  @0x{off:x}:', ' '.join(f'{u32(off+4*j):08x}' for j in range(11)))
print('\ngroup0 vOff region:')
v0 = groups[0][6]
for k in range(12):
    off = v0 + 44 * k
    print(f'  @0x{off:x}:', ' '.join(f'{u32(off+4*j):08x}' for j in range(11)))

# what is at the next-pointer targets?
for tgt in (0x1ea0, 0x1ed4, 0x1f0c, 0x1f44):
    print(f'\n@0x{tgt:x}:', ' '.join(f'{u32(tgt+4*j):08x}' for j in range(11)))
    # as f32
    print('   f32:', [round(f32(tgt + 4 * j), 4) for j in range(8)])
