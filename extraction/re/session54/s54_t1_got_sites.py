#!/usr/bin/env python3
"""s54 T1 step 23: for each pc-rel GOT ref site of the s_glide statics, dump the
surrounding instructions to find stores (init) and reads (physics usage)."""
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

TEXT = (0xa5d80, 0xac2190)
sites = []
for P in range(TEXT[0], TEXT[1], 4):
    L = struct.unpack_from('<i', data, v2o(P))[0]
    tgt = P + 8 + L
    if tgt in GOT_SLOTS:
        sites.append((P, tgt))

def is_store_site(P):
    # look at instructions in [P-0x20, P]: a str of an immediate/float to [rX]
    off = v2o(P - 0x20)
    for ins in md.disasm(data[off:off + 0x20], P - 0x20):
        if ins.mnemonic.startswith('str'):
            return ins
    return None

print('sites with a nearby STR (init candidates):')
for P, tgt in sites:
    ins = is_store_site(P)
    if ins:
        print('\n  pool@%#x (%s) in %s' % (P, GOT_SLOTS[tgt], sym_of(P)))
        off = v2o(P - 0x30)
        for i2 in md.disasm(data[off:off + 0x50], P - 0x30):
            note = ''
            if i2.mnemonic.startswith('ldr') and '[pc' in i2.op_str:
                try:
                    imm = int(i2.op_str.split('#')[1].rstrip(']'), 0)
                    base = (i2.address + 8) & ~3
                    val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                    fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
                    if val in GOT_SLOTS:
                        note = '   ; GOT %s' % GOT_SLOTS[val]
                    else:
                        note = '   ; =%#x' % val
                        if 0x2f000000 < val < 0x50000000:
                            note += ' (float %g)' % fv
                except Exception:
                    pass
            print('  %08x %-8s %-32s%s' % (i2.address, i2.mnemonic, i2.op_str, note))
