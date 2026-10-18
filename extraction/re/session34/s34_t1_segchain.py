#!/usr/bin/env python3
"""S34 T1: walk the segment-record chain. Idle's record near 0xccd0; extract
tablePtr + data ranges; enumerate all segments; find run's segment(s)."""
import struct, json
AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: return None

# dump 0xccc0..0xce40 to see record boundaries
print('=== 0xccc0..0xce60 ===')
for o in range(0xccc0, 0xce60, 8):
    print(f'  0x{o:06x}: {u32a(o):8x} {u32a(o+4):8x}')

# clip list for cross-reference (tickEnd values)
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', ad, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))
print(f'\n{len(clips)} clips; first 10: {[(nm, ts, te) for nm, ts, te in clips[:10]]}')
