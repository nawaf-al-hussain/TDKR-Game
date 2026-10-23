#!/usr/bin/env python3
"""s55 T2 part B final-4 — CORRECT GOT access model:
    ldr rD, [pc, #imm]     ; pool word W
    ldr rE, [pc, rD]       ; accessed addr = site_b + 8 + W  == a .got slot
    ldr/str ..., [rE]      ; read vs write of the variable
Scan: (a) build .got map slot->symbol from readelf R_ARM_RELATIVE/GLOB_DAT relocs + nm;
      (b) for each `ldr rX,[pc,rY]` @b find the preceding ldr-literal into rY, compute
          got addr, keep if it is an s_glide* slot; dataflow classify.
Sanity: k_glideWallEvadeDistance access from RefreshForcesGlide must be found."""
import struct, subprocess, bisect, re

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
SECS = [
    ('.data.rel.ro.local', 0xbbf930, 0xbbe930, 0xeb00),
    ('.init_array', 0xbce430, 0xbcd430, 0xd8),
    ('.data.rel.ro', 0xbce508, 0xbcd508, 0x39554),
    ('.got', 0xc07b58, 0xc06b58, 0x14a8),
    ('.data', 0xc09000, 0xc08000, 0x9834),
    ('.bss', 0xc12838, 0xc11838, 0x4e448),
]
TEXT = (0xa5d80, 0xac2490)

def v2o(v):
    for name, addr, off, sz in SECS:
        if addr <= v < addr + sz:
            return off + (v - addr)
    if 0 <= v < 0xbbe1ec:
        return v
    return None

# .got map from relocations
NAMES = ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
         's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
         's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle']
TADDR = {0xc17d5c + 4 * k: n for k, n in enumerate(NAMES)}
INV_T = {v: k for k, v in TADDR.items()}

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

rel = subprocess.run(['readelf', '-r', SO], capture_output=True, text=True).stdout
got_map = {}
for line in rel.splitlines():
    p = line.split()
    if len(p) >= 3 and p[1] in ('00000017', '17'):
        try:
            slot = int(p[0], 16)
        except ValueError:
            continue
        o = v2o(slot)
        if o is None:
            continue
        w = struct.unpack_from('<I', data, o)[0]
        got_map[slot] = ('%#x' % w) + (' ' + TADDR[w] if w in TADDR else '')
sg = {k: v for k, v in got_map.items() if any(t in v for t in NAMES)}
print('GOT slots holding s_glide* addresses:')
for k, v in sorted(sg.items()):
    print('   %#x -> %s' % (k, v))
SG_SLOTS = set(sg)
KG = {0xc0abc0: 'k_glideWallEvadeDistance', 0xc0abc4: 'k_glideWallEvadeMinDistance',
      0xc0abc8: 'k_glideWallEvadeMaxAngle'}
kg_slots = {}
# build value->nm-name reverse map to identify k_glide* slots
_val2name = {}
for _a, _n in syms:
    _val2name.setdefault(_a, _n)
for slot, v in got_map.items():
    val = int(v.split()[0], 16)
    n = _val2name.get(val, '')
    if n in KG.values():
        kg_slots[slot] = n
print('k_glide* GOT slots: %s' % {hex(k): v for k, v in kg_slots.items()})

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def scan(slog):
    """find ldr rX,[pc,rY] chains; classify use of the loaded pointer"""
    found = []
    a = TEXT[0]
    while a < TEXT[1]:
        o = v2o(a)
        w = struct.unpack_from('<I', data, o)[0]
        # LDR (register): cond 011 U B W L Rn Rd imm12, Rn=pc(0xF), B=0, L=1
        # U=1: bits[27:20]=0x79 ; U=0: 0x69  (P=W=0 handled by mask)
        top = (w >> 20) & 0x7F
        if (w >> 28) == 0xE and top in (0x79, 0x69) and ((w >> 16) & 0xF) == 0xF:
            Rd = (w >> 12) & 0xF
            # find preceding ldr-literal into Rd within 8 insns
            regv = None
            for back in range(1, 9):
                wa = a - 4 * back
                if wa < TEXT[0]:
                    break
                wo = v2o(wa)
                ww = struct.unpack_from('<I', data, wo)[0]
                if (ww >> 12) & 0xF != Rd:
                    continue
                if (ww & 0xFFF0000) == 0x059F0000:      # ldr Rd,[pc,#imm] (add)
                    imm = ww & 0xFFF
                    pool = ((wa + 8) & ~3) + imm
                    po = v2o(pool)
                    if po is not None:
                        regv = struct.unpack_from('<I', data, po)[0]
                    break
                if (ww & 0xFFF0000) == 0x051F0000:      # ldr Rd,[pc,-imm] (sub)
                    imm = ww & 0xFFF
                    pool = ((wa + 8) & ~3) - imm
                    po = v2o(pool)
                    if po is not None:
                        regv = struct.unpack_from('<I', data, po)[0]
                    break
            if regv is not None:
                got_addr = a + 8 + regv
                if got_addr in SG_SLOTS or got_addr in kg_slots:
                    found.append((a, Rd, got_addr, sg.get(got_addr) or kg_slots.get(got_addr)))
        a += 4
    return found

sites = scan(True)
print('\nchain sites (s_glide*/k_glide*): %d' % len(sites))
reads = writes = 0
for a, Rd, got, name in sites:
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
    tag = 'WRITE' if verdict and verdict[0] == 'WRITE' else ('read' if verdict else 'unused')
    if tag == 'WRITE':
        writes += 1
    elif tag == 'read':
        reads += 1
    print('  %-40s ldr-pc@%#x got=%#x -> %s | %s' % (name.split()[0] if isinstance(name, str) else name, a, got, sym_of(a), verdict or 'unused'))
print('reads=%d writes=%d' % (reads, writes))
