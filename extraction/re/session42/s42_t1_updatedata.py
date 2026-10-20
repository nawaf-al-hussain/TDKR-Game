#!/usr/bin/env python3
"""s42 T1: disassemble CCommonGLDriver::CTexture::updateData (0x7e7ea0, 1520 B, ARM) around glTexImage2D @0x7e827c."""
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

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
va, sz = 0x7E7EA0, 1520
o = v2o(va)
insns = list(md.disasm(data[o:o + sz], va))
idx_of = {ins.address: k for k, ins in enumerate(insns)}

# call site at 0x7e827c: dump the whole switch region 0x7e7f00..0x7e82c0
print("### updateData: full flow 0x7e7f58-0x7e82a0 (compressed out where linear)")
prev = None
for k, ins in enumerate(insns):
    a = ins.address
    if not (0x7e7f58 <= a < 0x7e82a4):
        continue
    # print only: cmp/mov-imm/ldr-literal/branchy
    keep = (ins.mnemonic.startswith("cmp") or ins.mnemonic.startswith("mov") or
            ins.mnemonic.startswith("ldr") or ins.mnemonic.startswith("b") or
            ins.mnemonic in ("bl", "blx") or ins.mnemonic.startswith("and") or
            ins.mnemonic.startswith("add") and ("pc" in ins.op_str or "lsl" in ins.op_str))
    if keep:
        print(f"0x{a:06x}: {ins.mnemonic}\t{ins.op_str}")

print("\n### GL constants in this function's literal pool words:")
# scan function bytes for GL constant words
words = range(o, o + sz - 3)
GL = {0x1907: "GL_RGB", 0x1908: "GL_RGBA", 0x80E0: "GL_BGR_EXT", 0x80E1: "GL_BGRA_EXT",
      0x1401: "GL_UNSIGNED_BYTE", 0x1902: "GL_RED??(0x1902=GL_2BYTES legacy)", 0x1906: "GL_ALPHA",
      0x1903: "GL_RGB_LEGACY?", 0x1909: "GL_LUMINANCE", 0x190A: "GL_LUMINANCE_ALPHA",
      0x80E1: "GL_BGRA"}
for w in words:
    val = struct.unpack_from("<I", data, w)[0]
    if val in GL:
        print(f"  @file 0x{w:x} (vaddr ~0x{v2o and (w - o + va):x}): 0x{val:04x} = {GL[val]}")
