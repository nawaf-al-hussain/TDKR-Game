#!/usr/bin/env python3
"""s54 T1 step 19 (fixed): parse .rel.dyn ABS32 relocs targeting glide .bss statics;
dump the .data statics (k_glide*) values."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

def f(v):
    return struct.unpack_from('<f', data, v2o(v))[0]

print('.data statics (CActorBaseComponent k_glide*):')
for a, n in ((0xc0abc0, 'k_glideWallEvadeDistance'),
             (0xc0abc4, 'k_glideWallEvadeMinDistance'),
             (0xc0abc8, 'k_glideWallEvadeMaxAngle'),
             (0xc0abcc, 's_fallAheadOffset')):
    print('  %-30s @%#x = %g' % (n, a, f(a)))

# .rel.dyn
rel_off, rel_size = 0x351fc, 0x6f118
TARGETS = {0xc17d5c: 's_glidePitchMin', 0xc17d60: 's_glidePitchMax',
           0xc17d64: 's_glideRollMax', 0xc17d68: 's_glideDeltaYawMax',
           0xc17d6c: 's_glideYawCoef', 0xc17d70: 's_glidePitchCoef',
           0xc17d74: 's_glideRollCoef', 0xc17d78: 's_glidePitchAutoLevelingCoef',
           0xc17d7c: 's_glideRollAutoLevelingCoef', 0xc17d80: 's_glideDeadAngle',
           0xc0abc0: 'k_glideWallEvadeDistance', 0xc0abc4: 'k_glideWallEvadeMinDistance',
           0xc0abc8: 'k_glideWallEvadeMaxAngle'}
n = rel_size // 8
print('\nscanning %d relocs...' % n)
found = []
types = {}
for k in range(n):
    r_offset, r_info = struct.unpack_from('<II', data, rel_off + 8 * k)
    typ = r_info & 0xff
    types[typ] = types.get(typ, 0) + 1
    if typ in (1, 2, 6):  # ABS32/GLOB_DAT variants
        o = v2o(r_offset)
        if o is None:
            continue
        addend = struct.unpack_from('<I', data, o)[0]
        if addend in TARGETS:
            found.append((r_offset, typ, addend))
print('reloc type census:', types)
print('\nrelocs whose addend == a glide static:')
for ro, typ, ad in found:
    print('  reloc @%#x type=%d addend=%#x %s' % (ro, typ, ad, TARGETS[ad]))

# also scan .got directly
got_off, got_addr, got_size = 0xc06b58, 0xc07b58, 0x14a8
print('\n.got slots holding glide static addends:')
for k in range(0, got_size, 4):
    v = struct.unpack_from('<I', data, got_off + k)[0]
    if v in TARGETS:
        print('  got %#x -> %s' % (got_addr + k, TARGETS[v]))
