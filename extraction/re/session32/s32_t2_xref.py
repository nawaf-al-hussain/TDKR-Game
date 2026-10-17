#!/usr/bin/env python3
"""S32 T2e: xref _008_run / _001_idle_stand strings; map the descriptor zone."""
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

for nm in (b'_008_run', b'_001_idle_stand', b'_002_idle_stand_breath'):
    offs = []
    start = 0
    while True:
        i = d.find(nm, start)
        if i < 0:
            break
        offs.append(i)
        start = i + 1
    print(f'{nm.decode()}: string at {[hex(x) for x in offs]}')
    for so in offs:
        # find u32 xrefs
        needle = struct.pack('<I', so)
        xr = []
        st = 0
        while True:
            j = d.find(needle, st)
            if j < 0:
                break
            xr.append(j)
            st = j + 4
        print(f'  xrefs to 0x{so:x}: {[hex(x) for x in xr[:10]]}'
              f'{"..." if len(xr) > 10 else ""}')

# descriptor zone census: 44-B records from 0xbf04 to 0x18c14
print('\n=== 44-B record census 0xbf04..0x18c14 ===')
n = (0x18c14 - 0xbf04) // 44
print(f'count if fully tiled: {n} (remainder {(0x18c14-0xbf04) % 44})')
# walk records: valid ones have [0]==1? and last word 0x14ffff
ok = 0
bad = 0
o = 0xbf04
kinds = {}
while o + 44 <= 0x18c14:
    w = [u32(o + 4 * j) for j in range(11)]
    if w[10] == 0x14FFFF and w[0] == 1:
        ok += 1
        kinds[w[7]] = kinds.get(w[7], 0) + 1
    else:
        bad += 1
    o += 44
print(f'valid 44-B records: {ok}, invalid: {bad}, field7 histogram: {kinds}')

# sample records beyond the first 78 channels
print('\nrecords 78..86:')
for k in range(78, 86):
    off = 0xbf04 + 44 * k
    w = [u32(off + 4 * j) for j in range(11)]
    nm = cstr(w[8]) if w[8] > 0x1000 and w[8] < len(d) else None
    print(f'  rec {k} @0x{off:x}: {w[:8]} tail=({w[8]:#x},{w[9]},{w[10]:#x}) '
          f'name={nm!r}')
