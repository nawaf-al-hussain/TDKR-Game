#!/usr/bin/env python3
"""S35 T1a16: dump idle stream table @0x53200 header + first entries;
resolve nent vs data base (0x536e4 per r23/r24)."""
import struct

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]

TBL = 0x53200
print('idle table raw (first 12 + last 6 entries of 157):')
for k in range(12):
    off, ln = u32a(TBL + 8 * k), u32a(TBL + 8 * k + 4)
    print(f'  [{k:3d}] off={off:6d} len={ln:6d}')
print('  ...')
for k in range(150, 158):
    off, ln = u32a(TBL + 8 * k), u32a(TBL + 8 * k + 4)
    print(f'  [{k:3d}] off={off:6d} len={ln:6d}  (@0x{TBL+8*k:x})')

# cumsum check against known base 0x536e4
base = 0x536e4
print(f'\nbase-table = 0x{base - TBL:x} = {base - TBL} bytes = {156*8}+4 = {157*8 - 12}')
cs = 0
for k in range(157):
    ln = u32a(TBL + 8 * k + 4)
    if k < 6 or k > 153:
        p = base + cs
        print(f'  k={k:3d} len={ln:5d} cumsum={cs:6d} -> file 0x{p:x}')
    cs += ln
print(f'total len sum = {cs}; table+dist = 0x{TBL + 65364:x} (next table 0x63154)')

# hypothesis: entry0 is a HEADER (nent=156?) and streams start at entry1
h0, h1 = u32a(TBL), u32a(TBL + 4)
print(f'\nentry0 = ({h0}, {h1})  -- if h0==156 or 157 it is a count header')
# check where the first TIME stream (ascending u32s) sits under different bases
for ne in (155, 156, 157):
    b = TBL + ne * 8
    ln0 = u32a(TBL + 8 * 0 + 4)
    w = [u32a(b + 4 * j) for j in range(min(ln0 // 4, 10))]
    asc = all(w[i] < w[i + 1] for i in range(len(w) - 1))
    print(f'  base=TBL+{ne}*8=0x{b:x}: first stream head {w[:6]} asc={asc}')

# run table 0xb2818
T2 = 0xb2818
print(f'\nrun table @0x{T2:x} first 8 entries:')
for k in range(8):
    off, ln = u32a(T2 + 8 * k), u32a(T2 + 8 * k + 4)
    print(f'  [{k}] off={off:6d} len={ln:6d}')
print(f'  run rec: start=13933 end=15566 dist=65400; blob end = 0x{T2+65400:x} (next tbl 0xc2790)')
