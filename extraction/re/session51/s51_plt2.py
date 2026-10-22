#!/usr/bin/env python3
"""s51 T1g: resolve PLT stubs (file-based, heredoc-safe) and find GL call sites."""
import struct, subprocess, pickle, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
data = open(SO, 'rb').read()
PLT_A, PLT_O, PLT_S = 0x000a4d9c, 0x0a4d9c, 0x000fe0

def imm12(w):
    r = (w >> 8) & 0xf
    v = w & 0xff
    return ((v >> (2 * r)) | (v << (32 - 2 * r))) & 0xffffffff if r else v

rel = subprocess.run(['readelf', '-rW', SO], capture_output=True, text=True).stdout
jump = {}
inrel = False
for line in rel.splitlines():
    if line.startswith("Relocation section '.rel.plt'"):
        inrel = True
        continue
    if inrel:
        if line.startswith('Relocation') or not line.strip():
            inrel = False
            continue
        p = line.split()
        if len(p) >= 4 and 'JUMP_SLOT' in line:
            jump[int(p[0], 16)] = p[4]

res = {}
npat = 0
_dbg = 0
for i in range(20, PLT_S, 12):
    a = PLT_A + i
    w0, w1, w2 = struct.unpack_from('<3I', data, PLT_O + i)
    ok0 = (w0 & 0x0fff0000) == 0x028f0000
    ok1 = (w1 & 0x0fff0000) == 0x028c0000
    ok2 = (w2 & 0x0ffff000) == 0x05bcf000
    if _dbg < 3:
        print('DBG i=%d a=%#x w0=%08x ok0=%s ok1=%s ok2=%s' % (i, a, w0, ok0, ok1, ok2))
        _dbg += 1
    if ok0 and ok1 and ok2:
        npat += 1
        got = (a + 8) + imm12(w0) + imm12(w1) + (w2 & 0xfff)
        if got in jump:
            res[a] = jump[got]
print('pattern matched %d stubs, resolved %d of %d slots' % (npat, len(res), len(jump)))
want = {}
for a, n in res.items():
    if n.startswith('glTexParameter') or n in ('glGenerateMipmap', 'glCompressedTexImage2D', 'glTexImage2D'):
        want[n] = a
        print('plt 0x%08x %s' % (a, n))
pickle.dump(res, open('/tmp/my-project/work/s51_plt_map.pkl', 'wb'))

e_phoff = struct.unpack_from('<I', data, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', data, 0x2a)[0]
e_phnum = struct.unpack_from('<H', data, 0x2c)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    t, off, va, _, fsz, _ = struct.unpack_from('<6I', data, p)
    if t == 1:
        segs.append((va, off, fsz))

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
callers = {a: [] for a in want.values()}
for va, off, fsz in segs:
    if fsz < 0x100000:
        continue
    for ins in md.disasm(data[off:off + fsz], va):
        if ins.mnemonic == 'bl' and ins.op_str.startswith('#0x'):
            t = int(ins.op_str[1:], 16)
            if t in callers:
                callers[t].append(ins.address)
for n, a in want.items():
    print('%s: %d callers: %s' % (n, len(callers[a]), ['#%08x' % c for c in callers[a][:12]]))
