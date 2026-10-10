#!/usr/bin/env python3
"""Session 16: locate the runtime material record array inside the compiled
bdae (little_endian_quantized.bdae) and dump it in array order.

Approach: material names sit in the string pool as [u32 len][chars]. Records
reference them by absolute offset (u32 LE). Find every pointer to a material
name string, dump the surrounding words, detect the record stride, then walk
the array.
"""
import re
import struct
import sys
import zipfile

ZONE = "/home/z/my-project/work/zone"


def strings_with_len(d):
    """[u32 len][chars] strings -> list of (content_off, s)."""
    out = []
    for m in re.finditer(rb"\x00\x00[\x20-\x7e][\x20-\x7e]", d):
        pass
    i = 0
    n = len(d)
    while i + 4 <= n:
        L = struct.unpack_from("<I", d, i)[0]
        if 4 <= L <= 64 and i + 4 + L <= n:
            s = d[i + 4:i + 4 + L]
            if all(0x20 <= c < 0x7f for c in s):
                out.append((i + 4, s.decode()))
                i += 4 + L + 1
                continue
        i += 1
    return out


def main():
    island = sys.argv[1] if len(sys.argv) > 1 else "GothamCity"
    variant = "little_endian_quantized.bdae"
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    d = z.read(variant)
    print(f"{island} {variant}: {len(d)} bytes")

    strs = strings_with_len(d)
    print(f"len-prefixed strings: {len(strs)}")
    mats = [(o, s) for o, s in strs
            if not s.startswith("#") and not s.startswith("image")
            and not s.startswith("ProfileCOMMON")]
    print(f"non-effect strings: {len(mats)}; first 10: {[s for _, s in mats[:10]]}")

    # pointers to material name content offsets
    ptrs = collections = {}
    ptr_list = []
    for off, s in mats:
        pat = struct.pack("<I", off)
        start = 0
        while True:
            j = d.find(pat, start)
            if j < 0:
                break
            ptr_list.append((j, off, s))
            start = j + 4
    print(f"u32 pointers to material names: {len(ptr_list)}")
    ptr_list.sort()
    for j, off, s in ptr_list[:12]:
        w = struct.unpack_from("<8I", d, max(0, j - 16))
        print(f"  ptr@{j:7d} -> {s[:40]:40s} ctxwords={[hex(x) for x in w]}")


if __name__ == "__main__":
    main()
