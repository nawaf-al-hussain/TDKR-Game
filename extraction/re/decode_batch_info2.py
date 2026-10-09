#!/usr/bin/env python3
"""Decode batch_info.bin records (307B each, unaligned) — find material index."""
import struct
import numpy as np
import collections

def decode(path, n_mat, label):
    d = open(path, 'rb').read()
    n = struct.unpack_from('<I', d, 0)[0]
    body = d[4:]
    rb = len(body) // n
    print(f'\n{label}: N={n} rec={rb}B (expect n_mat~{n_mat})')
    recs = np.frombuffer(body[:n*rb], np.uint8).reshape(n, rb)
    # u16 LE at every byte offset (unaligned)
    hits = []
    for off in range(rb - 1):
        col = recs[:, off].astype(np.int64) + 256 * recs[:, off + 1].astype(np.int64)
        if np.all(col < n_mat) and np.any((col > 0) & (col < 100)):
            hits.append((off, int(col.min()), int(col.max()),
                         len(set(col.tolist()))))
    print('u16 LE unaligned columns all < n_mat:', hits[:20])
    for off, mn, mx, uniq in hits[:6]:
        col = recs[:, off].astype(np.int64) + 256 * recs[:, off + 1].astype(np.int64)
        cnt = collections.Counter(col.tolist())
        print(f'  col@{off}: uniq={uniq} top={cnt.most_common(8)}')
    # single-byte columns all < n_mat
    for off in range(rb):
        col = recs[:, off]
        if np.all(col < n_mat) and np.any((col > 0) & (col < 200)):
            cnt = collections.Counter(col.tolist())
            if len(cnt) > 5:
                print(f'  byte@{off}: uniq={len(cnt)} top={cnt.most_common(6)}')

if __name__ == '__main__':
    decode('/home/z/my-project/work/zone/GothamCity/batch_info.bin', 307, 'island1')
    decode('/home/z/my-project/work/zone/GothamCity_Island2/batch_info.bin', 196, 'island2')
