#!/usr/bin/env python3
"""ARM BL xref scanner: find all bl <target> for given targets in .text."""
import struct, sys

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
d = open(SO, "rb").read()
# 1:1 vaddr/fileoff per RE_NOTES; .text roughly 0x113000..0xb0000? use full file
TEXT_LO, TEXT_HI = 0x0f0000, 0xb40000

targets = {}
for a in sys.argv[1:]:
    targets[int(a, 16)] = []

hits = []
for off in range(TEXT_LO, min(TEXT_HI, len(d)) - 4, 4):
    w = struct.unpack_from("<I", d, off)[0]
    if (w & 0xFF000000) == 0xEB000000:  # BL (ARM)
        imm24 = w & 0x00FFFFFF
        if imm24 & 0x800000:
            imm24 -= 1 << 24
        tgt = off + 8 + imm24 * 4
        if tgt in targets:
            hits.append((off, tgt))

for off, tgt in sorted(hits):
    print(f"bl {tgt:#x} from {off:#x}")
