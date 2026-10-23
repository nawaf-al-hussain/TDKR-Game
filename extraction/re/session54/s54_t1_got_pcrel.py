#!/usr/bin/env python3
"""s54 T1 step 22: find PC-relative references to the s_glide GOT slots.
For each pool word L at P in .text: target = P + 8 + L; if target is a GOT slot
(0xc080c8..0xc080ec) the code near P loads that static. Dump the code sites."""
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

TEXT = (0xa5d80, 0xac2190)
hits = []
for P in range(TEXT[0], TEXT[1], 4):
    L = struct.unpack_from('<i', data, v2o(P))[0]  # signed offset
    tgt = P + 8 + L
    if tgt in GOT_SLOTS:
        hits.append((P, tgt))

print('pc-rel refs to s_glide GOT slots:')
func_hits = {}
for P, tgt in hits:
    fn = sym_of(P)
    func_hits.setdefault(fn, []).append((hex(P), GOT_SLOTS[tgt]))
    print('  pool@%#x -> %s in %s' % (P, GOT_SLOTS[tgt], fn))

print('\nfunctions using the s_glide statics:')
for fn, lst in func_hits.items():
    print(' ', fn, lst)
