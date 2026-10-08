#!/usr/bin/env python3
"""Recursive-descent disassembly of CComponentFactory::CreateComponent.
Map: component typeId (movw/movt compare immediates) -> New() symbol called
in the matching branch block. Output: sorted table of fourCC -> class."""
import struct, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

SO = "lib_libKRHP.so"
d = open(SO, "rb").read()
syms = {}
for line in open("libKRHP_symbols.txt"):
    p = line.split()
    if len(p) >= 3 and p[1] == "FUNC":
        syms[int(p[0], 16)] = p[2]

FUNC_START, FUNC_SIZE = 0x223e3c, 7924
END = FUNC_START + FUNC_SIZE

md = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
md_thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)

visited = set()
blocks = {}   # addr -> list of (addr, mnem, ops)
todo = [FUNC_START]
while todo:
    start = todo.pop()
    if start in visited or not (FUNC_START <= start < END):
        continue
    q = [(start & ~1, (start & 1) == 1)]
    seq = []
    while q:
        addr, th = q.pop(0)
        if addr in visited or not (FUNC_START <= addr < END):
            continue
        visited.add(addr)
        m = md_thumb if th else md
        ok = False
        for ins in m.disasm(d[addr:addr + 4 * 40], addr):
            seq.append((ins.address, ins.mnemonic, ins.op_str))
            for tok in ins.op_str.replace(",", " ").split():
                if tok.startswith("#0x"):
                    try:
                        t = int(tok[1:], 16)
                    except ValueError:
                        continue
                    if ins.mnemonic in ("b", "beq", "bne", "ble", "bgt", "blt", "bge", "bls", "bhi", "bl"):
                        if t != addr + ins.size and FUNC_START <= t < END:
                            todo.append(t)
            if ins.mnemonic == "bl":
                try:
                    t = int(ins.op_str.lstrip("#"), 16)
                    if FUNC_START <= t < END:
                        todo.append(t)
                except ValueError:
                    pass
            if ins.mnemonic in ("pop", "bx") and ("pc" in ins.op_str or "lr" in ins.op_str):
                ok = True
                break
        if not ok:
            pass
    blocks[start] = seq

# now walk every instruction; track last-seen cmp immediates (movw+movt pairs)
events = []
pending_cmp = None
for start, seq in blocks.items():
    cur = None  # (imm, addrs)
    for addr, mn, ops in seq:
        if mn == "movw":
            try:
                imm = int(ops.split(",")[1].strip().lstrip("#"), 16)
                cur = [imm, [addr]]
            except Exception:
                cur = None
        elif mn == "movt" and cur is not None:
            try:
                hi = int(ops.split(",")[1].strip().lstrip("#"), 16)
                cur[0] |= hi << 16
                cur[1].append(addr)
            except Exception:
                cur = None
        elif mn == "cmp" and cur is not None:
            pending_cmp = cur
        elif mn == "bl":
            try:
                t = int(ops.lstrip("#"), 16)
            except Exception:
                continue
            nm = syms.get(t, hex(t))
            events.append((addr, t, nm, pending_cmp[0] if pending_cmp else None,
                           pending_cmp[1] if pending_cmp else []))

def fourcc(v):
    if v is None:
        return "--------"
    b = bytes([(v >> 24) & 0xff, (v >> 16) & 0xff, (v >> 8) & 0xff, v & 0xff])
    s = "".join(chr(c) if 32 <= c < 127 else "." for c in b)
    return f"{v:08x} {s!r}"

print("== bl targets in CreateComponent with nearest preceding typeId compare ==")
for addr, t, nm, imm, iaddrs in sorted(events):
    if "New" in nm or "new" in nm or "Create" in nm or "Component" in nm:
        print(f"bl@{addr:06x} -> {nm:60s} typeId={fourcc(imm)} cmp@{[hex(a) for a in iaddrs]}")
