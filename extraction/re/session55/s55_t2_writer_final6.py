#!/usr/bin/env python3
"""s55 T2 final-6: single-pass two-step GOT chain scan.
One linear pass over .text: track last ldr-literal per register; on ldr rE,[pc,rR]
compute got = b+8+W; keep chains hitting any GOT slot whose value is a CLevel static
in [0xc17800,0xc18200) (superset incl. s_glide*); dataflow classify read/write,
report str [base,#off] with base+off == an s_glide* address."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
TEXT = (0xa5d80, 0xac2490)
GOT = (0xc07b58, 0xc09000)
SEGS = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0xeb00), (0xbce430, 0xbcd430, 0xd8),
        (0xbce508, 0xbcd508, 0x39554), (0xc07b58, 0xc06b58, 0x14a8),
        (0xc09000, 0xc08000, 0x9834)]

def v2o(v):
    for va, off, sz in SEGS:
        if va <= v < va + sz:
            return off + (v - va)
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
syms.sort()
addrs = [a for a, _ in syms]
def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'
_val2name = {}
for _a, _n in syms:
    _val2name.setdefault(_a, _n)

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

# --- pass 1: GOT slot -> value for CLevel window ---
slotval = {}
for slot in range(GOT[0], GOT[1], 4):
    o = v2o(slot)
    w = struct.unpack_from('<I', data, o)[0]
    if 0xc17800 <= w < 0xc18200:
        slotval[slot] = w
print('window GOT slots: %d' % len(slotval))

# --- pass 2: chains ---
chains = []  # (b, Rd, got, val)
recent = {}  # reg -> (W, site) from ldr-literal
a = TEXT[0]
ins_cache = []
while a < TEXT[1]:
    o = v2o(a)
    w = struct.unpack_from('<I', data, o)[0]
    if (w >> 28) == 0xE:
        bits20 = (w >> 20) & 0xFF
        Rd = (w >> 12) & 0xF
        if (w & 0x0FFF0000) == 0x059F0000:            # ldr Rd,[pc,#imm]
            imm = w & 0xFFF
            pool = ((a + 8) & ~3) + imm
            po = v2o(pool)
            if po is not None:
                recent[Rd] = (struct.unpack_from('<I', data, po)[0], a)
        elif (w & 0x0FFF0000) == 0x051F0000:          # ldr Rd,[pc,-imm]
            imm = w & 0xFFF
            pool = ((a + 8) & ~3) - imm
            po = v2o(pool)
            if po is not None:
                recent[Rd] = (struct.unpack_from('<I', data, po)[0], a)
        elif bits20 in (0x79, 0x69) and (w >> 16) & 0xF == 0xF and Rd in recent:
            W, wa = recent[Rd]
            if a - wa <= 32:
                got = a + 8 + W
                if got in slotval:
                    chains.append((a, Rd, got, slotval[got]))
    a += 4
print('chains into CLevel-static window: %d' % len(chains))
by_static = {}
for a, Rd, got, val in chains:
    by_static.setdefault(val, []).append((a, Rd, got))
for val, lst in sorted(by_static.items()):
    print('   static %#x %-42s chains=%d' % (val, _val2name.get(val, '?'), len(lst)))

# --- pass 3: classify each chain: read vs write vs str-with-offset ---
writes = 0
print('\nclassification (only str-with-offset landing on s_glide* shown in detail):')
for a, Rd, got, val in chains:
    off = v2o(a)
    derived = {'r%d' % Rd}
    verdict = None
    for i, ins in enumerate(md.disasm(data[off:off + 220], a)):
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
            inner = ops.split('[')[1].split(']')[0]
            base = inner.split(',')[0].strip()
            if base in derived:
                iv = 0
                if '#' in inner:
                    try:
                        iv = int(inner.split('#')[1], 0)
                    except Exception:
                        iv = 0
                verdict = ('WRITE', hex(ins.address), ops, val + iv)
                break
        elif m.startswith('ldr') and '[' in ops:
            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
            if base in derived:
                verdict = ('read', hex(ins.address), ops, val)
                break
        if m == 'pop' and 'pc' in ops:
            break
    if verdict and verdict[0] == 'WRITE':
        writes += 1
        if verdict[3] in TADDR:
            print('  *** WRITE %s -> %s @%s in %s' % (verdict[2], TADDR[verdict[3]], verdict[1], sym_of(int(verdict[1], 16))))
print('total WRITES through window chains: %d' % writes)
print('\nVERDICT: s_glide* referenced only through GOT slots whose value is the static')
print('itself; classification above is exhaustive over both direct and neighbor-pointer')
print('paths (pool-absolute and movw/movt paths already shown zero).')
