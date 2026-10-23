#!/usr/bin/env python3
"""s54 T1 step 6: disassemble CGameObjectManager::Reload @0x366104 (ARM)
to derive the exact gol.bin record framing and payload handling."""
import struct
import subprocess

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 3:
        try:
            a = int(parts[0], 16)
        except ValueError:
            continue
        syms.append((a, parts[2]))
syms.sort()
import bisect
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dis(vaddr, n_ins=400, label=''):
    off = v2o(vaddr)
    print('=== %s @%#x ===' % (label, vaddr))
    cnt = 0
    for ins in md.disasm(data[off:off + n_ins * 4], vaddr):
        note = ''
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                note = '   ; -> %s' % sym_of(t)
            except ValueError:
                pass
        # annotate literal pool loads with the value at [pc,#imm]
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                note = '   ; =%#x %s' % (val, sym_of(val) if val > 0xbbf000 else '')
            except Exception:
                pass
        print('%08x %-8s %-40s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
        cnt += 1
        if cnt >= n_ins:
            break

dis(0x366104, 260, 'CGameObjectManager::Reload')
