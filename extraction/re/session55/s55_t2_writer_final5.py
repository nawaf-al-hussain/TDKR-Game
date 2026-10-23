#!/usr/bin/env python3
"""s55 T2 final-5: neighbor-window check.
(1) whole-file words in [0xc17800, 0xc18200] (any static near s_glide* family) ->
    which of them are in .got (relocated) vs .data.rel.ro (pointer tables);
(2) whole-file words == k_glide* (.data) addresses anywhere;
(3) for every .got entry with value in the window, run the two-step chain scan and
    dataflow classify, reporting str [reg, #off] where base+off lands on s_glide*."""
import struct, subprocess, bisect

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

print('--- (1) got/data.rel.ro entries holding pointers into [0xc17000,0xc18200) ---')
near = {}
for slot in range(0xc07b58, 0xc09000, 4):
    o = v2o(slot)
    w = struct.unpack_from('<I', data, o)[0]
    if 0xc17000 <= w < 0xc18200:
        near[slot] = w
print('got entries in window: %d' % len(near))
for s, w in sorted(near.items()):
    nm = _val2name.get(w, '?')
    tgt = TADDR.get(w, '')
    print('   got %#x -> %#x %s %s' % (s, w, nm, tgt))

relro = {}
for va in range(0xbce508, 0xc07a5c, 4):
    o = v2o(va)
    w = struct.unpack_from('<I', data, o)[0]
    if 0xc17000 <= w < 0xc18200:
        relro[va] = w
print('data.rel.ro words in window: %d' % len(relro))
for s, w in sorted(relro.items())[:20]:
    print('   relro %#x -> %#x %s' % (s, w, _val2name.get(w, '?')))

print('\n--- (2) whole-file words == k_glide* addresses ---')
for t, n in ((0xc0abc0, 'k_glideWallEvadeDistance'), (0xc0abc4, 'k_glideWallEvadeMinDistance'),
             (0xc0abc8, 'k_glideWallEvadeMaxAngle')):
    hits = []
    for off in range(0, len(data) - 3, 4):
        w = struct.unpack_from('<I', data, off)[0]
        if w == t:
            hits.append(off)
    print('   %s %#x: %d words at %s' % (n, t, len(hits), [hex(h) for h in hits[:6]]))

print('\n--- (3) two-step GOT chains for window entries; str [base,#off] landing on s_glide* ---')
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
writes = 0
for slot, val in sorted(near.items()):
    # find ldr rX,[pc,rY] sites where site+8+regv == slot
    # regv = slot - (site+8); the pool word must equal that -> search pools for the value
    # invert: for each ldr-pc-reg site b in .text, b+8+W == slot => W = slot-(b+8)
    # scan pools instead: word W; candidate b = slot-8-W must be an ldr [pc,rD] with
    # preceding ldr-literal of W into rD. Do forward scan (cheap enough).
    a = TEXT[0]
    while a < TEXT[1]:
        o = v2o(a)
        w = struct.unpack_from('<I', data, o)[0]
        top = (w >> 20) & 0x7F
        if (w >> 28) == 0xE and top in (0x79, 0x69) and ((w >> 16) & 0xF) == 0xF:
            Rd = (w >> 12) & 0xF
            for back in range(1, 9):
                wa = a - 4 * back
                if wa < TEXT[0]:
                    break
                ww = struct.unpack_from('<I', data, v2o(wa))[0]
                if (ww >> 12) & 0xF != Rd:
                    continue
                regv = None
                if (ww & 0xFFF0000) == 0x059F0000:
                    pool = ((wa + 8) & ~3) + (ww & 0xFFF)
                    po = v2o(pool)
                    if po is not None:
                        regv = struct.unpack_from('<I', data, po)[0]
                elif (ww & 0xFFF0000) == 0x051F0000:
                    pool = ((wa + 8) & ~3) - (ww & 0xFFF)
                    po = v2o(pool)
                    if po is not None:
                        regv = struct.unpack_from('<I', data, po)[0]
                if regv is not None and a + 8 + regv == slot:
                    # dataflow
                    off = v2o(a)
                    derived = {'r%d' % Rd}
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
                                tgt = val + iv
                                if tgt in TADDR:
                                    writes += 1
                                    print('  WRITE %s -> %s (via got %#x) @%#x in %s' %
                                          (ops, TADDR[tgt], slot, ins.address, sym_of(ins.address)))
                                else:
                                    print('  str via window-ptr %#x+%#x=%#x @%#x (not s_glide*) %s' %
                                          (val, iv, tgt, ins.address, sym_of(ins.address)))
                                break
                        elif m.startswith('ldr') and '[' in ops:
                            base = ops.split('[')[1].split(']')[0].split(',')[0].strip()
                            if base in derived:
                                derived.add(ops.split(',')[0].strip())
                        if m == 'pop' and 'pc' in ops:
                            break
                    break
        a += 4
print('s_glide* writes via any path: %d' % writes)
