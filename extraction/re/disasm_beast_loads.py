#!/usr/bin/env python3
"""Disassemble the Beast component Load() family + CMemoryStream readers.

Thumb-2 disassembly via capstone; symbol resolution from libKRHP_symbols.txt.
Goal: exact CMemoryStream byte layout of every bake-related component Load —
the authoritative answer to 'where does the FP-page origin come from'.
"""
import struct, sys, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYM = '/home/z/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'

TARGETS = {
    'CBeastAreaComponent::Load':          0x2b164c,
    'CBeastDirectionalComponent::Load':   0x2b17e0,
    'CBeastObjectComponent::Load':        0x2b1ea4,
    'CBeastObjectGlobalComponent::Load':  0x2b2a80,
    'CComponentBeastBakeGroup::Load':     0x3ce548,
    'CTemplateBakeGroup::Load':           0x49d870,
}

def load_syms():
    syms = {}
    for line in open(SYM, errors='replace'):
        m = re.match(r'^([0-9a-f]{8})\s+(.\S)', line.strip())
        if m:
            syms[int(m.group(1), 16)] = m.group(2)
    return syms

def main():
    blob = open(SO, 'rb').read()
    # ELF program headers: map vaddr -> file offset
    e_phoff = struct.unpack_from('<I', blob, 0x1c)[0]
    e_phentsize = struct.unpack_from('<H', blob, 0x2a)[0]
    e_phnum = struct.unpack_from('<H', blob, 0x2c)[0]
    segs = []
    for i in range(e_phnum):
        p = e_phoff + i * e_phentsize
        p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIIII', blob, p)
        if p_type == 1:
            segs.append((p_vaddr, p_offset, p_filesz))
    def v2f(v):
        for va, off, sz in segs:
            if va <= v < va + sz:
                return off + (v - va)
        return None

    syms = load_syms()
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = False

    which = sys.argv[1:] if len(sys.argv) > 1 else list(TARGETS)
    for name in which:
        va = TARGETS.get(name)
        if va is None:
            continue
        fo = v2f(va)
        print(f'\n===== {name} @ {va:#x} (file {fo:#x}) =====')
        code = blob[fo:fo + 0x1000]
        n_out = 0
        for ins in md.disasm(code, va):
            txt = f'{ins.address:#x}: {ins.mnemonic} {ins.op_str}'
            # annotate bl targets
            m = re.search(r'\bbl\s+#?0x([0-9a-f]+)', txt)
            ann = ''
            if m:
                t = int(m.group(1), 16)
                if t in syms:
                    ann = '   ; ' + syms[t]
            # annotate literal-pool loads
            print(txt + ann)
            n_out += 1
            if ins.mnemonic in ('pop', 'bx') and 'pc' in ins.op_str:
                break
            if n_out > 400:
                print('   ... (truncated)')
                break

if __name__ == '__main__':
    main()
