#!/usr/bin/env python3
"""Dump representative batch_info records and fit the engine structure:
[u16 self][30 attr bytes][u8][u32 N][N x 12B desc][P x 24B pairs][u32 X]
[seek X*desc0.f4][24B tail][seek table[kind]*count]
Goal: for each record find the pair count P and X that make the structure
consistent (and where the 24B tail lands within the 197B stride).
"""
import struct

ISLANDS = ("GothamCity", "GothamCity_Island2")
PICK = (0, 12, 23, 43, 76, 90, 97, 128, 141, 178)


def f32(rec, off):
    return struct.unpack_from("<f", rec, off)[0]


def dump(island, mids):
    d = open(f"/home/z/my-project/work/zone/{island}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    print(f"\n===== {island}: stride={stride} M={M}")
    for m in mids:
        if m >= M:
            continue
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        u16self = struct.unpack_from("<H", rec, 0)[0]
        N = struct.unpack_from("<I", rec, 33)[0]
        attrs = []
        for k in range(N):
            f0, f1, f2, f3, f4 = struct.unpack_from("<IHHHH", rec, 37 + 12 * k)
            attrs.append((f0, f1, f2, f3, f4))
        mask = 0
        for a in attrs:
            mask |= 1 << (a[1] & 0x1F)
        pstart = 37 + 12 * N
        print(f"-- m{m}: self={u16self} N={N} attrs={[(a[1], a[0], a[4]) for a in attrs]} "
              f"mask=0x{mask:05x} pop={bin(mask).count('1')} pop&0xFE={bin(mask & 0xFE).count('1')}")
        # print first floats at candidate pair slots
        s = []
        for slot in range(0, 5):
            o = pstart + 24 * slot
            if o + 24 <= len(rec):
                s.append(f"slot{k if False else slot}@{o}="
                         f"({f32(rec, o):.4g},{f32(rec, o+4):.4g},{f32(rec, o+8):.4g})|"
                         f"({f32(rec, o+12):.4g},{f32(rec, o+16):.4g},{f32(rec, o+20):.4g})")
        print("   " + "  ".join(s))
        # X candidates at pstart + 24*P for P in 2..5
        cands = []
        for P in range(2, 6):
            o = pstart + 24 * P
            if o + 4 <= len(rec):
                X = struct.unpack_from("<I", rec, o)[0]
                end = o + 4 + X * (attrs[0][4] if attrs else 24) + 24
                cands.append(f"P={P}:X={X},tail@{o+4+X*24},end={end}")
        print("   " + "  ".join(cands))


for isl in ISLANDS:
    dump(isl, PICK)
