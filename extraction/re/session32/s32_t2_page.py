#!/usr/bin/env python3
"""S32 T2i: page-pair dialect decode attempt for _008_run @0xbbf72c site."""
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

SITE = 0xbbf72c
# scan back/forward for the (name, size) pair array extent
pairs = []
o = SITE - 16
# find start: walk back while (name plausible, size plausible)
def plausible_pair(off):
    a, b = u32(off), u32(off + 4)
    return (0x1000 < a < 0xb500 and cstr(a) and b < 0x10000)

s = SITE - 16
while plausible_pair(s - 8):
    s -= 8
e = SITE - 16
while plausible_pair(e):
    e += 8
print(f'pair array @0x{s:x}..0x{e:x} = {(e-s)//8} pairs')
tot = 0
arr = []
for off in range(s, e, 8):
    a, b = u32(off), u32(off + 4)
    arr.append((a, b, cstr(a)))
    tot += b
for a, b, nm in arr[:20]:
    print(f'  ({a:#x}, {b:5d}) {nm!r}')
print(f'  ... total size {tot} B; array ends 0x{e:x}')
print('names distinct:', sorted({nm for _, _, nm in arr})[:12])

# hypothesis: streams packed right after array, in pair order
print('\n=== stream decode attempt (packed after table) ===')
off = e
for a, b, nm in arr[:8]:
    n20, n16, n12, n8 = b / 20, b / 16, b / 12, b / 8
    kind = None
    for lbl, n in (('q+t', n20), ('v3+t', n16), ('v3', n12), ('s+t', n8)):
        if abs(n - round(n)) < 1e-6 and round(n) > 0:
            kind = (lbl, round(n))
            break
    print(f'  {nm!r}: size {b} -> {kind}')
    if kind:
        lbl, n = kind
        stride = {'q+t': 20, 'v3+t': 16, 'v3': 12, 's+t': 8}[lbl]
        k0 = [f32(off + 4 * j) for j in range(4)]
        t0 = u32(off + stride - 4) if lbl != 'v3' else None
        print(f'      first f32s {[round(x,4) for x in k0]} '
              f'first-tick {t0}')
        # ticks ascending check
        ticks = [u32(off + stride * (k + 1) - 4) for k in range(min(n, 10))]
        asc = all(ticks[i] < ticks[i + 1] for i in range(len(ticks) - 1))
        print(f'      ticks {ticks} ascending={asc}')
    off += b
print(f'after streams @0x{off:x}:',
      ' '.join(f'{u32(off+4*j):08x}' for j in range(8)))
