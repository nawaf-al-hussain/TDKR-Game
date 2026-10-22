#!/usr/bin/env python3
"""Remove the leftover pre-refactor __GLDUMP + stale corr log from the main handler
of city_bisect.html (references corr/sa/n which no longer exist in that scope)."""
p = '/tmp/my-project/work/city_slice_wt/playable/city_bisect.html'
s = open(p).read()
start_marker = "    window.__GLDUMP = () => { const c = document.createElement('canvas');\n      c.width = W; c.height = H;"
i = s.find(start_marker)
if i < 0:
    print('already clean')
else:
    end_marker = "        ' ref_mean ' + (sb/n).toFixed(2));\n"
    j = s.index(end_marker, i) + len(end_marker)
    s = s[:i] + s[j:]
    open(p, 'w').write(s)
    print('removed stale block %d bytes' % (j - i))
assert s.count("c.width = W; c.height = H;") == 0, 'stale W/H GLDUMP remains'
print('page clean')
