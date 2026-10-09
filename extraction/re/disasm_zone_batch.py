#!/usr/bin/env python3
"""Disassemble key glitch zone-mesh functions to recover SBatch layout and
the batch_info.bin record format (batch -> material link)."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

LIB = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(LIB, 'rb').read()

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False

# read symtab for name lookup on bl targets
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

def disasm(addr, size, title):
    print(f'\n=== {title} @0x{addr:x} (0x{size:x} bytes) ===')
    code = d[addr:addr + size]
    for ins in md.disasm(code, addr):
        extra = ''
        if ins.mnemonic == 'bl':
            try:
                tgt = int(ins.op_str[1:], 16)
                if tgt in symname:
                    nm = symname[tgt]
                    extra = '   ; ' + (nm[:90] + '…' if len(nm) > 90 else nm)
            except ValueError:
                pass
        if ins.mnemonic in ('ldr',) and 'pc' in ins.op_str:
            m = ins.op_str.split('#')
            if len(m) > 1:
                try:
                    imm = int(m[-1], 0) & 0xfff
                    pool = (ins.address + 8 + imm) & ~3
                    val = struct.unpack_from('<I', d, pool)[0]
                    extra += f'   ; [0x{pool:x}] = 0x{val:x}'
                except ValueError:
                    pass
        print(f'  0x{ins.address:08x}: {ins.mnemonic:<8}{ins.op_str}{extra}')

disasm(0x44ef08, 0xb0, 'getBatchMaterial')
disasm(0x3f7abc, 8, 'ProcessBatchMeshFunctor_DB::operator() (thunk?)')
