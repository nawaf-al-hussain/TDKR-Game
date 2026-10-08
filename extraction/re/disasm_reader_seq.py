#!/usr/bin/env python3
"""Extract the CMemoryStream reader-call sequence from a function (ARM A32).

Walks instructions from a true ELF-symtab function entry, annotates every
`bl` with the resolved symbol (CMemoryStream readers highlighted), and prints
register/immediate context before each call — enough to reconstruct the exact
stream field order without a full decompiler.

Usage: python3 disasm_reader_seq.py <func_name_regex> [max_bytes]
"""
import sys, re, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elf_syms import load_funcs

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'

READERS = {
    '_ZN13CMemoryStream8ReadBoolERb': 'ReadBool&',
    '_ZN13CMemoryStream8ReadCharEv': 'ReadChar(1B)',
    '_ZN13CMemoryStream4ReadERc': 'Read(char&)',
    '_ZN13CMemoryStream8ReadByteEv': 'ReadByte(1B)',
    '_ZN13CMemoryStream9ReadShortEv': 'ReadShort(2B)',
    '_ZN13CMemoryStream4ReadERs': 'Read(short&)',
    '_ZN13CMemoryStream4ReadERt': 'ReadUShort(2B)',
    '_ZN13CMemoryStream7ReadIntEv': 'ReadInt(4B)',
    '_ZN13CMemoryStream4ReadERi': 'Read(int&)',
    '_ZN13CMemoryStream4ReadERj': 'Read(uint&)',
    '_ZN13CMemoryStream9ReadFloatEv': 'ReadFloat(4B)',
    '_ZN13CMemoryStream4ReadERf': 'Read(float&)',
    '_ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE': 'ReadString(std::string&)',
    '_ZN13CMemoryStream10ReadStringEv': 'ReadString()',
    '_ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE': 'ReadStringC',
    '_ZN13CMemoryStream4ReadERN6glitch4core8vector3dIfEE': 'Read(float3&)',
}

READER_ADDR = {
    0x339510: 'ReadBool&', 0x3395d8: 'ReadChar(1B)', 0x339690: 'ReadByte(1B)',
    0x339758: 'ReadShort(2B)', 0x339868: 'ReadUShort(2B)', 0x339914: 'ReadInt(4B)',
    0x3399d4: 'Read(int&)', 0x339ab4: 'Read(uint&)', 0x339b94: 'ReadFloat(4B)',
    0x339c58: 'Read(float&)', 0x33a0d4: 'ReadString(std::string&)',
    0x33ab94: 'ReadString()', 0x33ad74: 'ReadStringC', 0x33a730: 'ReadStringW',
    0x33b3d0: 'Read(float3&)',
}

def main():
    pat = sys.argv[1]
    maxb = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    funcs = load_funcs()
    blob = open(SO, 'rb').read()
    hits = [(a, (n, s)) for a, (n, s) in sorted(funcs.items()) if re.search(pat, n)]
    if not hits:
        print('no symbol matches', pat); return
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for addr, (name, size) in hits:
        size = max(size, 64)
        print(f'\n===== {name} @ {addr:#x} size={size} =====')
        code = blob[addr:addr + size]
        hist = []
        for ins in md.disasm(code, addr):
            txt = f'{ins.mnemonic} {ins.op_str}'
            m = re.match(r'bl\s+#?0x([0-9a-f]+)', txt)
            if m:
                t = int(m.group(1), 16)
                rd = READER_ADDR.get(t)
                if rd is None:
                    fn = funcs.get(t)
                    nm = fn[0] if fn else f'{t:#x}'
                    rd = READERS.get(nm) or nm.replace('_ZN13CMemoryStream', 'CMS:')[:70]
                label = rd
                print(f'  CALL@{ins.address:#x}: {label}')
                for h in hist[-5:]:
                    print(f'      {h}')
                hist = []
            else:
                hist.append(f'{ins.address:#x}: {txt}')
            if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
                break

if __name__ == '__main__':
    main()
