#!/usr/bin/env python3
"""s43 T1i: (1) identify lua API 0xa499c4 + ResetLuaGlobalVars push semantics;
(2) find lua_setmetatable export + xrefs (metatable hypothesis);
(3) active-line assignment scan in .lvc/gol.bin."""
import struct, re, collections
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


SYM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = p[-1]

# (1) what is 0xa499c4? print its disasm + the 10 lines
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
for probe in (0xa499c4, 0xa4a82c, 0xa49384, 0xa4944c, 0xa496f8, 0xa4ff0, 0xa4e94, 0xa4e34):
    a = probe
    sz = 32
    code = RAW[va2off(a):va2off(a) + sz]
    print(f'--- 0x{a:06x} {SYM.get(a, "(no sym)")} ---')
    for ins in md.disasm(code, a):
        print(f'   0x{ins.address:06x}: {ins.mnemonic:6s} {ins.op_str}')

# (2) lua_setmetatable: find by name
setmeta = None
for a, nm in SYM.items():
    if nm.endswith('lua_setmetatable'):
        setmeta = a
        print(f'\nlua_setmetatable @0x{a:x}')
if setmeta:
    hits = []
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
                if (src + 8 + imm24 * 4) & 0xFFFFFFFF == setmeta:
                    hits.append(src)
    print('lua_setmetatable BL xrefs:')
    for h in hits:
        own = [a for a in SYM if a <= h]
        print(f'  0x{h:06x} in {hex(max(own)) if own else "static"}')

# (3) active assignment scan
P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
raw = open(P, 'rb').read()
tag, idxsz, tabsz, nent = struct.unpack_from('>4I', raw, 0)
ents = [struct.unpack_from('>4I', raw, 16 + i * 16) for i in range(nent)]
pool = 16 + nent * 16
mem = {}
for (o, s, no, _p) in ents:
    e = raw.find(b'\0', pool + no)
    mem[raw[pool + no:e].decode('ascii', 'replace')] = (o, s)
asg = re.compile(r'MC_MAX_DISTANCE\s*=[^=]')
tot = collections.Counter()
for nm, (o, s) in mem.items():
    blob = raw[o:o + s].decode('latin-1')
    for line in blob.split('\n'):
        st = line.strip()
        if 'MC_MAX_DISTANCE' not in st or st.startswith('--'):
            continue
        code_part = st.split('--')[0]
        if asg.search(code_part):
            tot[nm] += 1
print('\nactive assignment lines per member:', dict(tot) if tot else 'NONE')
