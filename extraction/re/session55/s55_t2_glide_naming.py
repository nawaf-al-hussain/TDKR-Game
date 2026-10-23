#!/usr/bin/env python3
"""s55 T2 (a)+(b-logic): glide float naming + comprehensive s_glide* static writer search.

Part A: bounded ARM disassembly of the 6 glide functions. Every ldr [rX, #off] where the
base register holds the CComponentGlide pointer (from CGadgetManager::GetGlide) and
8 <= off <= 0x58 is annotated as component float f<(off-8)/4> (layout: vptr@0, int1@4,
f0..f20 @8..0x58, int2@0x5c — s54 handoff).

Part B: exhaustive store search to CLevel::s_glide* (.bss @0xc17d5c..0xc17d80).
Encoding forms covered (ARM mode, whole .text):
  B1 literal-pool absolute: a 4-byte word anywhere in .text equal to a target addr
     (then ldr rB,[pc..] + str ..., [rB] or [rB,#off]);
  B2 movw/movt immediate: pairs building any value in [0xc17d40, 0xc17d9f]
     (catches base+offset block writes s54's exact-match scan missed);
  B3 GOT-indirect: pc-relative ldr of a GOT slot (0xc080c8..0xc080ec), classify
     the use of the loaded pointer as read (ldr [rB]) vs write (str [rB]);
  B4 ldm/stm block copies targeting a base in the window.
"""
import struct, subprocess, bisect, json, sys

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
SEGS = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in SEGS:
        if va <= v < va + sz:
            return off + (v - va)
    return None

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3:
        try:
            syms.append((int(pr[0], 16), pr[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False

TARGETS = {
    0xc17d5c: 's_glidePitchMin', 0xc17d60: 's_glidePitchMax',
    0xc17d64: 's_glideRollMax', 0xc17d68: 's_glideDeltaYawMax',
    0xc17d6c: 's_glideYawCoef', 0xc17d70: 's_glidePitchCoef',
    0xc17d74: 's_glideRollCoef', 0xc17d78: 's_glidePitchAutoLevelingCoef',
    0xc17d7c: 's_glideRollAutoLevelingCoef', 0xc17d80: 's_glideDeadAngle',
}
GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(
    ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
     's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
     's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle'])}
WIN_LO, WIN_HI = 0xc17d40, 0xc17d9f
TEXT_LO, TEXT_HI = 0xa5d80, 0xac2490  # .text section bounds (readelf -S)

def note_for(ins):
    note = ''
    if ins.mnemonic in ('bl', 'blx') and ins.op_str[:1] != 'r':
        try:
            t = int(ins.op_str.replace('#', ''), 16)
            note = '   ; -> ' + sym_of(t)
        except ValueError:
            pass
    if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
            base = (ins.address + 8) & ~3
            val = struct.unpack_from('<I', data, v2o(base + imm))[0]
            fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
            note = '   ; =%#x' % val
            if val in GOT_SLOTS:
                note += ' (GOT->%s)' % GOT_SLOTS[val]
            elif val in TARGETS:
                note += ' (ADDR %s)' % TARGETS[val]
            elif 0x2f000000 < val < 0x50000000:
                note += ' (float %g)' % fv
            elif val < 0x10000:
                note += ' (int %d)' % val
        except Exception:
            pass
    return note

print('#' * 20, 'PART A: glide function disassembly with component-float mapping', '#' * 20)
FUNCS = [
    ('StartGlide', 0x380590, 0x3809c0),
    ('StartGlideFromGrapnel', 0x380a0c, 0x380cbc),
    ('SetInitialGlideAngle', 0x380e34, 0x380e90),
    ('UpdateNavGlide', 0x380e94, 0x381348),
    ('RefreshForcesGlide', 0x3836b0, 0x383a08),
    ('RefreshForcesFallGrapnel', 0x383a08, 0x383ab0),
]
comp_reads = {}  # (func, floatidx) -> [sites]
for name, lo, hi in FUNCS:
    print('\n=== %s (%#x..%#x) ===' % (name, lo, hi))
    off = v2o(lo)
    for ins in md.disasm(data[off:off + (hi - lo)], lo):
        note = note_for(ins)
        # component float field detection: ldr/str [rX, #off], 8<=off<=0x58
        if ('ldr' in ins.mnemonic or 'str' in ins.mnemonic) and '#0x' in ins.op_str and '[' in ins.op_str:
            try:
                o = ins.op_str.split('#')[1].split(']')[0]
                ov = int(o, 16)
                if 8 <= ov <= 0x58 and (ov - 8) % 4 == 0:
                    fi = (ov - 8) // 4
                    note += ' (COMP f%d)' % fi
                    kind = 'r' if ins.mnemonic.startswith('ldr') else 'w'
                    comp_reads.setdefault((name, fi), []).append((hex(ins.address), kind, ins.mnemonic + ' ' + ins.op_str))
            except Exception:
                pass
        print('%08x %-8s %-34s%s' % (ins.address, ins.mnemonic, ins.op_str, note))

print('\n#' * 1, 'PART A2: component-float access summary')
for (fn, fi), sites in sorted(comp_reads.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    kinds = ''.join(sorted(set(s[1] for s in sites)))
    print('  %-24s f%-2d %s  n=%d  e.g. %s' % (fn, fi, kinds, len(sites), sites[0][2]))

print('\n' + '#' * 20, 'PART B: s_glide* store search', '#' * 20)
# B1: literal-pool absolute words
print('\n--- B1: literal-pool words equal to a target address ---')
lit_hits = []
for a in range(TEXT_LO, TEXT_HI, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    if w in TARGETS:
        lit_hits.append((a, w))
for a, w in lit_hits:
    print('  literal @%#x = %s' % (a, TARGETS[w]))
if not lit_hits:
    print('  none')

# B1b: literal-pool words equal to GOT slots (ldr rX,[pc] then str through it)
print('\n--- B1b: literal-pool words equal to a GOT slot ---')
lit_got = []
for a in range(TEXT_LO, TEXT_HI, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    if w in GOT_SLOTS:
        lit_got.append((a, w))
for a, w in lit_got:
    print('  literal @%#x = GOT slot of %s' % (a, GOT_SLOTS[w]))
if not lit_got:
    print('  none')

# B2: movw/movt building anything in the window
print('\n--- B2: movw/movt pairs building an address in [%#x,%#x] ---' % (WIN_LO, WIN_HI))
def movw_imm(w):
    return ((w >> 4) & 0xf000) | (w & 0xfff)
state = {}
mov_sites = []
for a in range(TEXT_LO, TEXT_HI, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    t = (w >> 20) & 0x0fff
    rd = (w >> 12) & 0xf
    if t == 0x300:
        state[rd] = (movw_imm(w), a)
    elif t == 0x304 and rd in state:
        val = (movw_imm(w) << 16) | state[rd][0]
        if WIN_LO <= val <= WIN_HI:
            mov_sites.append((a, val, state[rd][1]))
for a, val, lw in mov_sites:
    print('  movw@%#x movt@%#x -> %#x in %s' % (lw, a, val, sym_of(a)))
if not mov_sites:
    print('  none')

# B3: pc-relative ldr of GOT slot, classify use
print('\n--- B3: GOT-slot pc-relative loads, read vs write classification ---')
got_sites = []
for P in range(TEXT_LO, TEXT_HI, 4):
    L = struct.unpack_from('<i', data, v2o(P))[0]
    tgt = P + 8 + L
    if tgt in GOT_SLOTS:
        got_sites.append((P, tgt))
print('  pc-rel GOT loads: %d' % len(got_sites))
# disassemble forward from each site up to 40 insns; find first ldr/str using the
# destination register as base; classify. Also handle str into the GOT slot itself.
wr, rd_ = [], []
for P, tgt in got_sites:
    off = v2o(P)
    dstreg = None
    found = None
    for i, ins in enumerate(md.disasm(data[off:off + 160], P)):
        if i == 0 and ins.mnemonic.startswith('ldr'):
            dstreg = ins.op_str.split(',')[0].strip()
            continue
        if dstreg and (ins.mnemonic.startswith('ldr') or ins.mnemonic.startswith('str')):
            ops = ins.op_str
            if ops.startswith(dstreg + ',') or (']' in ops and dstreg in ops.split('[')[1] if '[' in ops else False):
                # base use
                if ops.startswith(dstreg + ', [') or (', [' + dstreg + ']') in ops or (', [' + dstreg + ',') in ops:
                    found = (ins.mnemonic, ins.op_str, hex(ins.address))
                    break
        if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            break
    if found:
        (mnem, ops, site) = found
        if mnem.startswith('str'):
            wr.append((P, GOT_SLOTS[tgt], site, ops))
        else:
            rd_.append((P, GOT_SLOTS[tgt], site, ops))
print('  classified: %d reads, %d WRITES' % (len(rd_), len(wr)))
for x in wr:
    print('  WRITE: ldr@%#x -> %s str %s @%s' % (x[0], x[1], x[3], x[2]))
if not wr:
    print('  NO writes through GOT pointers anywhere in .text')

# B4: ldm/stm with base in window
print('\n--- B4: ldm/stm base registers built from the window ---')
print('  (B2 found no base in window => no ldm/stm can target it)')
