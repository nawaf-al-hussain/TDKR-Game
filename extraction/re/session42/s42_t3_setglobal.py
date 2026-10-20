#!/usr/bin/env python3
"""s42 T3b: all callers of CLuaScriptManager::SetGlobal(const char*, int, bool) @0x149178 —
resolve r1 (name) and r2 (value) per site."""
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

SETGLOBAL = 0x149178
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

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
sites = []
for i in range(0, len(td) - 4, 4):
    w = struct.unpack_from("<I", td, i)[0]
    if (w >> 24) == 0xEB:
        tgt = t + i + 8 + sext(w & 0xFFFFFF, 24) * 4
        if tgt == SETGLOBAL:
            sites.append(t + i)
print(f"SetGlobal(const char*, int, bool) direct call sites: {len(sites)}")

seen_fn = {}
for site in sites:
    fn = enc(site)
    seen_fn[fn] = seen_fn.get(fn, 0) + 1
print("by function:")
for fn, n in sorted(seen_fn.items(), key=lambda kv: -kv[1]):
    print(f"  {n:3d}x {fn}")

# for the top non-loop functions, resolve r1/r2 per site
print("\nper-site name/value resolution (functions with <20 sites):")
for site in sites:
    fn = enc(site)
    if seen_fn[fn] >= 20:
        continue
    lo = max(t, site - 0x100)
    insns = list(md.disasm(data[v2o(lo):v2o(lo) + (site - lo) + 4], lo))
    regs = {}
    name = None
    val = None
    for ins in insns:
        m, ops = ins.mnemonic, ins.op_str
        if m in ("mov", "mvn") and ops.count(",") == 1:
            d, s = [x.strip() for x in ops.split(",")]
            if s.startswith("#"):
                try:
                    v = int(s[1:], 0)
                    regs[d] = (~v) & 0xFFFFFFFF if m == "mvn" else v
                except ValueError:
                    pass
        elif m == "movt" and ops.count(",") == 1:
            d, s = [x.strip() for x in ops.split(",")]
            if s.startswith("#") and d in regs:
                try:
                    regs[d] = (int(s[1:], 0) << 16) | (regs[d] & 0xFFFF)
                except ValueError:
                    pass
        elif m == "ldr" and "[pc" in ops:
            d = ops.split(",")[0]
            try:
                off = int(ops.split("#")[1].rstrip("]"), 0)
                regs[d] = struct.unpack_from("<I", data, v2o(ins.address + 8 + off))[0]
            except Exception:
                regs.pop(d, None)
        elif m == "add" and ", pc, #" in ops:
            d, _, imm = [x.strip() for x in ops.split(",")]
            try:
                regs[d] = ins.address + 8 + int(imm[1:], 0)
            except ValueError:
                pass
        elif m == "add" and ops.count(",") == 3:
            d, s1, s2 = [x.strip() for x in ops.split(",")][:3]
            if s1 in regs and s2.startswith("#"):
                try:
                    regs[d] = regs[s1] + int(s2[1:], 0)
                except ValueError:
                    pass
    r1 = regs.get("r1")
    r2 = regs.get("r2")
    nm = cstr(r1) if isinstance(r1, int) else None
    extra = ""
    if isinstance(r1, int) and 0xb30000 <= r1 < 0xb32000:
        extra = "  <<<< POOL NAME"
    r1hex = f"0x{r1:x}" if isinstance(r1, int) else "None"
    print(f"  0x{site:x} in {fn[:60]}: name={nm!r} ({r1hex}) val={r2}{extra}")
