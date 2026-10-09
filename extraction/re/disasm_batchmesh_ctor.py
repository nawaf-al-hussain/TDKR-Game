#!/usr/bin/env python3
"""Disassemble CDoubleBufferedDynamicBatchMesh ctor @0x45c750 and
CDoubleBufferedLODStreaming ctor @0x45e190 — locate batch_info parsing."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

LIB = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(LIB, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

e_shoff = struct.unpack_from('<I', d, 0x20)[0]
e_shentsize, e_shnum = struct.unpack_from('<HH', d, 0x2e)
secs = [struct.unpack_from('<10I', d, e_shoff + i * e_shentsize) for i in range(e_shnum)]
shstr_off = secs[-1][4]
def secname(x):
    end = d.index(b'\x00', shstr_off + x)
    return d[shstr_off + x:end].decode()
symtab = next(s for s in secs if secname(s[0]) == '.symtab')
strtab = next(s for s in secs if secname(s[0]) == '.strtab')
def strname(x):
    end = d.index(b'\x00', strtab[4] + x)
    return d[strtab[4] + x:end].decode('latin1')
symname = {}
nsym = symtab[5] // 16
for i in range(nsym):
    p = symtab[4] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', d, p)
    if info & 0xf == 2 and val:
        symname[val] = strname(nm)

def disasm(addr, size, title, maxlines=400):
    print(f'\n=== {title} @0x{addr:x} (0x{size:x}) ===')
    cnt = 0
    for ins in md.disasm(d[addr:addr + size], addr):
        extra = ''
        if ins.mnemonic == 'bl':
            try:
                tgt = int(ins.op_str[1:], 16)
                if tgt in symname:
                    nm = symname[tgt]
                    short = nm.split('(')[0].replace('_ZN', '')[:70]
                    extra = f'   ; {short}'
            except ValueError:
                pass
        print(f'  0x{ins.address:08x}: {ins.mnemonic:<7}{ins.op_str}{extra}')
        cnt += 1
        if cnt > maxlines:
            print('  ...(truncated)')
            break

# sizes from symtab
for want in (0x45c750, 0x45e190):
    nm = symname.get(want, '?')
    sz = 0x800
    print(f'FUNC 0x{want:x} {nm[:90]}')

disasm(0x45c750, 0x540, 'CDoubleBufferedDynamicBatchMesh ctor', 200)
