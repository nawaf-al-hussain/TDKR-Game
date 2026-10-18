#!/usr/bin/env python3
"""S37 T1d: close the writer hunt with the remaining static checks.
1. indirect refs to CanReachCellFrom (literal-pool words 0x1d2c28/0x1d2c29)
2. CLevel load context 0x48af40-0x48b040 (what surrounds Create+SetNavMesh)
3. ldr [rX,#0x5c/0x60] inside SearchPortalPath / AppendPath(big) /
   HasPath / HasPathExact - does the path search ever read the pair table?
4. CNavMeshQuery ctor str site 0x1d3ab0 register context (stack?)
5. bl to AppendPath.part (0x1f1234) - who drives the big search
"""
import struct, json, bisect
import capstone

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    t, off, va, pa, fsz, msz = struct.unpack_from('<6I', d, o)
    if t == 1 and fsz:
        segs.append((va, off, fsz, msz))

def v2f(v):
    for va, off, fsz, msz in segs:
        if va <= v < va + max(fsz, msz):
            return off + (v - va)
    return None

syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
sa = sorted((int(k, 16), str(v[0])) for k, v in syms.items())
keys = [x[0] for x in sa]

def who(a):
    i = bisect.bisect_right(keys, a) - 1
    return sa[i] if i >= 0 else (0, '?')

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
TEXT_VA = TEXT_OFF = TEXT_FSZ = None
for va, off, fsz, msz in segs:
    if va <= 0x1d17cc < va + fsz:
        TEXT_VA, TEXT_OFF, TEXT_FSZ = va, off, fsz
        break

# 1. pool refs to CanReachCellFrom
print('=== 1. literal-pool refs to 0x1d2c28/0x1d2c29 (CanReachCellFrom) ===')
n = 0
for va, off, fsz, msz in segs:
    blob = d[off:off + fsz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        if w in (0x1d2c28, 0x1d2c29) and 0x8000 <= va + i < 0x400000:
            print(f'  pool@0x{va + i:08x} = 0x{w:08x} in {who(va + i)[1][:50]}')
            n += 1
print(f'  total: {n}')

# 2. load context
print('=== 2. CLevel load context 0x48af40-0x48b040 ===')
f = v2f(0x48af40)
for ins in md.disasm(d[f:f + 0x100], 0x48af40):
    print(f'  0x{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}')

# 3. ldr pair-table reads inside search functions
print('=== 3. ldr imm 0x5c/0x60 inside search functions ===')
RANGES = [
    (0x1d44b0, 0x1d44b0 + 1528, 'SearchPortalPath'),
    (0x1d4aa8, 0x1d4aa8 + 3544, 'AppendPath(big)'),
    (0x1d42d0, 0x1d42d0 + 268, 'HasPath'),
    (0x1d43dc, 0x1d43dc + 212, 'HasPathExact'),
    (0x1d3f78, 0x1d3f78 + 588, 'AppendForcePath'),
    (0x1d2550, 0x1d2550 + 732, 'FindClosestCellInRegion'),
]
for lo, hi, name in RANGES:
    f = v2f(lo)
    cnt = 0
    sites = []
    for ins in md.disasm(d[f:f + (hi - lo)], lo):
        if ins.mnemonic.startswith('ldr') and ('#0x5c]' in ins.op_str or '#0x60]' in ins.op_str) \
           and '[sp' not in ins.op_str:
            cnt += 1
            sites.append(f"0x{ins.address:08x} {ins.mnemonic} {ins.op_str}")
    print(f'  {name}: {cnt} non-stack ldr 0x5c/0x60')
    for s in sites:
        print(f'    {s}')

# 4. CNavMeshQuery ctor site context
print('=== 4. str site 0x1d3ab0 context ===')
f = v2f(0x1d3a9c)
for ins in md.disasm(d[f:f + 0x20], 0x1d3a9c):
    print(f'  0x{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}')

# 5. bl to AppendPath.part
print('=== 5. bl to AppendPath.part 0x1f1234 ===')
blob = d[TEXT_OFF:TEXT_OFF + TEXT_FSZ]
sites = []
for i in range(0, len(blob) - 4, 4):
    w = struct.unpack_from('<I', blob, i)[0]
    if (w & 0x0F000000) == 0x0B000000:
        imm = w & 0x00FFFFFF
        if imm & 0x800000:
            imm -= 0x1000000
        tgt = (TEXT_VA + i + 8 + imm * 4) & 0xFFFFFFFF
        if tgt in (0x1f1234,):
            sites.append(TEXT_VA + i)
for s in sites:
    print(f'  from 0x{s:08x} in {who(s)[1][:60]}')
print(f'  total: {len(sites)}')
