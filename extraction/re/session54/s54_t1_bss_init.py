#!/usr/bin/env python3
"""s54 T1 step 17: find the static-init code writing the .bss glide constants.
Scan .text for movw/movt pairs building addresses in [0xc17d40, 0xc17d90] and
[0xc0abb0, 0xc0abd0]; disassemble those sites to read the stored float values."""
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

def movw_imm(w):
    return ((w >> 4) & 0xf000) | (w & 0xfff)

TARGETS = {
    0xc17d5c: 's_glidePitchMin', 0xc17d60: 's_glidePitchMax',
    0xc17d64: 's_glideRollMax', 0xc17d68: 's_glideDeltaYawMax',
    0xc17d6c: 's_glideYawCoef', 0xc17d70: 's_glidePitchCoef',
    0xc17d74: 's_glideRollCoef', 0xc17d78: 's_glidePitchAutoLevelingCoef',
    0xc17d7c: 's_glideRollAutoLevelingCoef', 0xc17d80: 's_glideDeadAngle',
    0xc0abc0: 'k_glideWallEvadeDistance', 0xc0abc4: 'k_glideWallEvadeMinDistance',
    0xc0abc8: 'k_glideWallEvadeMaxAngle',
}

state = {}
sites = []  # (addr, target, func)
lo, hi = 0x8000, 0xbbe000
for a in range(lo, hi, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    t = (w >> 20) & 0x0fff
    rd = (w >> 12) & 0xf
    if t == 0x300:
        state[rd] = movw_imm(w)
    elif t == 0x304 and rd in state:
        val = (movw_imm(w) << 16) | state[rd]
        if val in TARGETS:
            sites.append((a, val))
print('sites writing glide statics:')
for a, val in sites:
    print('  %#x -> %s (%#x) in %s' % (a, TARGETS[val], val, sym_of(a)))

# dump each site's neighborhood to read the value being stored
def dis_around(addr, back=0x14, fwd=0x10):
    for ins in md.disasm(data[v2o(addr - back):v2o(addr - back) + back + fwd], addr - back):
        note = ''
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
                note = '   ; =%#x' % val
                if 0x2f000000 < val < 0x50000000:
                    note += ' (float %g)' % fv
            except Exception:
                pass
        print('%08x %-8s %-34s%s' % (ins.address, ins.mnemonic, ins.op_str, note))

seen_funcs = set()
for a, val in sites:
    fn = sym_of(a)
    if fn in seen_funcs:
        continue
    seen_funcs.add(fn)
    print('\n=== %s (writes %s) ===' % (fn, TARGETS[val]))
    dis_around(a)
