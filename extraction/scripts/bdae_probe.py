#!/usr/bin/env python3
"""BDAE (BRES) structure probe — classifies byte regions to locate vertex/index buffers.

Region classification per 16-byte block:
  F = float-plausible (>=75% dwords decode to f32 in [-4000,4000] with sane exponents)
  I = small-uint   (>=75% dwords < 0x10000, non-zero)
  Z = zeros        (all zero)
  A = ascii        (>=50% printable)
  ? = mixed/binary
"""
import struct, sys, os

def classify_block(blk):
    n = len(blk) // 4
    if n == 0:
        return '?'
    zeros = floats = smalls = 0
    for i in range(n):
        dw = struct.unpack_from('<I', blk, i*4)[0]
        f = struct.unpack_from('<f', blk, i*4)[0]
        if dw == 0:
            zeros += 1
        elif abs(f) < 4000 and (f == 0.0 or 1e-6 < abs(f) < 1e6):
            floats += 1
        elif dw < 0x10000:
            smalls += 1
    if zeros == n:
        return 'Z'
    if floats >= n * 0.75:
        return 'F'
    if smalls + zeros >= n * 0.9:
        return 'I'
    printable = sum(1 for b in blk if 32 <= b < 127 or b in (9, 10, 13, 0))
    if printable >= len(blk) * 0.6:
        return 'A'
    return '?'

def probe(path):
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    print(f'== {os.path.basename(path)}  size={len(d):#x} ({len(d)})')
    print(f'   hdr: ver={h[1]:#x} root@={h[2]:#x} strcount={h[4]} | sec: '
          f'h5={h[5]:#x} h6={h[6]:#x} h7={h[7]:#x} h8={h[8]:#x} h9={h[9]:#x} '
          f'hA={h[10]:#x} hB={h[11]:#x} hC={h[12]:#x} hD={h[13]:#x}')
    # region map
    blocks = []
    for off in range(0x3c, len(d) - 15, 16):
        c = classify_block(d[off:off+16])
        if blocks and blocks[-1][2] == c and off == blocks[-1][1]:
            blocks[-1][1] = off + 16
        else:
            blocks.append([off, off + 16, c])
    # merge tiny islands into neighbors for readability (keep F/I distinct)
    merged = []
    for b in blocks:
        if merged and (b[1] - b[0]) <= 32 and merged[-1][2] == b[2]:
            merged[-1][1] = b[1]
        else:
            merged.append(b)
    out = []
    for s, e, c in merged:
        if e - s >= 48 or c in 'FA':
            out.append(f'     {s:06x}-{e:06x} ({e-s:6d}B) {c}')
    print('\n'.join(out))

if __name__ == '__main__':
    base = '/home/z/my-project/download/TDKR_assets/raw'
    files = sys.argv[1:] or [
        f'{base}/l_gothamcity/GC_Bigbridge.bdae.bin',
        f'{base}/l_gothamcity/GC_Prop_Tree_07_S_Collision.bdae.bin',
        f'{base}/l_gothamcity/GC_island1_LongDist.bdae.bin',
        f'{base}/actors/batman.bdae.bin',
        f'{base}/actors/Batarang.bdae.bin',
        f'{base}/l_gothamcity/GC_Footprint_LE_Reflections.bdae.bin',
    ]
    for f in files:
        probe(f)
