#!/usr/bin/env python3
"""s55 T2 part B final-2:
(1) real GOT = 0xc070c8..0xc070ec (STEP-1 finding): search .text for real ldr-literal
    pools containing these addresses, dataflow classify read/write;
(2) identify the 0xd0d668 16-byte-stride pointer table: dump entries + follow string
    pointers (name exposure => config/debug data-driven init);
(3) confirm what 0xc080c8 (s54's 'GOT') actually is."""
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
TADDR = {0xc17d5c + 4 * k: n for k, n in enumerate(NAMES)}
REALGOT = {0xc070c8 + 4 * k: n for k, n in enumerate(NAMES)}

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

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

print('--- (1) real ldr-literal referencing REAL GOT (0xc070c8..) ---')
sites = []
for a in range(TEXT[0], TEXT[1], 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    if (w >> 28) != 0xE:
        continue
    bits = (w >> 20) & 0xFF
    if (bits & 0x0F) != 0x0F:          # Rn must be pc
        continue
    if (bits >> 6) != 0b010110 >> 2:   # bits[27:26] == 01 (ldr/str imm off)
        pass
    Pbit = (bits >> 7) & 1
    Ubit = (bits >> 6) & 1
    if not Pbit:
        continue
    imm12 = w & 0xFFF
    off = imm12 if Ubit else -imm12
    pool = ((a + 8) & ~3) + off
    if pool in REALGOT:
        Rd = (w >> 12) & 0xF
        Lbit = (bits >> 5) & 1
        sites.append((a, Rd, Lbit, REALGOT[pool], pool))
print('sites: %d' % len(sites))
reads = writes = 0
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
            writes += 1
        else:
            reads += 1
        print('  %-28s ldr@%#x %s %s %s' % (name, a, verdict[0], verdict[1], verdict[2]))
    else:
        print('  %-28s ldr@%#x unused/noise (in %s)' % (name, a, sym_of(a)))
print('reads=%d writes=%d' % (reads, writes))

print('\n--- (2) 0xd0d668 16-byte-stride pointer table ---')
base = 0xd0d668
for k in range(6):
    ea = base + 0x10 * k
    words = [struct.unpack_from('<I', data, v2o(ea + 4 * j))[0] for j in range(4)]
    row = [hex(x) for x in words]
    # try to read a string at each word address
    strs = []
    for w in words:
        o = v2o(w)
        if o:
            end = data.find(b'\x00', o, o + 64)
            if end > o:
                try:
                    s = data[o:end].decode('ascii')
                    if len(s) >= 3 and s.isprintable():
                        strs.append(s)
                except Exception:
                    pass
    print('  entry%d @%#x: %s strings=%s' % (k, ea, row, strs))

print('\n--- (3) what is 0xc080c8 (s54 GOT) ---')
o = v2o(0xc080c8)
vals = [struct.unpack_from('<I', data, o + 4 * j)[0] for j in range(4)]
print('  words:', [hex(v) for v in vals])
import subprocess as sp
rel = sp.run(['readelf', '-r', SO], capture_output=True, text=True).stdout
for line in rel.splitlines():
    if line.strip().startswith('00c080c8') or line.strip().startswith('00c070c8') or line.strip().startswith('00c070cc'):
        print('  REL:', line.strip())
# which section holds 0xc070c8 and 0xc080c8?
sec = sp.run(['readelf', '-S', '-W', SO], capture_output=True, text=True).stdout
for line in sec.splitlines():
    p = line.split()
    if len(p) > 7 and p[1] in ('.got', '.got.plt', '.data', '.data.rel.ro', '.bss', '.rodata'):
        print('  SEC:', p[1], p[3], p[4], p[5])
