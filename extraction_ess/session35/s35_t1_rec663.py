#!/usr/bin/env python3
"""S35 T1a12: parse the TRUE 663-record segment directory @0xccfc
[start][end][0][0][tablePtr][dist][0]; verify chain; decode ch0 time extent
of every segment; correlate with clip windows."""
import struct, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

SEG_CNT_OFF = 0xccf4
cnt = u32a(SEG_CNT_OFF)
arr = u32a(SEG_CNT_OFF + 4)
print(f'segment container: count={cnt} array=0x{arr:x} (expect 663, 0xccfc)')

recs = []
for k in range(cnt):
    o = arr + k * 0x1c
    f = [u32a(o + 4 * j) for j in range(7)]
    recs.append(f)

chain_ok = sum(1 for k in range(cnt - 1) if recs[k][1] == recs[k + 1][0])
print(f'chain rec[k].end == rec[k+1].start: {chain_ok}/{cnt - 1}')
print(f'span: {recs[0][0]}..{recs[-1][1]}  (packed timeline)')
print('first 8:', [(f[0], f[1], hex(f[4]), f[5]) for f in recs[:8]])

# decode ch0 (time stream) extent per segment: table = nent x (off,len);
# data base = table + nent*8 + pad? r24 rule: data = seg_base + cumsum(len)
# seg_base = tablePtr + nent*8 (data right after table)
def ch0_extent(table, dist):
    pairs = []
    k = 0
    while k < 220:
        off, ln = u32a(table + 8 * k), u32a(table + 8 * k + 4)
        if ln == 0 or ln > 0x4000 or ln % 4 or off > 0x30000: break
        pairs.append((off, ln)); k += 1
    ne = len(pairs)
    if ne == 0: return None
    base = table + ne * 8
    for extra in (0, 4, 8, 12, 16, 20):
        p = base + extra
        ln0 = pairs[0][1]
        if p + ln0 > N: continue
        w = [u32a(p + 4 * j) for j in range(ln0 // 4)]
        if len(w) >= 2 and all(w[i] < w[i + 1] for i in range(len(w) - 1)) and w[-1] < 2_000_000:
            return w[0], w[-1], len(w), ne, extra
    return None

rows = []
for k in range(cnt):
    f = recs[k]
    e = ch0_extent(f[4], f[5])
    if e is None:
        rows.append((k, f[0], f[1], None, None, None, f[4], f[5]))
    else:
        t0, t1, nk, ne, extra = e
        rows.append((k, f[0], f[1], t0, t1, nk, f[4], f[5]))

ok = [r for r in rows if r[3] is not None]
print(f'\nch0 decoded: {len(ok)}/{cnt}')
bleed0 = [r[3] - r[1] for r in ok]
bleed1 = [r[4] - r[2] for r in ok]
import collections
print(f'bleed start (t0 - segStart): median {sorted(bleed0)[len(bleed0)//2]}, min {min(bleed0)}, max {max(bleed0)}')
print(f'bleed end   (t1 - segEnd):   median {sorted(bleed1)[len(bleed1)//2]}, min {min(bleed1)}, max {max(bleed1)}')
exact = sum(1 for r in ok if r[3] == r[1] and r[4] == r[2])
print(f'exact [t0==start and t1==end]: {exact}/{len(ok)}')

print('\nsample rows (seg, [start,end], ch0 [t0,t1], nkeys, nent):')
for r in rows[:10] + rows[630:663][:10]:
    print(f'  seg{r[0]:3d} [{r[1]:7d}..{r[2]:7d}] ch0 [{r[3] if r[3] else "??"}..{r[4] if r[4] else "??"}] nk={r[5]} tbl=0x{r[6]:x}')

json.dump({'count': cnt, 'array': arr,
           'recs': recs,
           'ch0': [{'k': r[0], 'start': r[1], 'end': r[2], 't0': r[3], 't1': r[4], 'nk': r[5], 'tbl': r[6], 'dist': r[7]} for r in rows]},
          open('/home/z/my-project/scripts/s35_t1_segs663.json', 'w'))
print('\nsaved s35_t1_segs663.json')
