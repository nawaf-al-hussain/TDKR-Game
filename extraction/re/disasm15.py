#!/usr/bin/env python3
"""A32 disasm toolchain v15: symbol-annotated, literal-pool xref aware.

- funcs map from .symtab (addr -> (size, name))
- literal_scan(va): functions whose literal pools contain `va`
- dis(addr, n): annotated ARM disassembly (bl/jal targets -> symbol names,
  ldr rX,[pc,#imm] -> pool word + symbol if it looks like a VA/string)
"""
import re
import struct
import subprocess

import capstone

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
_data = open(SO, "rb").read()

_secs = []
for ln in subprocess.run(["readelf", "-SW", SO], capture_output=True,
                         text=True).stdout.splitlines():
    m = re.match(r"\s*\[\s*\d+\]\s+(\S+)\s+\S+\s+([0-9a-f]+)\s+([0-9a-f]+)"
                 r"\s+([0-9a-f]+)", ln)
    if m:
        _secs.append((m.group(1), int(m.group(2), 16), int(m.group(3), 16),
                      int(m.group(4), 16)))


def v2f(va):
    for nm, addr, off, size in _secs:
        if nm == ".text" and addr <= va < addr + size:
            return off + (va - addr)
    for nm, addr, off, size in _secs:
        if addr and off and addr <= va < addr + size:
            return off + (va - addr)
    raise ValueError(hex(va))


def f2v(off):
    for nm, addr, foff, size in _secs:
        if foff and foff <= off < foff + size:
            return addr + (off - foff)
    raise ValueError(hex(off))


FUNCS = {}
for ln in subprocess.run(["readelf", "-sW", SO], capture_output=True,
                         text=True).stdout.splitlines():
    m = re.match(r"\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)", ln)
    if m:
        FUNCS[int(m.group(1), 16)] = (int(m.group(2)), m.group(3))

_FUNC_ADDRS = sorted(FUNCS.keys())


def func_of(va):
    import bisect
    i = bisect.bisect_right(_FUNC_ADDRS, va) - 1
    if i >= 0:
        a = _FUNC_ADDRS[i]
        sz, nm = FUNCS[a]
        if va < a + max(sz, 4):
            return a, nm
    return None, None


def short(nm, n=64):
    nm = nm.replace("_ZN", "").replace("_ZThn", "Thn").replace("_ZNS", "std::")
    return nm[:n]


md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
md.detail = True


def dis(va, size, title=""):
    """Disassemble [va, va+size), annotate bl targets and pc-relative pools."""
    print(f"\n===== {title} @ {va:#x} ({size} B) =====")
    off = v2f(va)
    code = _data[off:off + size]
    for ins in md.disasm(code, va):
        line = f"  {ins.address:08x}: {ins.mnemonic:<8}{ins.op_str}"
        ann = []
        if ins.mnemonic in ("bl", "blx"):
            try:
                t = int(ins.op_str.lstrip("#"), 16)
            except ValueError:
                t = None
            if t is not None:
                a, nm = func_of(t)
                ann.append("-> " + (short(nm) if nm else hex(t)))
        # pc-relative loads: annotate pool content
        if ins.mnemonic.startswith("ldr") and "[pc" in ins.op_str:
            m = re.search(r"\[pc,\s*#(\d+)\]", ins.op_str)
            if m:
                pcv = ins.address + 8 + int(m.group(1))
                try:
                    pw = struct.unpack_from("<I", _data, v2f(pcv))[0]
                except Exception:
                    pw = None
                if pw is not None:
                    a, nm = func_of(pw)
                    tag = f"pool@{pcv:x}={pw:#x}"
                    if nm:
                        tag += f" <{short(nm, 48)}>"
                    ann.append(tag)
        if ann:
            line += "   ; " + " | ".join(ann)
        print(line)


def literal_scan(va, limit=40):
    """Find functions whose literal pools contain the 4-byte value va."""
    pat = struct.pack("<I", va)
    hits = []
    start = 0
    while True:
        i = _data.find(pat, start)
        if i < 0:
            break
        start = i + 1
        try:
            code_va = f2v(i)
        except ValueError:
            continue
        a, nm = func_of(code_va)
        if nm:
            hits.append((code_va, a, nm))
    print(f"\nliteral-pool refs to {va:#x}: {len(hits)}")
    seen = {}
    for code_va, a, nm in hits:
        seen.setdefault((a, nm), []).append(code_va)
    for (a, nm), locs in sorted(seen.items())[:limit]:
        print(f"  func {a:#x} {short(nm, 80)}  pool@{[hex(x) for x in locs]}")
    return seen


if __name__ == "__main__":
    import sys
    # CLevelStreaming_DB::Load — the orchestrator (symtab-true)
    for a, (sz, nm) in FUNCS.items():
        if "CLevelStreaming_DB" in nm and "4Load" in nm:
            dis(a, min(sz, 1400), "CLevelStreaming_DB::Load")
            break
