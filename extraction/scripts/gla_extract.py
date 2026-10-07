#!/usr/bin/env python3
"""
TDKR (Gameloft 2012) .gla container extractor — private research use.

Container format (reverse-engineered, big-endian):
  u32[0]  build/tag (varies, unused)
  u32[1]  indexSize  = end of header+table+name-pool = data start
  u32[2]  tableBytes = (numEntries + 1) * 16
  u32[3]  numEntries
  then numEntries x 16B entries: [u32 offset][u32 size][u32 nameOff][u32 pad]
  then name pool: NUL-terminated names, alphabetical
  then contiguous chunk data; offsets are absolute from file start.
"""
import csv
import hashlib
import os
import shutil
import struct
import sys

BASE = "/home/z/my-project/work/TDKR_data/com.gameloft.android.AMAZ.GloftKRAS/files"
OUT = "/home/z/my-project/download/TDKR_assets"
RAW = os.path.join(OUT, "raw")
MANIFEST = os.path.join(OUT, "_manifest.csv")

MAGICS = [
    (b"PVR!", "pvr"),
    (b"PKM ", "pkm"),
    (b"OggS", "ogg"),
    (b"RIFF", "riff"),
    (b"\x89PNG", "png"),
    (b"DDS ", "dds"),
    (b"Vxvs", "vxa"),
    (b"ID3 ", "mp3"),
    (b"\xff\xfb", "mp3"),
    (b"KTX ", "ktx"),
    (b"\xabKTX", "ktx"),
]


def sniff(data: bytes):
    for m, ext in MAGICS:
        if data[: len(m)] == m:
            return ext
    if data[:2] in (b"\x78\x01", b"\x78\x9c", b"\x78\xda"):
        return "zlib"
    return "bin"


def sanitize(name: str) -> str:
    name = name.replace("\\", "/").split("/")[-1]
    return name.replace("..", "_").strip() or "unnamed"


def parse_archive(path):
    """Return (entries, pool) or raise. entries = list of (off, size, name)."""
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        if size < 16:
            raise ValueError(f"too small: {size}")
        tag, idx_size, table_bytes, n = struct.unpack(">IIII", fh.read(16))
        if table_bytes != (n + 1) * 16:
            raise ValueError(
                f"table check failed: tableBytes={table_bytes} n={n} (expected {(n+1)*16})"
            )
        table_end = 16 + n * 16
        if idx_size > size or table_end > idx_size:
            raise ValueError(f"index size mismatch: idx={idx_size} tableEnd={table_end} file={size}")
        entries = []
        for _ in range(n):
            off, sz, name_off, _pad = struct.unpack(">IIII", fh.read(16))
            entries.append([off, sz, name_off])
        pool = fh.read(idx_size - table_end)
        out = []
        for off, sz, name_off in entries:
            if name_off >= len(pool):
                out.append((off, sz, f"INVALID_{len(out)}"))
                continue
            end = pool.find(b"\x00", name_off)
            if end == -1:
                end = len(pool)
            out.append((off, sz, pool[name_off:end].decode("latin1")))
        return out


def main():
    archives = []
    for sub in ("data", "textures"):
        d = os.path.join(BASE, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".gla"):
                archives.append(os.path.join(d, fn))

    os.makedirs(RAW, exist_ok=True)
    rows = []
    stats = {}

    for path in archives:
        sub = os.path.basename(os.path.dirname(path))
        arch = os.path.splitext(os.path.basename(path))[0]
        outdir = os.path.join(RAW, arch)
        fsize = os.path.getsize(path)
        try:
            entries = parse_archive(path)
        except ValueError as e:
            print(f"[skip] {sub}/{arch}: {e}")
            continue

        n_types = {}
        contiguous = True
        prev_end = None
        os.makedirs(outdir, exist_ok=True)
        with open(path, "rb") as fh:
            for i, (off, sz, name) in enumerate(entries):
                if prev_end is not None and off != prev_end:
                    contiguous = False
                prev_end = off + sz
                if off + sz > fsize:
                    print(f"  [warn] {arch} entry {i} ({name}): off={off}+{sz} > filesize")
                    continue
                nm = sanitize(name)
                fh.seek(off)
                head = fh.read(16)
                ext = sniff(head)
                real_ext = ext if ext != "riff" else "wav"
                outname = nm if nm.lower().endswith("." + real_ext.lower()) else f"{nm}.{real_ext}"
                dst = os.path.join(outdir, outname)
                fh.seek(off)
                rem = sz
                with open(dst, "wb") as w:
                    while rem > 0:
                        buf = fh.read(min(1 << 20, rem))
                        if not buf:
                            break
                        w.write(buf)
                        rem -= len(buf)
                n_types[ext] = n_types.get(ext, 0) + 1
                rows.append({
                    "archive": arch,
                    "index": i,
                    "name": name,
                    "offset": off,
                    "size": sz,
                    "magic": ext,
                    "sha256_head16": hashlib.sha256(head).hexdigest()[:16],
                })
        stats[arch] = (len(entries), n_types, contiguous)
        tsum = ", ".join(f"{k}:{v}" for k, v in sorted(n_types.items()))
        print(f"[ok] {arch:24s} entries={len(entries):5d} contiguous={contiguous} types: {tsum}")

    with open(MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\ntotal chunks: {len(rows)}  ->  {RAW}")
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
