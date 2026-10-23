#!/usr/bin/env python3
"""s54 T1 step 12: CComponentGlide::Load @0x3c0938 full ARM disassembly.
Pin the exact read sequence (s53 claimed 2x ReadInt + 41x ReadFloat from a THUMB
disasm - s48 warned Thumb is a junk-disasm artifact for this binary; verify in ARM).
Also: CComponentGlide::New @0x3c0824 to get the object size/defaults."""
import struct
import subprocess
import bisect

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3:
        try:
            a = int(pr[0], 16)
        except ValueError:
            continue
        syms.append((a, pr[2]))
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dis(vaddr, nbytes, label):
    print('=== %s @%#x ===' % (label, vaddr))
    off = v2o(vaddr)
    for ins in md.disasm(data[off:off + nbytes], vaddr):
        note = ''
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                note = '   ; -> %s' % sym_of(t)
            except ValueError:
                pass
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                note = '   ; =%#x' % val
            except Exception:
                pass
        print('%08x %-8s %-36s%s' % (ins.address, ins.mnemonic, ins.op_str, note))

dis(0x3c0938, 0x120, 'CComponentGlide::Load')
print()
dis(0x3c0824, 0x38, 'CComponentGlide::New')
