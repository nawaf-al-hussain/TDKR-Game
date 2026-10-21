#!/usr/bin/env python3
"""s43 T1d: identify lua API helpers by export symbol, disasm chunk-runner 0x14b2dc,
GlobalVarAddToLocalTable 0x14966c, and walk UP from 0x3f36c8."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
RAW = open(SO, 'rb').read()
PHOFF = struct.unpack_from('<I', RAW, 0x1c)[0]
PHNUM = struct.unpack_from('<H', RAW, 0x2c)[0]
SEGS = []
for i in range(PHNUM):
    o = PHOFF + i * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', RAW, o)[:6]
    if t == 1 and fs > 0:
        SEGS.append((va, off, fs, ms))


def va2off(va):
    for (v, o, fs, ms) in SEGS:
        if v <= va < v + fs:
            return o + (va - v)
    return None


def cstr_at(va, m=64):
    o = va2off(va)
    if o is None:
        return None
    d = RAW[o:o + m]
    e = d.find(b'\0')
    if e < 0:
        return None
    try:
        s = d[:e].decode('ascii')
        return s if all(32 <= ord(c) < 127 for c in s) else None
    except Exception:
        return None


SYM = {}
DEM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = int(p[1])
        DEM[int(p[0], 16)] = p[-1]
# demangled file maps address + mangled? check format quickly by grepping
print('=== api ident ===')
for a in (0xa49148, 0xa49cf0, 0xa499c4, 0xa49384, 0xa4944c, 0xa496f8, 0xa4ff0,
          0xa4e94, 0xa4e34, 0xa4a82c, 0xa49fc8, 0xa499dc, 0xa49e48, 0x3395d8,
          0x339914, 0x3399d4, 0x339c58, 0x339574):
    print(f'  0x{a:06x}: {DEM.get(a, "?")}  (size {SYM.get(a)})')


def disasm(lo, size, note=''):
    print(f'\n=== disasm 0x{lo:06x} ({size} B) {note} ===')
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = RAW[va2off(lo):va2off(lo) + size]
    for ins in md.disasm(code, lo):
        tgt = ''
        if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
            try:
                t = int(ins.op_str.lstrip('#'), 0)
                nm = DEM.get(t, '')
                tgt = f'   ; -> 0x{t:x} {nm}'
            except ValueError:
                pass
        if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                la = ((ins.address + 8) & ~3) + imm
                w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
                tgt += f'   ; lit@0x{la:06x}=0x{w:08x}'
                if 0x1000 < w < 0xc40000:
                    s = cstr_at(w)
                    if s:
                        tgt += f' str={s!r}'
            except Exception:
                pass
        print(f'0x{ins.address:06x}: {ins.mnemonic:8s} {ins.op_str}{tgt}')


disasm(0x14b2dc, 412, 'chunk runner?')

print('\n=== BL xrefs to 0x3f36c8 ===')
for (v, o, fs, ms) in SEGS:
    if ms == 0:
        continue
    blob = RAW[o:o + fs]
    for i in range(0, len(blob) - 4, 2):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0F000000) == 0x0B000000:
            imm24 = w & 0x00FFFFFF
            if imm24 & 0x800000:
                imm24 -= 1 << 24
            src = v + i
            if (src + 8 + imm24 * 4) & 0xFFFFFFFF == 0x3f36c8:
                # containing fn?
                own = [a for a, s in SYM.items() if a <= src < a + s]
                print(f'  BL from 0x{src:06x} in fn {[hex(x) for x in own]}')
