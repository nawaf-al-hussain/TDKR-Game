#!/usr/bin/env python3
"""Disassemble CComponentFactory::CreateComponent @0x233e3c (real vaddr)
and every function it calls, to map component typeIds -> classes.
Capstone per-function decoding (literal pools break linear disasm)."""
import struct, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

SO = "lib_libKRHP.so"
d = open(SO, "rb").read()

# dynsym addr -> name
syms = {}
for line in open("libKRHP_symbols.txt"):
    parts = line.split()
    if len(parts) >= 3 and parts[1] == "FUNC":
        syms[int(parts[0], 16)] = parts[2]

FUNC_START = 0x223e3c  # real vaddr (libKRHP_symbols.txt); size 7924

def func_bytes(va):
    # next FUNC start after va (sorted), cap at 0x8000
    nxt = min((a for a in syms if a > va), default=va + 0x2000)
    size = min(nxt - va, 0x2000)
    return d[va:va + size]

def disas(va, thumb=False):
    md = Cs(CS_ARCH_ARM, (CS_MODE_THUMB if thumb else CS_MODE_ARM) | CS_MODE_LITTLE_ENDIAN)
    code = func_bytes(va)
    out = []
    for ins in md.disasm(code, va):
        out.append((ins.address, ins.mnemonic, ins.op_str))
        if ins.mnemonic in ("bx",) and 'lr' in ins.op_str:
            break
        if ins.mnemonic == "pop" and 'pc' in ins.op_str:
            break
    return out

print(f"== CComponentFactory::CreateComponent @ {FUNC_START:#x} ==")
for a, m, o in disas(FUNC_START):
    ann = ""
    # annotate branch targets + bl targets with symbol names
    for tok in o.replace(",", " ").split():
        if tok.startswith("#0x") or tok.startswith("0x"):
            try:
                v = int(tok.lstrip("#"), 16)
            except ValueError:
                continue
            if v in syms:
                ann += f"  ; {syms[v]}"
    print(f"{a:06x}  {m:8s} {o}{ann}")
