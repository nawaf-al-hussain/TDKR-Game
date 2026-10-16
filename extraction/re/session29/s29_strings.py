#!/usr/bin/env python3
"""S29 T1: find class-name strings in .so and xref -> registration/hash code."""
import struct, re, json, sys
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

# .rodata: vaddr==off for first LOAD (0..0xbbe1ec); second LOAD: vaddr=off+0x1000 (>=0xbbe930)
def off2v(o): return o if o < 0xbbe1ec else o + 0x1000
def v2o(v): return v if v < 0xbbe1ec else v - 0x1000

# 1. find candidate class-name strings
pats = [rb'(?:C[A-Za-z0-9_]*Component[A-Za-z0-9_]*)', rb'(?:C[A-Z][A-Za-z0-9_]{3,40})']
seen = {}
for m in re.finditer(rb'[\x20-\x7e]{4,64}', data[:0xbbe1ec]):  # scan first LOAD incl .rodata+text-as-rodata? restrict later
    s = m.group()
    if re.fullmatch(rb'C[A-Z][A-Za-z0-9_]*(Component|Object|Level|Light|Trigger|Actor|Controller|Setting|Camera|Effect|Sound|SoundAndLight|Cinematic|Traffic|Init|Dummy)\b[a-zA-Z0-9_]*', s) or \
       re.fullmatch(rb'C[A-Z][A-Za-z0-9_]*Component', s):
        off = m.start()
        seen[off] = s.decode()
print('candidate C* strings:', len(seen))
comp = {off: s for off, s in seen.items() if 'Component' in s}
print('with "Component":', len(comp))
for off in sorted(comp)[:60]:
    print(f'  vaddr {off2v(off):#x}  {comp[off]}')
json.dump({hex(off2v(k)): v for k, v in seen.items()}, open('/tmp/my-project/work/re29/cstrings.json', 'w'), indent=0)
