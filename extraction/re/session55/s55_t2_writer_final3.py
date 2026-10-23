#!/usr/bin/env python3
"""s55 T2 final-3: full section map; decoder sanity check on k_glideWallEvadeDistance;
real search for s_glide* references; dump 0xd0d668 table."""
import struct, subprocess, bisect

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

# full section map
secs = []
out = subprocess.run(['readelf', '-S', '-W', SO], capture_output=True, text=True).stdout
for line in out.splitlines():
    p = line.split()
    if len(p) >= 8 and p[0].startswith('[') and p[2] in ('PROGBITS', 'NOBITS', 'INIT_ARRAY', 'FINI_ARRAY'):
        try:
            addr, off, size = int(p[3], 16), int(p[4], 16), int(p[5], 16)
        except ValueError:
            continue
        secs.append((p[1], addr, off, size, p[2]))
        print('SEC %-18s addr=%#010x off=%#010x size=%#x %s' % (p[1], addr, off, size, p[2]))

def v2o(v):
    for name, addr, off, size, typ in secs:
        if addr and addr <= v < addr + size:
            return off + (v - addr)
    return None

NAMES = ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
         's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
         's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle']
TADDR = {0xc17d5c + 4 * k: n for k, n in enumerate(NAMES)}

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    p = line.split()
    if len(p) == 3 and not p[2].startswith('$'):
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
symmap = dict(syms)
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

def ldr_lit_scan(target_set, label):
    """scan .text for real ldr-literal instructions whose pool word is in target_set"""
    hits = []
    a = 0xa5d80
    end = 0xac2490
    while a < end:
        o = v2o(a)
        if o is None:
            a += 4
            continue
        w = struct.unpack_from('<I', data, o)[0]
        if (w >> 28) == 0xE:
            bits = (w >> 20) & 0xFF
            if (bits & 0x0F) == 0x0F and (bits >> 6) == 0b010110 >> 2:
                Pbit = (bits >> 7) & 1
                Ubit = (bits >> 6) & 1
                if Pbit:
                    imm12 = w & 0xFFF
                    off = imm12 if Ubit else -imm12
                    pool = ((a + 8) & ~3) + off
                    if pool in target_set:
                        hits.append((a, (w >> 12) & 0xF, target_set[pool], pool))
        a += 4
    print('%s: %d ldr-literal hits' % (label, len(hits)))
    return hits

# sanity check 1: k_glideWallEvadeDistance @0xc0abc0 — s54 says glide funcs read it
kw = {0xc0abc0: 'k_glideWallEvadeDistance', 0xc0abc4: 'k_glideWallEvadeMinDistance',
      0xc0abc8: 'k_glideWallEvadeMaxAngle'}
h = ldr_lit_scan(kw, 'SANITY k_glide*')
for a, rd, n, pool in h:
    print('   ldr r%d @%#x pool=%#x in %s' % (rd, a, pool, sym_of(a)))

# sanity check 2: a busy .data symbol — CObjectManager or similar heavily-read table
# use CLevel statics
tg = dict(TADDR)
h2 = ldr_lit_scan(tg, 's_glide* direct (.bss addr in pool)')
for a, rd, n, pool in h2:
    print('   ldr r%d @%#x pool=%#x in %s' % (rd, a, pool, sym_of(a)))

# also: pools containing the .bss addresses (any, not just via ldr scan)
print('\npool words == s_glide* addr anywhere in .text:')
n = 0
for a in range(0xa5d80, 0xac2490, 4):
    o = v2o(a)
    w = struct.unpack_from('<I', data, o)[0]
    if w in TADDR:
        print('   %#x -> %s (in %s)' % (a, TADDR[w], sym_of(a)))
        n += 1
print('   count:', n)

# dump 0xd0d668 table with correct v2o
print('\n0xd0d668 16B-stride table (section: %s):' % [s[0] for s in secs if s[1] and s[1] <= 0xd0d668 < s[1] + s[3]])
for k in range(8):
    ea = 0xd0d668 + 0x10 * k
    o = v2o(ea)
    if o is None:
        print('  entry%d: unmapped' % k)
        continue
    words = [struct.unpack_from('<I', data, o + 4 * j)[0] for j in range(4)]
    strs = []
    for w in words:
        oo = v2o(w)
        if oo:
            e2 = data.find(b'\x00', oo, oo + 64)
            if e2 > oo:
                try:
                    s = data[oo:e2].decode('ascii')
                    if len(s) >= 3 and s.isprintable():
                        strs.append(s)
                except Exception:
                    pass
    symn = [sym_of(w) if sym_of(w) != '<none>' else '' for w in words]
    print('  entry%d @%#x: %s %s strs=%s' % (k, ea, [hex(x) for x in words], symn, strs))

# where do the 0xc070c8 / 0xc080c8 tables live (section names)?
for probe in (0xc070c8, 0xc080c8):
    sect = [s[0] for s in secs if s[1] and s[1] <= probe < s[1] + s[3]]
    print('probe %#x -> section %s' % (probe, sect))
