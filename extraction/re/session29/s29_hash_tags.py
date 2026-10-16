#!/usr/bin/env python3
"""S29 T1: hash the short registration tags; scan .text for hash constants."""
import struct, zlib
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

# reuse hash defs
import importlib.util
spec = importlib.util.spec_from_file_location('hh', '/home/z/my-project/scripts/s29_hash_hunt.py')
# can't import (it runs main); inline the hashes instead
def crc32(b): return zlib.crc32(b) & 0xFFFFFFFF
def fnv1(b):
    h = 0x811C9DC5
    for c in b: h = (h * 0x01000193) & 0xFFFFFFFF; h ^= c
    return h
def fnv1a(b):
    h = 0x811C9DC5
    for c in b: h ^= c; h = (h * 0x01000193) & 0xFFFFFFFF
    return h
def djb2(b):
    h = 5381
    for c in b: h = (h * 33 + c) & 0xFFFFFFFF
    return h
def djb2x(b):
    h = 5381
    for c in b: h = ((h * 33) ^ c) & 0xFFFFFFFF
    return h
def sdbm(b):
    h = 0
    for c in b: h = (c + (h << 6) + (h << 16) - h) & 0xFFFFFFFF
    return h
def joaat(b):
    h = 0
    for c in b:
        h = (h + c) & 0xFFFFFFFF; h = (h + (h << 10)) & 0xFFFFFFFF; h ^= h >> 6
    h = (h + (h << 3)) & 0xFFFFFFFF; h ^= h >> 11; h = (h + (h << 15)) & 0xFFFFFFFF
    return h
def murmur2(b, seed=0):
    m, r = 0x5BD1E995, 24
    h = (seed ^ len(b)) & 0xFFFFFFFF; i = 0
    while len(b) - i >= 4:
        k = int.from_bytes(b[i:i+4], 'little'); i += 4
        k = (k * m) & 0xFFFFFFFF; k ^= k >> r; k = (k * m) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF; h ^= k
    rem = len(b) - i
    if rem == 3: h ^= b[i+2] << 16
    if rem >= 2: h ^= b[i+1] << 8
    if rem >= 1: h ^= b[i]; h = (h * m) & 0xFFFFFFFF
    h ^= h >> 13; h = (h * m) & 0xFFFFFFFF; h ^= h >> 15
    return h

TESTS = [
    (b'Cinematic', 0x17AC851F), (b'Trigger', None), (b'CinematicComponent', 0x17AC851F),
    (b'CCinematicComponent', 0x17AC851F), (b'CDummyComponent', 0x10FF796),
    (b'DummyComponent', 0x10FF796), (b'ComponentLevelInit', 0x2657),
    (b'CComponentLevelInit', 0x2657), (b'CollisionComponent', None), (b'TrafficSetting', None),
]
HFN = {'crc32': crc32, 'fnv1': fnv1, 'fnv1a': fnv1a, 'djb2': djb2, 'djb2x': djb2x, 'sdbm': sdbm, 'joaat': joaat, 'murmur2': murmur2}
VAR = {'raw': lambda s: s, 'nul': lambda s: s + b'\0', 'upper': lambda s: s.upper(), 'uppernul': lambda s: s.upper() + b'\0', 'lower': lambda s: s.lower()}
print('== hash tests on tags/class names ==')
best = []
for hn, hf in HFN.items():
    for vn, vf in VAR.items():
        ok = []
        for s, want in TESTS:
            if want is None: continue
            if hf(vf(s)) == want: ok.append(s.decode())
        if ok: best.append((len(ok), hn, vn, ok))
for n, hn, vn, ok in sorted(best, reverse=True): print(f'  {n} {hn} {vn} {ok}')
if not best: print('  (none matched)')

# scan .text for hash constants (ARM or Thumb, little-endian words + Thumb2 MOVW pairs)
CONSTS = {0x01000193: 'FNV prime', 0x811C9DC5: 'FNV offset', 0x5BD1E995: 'murmur2 m', 0xCC9E2D51: 'murmur3 c1',
          0xE6546B64: 'murmur3 c2', 0x85EBCA6B: 'murmur3 fmix1', 0xC2B2AE35: 'murmur3 fmix2', 0x9E3779B9: 'teapot/jenkins',
          0x0001003F: '?', 0x00000021: 'mul33'}
print('== .text constant scan ==')
for i in range(0xa5d80, 0xac2490 - 4, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if w in CONSTS and w > 0x1000:
        print(f'  {i:#x}: {CONSTS[w]} ({w:#x})')
# Thumb2 MOVW-based constants: scan for MOVW+MOVT pairs forming the consts
pairs = {}
for i in range(0xa5d80, 0xac2490 - 4, 2):
    hw = struct.unpack_from('<H', data, i)[0]
    # MOVW T3: hw1 0xF240-0xF2 3F with bits: 11110 i 10 0100 imm4
    if (hw & 0xFBF0) == 0xF240:
        hw2 = struct.unpack_from('<H', data, i + 2)[0]
        if not (hw2 & 0x8000):
            imm4 = hw & 0xF; i_bit = (hw >> 10) & 1
            imm3 = (hw2 >> 12) & 7; imm8 = hw2 & 0xFF
            v16 = (i_bit << 15) | (imm4 << 12) | (imm3 << 8) | imm8
            rd = (hw2 >> 8) & 0xF
            pairs.setdefault(rd, []).append((i, v16, 'W'))
    elif (hw & 0xFBF0) == 0xF2C0:  # MOVT
        hw2 = struct.unpack_from('<H', data, i + 2)[0]
        if not (hw2 & 0x8000):
            imm4 = hw & 0xF; i_bit = (hw >> 10) & 1
            imm3 = (hw2 >> 12) & 7; imm8 = hw2 & 0xFF
            v16 = (i_bit << 15) | (imm4 << 12) | (imm3 << 8) | imm8
            rd = (hw2 >> 8) & 0xF
            pairs.setdefault(rd, []).append((i, v16, 'T'))
print('== Thumb2 MOVW/MOVT formed constants ==')
found = {}
for rd, lst in pairs.items():
    for a, v16, t in lst:
        for b2, v16b, t2 in lst:
            if t == 'W' and t2 == 'T' and b2 > a and b2 - a < 0x20:
                val = (v16b << 16) | v16
                if val in CONSTS and val > 0xFFFF:
                    found.setdefault(val, []).append((hex(a), hex(b2)))
for val, locs in found.items():
    print(f'  {CONSTS[val]} ({val:#x}): {len(locs)} sites {locs[:5]}')
