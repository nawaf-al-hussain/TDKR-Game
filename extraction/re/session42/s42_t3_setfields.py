#!/usr/bin/env python3
"""s42 T3: enumerate engine-defined Lua globals from lua_setfield call sites.
Single-float Lua build: lua_pushnumber(L, float) -> number in r1 (32-bit float).
lua_setfield(L, idx, k) -> r0=L, r1=idx (globals: -10002 = 0xFFFFD8EE), r2=name.
Per setfield site: linear scan of the preceding window with simple reg dataflow;
record the nearest preceding lua_pushnumber's r1 (float bits) as the value."""
import struct, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = "/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so"
data = open(SO, "rb").read()
e_phoff = struct.unpack_from("<I", data, 0x1C)[0]
e_phentsize = struct.unpack_from("<H", data, 0x2A)[0]
e_phnum = struct.unpack_from("<H", data, 0x2C)[0]
segs = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _pa, p_filesz, _m = struct.unpack_from("<6I", data, off)
    if p_type == 1: segs.append((p_vaddr, p_offset, p_filesz))
def v2o(v):
    for va, o, sz in segs:
        if va <= v < va + sz: return o + (v - va)
    return None
def cstr(v, m=64):
    o = v2o(v)
    if o is None: return None
    e = data.find(b"\0", o, o + m)
    if e < 0: return None
    try: return data[o:e].decode("ascii")
    except: return None

t = 0xa5d80; tsz = 10602256
td = data[v2o(t):v2o(t) + tsz]
def sext(v, b): return v - (1 << b) if v & (1 << (b - 1)) else v

SETFIELD, PUSHNUM = 0xa49fc8, 0xa499dc
sites = []
for i in range(0, len(td) - 4, 4):
    w = struct.unpack_from("<I", td, i)[0]
    if (w >> 24) == 0xEB:
        tgt = t + i + 8 + sext(w & 0xFFFFFF, 24) * 4
        if tgt == SETFIELD:
            sites.append(t + i)

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
syms = []
for line in open("/tmp/krhp_syms.txt"):
    p = line.split()
    if len(p) >= 8 and p[3] == "FUNC":
        try: v, sz = int(p[1], 16), int(p[2])
        except: continue
        if sz > 0: syms.append((v, sz, p[7]))
syms.sort()
starts = [s[0] for s in syms]
def enc(a):
    i = bisect.bisect_right(starts, a) - 1
    if i >= 0:
        v, sz, n = syms[i]
        if v <= a < v + sz: return n[:70]
    return "??"

GLOBALS = 0xFFFFD8EE  # -10002
out = []
for site in sites:
    lo = max(t, site - 0x140)
    o = v2o(lo)
    insns = list(md.disasm(data[o:o + (site - lo) + 4], lo))
    regs = {}
    last_pn = None   # (site_addr, r1_value)
    res = None
    for ins in insns:
        m, ops = ins.mnemonic, ins.op_str
        if m == "bl":
            try:
                tgt = int(ops.lstrip("#"), 0)
            except ValueError:
                tgt = None
            if tgt == PUSHNUM:
                last_pn = (ins.address, regs.get("r1"))
            elif tgt == SETFIELD:
                r1v = regs.get("r1")
                r2v = regs.get("r2")
                nm = cstr(r2v) if isinstance(r2v, int) else None
                res = (site, r1v, nm, last_pn)
        elif m in ("mov", "mvn") and ops.count(",") == 1:
            d, s = [x.strip() for x in ops.split(",")]
            if s.startswith("#"):
                try:
                    v = int(s[1:], 0)
                    regs[d] = (~v) & 0xFFFFFFFF if m == "mvn" else v
                except ValueError:
                    pass
        elif m == "ldr" and "[pc" in ops:
            try:
                d = ops.split(",")[0]
                off = int(ops.split("#")[1].rstrip("]"), 0)
                lit = ins.address + 8 + off
                wo = v2o(lit)
                if wo is not None:
                    regs[d] = struct.unpack_from("<I", data, wo)[0]
            except Exception:
                pass
        elif m == "add" and ", pc, #" in ops:
            d, _, imm = [x.strip() for x in ops.split(",")]
            try:
                regs[d] = ins.address + 8 + int(imm[1:], 0)
            except ValueError:
                pass
        elif m in ("ldr", "mov", "add") and "," in ops:
            d = ops.split(",")[0].strip()
            regs.pop(d, None)  # conservative invalidate on complex defs
    if res:
        out.append(res)

print(f"analyzed setfield sites with resolvable args: {len(out)}/{len(sites)}")
for site, r1v, nm, pn, in sorted(out):
    tag = "GLOBAL" if r1v == GLOBALS else (f"idx={r1v}" if isinstance(r1v, int) else "idx=?")
    val = None
    if pn and isinstance(pn[1], int):
        val = struct.unpack("<f", struct.pack("<I", pn[1]))[0]
    print(f"setfield@0x{site:x} [{tag}] name={nm!r} pushnum={val} pn@0x{pn[0]:x}" if pn else
          f"setfield@0x{site:x} [{tag}] name={nm!r} pushnum=None fn={enc(site)}")
