#!/usr/bin/env python3
"""Directly normalize the generated city_bisect.html corrVsRef/__GLDUMP to canvas dims.
Idempotent; run after any regeneration."""
p = '/tmp/my-project/work/city_slice_wt/playable/city_bisect.html'
s = open(p).read()
i0 = s.index('async function corrVsRef(buf) {')
i1 = s.index("document.querySelector('#f').addEventListener('change'", i0)
blk = s[i0:i1]
if 'const RW = glz.width' not in blk:
    blk = blk.replace('async function corrVsRef(buf) {',
        'async function corrVsRef(buf) {\n  const RW = glz.width, RH = glz.height;', 1)
blk = blk.replace('c.width = W; c.height = H;', 'c.width = RW; c.height = RH;')
blk = blk.replace('new Uint8ClampedArray(W * H * 4)', 'new Uint8ClampedArray(RW * RH * 4)')
blk = blk.replace('for (let y = 0; y < H; y++)', 'for (let y = 0; y < RH; y++)')
blk = blk.replace('buf.subarray(y * W * 4, (y + 1) * W * 4)', 'buf.subarray(y * RW * 4, (y + 1) * RW * 4)')
blk = blk.replace('(H - 1 - y) * W * 4', '(RH - 1 - y) * RW * 4')
blk = blk.replace('putImageData(new ImageData(flipped, W, H)', 'putImageData(new ImageData(flipped, RW, RH)')
blk = blk.replace('cc.width = W; cc.height = H;', 'cc.width = RW; cc.height = RH;')
blk = blk.replace('const ref = cx2.getImageData(0, 0, W, H).data;', 'const ref = cx2.getImageData(0, 0, RW, RH).data;')
blk = blk.replace('const n = W * H;', 'const n = RW * RH;')
s = s[:i0] + blk + s[i1:]
open(p, 'w').write(s)
import re
assert 'c.width = RW' in blk and 'c.width = W;' not in blk
print('page normalized OK')
