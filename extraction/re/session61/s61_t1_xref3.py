#!/usr/bin/env python3
"""S61 T1 step 6: (1) find xrefs to 'gol.bin' string @0xb3ea64 (pool literals + pc-rel).
(2) disasm CGameObjectManager ctor around the Load call.
(3) disasm CreateObject GCT call context 0x367f80..0x368020.
(4) search .text for other IDCT magic compares (movw 0x4354/movt 0x4449 pairs)."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    pt, po, pv, _, ps = struct.unpack_from('<5I', data, p)
    if pt == 1:
        segs.append((pv, po, ps))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

TEXT_LO, TEXT_HI = 0xa5d80, 0xac2190
nm = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for l in nm.splitlines():
    p = l.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

def dem(n):
    return subprocess.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

# 1) pool-literal refs to 0xb3ea64 and nearby string addrs
print("=== literal pool refs to gol.bin str 0xb3ea64 (and +-0x10) ===")
for off in range(0xb3ea60, 0xb3ea80, 4):
    val = struct.unpack_from('<I', data, off)[0]
    # find in .text pools
    tlo = v2o(TEXT_LO)
    hay = data[tlo:v2o(TEXT_HI)]
    needle = struct.pack('<I', val)
    hits = []
    start = 0
    while True:
        j = hay.find(needle, start)
        if j < 0:
            break
        hits.append(TEXT_LO + j)
        start = j + 1
    if hits:
        print(f"  str@{off:#x} val {val:#x} -> pool sites {[hex(h) for h in hits[:8]]}")

# 2) ctor disasm
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
def dump(start, end, title):
    print(f"\n=== {title} {start:#x}..{end:#x} = {dem(sym_of(start)[0])}")
    o = v2o(start)
    insns = list(md.disasm(data[o:o + (end - start)], start))
    lit = {}
    for ins in insns:
        if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].split(']')[0], 0)
            except Exception:
                continue
            pc = ins.address + 8
            vv = struct.unpack_from('<I', data, v2o(pc))[0] if v2o(pc) else None
            lit[ins.address] = (pc, vv)
    for ins in insns:
        line = f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}"
        ann = ''
        if 'bl' in ins.mnemonic and ins.op_str.startswith('#'):
            try:
                t = int(ins.op_str[1:], 0)
                ann = f"  ; -> {dem(sym_of(t)[0])}"
            except Exception:
                pass
        elif ins.address in lit:
            va, val = lit[ins.address]
            if val is not None:
                s = sym_of(val)
                ann = f"  ; [{va:#x}] = {val:#x}"
                if s[0] != '<none>':
                    ann += f" {dem(s[0])[:60]}"
                elif 0xb3e000 <= val <= 0xb3f000:
                    s2 = data[v2o(val):v2o(val) + 24] if v2o(val) else b''
                    ann += f" STR={s2[:16]}"
        print(line + ann)

dump(0x365598, 0x365650, 'CGameObjectManager ctor (caller of Load)')
dump(0x367f60, 0x368010, 'CreateObject GCT call site context')

# 3) other IDCT magic compares in .text
print("\n=== movw 0x4354 + movt 0x4449 pairs in .text (IDCT magic) ===")
md2 = Cs(CS_ARCH_ARM, CS_MODE_ARM)
tlo = v2o(TEXT_LO)
buf = data[tlo:v2o(TEXT_HI)]
pos = 0
n = 0
while pos < len(buf) - 8:
    # movw rX, #0x4354 = e3?? encoding varies; scan raw for movw+movt pattern is unreliable;
    # instead look for the constant pair in code as immediates via disasm of windows around
    # found pool values 0x44494354
    j = buf.find(struct.pack('<I', 0x44494354), pos)
    if j < 0:
        break
    site = TEXT_LO + j
    s = sym_of(site)
    print(f"  pool value 0x44494354 at {site:#x} in {dem(s[0])[:70]} +{s[1]:#x}")
    pos = j + 4
    n += 1
print(f"(total {n})")
