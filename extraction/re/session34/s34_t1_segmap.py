#!/usr/bin/env python3
"""S34 T1e: decode ch0 tick ranges + spread profile for segments 0..16,
compare with clip windows -> determine the clip<->segment mapping."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

segs = json.load(open('/home/z/my-project/scripts/s34_t1_segs.json'))

def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: return None
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', ad, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))

def ch0_range(ptr):
    """read first entry (time stream) directly: ticks = first ln/4 u32s after table"""
    # entry0 = (off, ln): data starts at ptr + nent*8 + delta; but for a quick
    # range check, find 38-75-length ascending runs after the table... use the
    # full decode but only ch0 (cheap): scan entries until first non-sane.
    pairs = []
    k = 0
    while k < 200:
        off, ln = u32a(ptr + 8*k), u32a(ptr + 8*k + 4)
        if ln == 0 or ln > 0x4000 or off > 0x20000 or ln % 4: break
        pairs.append((off, ln)); k += 1
    ne = len(pairs)
    for extra in (0, 4, 8, 12):
        base = ptr + ne*8 + extra
        pos = base; ok = True
        # validate ch0 time only, then read range
        ln0 = pairs[0][1]
        w = [u32a(pos + 4*j) for j in range(ln0 // 4)]
        if not all(w[i] < w[i+1] for i in range(len(w)-1)) or w[-1] >= 2e6:
            continue
        return w[0], w[-1], len(w), ne
    return None

print(f'{"seg":>4} {"clip (by index)":34} {"clip window":>16} {"recEnd":>8} '
      f'{"ch0 ticks":>18} {"nkeys":>6}')
for i in range(17):
    s = segs[i]
    nm, ts, te = clips[i]
    r = ch0_range(s['ptr'])
    rr = f'{r[0]}..{r[1]} ({r[2]})' if r else 'FAIL'
    print(f'{i:4d} {nm:34} [{ts:6d}..{te:6d}] {s["tickEnd"]:8d} {rr:>22}')

# where does run's window [30000..30666] sit? which segments' ch0 ranges cover it?
print('\nsegments whose ch0 range intersects [30000..30666]:')
for i in range(20):
    r = ch0_range(segs[i]['ptr'])
    if r and r[0] <= 30666 and r[1] >= 30000:
        print(f'  seg{i} ({clips[i][0]}): ch0 {r[0]}..{r[1]}')
