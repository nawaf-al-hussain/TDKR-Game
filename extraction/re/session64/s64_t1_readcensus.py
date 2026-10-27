#!/usr/bin/env python3
"""S64 T1 step 7: read-site census for CameraParams::Load (0x3bf038) and
Glide::Load (0x3c0938) - find the trailing fields the specs miss."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    pt, po, pv, _, ps = struct.unpack_from('<5I', data, p)
    if pt == 1:
        segs.append((pv, po, ps))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

nm = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for l in nm.splitlines():
    p = l.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.skipdata = True

def census(start, end, label):
    print('==== %s 0x%x..0x%x' % (label, start, end))
    o = v2o(start)
    code = data[o:o + (end - start)]
    n = {'i': 0, 'f': 0, 'STR': 0, 'other': []}
    seq = []
    for ins in md.disasm(code, start):
        if ins.mnemonic == 'bl':
            t = int(ins.op_str.replace('#', ''), 16)
            s, off = sym_of(t)
            if 'ReadInt' in s:
                seq.append('i'); n['i'] += 1
            elif 'ReadFloat' in s:
                seq.append('f'); n['f'] += 1
            elif 'ReadString' in s:
                seq.append('STR'); n['STR'] += 1
            elif 'CMemoryStream' in s and 'Read' in s:
                seq.append(s.split('::')[-1].split('(')[0]); n['other'].append(s.split('::')[-1].split('(')[0])
    print(' reads: %d ints, %d floats, %d strings, other=%s' % (n['i'], n['f'], n['STR'], n['other']))
    print(' stream order:', ' '.join(seq))
    print()

# symbol ranges: find the enclosing symbols
for a in (0x3bf038, 0x3c0938):
    s, off = sym_of(a)
    print('reader 0x%x = %s +0x%x' % (a, s, off))
# next symbol after each
for a in (0x3bf038, 0x3c0938):
    i = bisect.bisect_right(addrs, a)
    print('next sym after 0x%x: 0x%x %s' % (a, addrs[i], syms[i][1][:70]))
print()
census(0x3bf038, 0x3bf184, 'CameraParams')
census(0x3c0938, 0x3c0a5c, 'Glide')
