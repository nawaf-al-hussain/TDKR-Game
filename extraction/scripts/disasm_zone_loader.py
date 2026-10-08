#!/usr/bin/env python3
"""Disassemble the glitch zone-streaming loaders to reverse the
lod_table.bin / batch_info.bin / lod_data.bin formats.

Targets (from libKRHP_symbols.txt):
  0x45e190 CDoubleBufferedLODStreaming<...>::C1 (2176 B)  - takes 3 IReadFile
  0x45c750 CDoubleBufferedDynamicBatchMesh<...>::C1 (3828 B) - takes 3 IReadFile
"""
import struct, sys, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/home/z/work/TDKR-Game/extraction/lib_libKRHP.so'
SYM = '/home/z/work/TDKR-Game/extraction/libKRHP_symbols.txt'

TARGETS = {
    'LODStreaming::C1':        (0x45e190, 2176),
    'DynamicBatchMesh::C1':    (0x45c750, 3828),
}


def load_syms():
    syms = {}
    for line in open(SYM, errors='replace'):
        m = re.match(r'^([0-9a-f]{8})\s+(.\S)', line.strip())
        if m:
            syms[int(m.group(1), 16)] = m.group(2)
    return syms


def main():
    which = sys.argv[1:] or list(TARGETS)
    blob = open(SO, 'rb').read()
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

    for name in which:
        va, size = TARGETS[name]
        fo = v2f(va)
        code = blob[fo:fo + size]
        print(f'\n===== {name} @ {va:#x} =====')
        for ins in md.disasm(code, va):
            annot = ''
            if ins.mnemonic in ('bl', 'blx') and ins.op_str.startswith('#'):
                try:
                    tgt = int(ins.op_str[1:], 0)
                except ValueError:
                    tgt = None
                if tgt is not None and tgt in syms:
                    annot = '   ; -> ' + syms[tgt]
            print(f'  {ins.address:#08x}: {ins.mnemonic:<8} {ins.op_str}{annot}')


if __name__ == '__main__':
    main()
