#!/usr/bin/env python3
"""Idempotently normalize corrVsRef/__GLDUMP in s50_t1_make_bisect.py to RW/RH."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_make_bisect.py'
s = open(p).read()
# operate only on the corrVsRef injection block
i0 = s.index('async function corrVsRef(buf) {')
i1 = s.index("document.querySelector('#f').addEventListener('change'", i0)
blk = s[i0:i1]
blk = blk.replace('c.width = W; c.height = H;', 'c.width = RW; c.height = RH;')
blk = blk.replace('new Uint8ClampedArray(W * H * 4)', 'new Uint8ClampedArray(RW * RH * 4)')
blk = blk.replace('for (let y = 0; y < H; y++)', 'for (let y = 0; y < RH; y++)')
blk = blk.replace('buf.subarray(y * W * 4, (y + 1) * W * 4)', 'buf.subarray(y * RW * 4, (y + 1) * RW * 4)')
blk = blk.replace('(H - 1 - y) * W * 4', '(RH - 1 - y) * RW * 4')
blk = blk.replace('putImageData(new ImageData(flipped, W, H)', 'putImageData(new ImageData(flipped, RW, RH)')
s = s[:i0] + blk + s[i1:]
open(p, 'w').write(s)
print('normalized; c.width=RW count in block:', blk.count('c.width = RW'))
