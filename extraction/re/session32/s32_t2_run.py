#!/usr/bin/env python3
"""S32 T2d: decode _008_run clip data block + the 0xb480 zone."""
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

# find _008_run triple
o = 0x11e54
run_rec = None
idle_rec = None
recs = {}
for k in range(734):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    nm = cstr(C)
    recs[nm] = (A, B, o + 12 * k)
    if nm == '_008_run':
        run_rec = (A, B)
    if nm == '_001_idle_stand':
        idle_rec = (A, B)
print('_008_run record:', [hex(x) for x in run_rec] if run_rec else None)
print('_001_idle_stand record:',
      [hex(x) for x in idle_rec] if idle_rec else None)

A, B = run_rec
print(f'\n=== _008_run data @0x{A:x}..0x{B:x} ({B-A} B) ===')
print('first 16 u32:', [f'{u32(A+4*j):08x}' for j in range(16)])
print('first 8 f32:', [round(f32(A + 4 * j), 4) for j in range(8)])

A2, B2 = idle_rec
print(f'\n=== _001_idle_stand data @0x{A2:x}..0x{B2:x} ({B2-A2} B) ===')
print('first 16 u32:', [f'{u32(A2+4*j):08x}' for j in range(16)])
print('first 8 f32:', [round(f32(A2 + 4 * j), 4) for j in range(8)])

# the 0xb480 zone (341 'pairs')
print('\n=== zone @0xb480 (before named groups) ===')
print('as u32:', [f'{u32(0xb480+4*j):08x}' for j in range(24)])
print('as f32:', [round(f32(0xb480 + 4 * j), 4) for j in range(16)])
# where does the zone start? scan back for a header
print('context @0xb400..0xb53c:')
for off in range(0xb400, 0xb540, 16):
    print(f'  @0x{off:x}:', ' '.join(f'{u32(off+4*j):08x}' for j in range(4)))

# header table @0x10 revisited: 0xb45c 0xb53c 0x18c14 0x3a5ec
print('\n@0xb45c:', ' '.join(f'{u32(0xb45c+4*j):08x}' for j in range(8)))
print('@0xb45c f32:', [round(f32(0xb45c + 4 * j), 4) for j in range(8)])
# 0x18c14 zone start
print('=== zone @0x18c14 ===')
print('as u32:', [f'{u32(0x18c14+4*j):08x}' for j in range(16)])
print('as f32:', [round(f32(0x18c14 + 4 * j), 4) for j in range(12)])
print('=== zone @0x3a5ec ===')
print('as u32:', [f'{u32(0x3a5ec+4*j):08x}' for j in range(16)])
