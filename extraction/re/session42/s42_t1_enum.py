#!/usr/bin/env python3
"""s42 T1: dump glitch E_PIXEL_FORMAT enum name table + GL constants near glTexImage2D call sites."""
import struct, sys, subprocess

SO = "/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so"
data = open(SO, "rb").read()

# --- ELF: build vaddr->file offset map from program headers (32-bit LE) ---
e_phoff = struct.unpack_from("<I", data, 0x1C)[0]
e_phentsize = struct.unpack_from("<H", data, 0x2A)[0]
e_phnum = struct.unpack_from("<H", data, 0x2C)[0]
segs = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _pa, p_filesz, _memsz = struct.unpack_from("<6I", data, off)
    if p_type == 1:  # PT_LOAD
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(vaddr):
    for v, o, sz in segs:
        if v <= vaddr < v + sz:
            return o + (vaddr - v)
    return None

def cstr(vaddr, maxlen=32):
    o = v2o(vaddr)
    if o is None: return None
    end = data.find(b"\0", o, o + maxlen)
    if end < 0: return None
    s = data[o:end]
    try: return s.decode("ascii")
    except: return None

print("=== E_PIXEL_FORMAT name table (glitch::video::getStringsInternal) @0xbca67c ===")
base = 0xbca67c
o = v2o(base)
n_entries = 208 // 4
for i in range(n_entries):
    ptr = struct.unpack_from("<I", data, o + i * 4)[0]
    name = cstr(ptr)
    mark = ""
    if i == 0x15: mark = "   <=== 0x15 (the RGB888 header code)"
    if i == 0x1D: mark = "   <=== 0x1D=29 (ETC1 per prior sessions)"
    if name:
        print(f"  [{i:2d}] 0x{i:02x}  {name!r}{mark}")
    else:
        print(f"  [{i:2d}] 0x{i:02x}  (null/terminator){mark}")
    if name is None and i > 0x25: break
