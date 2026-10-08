#!/usr/bin/env python3
"""Disassemble the REAL bake-related functions (symbol-table addresses).

Key discovery: previous session's addresses were +0x10000 off.
The real smoking gun: CZone::ChangeLightMap(const char*, const char*) @0x2b9208
— this is how the game assigns lightmap/bake pages to zones at runtime.
"""
import struct, sys, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYM = '/home/z/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'

TARGETS = {
    'ChangeLightMap(lua)':                    (0x167a28, 76),
    'CZone::ChangeLightMap':                  (0x2b9208, 980),
    'CZonesManager::ChangeLightMap':          (0x2bdb94, 56),
    'CComponentBeastBakeGroup::Load':         (0x3be548, 64),
    'CTemplateBakeGroup::Load':               (0x48d870, 264),
    'CComponentBeastObjectComponent::Load':   (0x2e1e8c, 136),
    'CComponentBeastObjectComponentGlobal::Load': (0x2e1fb0, 52),
}

def load_syms():
    syms = {}
    for line in open(SYM, errors='replace'):
        m = re.match(r'^([0-9a-f]{8})\s+(?:\S+\s+)?(\S+)', line.strip())
        if m and m.group(2) not in ('FUNC', 'OBJ', ''):
            pass
    # simpler: map addr -> demangled-ish tail
    for line in open(SYM, errors='replace'):
        parts = line.strip().split()
        if len(parts) >= 4 and parts[1] == 'FUNC':
            syms[int(parts[0], 16)] = parts[3]
    return syms

def v2f_map(blob):
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
    return v2f

def main():
    blob = open(SO, 'rb').read()
    v2f = v2f_map(blob)
    syms = load_syms()
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = False

    which = sys.argv[1:] if len(sys.argv) > 1 else list(TARGETS)
    for name in which:
        va, size = TARGETS[name]
        fo = v2f(va)
        print(f'\n===== {name} @ {va:#x} size={size} (file {fo:#x}) =====')
        code = blob[fo:fo + size + 64]
        n_out = 0
        end_va = va + size
        for ins in md.disasm(code, va):
            if ins.address >= end_va + 8:
                break
            txt = f'{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}'
            m = re.search(r'\bbl\s+#?0x([0-9a-f]+)', txt)
            ann = ''
            if m:
                t = int(m.group(1), 16)
                if t in syms:
                    ann = '   ; <' + syms[t] + '>'
            print(txt + ann)
            n_out += 1
            if n_out > 500:
                print('   ... (truncated)')
                break

if __name__ == '__main__':
    main()
