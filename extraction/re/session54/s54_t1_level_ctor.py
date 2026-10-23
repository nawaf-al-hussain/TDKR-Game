#!/usr/bin/env python3
"""s54 T1 step 21: disassemble CLevel.cpp's static initializer @0x488af4
(writes s_glidePitchMin etc.) and dump every float stored to the .bss GOT slots."""
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

GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(
    ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
     's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
     's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle'])}

start = 0x488af4
# function length: until pop {pc}; give generous window
off = v2o(start)
print('=== CLevel static-init @%#x ===' % start)
writes = []
for ins in md.disasm(data[off:off + 0x600], start):
    note = ''
    if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
            base = (ins.address + 8) & ~3
            val = struct.unpack_from('<I', data, v2o(base + imm))[0]
            fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
            if val in GOT_SLOTS:
                note = '   ; GOT %s' % GOT_SLOTS[val]
            else:
                note = '   ; =%#x' % val
                if 0x2f000000 < val < 0x50000000:
                    note += ' (float %g)' % fv
                elif val == 0:
                    note += ' (float 0)'
        except Exception:
            pass
    print('%08x %-8s %-34s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
    if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
        break
