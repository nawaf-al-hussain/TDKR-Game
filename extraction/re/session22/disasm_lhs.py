#!/usr/bin/env python3
"""Disassemble glitch::io::loadHeadersAndSkipData @0x8e1d34 (size 0x564)
from libKRHP.so with capstone (ARM mode). Prints annotated listing with
bl/blx targets resolved against the symbol table."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = "/home/z/my-project/repo/extraction/lib_libKRHP.so"
START = 0x8E1D34
SIZE = 0x564

# build symbol map
sym = {}
for line in open("/home/z/my-project/repo/extraction/libKRHP_symbols.txt"):
    parts = line.split(None, 3)
    if len(parts) >= 3 and parts[2] == "FUNC":
        sym[int(parts[0], 16)] = (int(parts[1]), parts[3].strip())

code = open(SO, "rb").read()[START:START + SIZE]
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.skipdata = True
out = []
bl_targets = set()
insns = list(md.disasm(code, START))
for ins in insns:
    if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#"):
        t = int(ins.op_str.lstrip("#"), 16)
        bl_targets.add(t)

for ins in insns:
    note = ""
    if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#"):
        t = int(ins.op_str.lstrip("#"), 16)
        if t in sym:
            note = "  ; -> %s" % sym[t][1][:90]
        else:
            note = "  ; -> 0x%x" % t
    if ins.mnemonic in ("ldr",) and "[pc" in ins.op_str:
        # resolve literal pool
        try:
            import re
            m = re.search(r"\[pc, #(-?\d+)\]", ins.op_str)
            if m:
                pc = (ins.address + 8) & ~3
                lit = pc + int(m.group(1))
                val = struct.unpack("<I", open(SO, "rb").read()[lit:lit + 4])[0]
                note += "  ; =[0x%x]=0x%08x (%s)" % (lit, val, sym.get(val, ("", ""))[1][:60] if val in sym else "")
        except Exception:
            pass
    out.append("%08x  %-8s %-40s%s" % (ins.address, ins.mnemonic, ins.op_str, note))
print("\n".join(out))
print("\nBL TARGETS:", ", ".join("0x%x%s" % (t, " " + sym[t][1][:70] if t in sym else "") for t in sorted(bl_targets)))
