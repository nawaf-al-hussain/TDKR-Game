#!/usr/bin/env python3
"""Decode batch_info.bin: [u32 N][N x 307B records].
Find the material-index field per record by scanning for stable small values."""
import struct, sys
import numpy as np

def decode(path, n_mat):
    d = open(path, 'rb').read()
    n = struct.unpack_from('<I', d, 0)[0]
    body = d[4:]
    rb = len(body) // n
    print(f'{path}: N={n} rec_bytes={rb}')
    recs = np.frombuffer(body[:n*rb], np.uint8).reshape(n, rb)
    # candidate u16 fields: value < n_mat at every record
    u16 = recs.view('<u2')
    cols = u16.shape[1]
    cand = []
    for c in range(cols):
        col = u16[:, c].astype(np.int64)
        if np.all(col < n_mat) and np.any(col > 0):
            cand.append((c, int(col.min()), int(col.max())))
    print('u16 columns always < n_mat:', cand[:30])
    # u32 candidates
    u32 = recs.view('<u4')
    cand32 = []
    for c in range(u32.shape[1]):
        col = u32[:, c].astype(np.int64)
        if np.all(col < n_mat) and np.any(col > 0):
            cand32.append((c, int(col.min()), int(col.max())))
    print('u32 columns always < n_mat:', cand32[:30])
    # distribution of the most material-like column
    if cand:
        c = cand[0][0]
        col = u16[:, c]
        import collections
        cnt = collections.Counter(col.tolist())
        print(f'column {c} distribution (top 20):', cnt.most_common(20))
    # dump record 0 fully as u16 grid
    r0 = u16[0]
    print('rec0 u16:', ' '.join(f'{v:04x}' for v in r0[:64]))
    print('rec0 tail u16:', ' '.join(f'{v:04x}' for v in r0[-32:]))
    print('rec1 tail u16:', ' '.join(f'{v:04x}' for v in u16[1][-32:]))
    print('rec2 tail u16:', ' '.join(f'{v:04x}' for v in u16[2][-32:]))

if __name__ == '__main__':
    decode('/home/z/my-project/work/zone/GothamCity/batch_info.bin', 307)
    decode('/home/z/my-project/work/zone/GothamCity_Island2/batch_info.bin', 196)
