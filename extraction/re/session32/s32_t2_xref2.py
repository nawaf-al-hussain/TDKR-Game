#!/usr/bin/env python3
"""S32 T2f: inspect per-clip structures at name-xref sites."""
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

def dump(off, n=14, label=''):
    print(f'  @0x{off:x} {label}:')
    print('    u32:', ' '.join(f'{u32(off+4*j):08x}' for j in range(n)))
    print('    f32:', [round(f32(off + 4 * j), 4) for j in range(8)])
    strs = [cstr(u32(off + 4 * j)) for j in range(n)]
    if any(strs):
        print('    strs:', [s for s in strs if s][:4])

print('=== _008_run xref sites ===')
for x in (0x834348, 0xbbf73c, 0x18cb024, 0x22c6d68, 0x23a5584):
    dump(x - 16, 16, '(run str at +16)')

print('\n=== _002 cluster @0xa2f10 ===')
for x in (0xa2f10, 0xa31f0, 0xa34ec):
    dump(x - 16, 16, '(002 str at +16)')

# walk around 0x834348: what precedes/follows (record array?)
print('\n=== context walk 0x834280..0x834480 ===')
for off in range(0x834280, 0x834480, 32):
    print(f'  @0x{off:x}:', ' '.join(f'{u32(off+4*j):08x}' for j in range(8)))
