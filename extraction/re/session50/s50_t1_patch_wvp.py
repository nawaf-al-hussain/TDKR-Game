#!/usr/bin/env python3
"""Widen the height-depth window in city_bisect.html: clip_z = 1 - h/200 (h in
[0,200], clips h<0 water/shore = 31% of ref coverage) -> clip_z = -2h/350 + 150/350
(h in [-100, +250], same orientation: higher = nearer). Idempotent."""
p = '/tmp/my-project/work/city_slice_wt/playable/city_bisect.html'
s = open(p).read()
old = '0, 0, -1/200, 0,\n      -1, -1, 1, 1,'
new = '0, 0, -2/350, 0,\n      -1, -1, 150/350, 1,'
n1 = s.count(old)
s = s.replace(old, new)
old2 = 'new Float32Array([2/W,0,0,0, 0,2/H,0,0, 0,0,-1/200,0, -1,-1,1,1])'
new2 = 'new Float32Array([2/W,0,0,0, 0,2/H,0,0, 0,0,-2/350,0, -1,-1,150/350,1])'
n2 = s.count(old2)
s = s.replace(old2, new2)
open(p, 'w').write(s)
print('WVP z-rows patched: %d + %d occurrences' % (n1, n2))
assert '-1/200' not in s, 'stale depth window remains'
print('no stale -1/200 left')
