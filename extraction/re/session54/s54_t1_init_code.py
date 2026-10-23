#!/usr/bin/env python3
"""s54 T1 step 20: find code referencing the GOT slots of the .bss s_glide*
statics (pool words 0xc080c8..0xc080ec) and disassemble the init/update paths
to read the stored values."""
import struct
import subprocess
import bisect

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3:
        try:
            a = int(pr[0], 16)
        except ValueError:
            continue
        syms.append((a, pr[2]))
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(
    ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
     's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
     's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle'])}

# scan whole file for literal words equal to the GOT slot addresses
refs = {}
for slot in GOT_SLOTS:
    pat = struct.pack('<I', slot)
    idx = 0
    while True:
        i = data.find(pat, idx, 0xbbe000)
        if i < 0:
            break
        refs.setdefault(slot, []).append(i)
        idx = i + 1
for slot, hs in refs.items():
    for h in hs:
        print('GOT slot %#x (%s) referenced from pool @%#x in %s'
              % (slot, GOT_SLOTS[slot], h, sym_of(h)))

# .init_array members (static ctors)
ia_off, ia_size = 0xbcd430, 0xd8
print('\n.init_array members:')
for k in range(0, ia_size, 4):
    a = struct.unpack_from('<I', data, ia_off + k)[0]
    print('  %#x %s' % (a, sym_of(a)))
