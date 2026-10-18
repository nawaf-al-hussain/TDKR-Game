#!/usr/bin/env python3
"""S33 T2b: locate the cape vertex blocks (394 / 194 verts, 80 B each)."""
import struct
import numpy as np

MD = '/tmp/my-project/work/data/batman.bdae'
md = open(MD, 'rb').read()
N = len(md) // 4
f32 = np.frombuffer(md[:N * 4], np.float32)
u32 = lambda o: struct.unpack_from('<I', md, o)[0]
print(f'batman.bdae size {len(md)}')

# body vertex block: 1449 x 80 B @0x4b5c (known). Verify layout: pos at +0
v0 = struct.unpack_from('<3f', md, 0x4b5c)
print('body v0 pos:', [round(x, 4) for x in v0])

# scan: candidate vertex-block starts = offsets where 394 consecutive
# 80-B records have finite |pos| < 10 at +0 and finite normals at +12
W = f32  # word view
def plausible_run(vert_off, nverts):
    for i in range(nverts):
        p = vert_off + i * 80
        w = p // 4
        x, y, z = W[w], W[w + 1], W[w + 2]
        if not (np.isfinite(x) and np.isfinite(y) and np.isfinite(z)
                and abs(x) < 10 and abs(y) < 10 and abs(z) < 10):
            return False
    return True

# efficient: word-plausible mask, then check 394*20-word windows with stride 20 words
plaus = np.isfinite(W) & (np.abs(W) < 10)
# a block of nverts needs words [w, w+80*nverts/4) plausible except struct fields
step = 20  # words per vertex
c = np.cumsum(np.concatenate(([0], plaus.view(np.int8))))
hits = []
for nverts in (394, 194):
    need = nverts * step
    win = (c[need::1] - c[:-need])  # too heavy; do coarse: every 4 B
    # instead: sample positions where 20 consecutive words plausible and pos x plausible
    # coarse scan on 80-B stride: candidate w where words w..w+19 plausible
    cand = np.flatnonzero(plaus[:-20:1] [:len(plaus)-20])
    # too many; restrict: check windows at every 4-B offset but quick-reject
    w_c = np.flatnonzero((c[20:] - c[:-20]) == 20)
    cnt = 0
    for w0 in w_c[::7]:
        if plausible_run(w0 * 4, nverts):
            hits.append((nverts, w0 * 4))
            cnt += 1
            if cnt > 8: break
    print(f'{nverts}-vert candidate blocks: {len(hits)}')
for nverts, off in hits:
    print(f'  {nverts} verts @0x{off:x}')
    ps = [struct.unpack_from('<3f', md, off + i * 80) for i in range(0, nverts, max(1, nverts // 6))]
    for p in ps:
        print('    pos', [round(x, 3) for x in p])
