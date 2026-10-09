#!/usr/bin/env python3
"""Find 'batch_info' string + xrefs in libKRHP.so; disassemble the parser."""
import re
import struct
import subprocess

import capstone

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
data = open(SO, "rb").read()

out = subprocess.run(["readelf", "-SW", SO], capture_output=True,
                     text=True).stdout
secs = []
for ln in out.splitlines():
    m = re.match(r"\s*\[\s*\d+\]\s+(\S+)\s+\S+\s+([0-9a-f]+)\s+([0-9a-f]+)"
                 r"\s+([0-9a-f]+)", ln)
    if m:
        secs.append((m.group(1), int(m.group(2), 16), int(m.group(3), 16),
                     int(m.group(4), 16)))


def v2f(va):
    for nm, addr, off, size in secs:
        if addr and addr <= va < addr + size and size and off:
            return off + (va - addr)
    return None


def f2v(fo):
    for nm, addr, off, size in secs:
        if off and off <= fo < off + size:
            return addr + (fo - off)
    return None


# 1) locate all 'batch_info' occurrences in FILE, map to vaddr
print("== 'batch_info' strings in file ==")
locs = []
start = 0
while True:
    j = data.find(b"batch_info", start)
    if j < 0:
        break
    va = f2v(j)
    ctx = data[max(0, j - 24):j + 32]
    va_s = f"{va:#x}" if va else "??"
    print(f"  file {j:#x} vaddr {va_s} ctx={ctx!r}")
    locs.append((j, va))
    start = j + 1

# 2) find references: ARM literal pools (word == vaddr) in .text
print("\n== literal-pool refs ==")
text = next(s for s in secs if s[0] == ".text")
tnm, taddr, toff, tsize = text
refs = []
for j, va in locs:
    if va is None:
        continue
    pat = struct.pack("<I", va)
    s = toff
    while True:
        k = data.find(pat, s, toff + tsize)
        if k < 0:
            break
        refs.append((k, f2v(k), va))
        s = k + 1
for fo, lva, sva in refs:
    print(f"  literal @vaddr {lva:#x} -> string {sva:#x}")

# 3) disassemble around each literal ref to find the LDR + function
elf = subprocess.run(["readelf", "-sW", SO], capture_output=True,
                     text=True).stdout
funcs = {}
for ln in elf.splitlines():
    m = re.match(r"\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+"
                 r"\s+(\S+)", ln)
    if m:
        funcs[int(m.group(1), 16)] = (int(m.group(2)), m.group(3))


def fname(va):
    best = (None, "")
    for a, (sz, nm) in funcs.items():
        if a <= va < a + max(sz, 1):
            if best[0] is None or a > best[0]:
                best = (a, nm)
    return best[1] or hex(va)


md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
seen_funcs = set()
for fo, lva, sva in refs:
    # find LDR rn, [pc, ...] instructions within 4KB before the literal
    lo = max(taddr, lva - 4096)
    off = v2f(lo)
    code = data[off:off + (lva - lo) + 64]
    for ins in md.disasm(code, lo):
        if ins.mnemonic == "ldr" and "[pc" in ins.op_str:
            # compute target
            m = re.search(r"\[pc, #(\d+)\]", ins.op_str)
            m2 = re.search(r"\[pc, #-(\d+)\]", ins.op_str)
            if m or m2:
                pc = ins.address + 8
                tgt = pc + (int(m.group(1)) if m else -int(m2.group(1)))
                if tgt == lva:
                    fn = fname(ins.address)
                    if fn not in seen_funcs:
                        seen_funcs.add(fn)
                        print(f"  {ins.address:#x}: {ins.mnemonic} "
                              f"{ins.op_str}  in {fn}")
