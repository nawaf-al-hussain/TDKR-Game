#!/usr/bin/env python3
"""Exact dataflow scan v2 for config-singleton (GOT 0xc07f18 -> obj 0xc22ce4) accesses.

Fixes vs v4: capstone renders immediates as hex (#0xb0); proper kill-def; proper
operand regex for ldr/vldr/str forms.
"""
import struct, re, subprocess, collections, json, sys
from capstone import *

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
GOT = 0x00c07f18
OBJ = 0x00c22ce4
f = open(SO, "rb").read()
TEXT_VA, TEXT_OFF, TEXT_SZ = 0xa5d80, 0xa5d80, 0xa1c710

out = subprocess.check_output(["readelf", "-s", "-W", SO], text=True)
funcs = []
for line in out.splitlines():
    p = line.split()
    if len(p) >= 8 and p[3] == "FUNC" and re.fullmatch(r"[0-9a-f]{8}", p[1]):
        va, sz = int(p[1], 16), int(p[2])
        if sz and TEXT_VA <= va < TEXT_VA + TEXT_SZ:
            funcs.append((va, sz, p[7]))
funcs.sort()
print(f"{len(funcs)} FUNC symbols", file=sys.stderr)

md_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md_thm = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

def word_at(va):
    if TEXT_VA <= va < TEXT_VA + TEXT_SZ - 3:
        return struct.unpack_from("<I", f, TEXT_OFF + (va - TEXT_VA))[0]
    return None

IMM = r"#(0x[0-9a-f]+|\d+)"
hits = []

for va, sz, name in funcs:
    real = va & ~1
    md = md_thm if (va & 1) else md_arm
    blob = f[TEXT_OFF + (real - TEXT_VA): TEXT_OFF + (real - TEXT_VA) + sz]
    regs = {}
    objregs = set()
    for ins in md.disasm(blob, real):
        op = ins.op_str or ""
        m = ins.mnemonic
        rd = op.split(",")[0].strip() if op else None
        defined = False

        mm = re.match(rf"r(\d+), \[pc, {IMM}\]$", op)
        if m == "ldr" and mm:
            w = word_at(ins.address + 8 + int(mm.group(2), 0))
            regs[rd] = ("lit", w) if w is not None else None
            defined = True
        else:
            mm = re.match(rf"r(\d+), \[pc, r(\d+)\]$", op)
            if m == "ldr" and mm:
                v = regs.get("r" + mm.group(2))
                tgt = (ins.address + 8 + v[1]) & 0xffffffff if v and v[0] == "lit" else None
                if tgt == GOT:
                    regs[rd] = ("got",)
                    hits.append((ins.address, name, "GOT-load", f"tgt={tgt:#x}"))
                elif tgt == OBJ:
                    regs[rd] = ("obj",)
                    objregs.add(rd)
                    hits.append((ins.address, name, "OBJ-load", f"tgt={tgt:#x}"))
                else:
                    regs[rd] = None
                defined = True
            else:
                mm = re.match(r"r(\d+), \[r(\d+)\]$", op)
                if m == "ldr" and mm:
                    rZ = "r" + mm.group(2)
                    if regs.get(rZ) == ("got",):
                        regs[rd] = ("obj",)
                        objregs.add(rd)
                        hits.append((ins.address, name, "OBJ-deref", "*(got)"))
                    else:
                        regs[rd] = None
                    defined = True
                else:
                    # generic reg-imm mem ops touching obj regs
                    mm = re.match(rf"\S+, \[(r\d+), {IMM}\]$", op)
                    if mm and mm.group(1) in objregs:
                        is_write = m.startswith("str") or m.startswith("vstr")
                        kind = "SCALE-ACCESS" if int(mm.group(2), 0) == 0x1c else "OBJ+off"
                        hits.append((ins.address, name, kind,
                                     f"{'WRITE' if is_write else 'read'} [{mm.group(2)}]"))
                    else:
                        mm = re.match(r"\S+, \[(r\d+), r\d+\]$", op)
                        if mm and mm.group(1) in objregs:
                            hits.append((ins.address, name, "OBJ+regoff", "dynamic offset"))

        if rd and re.fullmatch(r"r\d+", rd) and not defined:
            regs[rd] = None
            objregs.discard(rd)

print(f"=== {len(hits)} sites ===")
byfn = collections.OrderedDict()
for a, fn, kind, det in sorted(hits):
    byfn.setdefault(fn, []).append((a, kind, det))
for fn, lst in byfn.items():
    flag = " <-- SCALE ACCESSED" if any("SCALE" in k for _, k, _ in lst) else ""
    print(f"\n{fn} ({len(lst)}x){flag}")
    for a, kind, det in lst:
        print(f"   {a:#09x} {kind:14s} {det}")

json.dump([{"insn": hex(a), "kind": k, "det": d, "func": fn} for a, fn, k, d in sorted(hits)],
          open("/home/z/my-project/work/singleton_xrefs.json", "w"), indent=1)
print("\nsaved /home/z/my-project/work/singleton_xrefs.json", file=sys.stderr)
