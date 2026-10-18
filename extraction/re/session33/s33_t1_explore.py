#!/usr/bin/env python3
"""S33 T1: fresh exploration of batman_anims.bdae structure.

Goals:
- clip table @0x11580 (921 x 12B [nameOff, tickStart, tickEnd])
- named-group head @0xb53c (78 x 32B) + descriptor chain zone
- per-clip self-contained blocks @0x11e54 (733 x 12B [A,B,name])
- page table @0x18c14
- dump _008_run + _001_idle_stand blocks fully as u32/f32
"""
import struct

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
print(f'file size {len(d)} B (0x{len(d):x})')
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

# ---- clip table ----
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te, o + 12 * len(clips)))
print(f'\n{len(clips)} clips @0x11580..0x{clips[-1][3]+12:x}')
print('table end zone:',
      ' '.join(f'{u32(clips[-1][3]+12+4*j):08x}' for j in range(8)))
for i in list(range(6)) + [183, 184, 185, 186, 187, 200]:
    nm, ts, te, off = clips[i]
    print(f'  clip[{i:3d}] @0x{off:x} {nm!r:44s} ts={ts:8d} te={te:8d} dur={te-ts}')

# ---- named groups ----
groups = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if not (w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1):
        break
    groups.append((o, w))
    o += 32
print(f'\n{len(groups)} named groups @0xb53c..0x{o:x}')
for k in (0, 1, 2):
    off, w = groups[k]
    print(f'  g[{k}] @0x{off:x}: {[hex(x) for x in w]} name={cstr(w[2])!r}')
print('  ...')
off, w = groups[-1]
print(f'  g[-1] @0x{off:x}: {[hex(x) for x in w]} name={cstr(w[2])!r}')

# descriptor records for group 0: w[4]=tOff, w[6]=vOff
off, w = groups[0]
for lbl, p in (('tOff', w[4]), ('vOff', w[6])):
    r = [u32(p + 4 * j) for j in range(11)]
    print(f'  g0 {lbl}=0x{p:x}: {[hex(x) for x in r]}')
    # next-pointer chase: which field is next? dump following records
    for j in range(1, 4):
        r2 = [u32(p + 44 * j + 4 * k) for k in range(11)]
        print(f'    +{j} @0x{p+44*j:x}: {[hex(x) for x in r2]}')

# ---- per-clip blocks ----
print(f'\n733-block table @0x11e54:')
blocks = []
o = 0x11e54
for k in range(734):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    nm = cstr(C)
    if not nm:
        break
    blocks.append((nm, A, B, o + 12 * k))
print(f'  {len(blocks)} blocks, end 0x{o+12*len(blocks):x}')
bynm = {nm: (A, B) for nm, A, B, _ in blocks}
for nm in ('_008_run', '_001_idle_stand', '_002_walk'):
    if nm in bynm:
        A, B = bynm[nm]
        print(f'  {nm}: 0x{A:x}..0x{B:x} ({B-A} B)')
print('  first 6 blocks:', [(nm, f'0x{A:x}', f'0x{B:x}', B - A)
                            for nm, A, B, _ in blocks[:6]])

# ---- page table ----
print('\npage table @0x18c14 (16 u32):',
      ' '.join(f'{u32(0x18c14+4*j):08x}' for j in range(16)))

# ---- _008_run block raw ----
if '_008_run' in bynm:
    A, B = bynm['_008_run']
    print(f'\n=== _008_run @0x{A:x}..0x{B:x} ({B-A} B) ===')
    for off in range(A, min(B, A + 192), 16):
        ws = [u32(off + 4 * j) for j in range(4)]
        print(f'  0x{off:x}: ' + ' '.join(f'{x:08x}' for x in ws)
              + '   | ' + ' '.join(f'{f32(off+4*j):9.4f}' for j in range(4)))
