#!/usr/bin/env python3
"""S40 T3b: find the registrant function referencing the constant-name table
(vaddr 0xc0b0xx region), disassemble it, and extract the (name, value) pairs
it registers via lua_setglobal/lua_pushnumber — or via a parallel value array."""
import struct, sys
sys.path.insert(0, '/home/z/my-project/scripts')
from s40_xref import callers_of
from capstone import *
import json

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    t, off, va, _, fs, _ = struct.unpack_from('<6I', d, o)
    if t == 1: segs.append((va, off, fs))

def v2o(va):
    for v, o, s in segs:
        if v <= va < v + s: return o + (va - v)
    return None

def rd_cstr(va, n=32):
    o = v2o(va)
    if o is None: return None
    e = d.find(b'\0', o, o + n)
    if e < 0: return None
    try: return d[o:e].decode('latin1')
    except Exception: return None

# map the name-pointer table entries at 0xc0a028- (file) => vaddr +0x1000
base = 0xc0a028
names = []
o = base
while True:
    ptr = struct.unpack_from('<I', d, o)[0]
    nm = rd_cstr(ptr, 40) if ptr else None
    if nm is None or not nm.isprintable() or len(nm) < 2:
        break
    names.append((hex(0xc0b000 + (o - 0xc0a000)), nm))
    o += 4
    if o > base + 0x200: break
print('name table entries:')
for a, nm in names: print(' ', a, repr(nm))

# table vaddr range
tv0, tv1 = 0xc0b000 + (base - 0xc0a000) - 0x10, 0xc0b000 + (o - 0xc0a000)
print(f'table vaddr range ~{hex(tv0)}..{hex(tv1)}')
# find code refs to any u32 in [tv0, tv1): Thumb LDR-literal pools + ARM pools
refs = []
for tv in range(tv0 & ~3, tv1, 4):
    for m, addr in callers_of(tv):
        refs.append((hex(tv), m, addr))
print('code refs to table entries:')
for r in refs[:20]: print(' ', r)
json.dump({'names': names, 'refs': refs},
          open('/home/z/my-project/scripts/s40_t3_registrant.json', 'w'), indent=1)
