#!/usr/bin/env python3
"""First-pass forensic scan of Gameloft .gla archives (TDKR) — partial streaming read from zip."""
import zipfile, struct, sys, collections

ZIP = "/home/z/my-project/download/TDKR/TDKR_v1.1.6b_APK_OBB.zip"
PREFIX = "com.gameloft.android.AMAZ.GloftKRAS/files/"

MAGICS = {
    b"\x89PNG": "PNG image",
    b"DDS ": "DDS texture",
    b"PVR\x03": "PVR v3 texture",
    b"PVR!": "PVR v2 texture",
    b"PKM ": "ETC1 texture",
    b"OggS": "OGG audio",
    b"RIFF": "RIFF (WAV)",
    b"ID3": "MP3",
    b"\xff\xfb": "MP3 frame",
    b"GLA\x00": "GLA magic",
    b"\x00ALG": "GLA magic rev",
    b"FSA\x00": "FSA magic",
    b"KRHP": "KRHP chunk",
    b"SKEL": "skeleton",
    b"MESH": "mesh chunk",
    b"TXTR": "texture chunk",
    b"SHDR": "shader chunk",
    b"ANIM": "anim chunk",
    b"HFST": "possible header",
    b"TFDA": "possible header rev",
}

def scan_member(zf, name, window_mb=12):
    """Read first window_mb MB and last 1MB of a member; report magic hits + header hex."""
    hits = collections.Counter()
    offsets = {}
    with zf.open(name) as f:
        window = f.read(window_mb * 1024 * 1024)
    for magic, label in MAGICS.items():
        idx = 0
        count = 0
        while True:
            idx = window.find(magic, idx)
            if idx == -1 or count >= 200:
                break
            hits[label] += 1
            if label not in offsets:
                offsets[label] = []
            if len(offsets[label]) < 5:
                offsets[label].append(idx)
            idx += 1
            count += 1
    return hits, offsets, window

def main():
    zf = zipfile.ZipFile(ZIP)
    targets = [
        PREFIX + "data/l_gothamcity.gla",
        PREFIX + "textures/l_gothamcity_tex.gla",
        PREFIX + "data/game_config.gla",
    ]
    for t in targets:
        try:
            info = zf.getinfo(t)
        except KeyError:
            print(f"MISSING: {t}")
            continue
        print(f"\n{'='*70}\n{t}\ncompressed={info.compress_size:,} raw={info.file_size:,}")
        hits, offsets, window = scan_member(zf, t)
        print("HEADER (first 96 bytes):")
        for row in range(6):
            chunk = window[row*16:(row+1)*16]
            hexs = " ".join(f"{b:02x}" for b in chunk)
            asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            print(f"  {row*16:06x}  {hexs:<48}  {asc}")
        print("MAGIC HITS (first 12MB):")
        for label, n in hits.most_common(12):
            offs = ",".join(f"0x{o:x}" for o in offsets.get(label, []))
            print(f"  {label:<18} x{n:<4} @ {offs}")
        # tail check (last 1MB)
        with zf.open(t) as f:
            f.seek(max(0, info.file_size - 1024*1024))
            tail = f.read()
        tail_hits = {lbl: tail.count(m) for m, lbl in MAGICS.items() if tail.count(m)}
        if tail_hits:
            print("TAIL HITS (last 1MB):", tail_hits)

if __name__ == "__main__":
    main()
