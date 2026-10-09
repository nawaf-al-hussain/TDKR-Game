#!/usr/bin/env python3
"""Restore the raw assets this project's scripts expect (sandbox was reset):
  - l_gothamcity.gla chunks -> raw/l_gothamcity/  (bdae files + city zips)
  - game_config.gla chunks  -> raw/game_config/   (GothamCity.lvc)
  - GothamCity*.zip         -> work/zone/         (batch_info.bin, lod_*.bin)
"""
import os
import struct
import sys
import zipfile

OBB = "/home/z/my-project/work/obb_extract/com.gameloft.android.AMAZ.GloftKRAS/files"
OUT = "/home/z/my-project/download/TDKR_assets"
RAW = os.path.join(OUT, "raw")
WORK = "/home/z/my-project/work"


def gla_entries(path):
    d = open(path, "rb").read(16)
    _, idx_size, table_bytes, n = struct.unpack(">IIII", d)
    f = open(path, "rb")
    f.seek(16)
    tbl = f.read(n * 16)
    pool_start = 16 + n * 16
    f.seek(pool_start)
    pool = f.read(idx_size - pool_start)
    f.close()
    out = []
    for i in range(n):
        off, sz, no, _ = struct.unpack(">IIII", tbl[i * 16:(i + 1) * 16])
        name = pool[no:pool.index(b"\0", no)].decode("ascii", "replace")
        out.append((name, off, sz))
    return out


def pull_chunks(gla_path, out_dir, prefix=None):
    os.makedirs(out_dir, exist_ok=True)
    ents = gla_entries(gla_path)
    n = 0
    f = open(gla_path, "rb")
    for name, off, sz in ents:
        if prefix and not name.startswith(prefix):
            continue
        base = name.split("/")[-1]
        f.seek(off)
        buf = f.read(sz)
        with open(os.path.join(out_dir, base), "wb") as g:
            g.write(buf)
        n += 1
    f.close()
    return n, len(ents)


if __name__ == "__main__":
    n, tot = pull_chunks(os.path.join(OBB, "data", "l_gothamcity.gla"),
                         os.path.join(RAW, "l_gothamcity"))
    print(f"l_gothamcity: pulled {n}/{tot} chunks")
    n, tot = pull_chunks(os.path.join(OBB, "data", "game_config.gla"),
                         os.path.join(RAW, "game_config"))
    print(f"game_config:  pulled {n}/{tot} chunks")

    # zone zips -> work/zone/<stem>/
    zdir = os.path.join(RAW, "l_gothamcity")
    for fn in sorted(os.listdir(zdir)):
        if fn.startswith("GothamCity") and fn.endswith(".zip"):
            stem = fn[:-4]
            dst = os.path.join(WORK, "zone", stem)
            os.makedirs(dst, exist_ok=True)
            with zipfile.ZipFile(os.path.join(zdir, fn)) as z:
                z.extractall(dst)
            print(f"{fn} -> {dst}: {len(os.listdir(dst))} files")
