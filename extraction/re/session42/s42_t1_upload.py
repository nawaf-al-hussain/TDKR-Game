#!/usr/bin/env python3
"""s42 T1: find glTexImage2D call sites in libKRHP.so; report enclosing fn + GL format/type constants."""
import struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

SO = "/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so"
data = open(SO, "rb").read()

# --- ELF basics ---
e_shoff = struct.unpack_from("<I", data, 0x20)[0]
e_shentsize = struct.unpack_from("<H", data, 0x2E)[0]
e_shnum = struct.unpack_from("<H", data, 0x30)[0]
e_shstrndx = struct.unpack_from("<H", data, 0x32)[0]
shs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from("<10I", data, off)
    shs.append(dict(name=name, typ=typ, addr=addr, offset=offset, size=size, link=link, entsize=entsize))
shstr = shs[e_shstrndx]
def sname(n):
    end = data.find(b"\0", shstr["offset"] + n)
    return data[shstr["offset"] + n:end].decode()
for s in shs: s["nm"] = sname(s["name"])
sec = {s["nm"]: s for s in shs}

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

# --- dynamic symbols + rel.plt: find glTexImage2D GOT slot ---
dynsym = sec[".dynsym"]; dynstr = sec[".dynstr"]
def symname(idx):
    off = dynstr["offset"] + idx
    end = data.find(b"\0", off)
    return data[off:end].decode()
nsyms = dynsym["size"] // 16
gots = {}
for i in range(nsyms):
    st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack_from("<IIIBBH", data, dynsym["offset"] + i * 16)
    n = symname(st_name)
    if n in ("glTexImage2D", "glTexSubImage2D"):
        gots[n] = st_value  # GOT slot vaddr (for UND symbols via R_ARM_JUMP_SLOT)
print("GOT slots:", {k: hex(v) for k, v in gots.items()})

# --- PLT stubs: scan .plt for loads of these GOT addrs ---
plt = sec[".plt"]
plt_data = data[plt["offset"]:plt["offset"] + plt["size"]]
md_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md_thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
stubs = {}
insns_arm = list(md_arm.disasm(plt_data, plt["addr"]))
for ins in insns_arm:
    if ins.mnemonic == "ldr" and "]" in ins.op_str and "#" in ins.op_str:
        # ldr rX, [pc, #imm] -> compute target; match later via GOT value in literal? simpler: emulate below
        pass
# Robust approach: walk PLT as 12-byte Thumb stubs? Try both: find word equals GOT addr in plt literal windows
for name, got in gots.items():
    hits = []
    # search .plt bytes for pattern ldr rX, [pc, #imm] pointing at a literal containing got
    for i in range(0, len(plt_data) - 16, 4):
        word = struct.unpack_from("<I", plt_data, i)[0]
        # thumb plt stub: e59fC000 ldr ip,[pc,#..] ; e12fff1c bx ip ; <gotaddr>
        if plt_data[i:i+4] == b"\x1c\xff\x2f\xe1" or plt_data[i:i+4] == b"\x00\xc0\x9f\xe5":
            continue
    # fallback: literal scan
    for i in range(0, len(plt_data) - 4, 4):
        word = struct.unpack_from("<I", plt_data, i)[0]
        if word == got:
            hits.append(plt["addr"] + i)
    stubs[name] = hits
print("PLT literal slots:", {k: [hex(x) for x in v] for k, v in stubs.items()})

# A PLT stub is: (stub_start) b/pld stuff then ldr pc,[ip,...]... ARM PLT: add ip, pc, #..; add ip, ip, #..; ldr pc, [ip, #..]!
# The GOT addr literal usually sits INSIDE the plt after 'ldr pc,[ip,#imm]' using precomputed offsets.
# Simplify: PLT entry for jump-slot N (0-based among R_ARM_JUMP_SLOT rels in order) = plt.addr + 20 + N*12 (ARM) — but let's just scan .text for bl to candidate ranges after computing entries properly below.
# --- Parse .rel.plt order ---
relplt = sec.get(".rel.plt")
if relplt:
    symentries = []
    for i in range(relplt["size"] // 8):
        r_offset, r_info = struct.unpack_from("<II", data, relplt["offset"] + i * 8)
        symidx = r_info >> 8
        nm = symname(struct.unpack_from("<I", data, dynsym["offset"] + symidx * 16)[0])
        symentries.append((r_offset, nm))
    plt_base = plt["addr"]
    for idx, (gotv, nm) in enumerate(symentries):
        if nm in ("glTexImage2D", "glTexSubImage2D"):
            stub = plt_base + 20 + idx * 12
            print(f"{nm}: rel.idx={idx} got={hex(gotv)} plt_stub={hex(stub)}")
