#!/usr/bin/env python3
"""S41 T3: MC_MAX_DISTANCE — tail-merge check, sibling strings, registry
structure, and exhaustive refs (pool words, LDR-literal, MOVW/MOVT).
Positive control: FACE_HOSTAGE (registered; has registry table entries)."""
import struct, sys
import capstone
from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', d, o)[:6]
    if t == 1 and fs > 0: segs.append((va, off, fs, ms))

def v2o(va):
    for v, o, s, m in segs:
        if v <= va < v + s: return o + (va - v)
    return None

def o2v(o):
    for v, oo, s, m in segs:
        if oo <= o < oo + s: return v + (o - oo)
    return None

LOAD_MAX = max(v + s for v, o, s, m in segs)

# ---- 1. every occurrence of the name; tail-merge classification ----
name = b'MC_MAX_DISTANCE'
occs = []
p = 0
while True:
    i = d.find(name, p)
    if i < 0 or i > LOAD_MAX: break
    va = o2v(i)
    prev = d[i-1:i]
    nxt = d[i+len(name):i+len(name)+1]
    kind = 'exact' if prev == b'\x00' else 'embedded'
    occs.append((va, kind, i))
    p = i + 1
print(f'occurrences of MC_MAX_DISTANCE in loaded image: {len(occs)}')
for va, kind, i in occs:
    ctx = d[max(0, i-40):i+len(name)+40]
    print(f'  {va:#x} [{kind}] prev={prev!r} next={nxt!r}')
    print(f'    context: {ctx!r}'[:180])

# ---- 2. sibling strings around 0xb30948 ----
def cstrings_around(va, span=0x200):
    o = v2o(va) - span
    out = []
    cur = b''
    start = None
    for k in range(span * 2):
        c = d[o + k]
        if 0x20 <= c < 0x7f:
            if not cur: start = o + k
            cur += bytes([c])
        else:
            if len(cur) >= 4:
                out.append((o2v(start), cur.decode('latin1')))
            cur = b''
    return out

print('\nstrings near 0xb30948 (+-0x200):')
for v, s in cstrings_around(0xb30948):
    mark = ' <<<' if v == 0xb30948 else ''
    print(f'  {v:#x}: {s[:60]!r}{mark}')

# ---- 3. FACE registry structure @0xc0b018 ----
print('\nregistry words 0xc0b000..0xc0b0c0:')
base = v2o(0xc0b000)
for k in range(0, 0xc0, 4):
    w = struct.unpack_from('<I', d, base + k)[0]
    va = 0xc0b000 + k
    note = ''
    if 0xb000000 <= w < 0xc200000:
        so = v2o(w)
        if so is not None:
            s = d[so:d.index(b'\0', so)][:24] if b'\0' in d[so:so+64] else d[so:so+24]
            note = f' -> {s!r}'
    print(f'  {va:#x}: {w:#010x}{note}')

# ---- 4. exhaustive refs to every occurrence (+ positive control) ----
def refs_to(va):
    """(pool words, LDR-literal sites, movw/movt sites) for target address va."""
    pword = struct.pack('<I', va)
    pools = []
    o = 0
    while True:
        i = d.find(pword, o)
        if i < 0 or i > LOAD_MAX: break
        v = o2v(i)
        if v is not None: pools.append(v)
        o = i + 1
    # Thumb LDR-literal sites loading a pool at va
    ldr = []
    for (sv, so, s, m) in segs:
        hw = struct.unpack_from('<%dH' % ((s // 2)), d, so)
        for k in range(len(hw)):
            h = hw[k]
            if 0x4800 <= h <= 0x4F7F:
                imm = (h & 0xff) * 4
                pc = sv + k * 2 + 4
                if (pc & ~3) + imm == va:
                    ldr.append(sv + k * 2)
    # MOVW/MOVT pairs building va
    def t32imm(h1, h2):
        return ((h1 & 0xF) << 12) | (((h1 >> 10) & 1) << 11) | (((h1 >> 4) & 0x7) << 8) | \
               (((h2 & 0x700) << 4)) | (h2 & 0xFF)
    mov = []
    for (sv, so, s, m) in segs:
        hw = struct.unpack_from('<%dH' % (s // 2), d, so)
        n = len(hw)
        for k in range(n - 6):
            h1 = hw[k]
            if (h1 & 0xFBF0) != 0xF240: continue
            lo = t32imm(h1, h1)
            if lo != (va & 0xFFFF): continue
            for step in (2, 4, 6):
                if k + step >= n: break
                h2 = hw[k + step]
                if (h2 & 0xFBF0) == 0xF2C0 and t32imm(h2, h2) == (va >> 16) & 0xFFFF:
                    mov.append((sv + k * 2, sv + (k + step) * 2))
    return pools, ldr, mov

targets = {va: kind for (va, kind, i) in occs}
for ctl in (0xb42c6c,):  # FACE_HOSTAGE string
    targets[ctl] = 'CONTROL:FACE_HOSTAGE'
for va, kind in sorted(targets.items()):
    pools, ldr, mov = refs_to(va)
    print(f'refs to {va:#x} [{kind}]: pool_words={len(pools)} ldr_lit={len(ldr)} movwt={len(mov)}')
    if pools: print('   pools:', [hex(x) for x in pools[:6]])
    if ldr: print('   ldr:', [hex(x) for x in ldr[:6]])
    if mov: print('   movwt:', [(hex(a), hex(b)) for a, b in mov[:4]])
