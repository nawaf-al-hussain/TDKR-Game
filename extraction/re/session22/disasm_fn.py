#!/usr/bin/env python3
"""Disassemble CVertexStreams::allocate @0x86cd9c — find what it stores at
+0xc (the count byte that bounds the pair loop) and +0x10/+0x14."""
import struct
import re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = "/home/z/my-project/repo/extraction/lib_libKRHP.so"

sym = {}
for line in open("/home/z/my-project/repo/extraction/libKRHP_symbols.txt"):
    p = line.split(None, 3)
    if len(p) >= 3 and p[2] == "FUNC":
        sym[int(p[0], 16)] = (int(p[1]), p[3].strip())


def disasm(addr, size=None, label=""):
    if size is None:
        size = sym.get(addr, (0x100, ""))[0]
    code = open(SO, "rb").read()[addr:addr + size]
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.skipdata = True
    print(f"==== {label or sym.get(addr, ('', hex(addr)))[1][:80]} @0x{addr:x} size={size}")
    for ins in md.disasm(code, addr):
        note = ""
        if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#"):
            t = int(ins.op_str.lstrip("#"), 16)
            note = "  ; -> " + (sym[t][1][:70] if t in sym else hex(t))
        print("%08x  %-8s %-38s%s" % (ins.address, ins.mnemonic, ins.op_str, note))


if __name__ == "__main__":
    import sys
    a = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x86cd9c
    s = int(sys.argv[2], 0) if len(sys.argv) > 2 else None
    disasm(a, s)
