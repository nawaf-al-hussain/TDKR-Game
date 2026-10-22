#!/usr/bin/env python3
"""Patch s50_t1_make_bisect.py: remove the stale corr log line during generation."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_make_bisect.py'
s = open(p).read()
anchor = 's = s.replace(old_corr_block, new_corr_block)'
add = anchor + """
import re as _re
s = _re.sub(r"log\\('corr vs s48_ref_zone.*?\\n(?:        ' ref_mean.*?\\n)?", "", s)"""
assert anchor in s, 'anchor missing'
if '_re.sub' not in s:
    s = s.replace(anchor, add, 1)
open(p, 'w').write(s)
print('make script patched')
