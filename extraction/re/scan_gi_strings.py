#!/usr/bin/env python3
"""
Scan GothamCity.lvc.bin for CComponentBaseGlobalIllum preset blocks.
All primitives big-endian (ReadInt/ReadFloat compose BE; ReadChar = 1 byte).
Strategy: find every length-prefixed inline string (u32 BE len + chars) that looks
like a texture name, then inspect the byte neighborhood for the GI signature:
  ... [3 strings] [4 x BE float atlas] [fogTex string] [2 x BE float] [RGBA] [3 x BE float] [RGBA]
Decode and report plausible fog values.
"""
import struct, re

PATH = "/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc.bin"
d = open(PATH, "rb").read()
DEF_START = 0x5EB80B  # definitions region (inline strings)

def be_f32(o):
    return struct.unpack_from(">f", d, o)[0]

def be_u32(o):
    return struct.unpack_from(">I", d, o)[0]

# --- enumerate length-prefixed strings in the definitions region ---
strings = []  # (offset_of_len, length, text)
i = DEF_START
n = len(d)
tex_re = re.compile(r"\.(tga|dds|png|jpg|bmp)$", re.I)
while i < n - 4:
    ln = be_u32(i)
    if 1 <= ln <= 256 and i + 4 + ln <= n:
        raw = d[i + 4: i + 4 + ln]
        if all(32 <= c < 127 for c in raw):
            s = raw.decode()
            strings.append((i, ln, s))
            i += 4 + ln
            continue
    i += 1

print(f"length-prefixed strings in definitions region: {len(strings)}")
tex = [(o, ln, s) for (o, ln, s) in strings if tex_re.search(s)]
print(f"texture-name strings: {len(tex)}")
for o, ln, s in tex:
    print(f"  @{o:#x} {s}")

# --- for each texture string, inspect neighborhood for GI signature ---
# fogTex string is preceded by 4 BE floats (atlas) and 3 strings; followed by 2 floats, RGBA, 3 floats, RGBA
print("\n=== GI-signature scan around texture strings ===")
for o, ln, s in tex:
    # try: this string is the fogTex (+0x50). Before it: 4 BE floats at o-16.
    atlas = [be_f32(o - 16 + 4 * k) for k in range(4)]
    after1 = [be_f32(o + 4 + ln + 4 * k) for k in range(2)]
    after2 = [be_f32(o + 4 + ln + 8 + 4 * k) for k in range(3)]
    print(f"\n@{o:#x} {s}")
    print(f"   atlas? {['%.6g' % v for v in atlas]}")
    print(f"   after x2: {['%.6g' % v for v in after1]}  x3: {['%.6g' % v for v in after2]}")
    rgba_after = d[o + 4 + ln + 16: o + 4 + ln + 20]
    print(f"   rgba@+16: {rgba_after.hex(' ')}")
