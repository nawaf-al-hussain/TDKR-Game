#!/usr/bin/env python3
"""S61 T1 step 11: find ALL movw/movt compare pairs for DICT magic (0x44494354),
'GO' (0x474f), ver-3, and the s57-dialect header reads (offset-13 nrec).
Also dump gol.bin's first 32 bytes to pin the real header."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()

d = open('/home/z/my-project/work/data/gol.bin', 'rb').read()
print("gol.bin first 32 B:", d[:32].hex(' '))
print("  [0:4] =", d[0:4], " [4:8] =", struct.unpack_from('>I', d, 4)[0],
      " [8:12] =", d[8:12].hex(), " [12:17] =", d[12:17].hex())

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

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
o = v2o(TEXT_LO)
buf = data[o:o + (TEXT_HI - TEXT_LO)]

def scan_pairs(lo_val, hi_val, label):
    """Find movw lo + movt hi within 4B forming `val`, then report containing function."""
    hits = []
    pos = TEXT_LO
    while pos < TEXT_HI:
        off = pos - TEXT_LO
        chunk = buf[off:off + 0x4000]
        if not chunk:
            break
        stopped = pos
        for ins in md.disasm(chunk, pos):
            stopped = ins.address + ins.size
        pos = stopped + 2
    # simpler: brute-force instruction scan word by word
    n = 0
    for i in range(0, len(buf) - 8, 2):
        w0 = struct.unpack_from('<I', buf, i)[0]
        # movw rX, #imm16: cond=00x0 (ARM): 0xe30xxxxx pattern: bits 27-20 = 0x30, imm4=i, imm12
        if (w0 & 0x0ff00000) == 0x03000000:
            imm16_0 = ((w0 & 0xf0000) >> 4) | (w0 & 0xfff)
            w1 = struct.unpack_from('<I', buf, i + 4)[0]
            if (w1 & 0x0ff00000) == 0x03400000:  # movt
                imm16_1 = ((w1 & 0xf0000) >> 4) | (w1 & 0xfff)
                val = (imm16_1 << 16) | imm16_0
                if val == (hi_val << 16) | lo_val:
                    site = TEXT_LO + i
                    s = sym_of(site)
                    hits.append((site, s))
                    n += 1
    print(f"{label}: {n} movw/movt sites")
    for site, s in hits:
        print(f"  {site:#x} in {dem(s[0])[:80]} +{s[1]:#x}")
    return hits

scan_pairs(0x4354, 0x4449, "DICT magic (0x44494354)")
scan_pairs(0x474f, 0x0000, "'GO' (0x0000474f as movw-only)")
