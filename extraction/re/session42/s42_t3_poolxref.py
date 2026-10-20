#!/usr/bin/env python3
"""s42 T3: find engine code that defines Lua globals from the MC_* name pool.
Scan for BL/BLX to lua_setfield/lua_pushnumber/luaL_register/lua_getfield and for
pc-relative `add rX, pc, #imm` whose target lands in the script-name pool region."""
import struct, bisect, subprocess
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

t = 0xa5d80; tsz = 10602256
td = data[v2o(t):v2o(t) + tsz]
def sext(v, b): return v - (1 << b) if v & (1 << (b - 1)) else v

TARGETS = {0xa49fc8: "lua_setfield", 0xa499dc: "lua_pushnumber", 0xa4b754: "luaL_register", 0xa49cf0: "lua_getfield"}
POOL_LO, POOL_HI = 0xb30500, 0xb31400

calls = []
for i in range(0, len(td) - 4, 4):
    w = struct.unpack_from("<I", td, i)[0]
    if (w >> 24) == 0xEB:
        tgt = t + i + 8 + sext(w & 0xFFFFFF, 24) * 4
        if tgt in TARGETS:
            calls.append((t + i, TARGETS[tgt]))

# symbol map for enclosing functions
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
        if v <= a < v + sz: return f"0x{v:x}+{sz} {n[:80]}"
    return "??"

print(f"setfield callers: {sum(1 for _, n in calls if n == 'lua_setfield')}, "
      f"pushnumber callers: {sum(1 for _, n in calls if n == 'lua_pushnumber')}, "
      f"getfield callers: {sum(1 for _, n in calls if n == 'lua_getfield')}, "
      f"luaL_register callers: {sum(1 for _, n in calls if n == 'luaL_register')}")

# for each setfield caller, check within-window pc-relative add into the pool
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
hits = []
for site, name in calls:
    if name != "lua_setfield":
        continue
    fn_start = None
    i = bisect.bisect_right(starts, site) - 1
    if i >= 0 and syms[i][0] <= site < syms[i][0] + syms[i][1]:
        fn_start = syms[i][0]
    lo = max(0, site - 0x180)
    o = v2o(lo)
    insns = list(md.disasm(data[o:o + (site - lo) + 8], lo))
    for k, ins in enumerate(insns):
        if ins.mnemonic == "add" and "pc" in ins.op_str:
            # add rX, pc, #imm
            parts = ins.op_str.split(", ")
            if len(parts) == 3 and parts[1] == "pc" and parts[2].startswith("#"):
                try:
                    imm = int(parts[2][1:], 0)
                except ValueError:
                    continue
                tgt = ins.address + 8 + imm
                if POOL_LO <= tgt < POOL_HI:
                    hits.append((site, ins.address, tgt))
for site, iadr, tgt in hits:
    print(f"POOL-REF: setfield call @0x{site:x} <- add pc @0x{iadr:x} -> 0x{tgt:x}")
    print(f"   in {enc(site)}")
if not hits:
    print("NO pc-relative pool refs within 0x180 before any setfield call")

# also scan the WHOLE text for pc-relative adds into the pool (any function)
allhits = []
for i in range(0, len(td) - 4, 4):
    w = struct.unpack_from("<I", td, i)[0]
    # ARM add rX, pc, rY is `add rd, pc, #imm` = cond 0010 100F rd pc rot8imm — immediate form: bits27-25=001, U=1, S=0, Rn=15
    if (w & 0x0FF00000) == 0x028F0000:
        imm12 = w & 0xFFF
        rot = (w >> 8) & 0xF
        imm = (imm12 >> (2 * rot)) | (imm12 << (32 - 2 * rot)) if rot else imm12
        imm &= 0xFFFFFFFF
        tgt = t + i + 8 + imm
        if POOL_LO <= tgt < POOL_HI:
            allhits.append((t + i, tgt))
print(f"\nALL pc-relative adds into pool region across .text: {len(allhits)}")
for a, tv in allhits[:20]:
    print(f"  add pc @0x{a:x} -> 0x{tv:x}   in {enc(a)}")
