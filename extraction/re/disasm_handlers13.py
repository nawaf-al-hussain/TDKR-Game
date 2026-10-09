#!/usr/bin/env python3
"""Disassemble the missing CLevel::LoadNextObject handlers (0x2653, 0x265e,
0x2661, 0x2662, 0x1404050/51, 0x2669, 0x267d, 0x1869f) + CTemplateZone::Load
+ CTemplateBakeGroup::Load from lib_libKRHP.so (A32, symtab-true addresses).
Prints CMemoryStream call annotations where the target is a known reader.
"""
import re
import struct
import subprocess

import capstone

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
data = open(SO, "rb").read()

# --- section map: find .text vaddr/file-offset via readelf ---
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
        if nm == ".text" and addr <= va < addr + size:
            return off + (va - addr)
    # fallback: first PROGBITS with addr<=va
    for nm, addr, off, size in secs:
        if addr and addr <= va < addr + size and off:
            return off + (va - addr)
    raise ValueError(hex(va))

# --- known reader functions for annotation ---
out = subprocess.run(["readelf", "-sW", SO], capture_output=True,
                     text=True).stdout
funcs = {}
for ln in out.splitlines():
    m = re.match(r"\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+"
                 r"\s+(\S+)", ln)
    if m:
        funcs[int(m.group(1), 16)] = (int(m.group(2)), m.group(3))


def fname(va):
    for a, (sz, nm) in funcs.items():
        if a <= va < a + max(sz, 1):
            short = nm.replace("_ZN", "").replace("_ZThn", "Thn")
            return short[:70]
    return hex(va)

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
md.detail = False

RANGES = [
    ("h2653_Occluder", 0x48a808, 0x48a9f0),
    ("h265e", 0x48a240, 0x48a2c0),
    ("h2661", 0x48aad0, 0x48ad00),
    ("h1404051", 0x48ad00, 0x48aea0),
    ("h1869f_branch", 0x48aea0, 0x48af48),
    ("h2669", 0x48af48, 0x48af5c),
    ("h2662", 0x48af5c, 0x48b0a8),
    ("h2667d", 0x48afcc, 0x48b060),
    ("CTemplateZone::Load", 0x48d5f4, 0x48d6f8),
    ("CTemplateBakeGroup::Load", 0x48d870, 0x48d978),
]

for name, lo, hi in RANGES:
    print(f"\n===== {name}  {lo:#x}..{hi:#x} =====")
    fo = v2f(lo)
    code = data[fo:fo + (hi - lo)]
    for ins in md.disasm(code, lo):
        tgt = ""
        m = re.search(r"#0x([0-9a-f]+)$", ins.op_str)
        if ins.mnemonic in ("bl", "b", "blx") and m:
            t = int(m.group(1), 16)
            tgt = "  ; " + fname(t)
        print(f"{ins.address:#x}: {ins.mnemonic:<8} {ins.op_str}{tgt}")
