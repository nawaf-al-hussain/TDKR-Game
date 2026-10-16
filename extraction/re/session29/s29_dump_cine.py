#!/usr/bin/env python3
"""S29 T1: full annotated disasm of CCinematicComponent::Load and CContainerTracksAnimatedObject::Load."""
import json, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
SYMS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
by_addr = SYMS['by_addr']
READER_SHORT = {
    0x339510: 'B', 0x339574: 'b', 0x3395D8: 'c', 0x339634: 'c',
    0x339690: 'B', 0x3396EC: 'B', 0x339758: 's', 0x3397DC: 's',
    0x339868: 's', 0x339914: 'i', 0x3399D4: 'i', 0x339AB4: 'i',
    0x339B94: 'f', 0x339C58: 'f', 0x33A0D4: 'STR', 0x33AB94: 'STR',
    0x33AD74: 'STR', 0x33B01C: 'STR', 0x33B3D0: 'v3', 0x33B4DC: 'v2',
    0x33B6AC: 'v4', 0x33BB10: 'data', 0x33BB40: 'data',
}
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dump(start, size, path):
    out = []
    for ins in md.disasm(d[start:start + size], start):
        ann = ''
        if ins.mnemonic in ('bl', 'blx'):
            try: t = int(ins.op_str.lstrip('#'), 0)
            except ValueError: t = None
            if t in READER_SHORT: ann = f'   ; <<READER {READER_SHORT[t]}>>'
            else:
                sy = by_addr.get(hex(t)) if t is not None else None
                if sy and len(sy) > 1 and not sy[1].startswith('$'):
                    ann = f'   ; <<{sy[1][:70]}>>'
        # literal pool annotation
        if ins.mnemonic == 'ldr' and '[pc, #' in ins.op_str:
            try:
                off = int(ins.op_str.split('#')[1].rstrip(']'), 16)
                pa = ((ins.address + 8) & ~3) + off
                if pa + 4 <= len(d):
                    v = struct.unpack_from('<I', d, pa)[0]
                    ann += f'   ; pool[{pa:#x}]={v:#x}'
            except Exception: pass
        out.append(f'{ins.address:#x}: {ins.mnemonic:<7s} {ins.op_str}{ann}')
    open(path, 'w').write('\n'.join(out))
    print(f'{path}: {len(out)} insns')

dump(0x292b4c, 0x29320c - 0x292b4c, '/tmp/my-project/work/re29/cinecomp_load.asm')
dump(0x2d9118, 0x2d9988 - 0x2d9118, '/tmp/my-project/work/re29/conttracks_load.asm')
dump(0x2dce20, 0x2de6c8 - 0x2dce20, '/tmp/my-project/work/re29/compcine_load.asm')
