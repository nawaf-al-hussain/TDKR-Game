#!/usr/bin/env python3
"""Bit-level scan of batch_info records: find (bit_offset, width) fields whose
values are valid material indices (< n_mat) across ALL records."""
import struct
import numpy as np

def bits_of(d):
    return np.unpackbits(np.frombuffer(d, np.uint8), bitorder='little')

def scan(path, n_mat, n_bands=(9, 8)):
    d = open(path, 'rb').read()
    n = struct.unpack_from('<I', d, 0)[0]
    body = d[4:4 + n * ((len(d) - 4) // n)]
    rb = len(body) // n
    allbits = np.unpackbits(np.frombuffer(body, np.uint8), bitorder='little').reshape(n, rb * 8)
    print(f'{path}: {n} records x {rb}B = {rb*8} bits')
    found = []
    for width in (8, 9, 10, 12, 16):
        for boff in range(0, 96):
            vals = np.zeros(n, np.int64)
            ok = True
            for i in range(width):
                vals |= allbits[:, boff + i].astype(np.int64) << i
            if np.all(vals < n_mat) and len(np.unique(vals)) > 20:
                found.append((boff, width, len(np.unique(vals)), int(vals.min()), int(vals.max())))
    for f in found:
        print(f'  bit@{f[0]} w={f[1]} uniq={f[2]} range=[{f[3]},{f[4]}]')
    return found

scan('/home/z/my-project/work/zone/GothamCity/batch_info.bin', 307)
scan('/home/z/my-project/work/zone/GothamCity_Island2/batch_info.bin', 196)
