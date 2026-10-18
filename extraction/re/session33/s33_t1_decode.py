#!/usr/bin/env python3
"""S33 T1: decode _001_idle_stand via contiguous walk, verify stream shapes,
then FK-pose the T2 skeleton at two times and run the plausibility battery."""
import struct, math, json, collections
import numpy as np

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try: return d[v:e].decode('latin1')
            except Exception: pass

# ---- channel names in table order (78 named groups) ----
names = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if not (w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr(w[2]))
    o += 32

pairs = [(u32(0x53200 + 8 * k), u32(0x53200 + 8 * k + 4)) for k in range(156)]

# ---- contiguous walk from 0x536e8 ----
DATA0 = 0x536e8
pos = DATA0
streams = []   # (kind, offset, len, name, ch_idx)
ok_t = bad_t = ok_q = bad_q = ok_v = bad_v = 0
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else '?'
    is_time = (k % 2 == 0)
    # alignment: data must be 4-aligned; try pad 0 then 4
    placed = None
    for pad in (0, 4, 8):
        p = pos + pad
        if p % 4: continue
        if p + ln > len(d): continue
        if ln == 0:
            placed = p; break
        if is_time:
            w = [u32(p + 4 * j) for j in range(ln // 4)]
            if all(w[i] < w[i + 1] for i in range(len(w) - 1)) and w[-1] < 2_000_000:
                placed = p; break
        else:
            if ln % 16 == 0 and ln >= 0x20:
                q = [abs(math.sqrt(sum(f32(p + 16 * i + 4 * c) ** 2 for c in range(4))) - 1)
                     for i in range(min(4, ln // 16))]
                if max(q) < 5e-3: placed = p; break
            elif ln % 12 == 0:
                v = [f32(p + 4 * j) for j in range(min(6, ln // 4))]
                if all(abs(x) < 100 and math.isfinite(x) for x in v):
                    placed = p; break
            else:
                placed = p; break
    if placed is None: placed = pos
    pad_used = placed - pos
    if is_time and ln >= 8:
        w = [u32(placed + 4 * j) for j in range(ln // 4)]
        asc = all(w[i] < w[i + 1] for i in range(len(w) - 1))
        ok_t += asc; bad_t += not asc
    if (not is_time) and ln % 16 == 0 and ln >= 0x20:
        nrm = [math.sqrt(sum(f32(placed + 16 * i + 4 * c) ** 2 for c in range(4)))
               for i in range(ln // 16)]
        good = sum(1 for x in nrm if abs(x - 1) < 5e-3)
        ok_q += good >= len(nrm) - 1; bad_q += good < len(nrm) - 1
    if (not is_time) and ln % 12 == 0 and ln % 16:
        v = [f32(placed + 4 * j) for j in range(ln // 4)]
        good = all(abs(x) < 100 and math.isfinite(x) for x in v)
        ok_v += good; bad_v += not good
    streams.append((is_time, placed, ln, nm, pad_used))
    pos = placed + ln

print(f'walk consumed 0x{pos - DATA0:x} B; end 0x{pos:x}')
print(f'TIME arrays ascending: {ok_t}/{ok_t + bad_t}')
print(f'QUAT arrays unit:      {ok_q}/{ok_q + bad_q}')
print(f'VEC3 arrays finite:    {ok_v}/{ok_v + bad_v}')
print(f'pads used: {collections.Counter(s[4] for s in streams)}')
print('first 16 streams:')
for is_time, p, ln, nm, pad in streams[:16]:
    print(f'  {"T" if is_time else "V"} @0x{p:06x} len 0x{ln:<5x} pad{pad} {nm}')

# store decoded streams
out = []
for is_time, p, ln, nm, pad in streams:
    out.append(dict(kind='T' if is_time else 'V', off=p, len=ln, name=nm))
json.dump(dict(data0=DATA0, table=0x53200, streams=out,
               checks=dict(time=f'{ok_t}/{ok_t+bad_t}', quat=f'{ok_q}/{ok_q+bad_q}',
                           vec3=f'{ok_v}/{ok_v+bad_v}')),
          open('/tmp/my-project/scripts/s33_t1_streams.json', 'w'), indent=1)
