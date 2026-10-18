#!/usr/bin/env python3
"""S34 T3g: final .nm decode. stream@1: [char][int][9f first tri][3 chars]
[vertex soup: 3 BE f32 per vertex (x, y_up, z)][cell records: 7 BE u16 + u8]
Pin boundaries; build cells; adjacency; validate soup z vs collision ground."""
import struct
import numpy as np

F = '/tmp/my-project/work/game_config/GothamCity_502299_navdata.nm'
d = open(F, 'rb').read()
N = len(d)
print(f'file[0] = 0x{d[0]:02x}; stream char = 0x{d[1]:02x} ({chr(d[1])!r}); '
      f'int = 0x{struct.unpack_from(">I", d, 2)[0]:08x}')
fa = np.frombuffer(d[6:6 + (N - 6) // 4 * 4], '>f4').astype(np.float64)
plaus = np.isfinite(fa) & ((np.abs(fa) < 5000) | (fa == 0))
p = int(np.argmax(~plaus)) if (~plaus).any() else len(fa)
print(f'plausible floats from byte 6: {p}; p%3 = {p%3}; float bytes end '
      f'{6 + 4*p}')

# vertices: p//3 triples (allow 1-2 stray at end from the boundary)
V = p // 3
print(f'vertices V = {V} (rem {p % 3})')
verts = fa[:V * 3].reshape(V, 3)
print(f'vert x {verts[:,0].min():.1f}..{verts[:,0].max():.1f}; '
      f'y(up) {verts[:,1].min():.2f}..{verts[:,1].max():.2f} (median '
      f'{np.median(verts[:,1]):.2f}); z {verts[:,2].min():.1f}..{verts[:,2].max():.1f}')

# cell records from 6 + 4*p, stride 16, 7 BE shorts + u8
cs = 6 + 4 * p
# align: engine reads sequentially, so cs is the start (maybe +1 for the 3 chars already inside the plaus zone?)
for adj in range(-8, 9):
    s0 = cs + adj
    n = (N - s0) // 16
    if n < 1000: continue
    W = min(n, 8000)
    b = np.frombuffer(d[s0:s0 + W * 16], np.uint8).reshape(W, 16)
    sh = np.frombuffer(d[s0:s0 + W * 16], '>i2').reshape(W, 8)[:, :7]
    ch = b[:, 15]
    okv = ((sh[:, :3] >= 0) & (sh[:, :3] < V)).all(axis=1)
    okn = ((sh[:, 3:6] == -1) | ((sh[:, 3:6] >= 0) & (sh[:, 3:6] < n))).all(axis=1)
    frac = float((okv & okn).mean())
    if frac > 0.9:
        print(f'cells start {s0} (adj {adj:+d}): {frac*100:.2f}% valid of {W}; '
              f'total to EOF {(N - s0) // 16}')
        np.save('/home/z/my-project/scripts/s34_t3_gc_verts.npy', verts)
        np.save('/home/z/my-project/scripts/s34_t3_gc_cells.npy',
                np.frombuffer(d[s0:s0 + n * 16], '>i2').reshape(n, 8)[:, :7])
        np.save('/home/z/my-project/scripts/s34_t3_gc_cellflags.npy', 
                np.frombuffer(d[s0:s0 + n * 16], np.uint8).reshape(n, 16)[:, 15])
        print(f'saved {n} cells (7 shorts: [v0 v1 v2 n0 n1 n2 extra?]; flags)')
        break
