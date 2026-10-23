#!/usr/bin/env python3
"""s54 T1 step 25: disassemble the ACTUAL glide physics functions and extract
float constants (the CComponentGlide path is dead; these are the real params).
Functions: StartGlide(0x380590), StartGlideFromGrapnel(0x380a0c),
CanEnterGlide(0x380cbc), ExitGlide(0x380d10), PrepareForJumpGlide(0x380d9c),
SetInitialGlideAngle(0x380e34), RefreshForcesGlide(0x3836b0),
RefreshForcesFallGrapnel(0x383a08), GetGlideAttackLandOffset(0x374040)."""
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

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

FUNCS = [
    ('StartGlide', 0x380590, 0x3809c0),
    ('StartGlideFromGrapnel', 0x380a0c, 0x380cbc),
    ('CanEnterGlide', 0x380cbc, 0x380d10),
    ('ExitGlide', 0x380d10, 0x380d9c),
    ('PrepareForJumpGlide', 0x380d9c, 0x380e34),
    ('SetInitialGlideAngle', 0x380e34, 0x380e94),
    ('RefreshForcesGlide', 0x3836b0, 0x383a08),
    ('RefreshForcesFallGrapnel', 0x383a08, 0x383ab0),
]

import math
for name, lo, hi in FUNCS:
    print('\n=== %s (%#x..%#x, %d B) ===' % (name, lo, hi, hi - lo))
    off = v2o(lo)
    for ins in md.disasm(data[off:off + (hi - lo)], lo):
        note = ''
        if ins.mnemonic in ('bl', 'blx') and 'r' not in ins.op_str[:1]:
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                note = '   ; -> %s' % sym_of(t)
            except ValueError:
                pass
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
                note = '   ; =%#x' % val
                if val < 0x10000:
                    note += ' (int %d)' % val
                elif 0x2f000000 < val < 0x50000000:
                    note += ' (float %g)' % fv
            except Exception:
                pass
        print('%08x %-8s %-34s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
