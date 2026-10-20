#!/usr/bin/env python3
"""s42 T3d: ordered static decode of RegisterScriptGlobalVariables (0x146db0, 4784 B).
Segments: (1) SetGlobal(name, -1) x2; (2) SetGlobal(name, 1<<i) flag loop;
(3) SetGlobal(name, j) sequential loop; (4) push(value)+setfield(GLOBALS,name) pairs.
Per setfield: window-local back-scan -> nearest push-like bl = value; nearest
`mov r2, rX` -> resolve rX via last ldr-lit + add-pc in the same window."""
import struct
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
    try:
        s = data[o:e].decode("ascii")
        return s if s and all(32 <= ord(c) < 127 for c in s) else None
    except Exception:
        return None

FN, FSZ = 0x146DB0, 4784
insns = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(data[v2o(FN):v2o(FN) + FSZ], FN))
def f32(u): return struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]

# collect events in order
events = []   # (idx, 'setglobal'|'setfield'|'push', addr, aux)
for k, ins in enumerate(insns):
    if ins.mnemonic == "bl":
        try: tgt = int(ins.op_str.lstrip("#"), 0)
        except ValueError: continue
        if tgt == 0x149178: events.append((k, 'setglobal', ins.address, None))
        elif tgt == 0xa49fc8: events.append((k, 'setfield', ins.address, None))
        elif tgt == 0xa499dc: events.append((k, 'push', ins.address, 'num'))
        elif tgt == 0xa49e48: events.append((k, 'push', ins.address, 'table'))
        elif tgt == 0xa49e94 or tgt == 0xa49fb8 or tgt == 0xa49cd8:
            events.append((k, 'push', ins.address, 'str'))

def resolve_reg(insns, k, reg, lo_bound):
    """walk back from insn k to lo_bound tracking reg via ldr-lit / add-pc / movt."""
    val = None
    for j in range(k, lo_bound, -1):
        ins = insns[j]
        m, ops = ins.mnemonic, ins.op_str
        if m == "add" and ops.startswith(f"{reg}, pc, "):
            src = ops.split(", ")[2]
            base = 0
            if src.startswith("#"):
                base = int(src[1:], 0)
            elif src == reg and val is not None:
                base = val
            else:
                base = val if val is not None else 0
            val = ins.address + 8 + base
            return val
        if m == "ldr" and ops.startswith(f"{reg}, [pc"):
            off = int(ops.split("#")[1].rstrip("]"), 0)
            val = struct.unpack_from("<I", data, v2o(ins.address + 8 + off))[0]
            return val  # direct literal (absolute or offset; caller checks string)
        if m in ("mov", "movt") and ops.startswith(f"{reg}, #"):
            v = int(ops.split("#")[1], 0)
            if m == "movt":
                val = (v << 16) | (val if val is not None else 0)
            else:
                val = v
            return val
    return val

results = []
last_setfield_k = None
for k, kind, addr, aux in events:
    if kind == 'setfield':
        lo = last_setfield_k if last_setfield_k is not None else 0
        # value: nearest push in (lo, k)
        val_kind, val_raw = None, None
        for j in range(k - 1, lo, -1):
            ins = insns[j]
            if ins.mnemonic == "bl":
                try: tgt = int(ins.op_str.lstrip("#"), 0)
                except ValueError: continue
                if tgt == 0xa499dc:
                    val_kind = 'num'
                    # find r1 setup between this bl and the setfield: nearest mov/movw/movt/ldr r1 before j
                    val_raw = resolve_reg(insns, j - 1, 'r1', lo)
                    break
                elif tgt == 0xa49e48:
                    val_kind = 'table'
                    break
                elif tgt in (0xa49e94, 0xa49fb8, 0xa49cd8):
                    val_kind = 'str'
                    break
        # name: nearest `mov r2, rX` before k (within window), then resolve rX in window
        nm = None
        for j in range(k - 1, lo, -1):
            ins = insns[j]
            if ins.mnemonic == "mov" and ins.op_str.startswith("r2, r") and ins.op_str != "r2, r4":
                rX = ins.op_str[4:]
                a = resolve_reg(insns, j - 1, rX, lo)
                if isinstance(a, int):
                    nm = cstr(a)
                    if nm:
                        results.append((addr, 'setfield', nm, val_kind, f32(val_raw) if val_raw is not None else None, a))
                        break
                    else:
                        results.append((addr, 'setfield', None, val_kind, None, a))
                        break
        last_setfield_k = k
    elif kind == 'setglobal':
        lo = last_setfield_k if last_setfield_k is not None else 0
        # r1 = name (resolve), r2 = value
        nmr = resolve_reg(insns, k - 1, 'r1', lo)
        vr = resolve_reg(insns, k - 1, 'r2', lo)
        nm = cstr(nmr) if isinstance(nmr, int) else None
        results.append((addr, 'setglobal', nm, 'int', vr, nmr))

print(f"ordered registration events: {len(results)}")
for addr, kind, nm, vk, vv, raw in results:
    vv = f"{vv:.6g}" if isinstance(vv, float) else vv
    print(f"  0x{addr:06x} {kind:9s} {nm!r:42s} = {vv!r} [{vk}]")
mc = [r for r in results if r[2] and r[2].startswith("MC_")]
print("\nMC_*:")
for addr, kind, nm, vk, vv, raw in mc:
    print(f"  0x{addr:06x} {kind} {nm} = {vv!r} [{vk}] (str@0x{raw:x})")
