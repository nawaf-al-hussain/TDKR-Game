#!/usr/bin/env python3
"""S32 T2h: inspect the _002 channel cluster @0xa2f00.. and try to parse
one channel block end-to-end."""
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

# all xrefs to _002 string 0x300c
needle = struct.pack('<I', 0x300c)
xr = []
st = 0
while True:
    j = d.find(needle, st)
    if j < 0:
        break
    xr.append(j)
    st = j + 4
print(f'{len(xr)} xrefs to _002 name')
print([hex(x) for x in xr[:24]])
gaps = [xr[i + 1] - xr[i] for i in range(min(20, len(xr) - 1))]
print('gaps:', gaps)

# dump the first cluster
A = xr[0] - 16
print(f'\n=== dump 0x{A:x}.. +0x300 ===')
for off in range(A, A + 0x300, 32):
    ws = [u32(off + 4 * j) for j in range(8)]
    st2 = '/'.join(s for s in (cstr(w) or '' for w in ws) if s)[:44]
    print(f'  0x{off:x}: ' + ' '.join(f'{w:08x}' for w in ws) + '  ' + st2)
