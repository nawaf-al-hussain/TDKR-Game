#!/usr/bin/env python3
"""Forensic probe: full structure map of a .bdae file.

Goals:
  - decode ALL header fields (h[0..13]) as offsets
  - dump every ASCII string with offset
  - locate the string table region and see which strings are referenced where
  - find material blocks / texture refs between header and geometry
"""
import struct, sys, re

path = sys.argv[1]
d = open(path, 'rb').read()
print(f"file: {path}  size={len(d):#x} ({len(d)})")

# ---- top header ----
h = struct.unpack_from('<14I', d, 0)
print("\n== top header (14 u32 LE) ==")
for i, v in enumerate(h):
    print(f"  h[{i:2}] = {v:#10x}  ({v})")

G = h[10]
# ---- all strings with offsets ----
print("\n== strings (offset: text) ==")
strs = []
for m in re.finditer(rb'[\x20-\x7e]{4,}', d):
    s = m.group().decode()
    strs.append((m.start(), s))
for off, s in strs:
    zone = "HDR" if off < G else "GEO"
    print(f"  {off:#8x} [{zone}] {s}")

# ---- what's between header and geometry? ----
print("\n== bytes between header end and geometry start (G) ==")
head_end = 56
if G > head_end:
    chunk = d[head_end:G]
    print(f"  length: {len(chunk)}")
    # dump as u32 lines
    for i in range(0, min(len(chunk), 512), 16):
        words = struct.unpack_from('<4I', d, head_end + i) if head_end + i + 16 <= len(d) else None
        if words:
            print(f"  {head_end+i:#7x}: " + " ".join(f"{w:8x}" for w in words))
    if len(chunk) > 512:
        print(f"  ... ({len(chunk)-512} more bytes)")

# ---- walk geometry chain, show footer region including anything after indices ----
print("\n== geometry chain walk ==")
SIG = (0x5C, 0x4C, 0xA8, 0x40, 0x34, 0x28, 0x1C, 0x10)
g = G
n = 0
while g + 0x68 <= len(d) and n < 20:
    f = struct.unpack_from('<40I', d, g)
    if tuple(f[2:10]) != SIG:
        print(f"  @{g:#x}: no signature — stop")
        break
    print(f"  geo header @{g:#x}: f0={f[0]:#x} f1={f[1]:#x}", end='')
    # parse mesh like bdae_extract
    blk = None
    for i in range(2, 36):
        if f[i] == 0x10 and f[i+1] == 1:
            COUNT, ndw = f[i+2], f[i+3]
            if 0 < COUNT < 2_000_000 and 1 <= ndw <= 12:
                stride = 8 + ndw * 4
                end = G + f[1]
                start = end - COUNT * stride
                footer = G + f[0] - 8
                if start > G + 0x40 and footer + 0x1C <= len(d):
                    blk = (COUNT, ndw, stride, start, footer)
                    break
    if blk:
        COUNT, ndw, stride, start, footer = blk
        s0 = footer + 0x14
        e = d.index(b'\0', s0)
        mat = d[s0:e].decode('ascii', 'replace')
        print(f"  verts={COUNT} stride={stride} mat={mat!r}")
        # what's right after the material name / indices?
        idx_off = s0 + ((e - s0 + 1 + 3) & ~3)
        next_g = (idx_off + COUNT * 0 + (struct.unpack_from('<I', d, footer+4)[0]) * 2 + 3) & ~3
    else:
        print()
        break
    g = next_g if next_g > g else g + 0x40
    n += 1
print(f"  walked {n} blocks")
