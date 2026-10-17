#!/usr/bin/env python3
"""S32 T2g: fully dump + segment two per-clip data blocks."""
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

# collect the 733 per-clip records
o = 0x11e54
recs = []
for k in range(734):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    recs.append((cstr(C), A, B))
byname = {nm: (A, B) for nm, A, B in recs}

for nm in ('_187_enemy_idle_aim_to_run_aim', '_193_back_spin_kick2'):
    A, B = byname[nm]
    print(f'===== {nm} @0x{A:x}..0x{B:x} ({B-A} B) =====')
    off = A
    while off < B:
        words = [u32(off + 4 * j) for j in range(min(12, (B - off) // 4))]
        line = ' '.join(f'{w:08x}' for w in words)
        strs = [cstr(w) or '' for w in words]
        st = '/'.join(s for s in strs if s)[:60]
        print(f'  0x{off:x}: {line}  {st}')
        off += 48
    print()
