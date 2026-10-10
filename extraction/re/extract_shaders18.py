#!/usr/bin/env python3
"""Session 18 — extract the GLSL technique sources from effects.gla.

effects.gla ships in the release zip (APK data/, NOT the OBB .gla set).
Container: the standard .gla layout (16B header + 16B/entry table + name
pool + chunks). The 8 techniques relevant to the city are banked into
extraction/re/shaders18/ (LightMapDC, LightmapVCBlendDC, StandardDiffuseDC,
SimpleModulateDC — fragment + vertex each).
"""
import os
import struct
import zipfile

SRC_ZIP = "/home/z/my-project/work/TDKR_APK_OBB.zip"
MEMBER = "com.gameloft.android.AMAZ.GloftKRAS/files/data/effects.gla"
OUT = os.path.join(os.path.dirname(__file__), "shaders18")
WANT = {"LightMapDC-f.glsl", "LightMapDC-v.glsl",
        "LightmapVCBlendDC-f.glsl", "LightmapVCBlendDC-v.glsl",
        "StandardDiffuseDC-f.glsl", "StandardDiffuseDC-v.glsl",
        "SimpleModulateDC-f.glsl", "SimpleModulateDC-v.glsl"}


def main():
    with zipfile.ZipFile(SRC_ZIP) as z:
        d = z.read(MEMBER)
    tag, index_size, table_bytes, n = struct.unpack(">4I", d[:16])
    entries = [struct.unpack_from(">4I", d, 16 + 16 * i) for i in range(n)]
    pool = d[16 + n * 16: index_size]
    os.makedirs(OUT, exist_ok=True)
    for off, size, name_off, _pad in entries:
        end = pool.find(b"\0", name_off)
        name = pool[name_off:end].decode("ascii", "replace")
        if name in WANT:
            open(os.path.join(OUT, name), "wb").write(d[off:off + size])
            print(name, size)


if __name__ == "__main__":
    main()
