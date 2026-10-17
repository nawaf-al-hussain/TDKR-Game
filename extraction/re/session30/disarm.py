#!/usr/bin/env python3
"""S30 helper: disassemble arbitrary vaddr ranges of libKRHP.so (ARM)."""
import sys, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/re29/libKRHP.so'

def load_elf():
    d = open(SO, 'rb').read()
    e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
    e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
    e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
    segs = []
    for i in range(e_phnum):
        o = e_phoff + i * e_phentsize
        p_type, p_offset, p_vaddr, _, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
        if p_type == 1:
            segs.append((p_vaddr, p_offset, p_filesz, p_memsz))
    return d, segs

DATA, SEGS = load_elf()

def vread(vaddr, n):
    for v, o, fs, ms in SEGS:
        if v <= vaddr < v + fs:
            off = o + (vaddr - v)
            return DATA[off:off + n]
    raise ValueError(f'vaddr 0x{vaddr:x} not mapped')

def disasm(vaddr, count=60, size=None):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = vread(vaddr, size if size else count * 4)
    out = []
    for ins in md.disasm(code, vaddr):
        out.append(f'0x{ins.address:x}: {ins.mnemonic}\t{ins.op_str}')
    return out

def func_end_scan(vaddr, maxn=20000):
    """scan until pop {..., pc}"""
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = vread(vaddr, maxn)
    end = vaddr + maxn
    for ins in md.disasm(code, vaddr):
        if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            end = ins.address + 4
            break
    return end

if __name__ == '__main__':
    va = int(sys.argv[1], 16)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    end = None
    if len(sys.argv) > 3 and sys.argv[3] == 'full':
        end = func_end_scan(va)
        n = (end - va) // 4
    for l in disasm(va, n, size=(end - va) if end else None):
        print(l)
