#!/usr/bin/env python3
"""s55 T2 part B follow-up:
(B2w) movw/movt pairs building ANY base in [0xc16000,0xc19000] (catches str [base,#imm]
      landing on 0xc17d5c..0xc17d80), then disassemble around hits and check str offsets;
(B3w) for all 97 pc-rel GOT loads: small dataflow window — track dst reg copies (mov rY,rX,
      add rY,rX,#imm) and flag ANY str whose base register derives from the GOT pointer;
      also report the enclosing symbol of each site (who reads the statics);
(REL) confirm R_ARM_GLOB_DAT relocs fill the GOT slots with the .bss addresses."""
import struct, subprocess, bisect
from collections import defaultdict

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
SEGS = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in SEGS:
        if va <= v < va + sz:
            return off + (v - va)

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3 and not pr[2].startswith('$'):  # skip mapping symbols $a/$d/$t
        try:
            syms.append((int(pr[0], 16), pr[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

TARGETS = {0xc17d5c + 4 * k: n for k, n in enumerate(
    ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
     's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
     's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle'])}
GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(list(TARGETS.values()))}

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def movw_imm(w):
    return ((w >> 4) & 0xf000) | (w & 0xfff)

# ---- B2w ----
print('--- B2w: movw/movt building any base in [0xc16000,0xc19000] ---')
state = {}
hits = []
for a in range(0xa5d80, 0xac2490, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    t = (w >> 20) & 0x0fff
    rd = (w >> 12) & 0xf
    if t == 0x300:
        state[rd] = (movw_imm(w), a)
    elif t == 0x304 and rd in state:
        val = (movw_imm(w) << 16) | state[rd][0]
        if 0xc16000 <= val <= 0xc19000:
            hits.append((a, val, state[rd][1], rd))
print('  hits: %d' % len(hits))
for a, val, lw, rd in hits:
    print('  movw@%#x movt@%#x r%d -> %#x in %s' % (lw, a, rd, val, sym_of(a)))

# for each hit, disassemble fwd 40 insns and find str [rBase, #imm] where base==rd
print('\n  stores through these bases:')
any_store = False
for a, val, lw, rd in hits:
    off = v2o(a)
    for ins in md.disasm(data[off:off + 160], a):
        if ins.mnemonic.startswith('str') and ins.op_str.startswith('r') and '[' in ins.op_str:
            base = ins.op_str.split('[')[1].split(']')[0].split(',')[0].strip()
            if base == 'r%d' % rd:
                try:
                    o = ins.op_str.split('#')[1].split(']')[0] if '#' in ins.op_str else '0'
                    tgt = val + int(o, 0)
                except Exception:
                    tgt = None
                if tgt and tgt in TARGETS:
                    any_store = True
                    print('    WRITE %s -> %s @%#x (%s)' % (ins.op_str, TARGETS[tgt], ins.address, sym_of(ins.address)))
                else:
                    print('    str via base %#x @%#x %s (target %#x not a glide static)' % (val, ins.address, ins.op_str, tgt or 0))
        if ins.mnemonic in ('pop',) and 'pc' in ins.op_str:
            break
if not any_store:
    print('    none land on s_glide*')

# ---- B3w ----
print('\n--- B3w: GOT-site dataflow (97 sites) — reads vs writes + enclosing symbols ---')
sites = []
for P in range(0xa5d80, 0xac2490, 4):
    L = struct.unpack_from('<i', data, v2o(P))[0]
    tgt = P + 8 + L
    if tgt in GOT_SLOTS:
        sites.append((P, GOT_SLOTS[tgt]))
by_func = defaultdict(int)
writes = []
for P, name in sites:
    by_func[sym_of(P)] += 1
    off = v2o(P)
    loaded = None      # reg holding the .bss pointer
    derived = {None}
    for i, ins in enumerate(md.disasm(data[off:off + 200], P)):
        m, ops = ins.mnemonic, ins.op_str
        if i == 0 and m == 'ldr':
            loaded = ops.split(',')[0].strip()
            derived = {loaded}
            continue
        if m == 'mov' and ',' in ops:
            d, s = [x.strip() for x in ops.split(',', 1)]
            if s in derived:
                derived.add(d)
        elif m in ('add', 'sub') and ',' in ops:
            parts = [x.strip() for x in ops.split(',')]
            if len(parts) >= 2 and parts[1] in derived:
                derived.add(parts[0])
        elif m.startswith('str') and '[' in ops:
            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
            if base in derived:
                writes.append((P, name, hex(ins.address), ops))
                break
        elif m.startswith('ldr') and '[' in ops:
            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
            if base in derived:
                derived.add(ops.split(',')[0].strip())
        if m == 'pop' and 'pc' in ops:
            break
print('  sites by enclosing symbol:')
for fn, n in sorted(by_func.items(), key=lambda kv: -kv[1]):
    print('    %3d  %s' % (n, fn))
print('  WRITES found: %d' % len(writes))
for x in writes:
    print('    WRITE via GOT(%s): str %s @%s' % (x[1], x[3], x[2]))
if not writes:
    print('    none — no store anywhere in .text uses a GOT-derived s_glide* pointer')

# ---- REL ----
print('\n--- REL: dynamic relocations for the GOT slots ---')
import gzip
# .so is ELF32 LE; parse .rel.dyn via readelf if present
try:
    out = subprocess.run(['readelf', '-r', SO], capture_output=True, text=True).stdout
    n = 0
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0].startswith('c080'):
            try:
                a = int(parts[0], 16)
            except ValueError:
                continue
            if a in GOT_SLOTS:
                print('  %#x %s %s -> %s' % (a, parts[1], parts[2], GOT_SLOTS[a]))
                n += 1
    print('  (reloc rows shown: %d)' % n)
except FileNotFoundError:
    print('  readelf unavailable')
