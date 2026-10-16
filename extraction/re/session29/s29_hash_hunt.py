#!/usr/bin/env python3
"""Session 29 T1: find the engine class-id hash from known (name -> tid) pairs."""
import zlib, itertools, json, sys

KNOWN = [
    (b"CComponentLevelInit", 0x2657),
    (b"CCinematicComponent", 0x17AC851F),
    (b"CDummyComponent", 0x10FF796),
    # from round16/17 commit: waypoint class 0x798f, zone 0x2651, trigger Lua 0x2ee3/0x264b
]

# ---- hash candidates (32-bit) ----
def crc32(b): return zlib.crc32(b) & 0xFFFFFFFF
def crc32_noxor(b): return zlib.crc32(b) ^ 0xFFFFFFFF
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
        h = (h + c) & 0xFFFFFFFF
        h = (h + (h << 10)) & 0xFFFFFFFF
        h ^= h >> 6
    h = (h + (h << 3)) & 0xFFFFFFFF
    h ^= h >> 11
    h = (h + (h << 15)) & 0xFFFFFFFF
    return h
def java31(b):
    h = 0
    for c in b: h = (h * 31 + c) & 0xFFFFFFFF
    return h
def elf(b):
    h = 0
    for c in b:
        h = (h << 4) + c
        g = h & 0xF0000000
        if g: h ^= g >> 24
        h &= ~g & 0xFFFFFFFF
    return h
def murmur2(b, seed=0):
    m, r = 0x5BD1E995, 24
    h = (seed ^ len(b)) & 0xFFFFFFFF
    i = 0
    while len(b) - i >= 4:
        k = int.from_bytes(b[i:i+4], 'little'); i += 4
        k = (k * m) & 0xFFFFFFFF; k ^= k >> r; k = (k * m) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF; h ^= k
    rem = len(b) - i
    if rem == 3: h ^= b[i+2] << 16
    if rem >= 2: h ^= b[i+1] << 8
    if rem >= 1:
        h ^= b[i]; h = (h * m) & 0xFFFFFFFF
    h ^= h >> 13; h = (h * m) & 0xFFFFFFFF; h ^= h >> 15
    return h
def murmur3(b, seed=0):
    c1, c2 = 0xCC9E2D51, 0x1B873593
    h = seed; n = len(b) - (len(b) % 4)
    for i in range(0, n, 4):
        k = int.from_bytes(b[i:i+4], 'little')
        k = (k * c1) & 0xFFFFFFFF; k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF; k = (k * c2) & 0xFFFFFFFF
        h ^= k; h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 5 + 0xE6546B64) & 0xFFFFFFFF
    k = 0; rem = b[n:]
    if len(rem) >= 3: k ^= rem[2] << 16
    if len(rem) >= 2: k ^= rem[1] << 8
    if len(rem) >= 1:
        k ^= rem[0]; k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF; k = (k * c2) & 0xFFFFFFFF
        h ^= k
    h ^= len(b)
    h ^= h >> 16; h = (h * 0x85EBCA6B) & 0xFFFFFFFF; h ^= h >> 13
    h = (h * 0xC2B2AE35) & 0xFFFFFFFF; h ^= h >> 16
    return h
def rs_hash(b):
    a, b_ = 63689, 378551
    h = 0
    for c in b:
        h = (h * a + c) & 0xFFFFFFFF; a = (a * b_) & 0xFFFFFFFF
    return h
def bkdr(b):
    h = 0
    for c in b: h = (h * 131 + c) & 0xFFFFFFFF
    return h

HASHES = {n: f for n, f in list(globals().items()) if callable(f) and not n.startswith('_') and n not in ('json','itertools','zlib','sys')}

# byte variants
def variants(name):
    yield name
    yield name + b'\x00'
    yield name.upper()
    yield name.upper() + b'\x00'
    yield name.lower()
    yield name.lower() + b'\x00'
    yield b'class ' + name
    yield b'4' + name   # mangled length? no - lengths differ; keep simple mangle: len prefix
    yield str(len(name)).encode() + name
    yield name[::-1]

VAR_NAMES = ['raw','nul','upper','upper+nul','lower','lower+nul']
results = []
for hname, hf in HASHES.items():
    for vi, vname in enumerate(VAR_NAMES):
        ok = 0; tot = 0; details=[]
        for name, want in KNOWN:
            got = hf(list(variants(name))[vi])
            tot += 1
            if got == want:
                ok += 1; details.append(f"{name.decode()}={got:#x}")
        if ok:
            results.append((ok, tot, hname, vname, details))
results.sort(reverse=True)
for ok, tot, hname, vname, det in results:
    print(f"{ok}/{tot} {hname:10s} {vname:10s} {det}")
if not results:
    print("no candidate matched; printing per-hash outputs for CCinematicComponent for eyeballing:")
    want = 0x17AC851F
    for hname, hf in HASHES.items():
        for vi, vn in enumerate(['raw','nul','upper','upper+nul','lower','lower+nul']):
            v = list(variants(b"CCinematicComponent"))[vi]
            got = hf(v)
            mark = " <== MATCH" if got == want else ""
            if abs(got - want) < 0x1000000 or mark:  # near misses too
                print(f"  {hname:10s} {vn:10s} {got:#010x}{mark}")
