#!/usr/bin/env python3
"""s42 T1: scan .text for calls to glTexImage2D/glTexSubImage2D PLT stubs; dump context."""
import struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

SO = "/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so"
data = open(SO, "rb").read()

TARGETS = {0xa5890: "glTexImage2D", 0xa58b4: "glTexSubImage2D"}

# sections
e_shoff = struct.unpack_from("<I", data, 0x20)[0]
e_shentsize = struct.unpack_from("<H", data, 0x2E)[0]
e_shnum = struct.unpack_from("<H", data, 0x30)[0]
e_shstrndx = struct.unpack_from("<H", data, 0x32)[0]
shs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    vals = struct.unpack_from("<10I", data, off)
    shs.append(vals)
shstr = shs[e_shstrndx]
def sname(n):
    end = data.find(b"\0", shstr[4] + n)
    return data[shstr[4] + n:end].decode()
text = None
for s in shs:
    if sname(s[0]) == ".text":
        text = s
assert text
t_addr, t_off, t_size = text[3], text[4], text[5]
print(f".text @0x{t_addr:x} size {t_size}")

tdata = data[t_off:t_off + t_size]

def sext(v, bits):
    return v - (1 << bits) if v & (1 << (bits - 1)) else v

calls = []  # (site_addr, mode, target)
# ARM BL: word>>24 == 0xEB
for i in range(0, len(tdata) - 4, 4):
    w = struct.unpack_from("<I", tdata, i)[0]
    if (w >> 24) == 0xEB:
        imm = sext(w & 0xFFFFFF, 24)
        tgt = t_addr + i + 8 + imm * 4
        if tgt in TARGETS:
            calls.append((t_addr + i, "ARM", tgt))
# Thumb BL/BLX: 32-bit pairs
for i in range(0, len(tdata) - 4, 2):
    hw1 = struct.unpack_from("<H", tdata, i)[0]
    if (hw1 & 0xF800) == 0xF000:
        hw2 = struct.unpack_from("<H", tdata, i + 2)[0]
        if (hw2 & 0xD000) == 0xD000:  # BL
            imm22 = ((hw1 & 0x7FF) << 12) | ((hw2 & 0x7FF) << 1)
            tgt = t_addr + i + 4 + sext(imm22, 23)
            if tgt in TARGETS:
                calls.append((t_addr + i, "THUMB", tgt))

print(f"total call sites: {len(calls)}")

# symbol map (FUNC) from symtab
syms = []
out = subprocess.run(["readelf", "-sW", SO], capture_output=True, text=True).stdout
for line in out.splitlines():
    m = re_m = None
    parts = line.split()
    if len(parts) >= 8 and parts[3] == "FUNC":
        try:
            val = int(parts[1], 16); size = int(parts[2])
        except ValueError:
            continue
        name = parts[7]
        if size > 0:
            syms.append((val, size, name))
syms.sort()

import bisect
starts = [s[0] for s in syms]
def enclosing(addr):
    i = bisect.bisect_right(starts, addr) - 1
    if i >= 0:
        v, sz, n = syms[i]
        if v <= addr < v + sz:
            return n
    return "??"

for addr, mode, tgt in sorted(calls):
    print(f"\n=== {TARGETS[tgt]} call @0x{addr:x} ({mode}) in {enclosing(addr)}")

# save sites for the context dump step
import json
json.dump([[a, m, t] for a, m, t in calls], open("/home/z/my-project/scripts/s42_t1_sites.json", "w"))
