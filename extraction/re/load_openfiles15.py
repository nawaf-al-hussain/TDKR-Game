#!/usr/bin/env python3
"""Resolve CLevelStreaming_DB::Load zip-member opens: field offset -> member name."""
import re
import struct
import sys

sys.path.insert(0, "/home/z/my-project/work/TDKR-Game/extraction/re")
import disasm15 as D
import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
md.detail = False

VA, SIZE = 0x3F6DFC, 0xB00
code = D._data[D.v2f(VA):D.v2f(VA) + SIZE]
insns = list(md.disasm(code, VA))

# state machine: track last ldr rX,[pc,#imm] pool value per reg, then add r2,pc,r2
poolval = {}
field = None
prev = None
for i, ins in enumerate(insns):
    txt = f"{ins.mnemonic} {ins.op_str}"
    m = re.match(r"ldr (\w+), \[pc, #(\w+)\]", txt)
    if m:
        reg, imm = m.group(1), int(m.group(2), 0)
        pcv = ins.address + 8 + imm
        try:
            poolval[reg] = struct.unpack_from("<I", D._data, D.v2f(pcv))[0]
        except Exception:
            poolval.pop(reg, None)
    m = re.match(r"add (\w+), pc, (\w+)", txt)
    if m and m.group(2) in poolval:
        reg = m.group(1)
        sva = ins.address + 8 + poolval[m.group(2)]
        s = D._data[D.v2f(sva):D.v2f(sva) + 48]
        s = s.split(b"\x00")[0]
        print(f"  ADR string @ {sva:#x}: {s!r}")
    m = re.match(r"str r(\d+), \[r4, #(\w+)\]", txt)
    if m:
        field = int(m.group(2), 0)
    if ins.mnemonic == "bl" and field is not None:
        try:
            t = int(ins.op_str.lstrip("#"), 16)
            a, nm = D.func_of(t)
            nm = D.short(nm, 60) if nm else hex(t)
        except Exception:
            nm = "?"
        if "openFile" in nm:
            print(f"    -> openFile into this+{field:#x}")
            field = None
