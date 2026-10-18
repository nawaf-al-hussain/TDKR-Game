#!/usr/bin/env python3
"""S34 T1: find _008_run's stream tables (ch0 = 32 ticks -> len 0x80) and
their contiguous data blocks; decode run like idle (sequential cumsum rule)."""
import struct, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: return None

# clip list for windows
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', ad, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))
run_win = [(a, b) for nm, a, b in clips if nm == '_008_run'][0]
print(f'_008_run window: [{run_win[0]}..{run_win[1]}] ms')

# find tables: (0x9c, 0x80) prefix, at least 20 entries, lens plausible
tables = []
for o in range(0, N - 0x100, 4):
    if u32a(o) == 0x9c and u32a(o + 4) == 0x80:
        # count entries: (off,len) pairs with len<0x2000 and off<0x20000
        n = 0
        while n < 400:
            off, ln = u32a(o + 8*n), u32a(o + 8*n + 4)
            if ln == 0: n += 1; break
            if ln > 0x2000 or off > 0x20000: break
            n += 1
        if 20 <= n <= 300:
            tables.append((o, n))
# dedup overlapping
tables = [t for t in tables if all(not (t[0] > p[0] and t[0] < p[0] + 8*p[1])
                                   for p in tables)]
for o, n in tables:
    lens = [u32a(o + 8*k + 4) for k in range(n)]
    print(f'table @0x{o:06x}: {n} entries, sum(lens)=0x{sum(lens):x}, '
          f'first lens {[hex(l) for l in lens[:6]]}')
json.dump(tables, open('/home/z/my-project/scripts/s34_t1_tables.json', 'w'))
