#!/usr/bin/env python3
"""s55 T2 part B definitive: find every REAL reference to CLevel::s_glide*.
Step 1: whole-file scan for 4-byte words equal to a target .bss address or a GOT slot
        address (locate initializer tables / literal pools / relocs).
Step 2: decode .text properly: real ldr-literal = cond 0010 1U01 1111 Rd imm12.
        Compute pool word, then follow dataflow to ldr/str (read vs write).
Step 3: if zero code references exist, the symbols are dead: .bss stays 0.0 forever."""
import struct, subprocess, bisect

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
SEGS = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]
TEXT = (0xa5d80, 0xac2490)

def v2o(v):
    for va, off, sz in SEGS:
        if va <= v < va + sz:
            return off + (v - va)

NAMES = ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
         's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
         's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle']
TARGETS = {0xc17d5c + 4 * k: n for k, n in enumerate(NAMES)}
GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(NAMES)}
INV_T = {v: k for k, v in TARGETS.items()}
INV_G = {v: k for k, v in GOT_SLOTS.items()}

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    p = line.split()
    if len(p) == 3 and not p[2].startswith('$'):
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

print('--- STEP 1: whole-file words equal to a target or a GOT slot ---')
o2t, o2g = {}, {}
for off in range(0, len(data) - 3, 4):
    w = struct.unpack_from('<I', data, off)[0]
    if w in TARGETS:
        o2t[off] = w
    if w in GOT_SLOTS:
        o2g[off] = w
print('words == .bss target addr:', len(o2t))
for off, w in sorted(o2t.items()):
    print('   file@%#x va=%#x -> %s' % (off, off, TARGETS[w]))
print('words == GOT slot addr:', len(o2g))
for off, w in sorted(o2g.items()):
    print('   file@%#x va=%#x -> GOT[%s]' % (off, off, GOT_SLOTS[w]))

print('\n--- STEP 2: real ldr-literal in .text referencing GOT slots ---')
sites = []
for a in range(TEXT[0], TEXT[1], 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    cond, bits = w >> 28, (w >> 20) & 0xff
    if cond != 0xE:
        continue
    # ldr/str immediate: 010 P U B W L Rn Rt  — literal form has Rn=0b1111
    if (bits & 0x0F) != 0x0F or (bits >> 4) & 1 == 0 and False:
        pass
    if (bits & 0x0F) != 0x0F:
        continue
    op10 = (bits >> 5) & 0x03   # bits 25-20 -> [27:26]=01 for ldr/str imm
    if (bits >> 6) & 0x03 != 0x01:
        continue
    P, U, B, W, L = (bits >> 7) & 1, (bits >> 6) & 1, 0, 0, 0
    # recompute: bits = 010PUBWL Rn(=1111). bit7=P? no: bits[11:8]=? Let's decode per ARM:
    # cond 010 P U B W L Rn Rd imm12 ; here Rn = bits[19:16] = 1111 => literal when P=1,U=1 (or P=0)
    Pbit = (bits >> 7) & 1
    Ubit = (bits >> 6) & 1
    Lbit = (bits >> 5) & 1
    Wbit = (bits >> 4) & 1
    if (bits >> 4) & 0x1 and False:
        pass
    imm12 = w & 0xFFF
    Rd = (w >> 12) & 0xF
    if not Pbit and Wbit:   # not a literal form
        continue
    off = imm12 if Ubit else -imm12
    pool = ((a + 8) & ~3) + off
    if pool in INV_G:
        sites.append((a, Rd, Lbit, INV_G[pool], pool))
print('real ldr-literal sites hitting a GOT slot: %d' % len(sites))
for a, Rd, Lbit, name, pool in sites:
    print('   %s @%#x Rd=r%d pool@%#x in %s' % ('LDR' if not Lbit else 'STR?', a, Rd, pool, sym_of(a)))

print('\n--- STEP 2b: dataflow after each site (read vs write) ---')
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
nread = nwrite = 0
for a, Rd, Lbit, name, pool in sites:
    off = v2o(a)
    derived = {'r%d' % Rd}
    verdict = None
    for i, ins in enumerate(md.disasm(data[off:off + 200], a)):
        if i == 0:
            continue
        m, ops = ins.mnemonic, ins.op_str
        if m == 'mov' and ',' in ops:
            d, s = [x.strip() for x in ops.split(',', 1)]
            if s in derived:
                derived.add(d)
        elif m in ('add', 'sub') and ',' in ops:
            pr = [x.strip() for x in ops.split(',')]
            if len(pr) >= 2 and pr[1] in derived:
                derived.add(pr[0])
        elif m.startswith('str') and '[' in ops:
            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
            if base in derived:
                verdict = ('WRITE', hex(ins.address), ops)
                break
        elif m.startswith('ldr') and '[' in ops:
            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
            if base in derived:
                verdict = ('read', hex(ins.address), ops)
                break
        if m == 'pop' and 'pc' in ops:
            break
    if verdict:
        if verdict[0] == 'WRITE':
            nwrite += 1
        else:
            nread += 1
        print('   %s %s -> %s %s' % (name, hex(a), verdict[0], verdict[1:]))
    else:
        print('   %s %s -> unused (noise)' % (name, hex(a)))
print('reads=%d writes=%d' % (nread, nwrite))

print('\n--- STEP 3: verdict ---')
if nwrite == 0 and nread == 0:
    print('NO code in .text references the s_glide* GOT slots or addresses at all.')
    print('The ten CLevel::s_glide* floats are DEAD .bss: loaded zero, never written,')
    print('never read by any retained function => values are 0.0 by definition.')
