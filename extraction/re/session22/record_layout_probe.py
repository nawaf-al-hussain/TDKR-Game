#!/usr/bin/env python3
"""Static re-derivation of the batch_info.bin record layout from the
loadHeadersAndSkipData disassembly findings, cross-checked on real records.

Engine function (0x8e1d34) reads, from its file position:
  [u8][u32 N][N x 12B desc][N x 24B pairs][u32 X][seek X*desc0.f4][24B tail][seek table[kind]*count]
desc = {u32 f0; u16 f1(attr); u16 f2; u16 f3; u16 f4(stride)}
pair = (vec3f scale, vec3f offset)  -- scale FIRST.
Session-21 layout says records are: [u16 self][30 attr bytes][u8][u32 N]...
so the engine function is entered at record offset +32.
"""
import struct

for island in ("GothamCity", "GothamCity_Island2"):
    d = open(f"/home/z/my-project/work/zone/{island}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    print(f"\n=== {island}: file stride {stride}, {M} records (+{len(d)-4-stride*M} leftover)")
    rec = d[4 + stride * 90: 4 + stride * 91]
    print(f"-- m90 raw {len(rec)}B:")
    for off in range(0, min(len(rec), 200), 16):
        chunk = rec[off:off+16]
        hexs = " ".join(f"{b:02x}" for b in chunk)
        print(f"  {off:3d}: {hexs}")
    u16self = struct.unpack_from("<H", rec, 0)[0]
    print(f"  u16@0 = {u16self} (self-index?)")
    print(f"  u8@32 = {rec[32]}")
    N32 = struct.unpack_from("<I", rec, 33)[0]
    print(f"  u32@33 = {N32}")
    # engine: descriptors 12B from (33+4)=37
    base = 37
    for Ntry in range(1, 7):
        pstart = base + 12 * Ntry
        p00 = struct.unpack_from("<f", rec, pstart)[0]
        p120 = struct.unpack_from("<f", rec, pstart + 12)[0]
        print(f"  if N={Ntry}: pairs start {pstart}; pair0.scale.x={p00:.6g} pair0.offset.x={p120:.6g}")
    # first descriptor under N=4
    if N32 < 8:
        for k in range(min(N32, 6)):
            f0, f1, f2, f3, f4 = struct.unpack_from("<IHHHH", rec, 37 + 12 * k)
            print(f"  desc[{k}] @ {37+12*k}: f0={f0} f1={f1} f2={f2} f3={f3} f4={f4}")
    # tail: seek X*stride0 then 24B tail
    for Ntry in (4, 6):
        pstart = base + 12 * Ntry
        X = struct.unpack_from("<I", rec, pstart + 24 * Ntry)[0]
        print(f"  if N={Ntry}: X @ {pstart+24*Ntry} = {X}")
