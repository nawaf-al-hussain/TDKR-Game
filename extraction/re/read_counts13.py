#!/usr/bin/env python3
"""Count Read{Char,Int,Float,String} calls in each object-Load function to
derive exact payload sizes for the lvc sequential parser."""
import re
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
        if nm == ".text" and addr <= va < addr + size:
            return off + (va - addr)
    raise ValueError(hex(va))


elf = subprocess.run(["readelf", "-sW", SO], capture_output=True,
                     text=True).stdout
funcs = {}
for ln in elf.splitlines():
    m = re.match(r"\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+"
                 r"\s+(\S+)", ln)
    if m:
        funcs[int(m.group(1), 16)] = (int(m.group(2)), m.group(3))


def fname(va):
    for a, (sz, nm) in funcs.items():
        if a <= va < a + max(sz, 1):
            return nm[:78]
    return hex(va)


md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

TARGETS = {
    "CWorldBox::Load": (0x2b56f4, 344),
    "CTemplateMetaZone::Load": (0x48d708, 352),
    "CZonePortal::Create": (0x2b9dec, None),
    "CNavMeshNova::Create": (0x1d17cc, None),
    "CWayPointObject::Create": (0x2a8220, None),
    "Occluder_h(0x2653)_inline": (0x48a808, 0x48a9f0),
    "h1011_inline": (0x48af2c, 0x48af48),
    "h2669_inline": (0x48af48, 0x48af5c),
    "h140869f_inline": (0x48aea0, 0x48af48),
    "h1404051_inline": (0x48ad00, 0x48aea0),
    "h2661_inline": (0x48aad0, 0x48ad00),
    "ConstructColladaScene": (0x20414c, 788),
    "CComponentMesh::Load": (0x2d6ddc, 108),
}

READERS = {0x3395d8: "char", 0x339914: "int", 0x339b94: "float",
           0x33a0d4: "string", 0x3399d4: "Read(int&)"}


def walk(lo, size):
    """linear disasm; returns list of (mnemonic, opstr, target)"""
    fo = v2f(lo)
    code = data[fo:fo + size]
    ins_list = list(md.disasm(code, lo))
    return ins_list


def analyze(name, lo, size):
    if size is None:
        size = funcs.get(lo, (0, ""))[0] or 400
    ins_list = walk(lo, size)
    counts = {}
    branches_out = 0
    calls = []
    for ins in ins_list:
        if ins.mnemonic in ("bl", "blx"):
            m = re.search(r"#0x([0-9a-f]+)", ins.op_str)
            if m:
                t = int(m.group(1), 16)
                nm = fname(t)
                calls.append(nm)
                if t in READERS:
                    counts[READERS[t]] = counts.get(READERS[t], 0) + 1
        if ins.mnemonic == "b" and re.search(r"#0x([0-9a-f]+)", ins.op_str):
            t = int(re.search(r"#0x([0-9a-f]+)", ins.op_str).group(1), 16)
            if t < lo or t >= lo + size:
                branches_out += 1
    total = (1 * counts.get("char", 0) + 4 * counts.get("int", 0)
             + 4 * counts.get("float", 0) + 4 * counts.get("string", 0)
             + 4 * counts.get("Read(int&)", 0))
    print(f"{name:32s} {lo:#x} size={size}")
    print(f"   reads: {counts}  -> payload bytes (excl strings' len fields "
          f"included): {total}")
    ext = [c for c in calls if "Read" not in c and "MemoryStream" not in c]
    print(f"   other calls: {ext[:8]}")
    return counts, total


for name, (lo, sz) in TARGETS.items():
    analyze(name, lo, sz)
