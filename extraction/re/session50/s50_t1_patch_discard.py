#!/usr/bin/env python3
"""Fix the flat-mode discard wrap in s50_t1_make_bisect.py (empty if-body -> empty statement)."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_make_bisect.py'
s = open(p).read()
old = ".replace(/\\\\s*discard;/g, ' ')"
new = ".replace(/\\\\s*discard;/g, ' ;')"
assert old in s, 'pattern missing: %r' % old
s = s.replace(old, new)
open(p, 'w').write(s)
print('discard fix applied')
