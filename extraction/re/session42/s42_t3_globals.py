#!/usr/bin/env python3
"""s42 T3: extract ALL (name, value) Lua globals registered by
CLuaScriptManager::RegisterScriptGlobalVariables @0x146db0 (4784 B, ARM).
Pattern per global: float setup (mov r1,#imm / movw+movt / ldr lit) ->
bl lua_pushnumber -> ldr rName,[pc]; add rName,pc,rName -> mov r2,rName ->
movw/movt r1,#0xd8ee/0xffff -> bl lua_setfield."""
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

FN, FSZ = 0x146DB0, 4784
insns = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(data[v2o(FN):v2o(FN) + FSZ], FN))

def f32(u):
    return struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]

globals_found = []
pending_raw = None      # raw 32-bit float bits
last_push = None
name_reg = {}
for k, ins in enumerate(insns):
    m, ops = ins.mnemonic, ins.op_str
    if m == "movt" and ops.startswith("r1, #") and pending_raw is not None:
        # mov r1,#lo ; movt r1,#hi  (float assembled in two steps)
        hi = int(ops[5:], 0)
        pending_raw = (hi << 16) | (pending_raw & 0xFFFF)
    elif m == "mov" and ops.startswith("r1, #"):
        try:
            pending_raw = int(ops[5:], 0)
        except ValueError:
            pass
    elif m == "movw" and ops.startswith("r1, #"):
        pending_raw = int(ops[5:], 0)
    elif m == "ldr" and ops.startswith("r1, [pc"):
        try:
            off = int(ops.split("#")[1].rstrip("]"), 0)
            lit = v2o(ins.address + 8 + off)
            if lit is not None:
                pending_raw = struct.unpack_from("<I", data, lit)[0]
        except Exception:
            pass
    elif m == "ldr" and ", [pc" in ops and not ops.startswith("r1"):
        d = ops.split(",")[0]
        try:
            off = int(ops.split("#")[1].rstrip("]"), 0)
            name_reg[d] = struct.unpack_from("<I", data, v2o(ins.address + 8 + off))[0]
        except Exception:
            name_reg.pop(d, None)
    elif m == "add" and ", pc, " in ops:
        d = ops.split(",")[0]
        src = ops.split(", ")[2]
        if src.startswith("#"):
            try:
                name_reg[d] = ins.address + 8 + int(src[1:], 0)
            except ValueError:
                pass
        elif d in name_reg or src in name_reg:
            base = name_reg.get(src, 0)
            name_reg[d] = ins.address + 8 + base
    elif m == "bl":
        try:
            tgt = int(ops.lstrip("#"), 0)
        except ValueError:
            tgt = None
        if tgt == 0xa499dc:      # lua_pushnumber
            last_push = f32(pending_raw) if pending_raw is not None else None
        elif tgt == 0xa49fc8:    # lua_setfield
            pass  # name resolved below via r2 tracking; simpler: match next mov r2,rX
    elif m == "mov" and ops.startswith("r2, r") and ops != "r2, r4":
        rX = ops[4:]
        if rX in name_reg and last_push is not None:
            addr = name_reg[rX]
            nm = cstr(addr)
            globals_found.append((nm, last_push, addr))
            last_push = None

print(f"extracted {len(globals_found)} globals from RegisterScriptGlobalVariables:")
MC = [g for g in globals_found if g[0] and g[0].startswith("MC_")]
for nm, v, addr in globals_found:
    star = "   <<<<<<" if nm and nm.startswith("MC_") else ""
    vs = f"{v:.6g}" if isinstance(v, float) else v
    print(f"  {nm!r:38s} = {vs}   (str@0x{addr:x}){star}")
print()
print("MC_* entries:")
for nm, v, addr in MC:
    print(f"  {nm} = {v!r}")
