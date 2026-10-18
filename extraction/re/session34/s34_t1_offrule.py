#!/usr/bin/env python3
"""S34 T1: test whether stream-table 'off' field is the exact placement rule.
Hypotheses: off = absolute offset, off = offset from table, off = cumulative
byte offset from data pool start (contiguous). Compare against r23's walk."""
import struct, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]

TAB = 0x53200
pairs = [(u32a(TAB + 8 * k), u32a(TAB + 8 * k + 4)) for k in range(157)]
print('table @0x53200, 157 entries')

# r23 knowledge: table order names at 0xb53c, 78 channels x (time,value)
names = []
o = 0xb53c
def cstr_a(v):
    if 0 < v < len(ad):
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: pass
while True:
    w = struct.unpack_from('<8I', ad, o)
    if not (w[2] and cstr_a(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr_a(w[2]))
    o += 32
print(f'{len(names)} channel names')

print('\nfirst 16 (off,len):')
for k in range(16):
    print(f'  [{k:3d}] off=0x{pairs[k][0]:06x} len=0x{pairs[k][1]:06x}  {names[k//2] if k//2 < len(names) else "?"}')

offs = [p[0] for p in pairs]
lens = [p[1] for p in pairs]
print(f'\noff range: 0x{min(offs):x} .. 0x{max(offs):x}')
print(f'len sum: 0x{sum(lens):x}, nonzero lens: {sum(1 for l in lens if l)}')

# H1: off is absolute file offset
h1 = sum(1 for o_, l_ in pairs if l_ and 0 < o_ < len(ad))
print(f'H1 abs-offset: {h1}/{sum(1 for l in lens if l)} in-file-range')

# H2: off = cumulative offset from data pool start
# r23: data contiguous from 0x536e4; test base candidates
cum = np.cumsum([0] + lens[:-1])
for base in (0x536e4, TAB + 157 * 8, 0x53200):
    hit = sum(1 for k, (o_, l_) in enumerate(pairs)
              if l_ and o_ == base + int(cum[k]))
    print(f'H2 base 0x{base:x}: {hit} exact cumulative hits')

# H3: off = cumulative from pool start where pool start unknown: solve base = off[0]-0 if first len nonzero...
# H4: check monotonic + delta(off_k, off_{k+1}) == len_k (strictly contiguous, no pad in offsets)
d_ok = 0; d_tot = 0
for k in range(len(pairs) - 1):
    if lens[k] and pairs[k+1][0] and pairs[k][0]:
        d_tot += 1
        if pairs[k+1][0] - pairs[k][0] == lens[k]: d_ok += 1
print(f'H4 delta(off)==len: {d_ok}/{d_tot}')

# If H4 fails, off may include pad. Also test delta==padded len (pad to 4)
d_ok4 = 0
for k in range(len(pairs) - 1):
    if lens[k] and pairs[k+1][0] and pairs[k][0]:
        if pairs[k+1][0] - pairs[k][0] == (lens[k] + 3) & ~3: d_ok4 += 1
print(f'H4b delta==pad4(len): {d_ok4}/{d_tot}')

# what does off look like for zero-len entries?
zl = [(k, pairs[k]) for k in range(len(pairs)) if not lens[k]]
print(f'zero-len entries: {len(zl)}, first offs: {[hex(p[0]) for _, p in zl[:8]]}')

# save for next step
json.dump(dict(names=names, pairs=pairs),
          open('/home/z/my-project/scripts/s34_t1_pairs.json', 'w'))
print('\nwrote s34_t1_pairs.json')
