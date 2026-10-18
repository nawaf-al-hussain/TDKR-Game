#!/usr/bin/env python3
"""S35 T2b: layout-consistency test on 394/194 candidates — real streams
match the body layout: normals f32x3 @+12 unit-ish, UV u16 4.12 fixed @+72
in [0,16); descriptor/header + vertex count before the stream."""
import struct
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
NBYTES = len(md)
u32 = lambda o: struct.unpack_from('<I', md, o)[0]
u16 = lambda o: struct.unpack_from('<H', md, o)[0]
f32 = lambda o: struct.unpack_from('<f', md, o)[0]

def read_recs(vert_off, nverts):
    return [md[vert_off + i * 80: vert_off + i * 80 + 80] for i in range(nverts)]

def layout_score(vert_off, nverts):
    """fraction of records passing normal-unit + UV-range + finite-pos."""
    ok = 0
    for i in range(nverts):
        o = vert_off + i * 80
        p = struct.unpack_from('<3f', md, o)
        n = struct.unpack_from('<3f', md, o + 12)
        if not all(abs(x) < 10 and np.isfinite(x) for x in p):
            continue
        nl = math.sqrt(sum(x * x for x in n)) if (nn := n) else 0
        if not (0.7 < nl < 1.3):
            continue
        ur, vr = u16(o + 72), u16(o + 76)
        if not (ur < 65536 and vr < 65536):  # 4.12 fixed: u/v < 16 -> < 65536
            continue
        if ur >= 16 * 4096 or vr >= 16 * 4096:
            continue
        ok += 1
    return ok / nverts

import math
# positive control: body
print('body @0x4b5c layout score:', round(layout_score(0x4b5c, 1449), 4))
print('body @0x388a0 (zero run) layout score:', round(layout_score(0x388a0, 1449), 4))

# top 394 candidates from sweep
CANDS = [0x23c7c, 0x23c8c, 0x23cb8, 0x23c80, 0x23cb4, 0x23c94, 0x23c84, 0x23c98]
print('\n394 candidates layout scores:')
for off in CANDS:
    ls = layout_score(off, 394)
    # descriptor probe: u32==394 or f32 pair within 0x80 before
    desc = []
    for back in range(8, 0x84, 4):
        v = u32(off - back)
        if v == 394 or v == 2006:
            desc.append(f'u32@-{back}={v}')
    p1, p2 = f32(off - 8), f32(off - 4)
    print(f'  0x{off:x}: layout {ls:.3f} desc={desc} pre-f32=({p1:.4g},{p2:.4g})')

# the r34-declared cape stream headers
print('\ndeclared stream headers:')
for off, nv in ((0x388a0, 1449), (0x5cc24, 394), (0x6901c, 194)):
    p1, p2 = f32(off - 8), f32(off - 4)
    print(f'  0x{off:x} ({nv}v): pre-f32=({p1:.4g},{p2:.4g}) layout={layout_score(off, nv):.3f}')

# body stream header for comparison
p1, p2 = f32(0x4b5c - 8), f32(0x4b5c - 4)
print(f'  body 0x4b5c: pre-f32=({p1:.4g},{p2:.4g})')
# zone census around top candidate
print('\nzone around 0x23c7c (u32 view):')
for o in range(0x23c00, 0x23d00, 16):
    print(f'  0x{o:x}: ' + ' '.join(f'{u32(o+4*k):8d}' for k in range(4)))
