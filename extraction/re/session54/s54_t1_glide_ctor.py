#!/usr/bin/env python3
"""s54 T1 step 1: locate CComponentGlide ctor, its callers, and Load read-seq (ARM/Thumb check).

libKRHP.so: /tmp/my-project/work/re29/libKRHP.so
Known: _ZTV15CComponentGlide @vaddr 0xbd8990 (slots: +8 ~D1 0x3d780c, +0xc ~D0 0x3d7824,
+0x10 New 0x3c0824, +0x14 Clone 0x3c085c, +0x18 Load 0x3c0938).
Ctor stores vt+8 = 0xbd8998; literal found at vaddr 0x51644; no factory-switch reference.
"""
import struct
import subprocess
import bisect
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

# ---- program headers ----
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))
        print('PT_LOAD vaddr=%#x offset=%#x filesz=%#x' % (p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

# ---- symbols ----
syms = []
nmout = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
for line in nmout.splitlines():
    parts = line.split()
    if len(parts) == 3:
        try:
            a = int(parts[0], 16)
        except ValueError:
            continue
        syms.append((a, parts[2]))
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    if i >= 0:
        return syms[i][1]
    return '<none>'

def sym_addr(name):
    for a, n in syms:
        if n == name:
            return a
    return None

# ---- 1. verify vtable slots ----
vt = sym_addr('_ZTV15CComponentGlide')
o = v2o(vt)
print('\n_ZTV15CComponentGlide @%#x:' % vt)
for k in range(7):
    val = struct.unpack_from('<I', data, o + 4 * k)[0]
    print('  vt+%02x: %#x  %s' % (k * 4, val, sym_of(val) if val else ''))

# ---- 2. ctor: function containing the literal 0xbd8998 @vaddr 0x52b54 ----
print('\nliteral 0xbd8998 stored at vaddr 0x52b54; nearest symbol below:',
      sym_of(0x52b54))
# scan backwards for function start (push {rX..} or sub sp) - print symbols between 0x51000..0x52c00
print('symbols in 0x50000-0x53000:')
for a, n in syms:
    if 0x50000 <= a <= 0x53000:
        print('  %#x %s' % (a, n))

# ---- 3. disassemble the ctor (ARM first; check interworking) ----
def dis(vaddr, n=200, mode=CS_MODE_ARM, stop_at_pop=False):
    off = v2o(vaddr)
    md = Cs(CS_ARCH_ARM, mode)
    out = []
    for ins in md.disasm(data[off:off + n * 4], vaddr):
        out.append('%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
        if stop_at_pop and ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            break
    return out

# find ctor start: previous symbol after which 0x51644 lies
start = None
for a, n in syms:
    if a <= 0x51644 and (n.startswith('$') is False):
        cand = a
    if a > 0x51644:
        break
start = cand
print('\ndisasm around ctor literal (start %#x = %s):' % (start, sym_of(start)))
for l in dis(start, 120):
    print(' ', l)
