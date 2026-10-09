#!/usr/bin/env python3
"""Probe batch_info.bin bitstream layout: [u32 N][N bit-packed records]."""
import struct, sys
import numpy as np

def probe(path):
    d = open(path, 'rb').read()
    n = struct.unpack_from('<I', d, 0)[0]
    body = d[4:]
    print(f'{path}: N={n} body={len(body)} bytes  ({len(body)/n:.2f} B/rec)')
    # dump first records as hex/words
    for rec in range(min(3, n)):
        base = 4 + rec * (len(body) // n)
        w = struct.unpack_from(f'<{min(40, (len(body)//n))//4}I', d, base)
        print(f' rec{rec} @0x{base:x}:', ' '.join(f'{x:08x}' for x in w[:24]))
    # Try bit-level: find candidate fields. Dump first 128 bytes as bits
    base = 4
    seg = d[base:base+96]
    lines = []
    for byte_row in range(0, 96, 16):
        chunk = seg[byte_row:byte_row+16]
        bits = ''.join(f'{b:08b}' for b in chunk)
        hx = ' '.join(f'{b:02x}' for b in chunk)
        lines.append(f'  +{byte_row:3d}  {hx}\n        {bits}')
    print('\n'.join(lines))

    # Hypothesis: record = fixed bit width; look for material index patterns.
    # Material count = 307 (island1) -> 9 bits needed. Search for u32-aligned
    # values < 307 in the stream.
    w = np.frombuffer(d[4:], '<u4')
    lt307 = w[w < 307]
    print(f'words < 307: {len(lt307)}/{len(w)}  first 40: {lt307[:40]}')
    lt16 = w[w < 16]
    print(f'words < 16: {len(lt16)}/{len(w)}')

if __name__ == '__main__':
    probe(sys.argv[1] if len(sys.argv) > 1 else
          '/home/z/my-project/work/zone/GothamCity/batch_info.bin')
