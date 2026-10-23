#!/usr/bin/env python3
"""s54 T1 step 16: dump the named glide/grapnel static constants from .data."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))
        print('seg vaddr=%#x offset=%#x filesz=%#x' % (p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

def f(v):
    return struct.unpack_from('<f', data, v2o(v))[0]

def raw(v):
    return struct.unpack_from('<I', data, v2o(v))[0]

print('\nCActorBaseComponent named statics:')
for a, n in ((0xc0abc0, 'k_glideWallEvadeDistance'),
             (0xc0abc4, 'k_glideWallEvadeMinDistance'),
             (0xc0abc8, 'k_glideWallEvadeMaxAngle'),
             (0xc0abcc, 's_fallAheadOffset')):
    print('  %-30s @%#x = %g' % (n, a, f(a)))

print('\nCLevel s_glide family (0xc17d5c..0xc17d84):')
names = {0xc17d5c: 's_glidePitchMin', 0xc17d60: 's_glidePitchMax',
         0xc17d64: 's_glideRollMax', 0xc17d68: 's_glideDeltaYawMax',
         0xc17d6c: 's_glideYawCoef', 0xc17d70: 's_glidePitchCoef',
         0xc17d74: 's_glideRollCoef', 0xc17d78: 's_glidePitchAutoLevelingCoef',
         0xc17d7c: 's_glideRollAutoLevelingCoef', 0xc17d80: 's_glideDeadAngle'}
for a in sorted(names):
    print('  %-30s @%#x = %g' % (names[a], a, f(a)))

print('\nraw context 0xc17d40..0xc17d9c:')
for a in range(0xc17d40, 0xc17d9c, 4):
    print('  %#x: %g' % (a, f(a)))
