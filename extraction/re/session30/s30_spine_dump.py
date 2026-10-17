#!/usr/bin/env python3
"""S30 T1a: annotated reader spine of CComponentCinematic::Load.
Prints every reader BL, loop head, and conditional branch with 2-insn
context, plus resolved call names. Output: cine_spine.txt
"""
import re, collections

READERS = {
    0x339510: 'B:ReadBool_ref', 0x339574: 'B:Read_boolref',
    0x3395D8: 'c:ReadChar', 0x339634: 'c:Read_charref',
    0x339690: 'B:ReadByte', 0x3396EC: 'B:Read_ucharref',
    0x339758: 's:ReadShort', 0x3397DC: 's:Read_shortref',
    0x339868: 'S:Read_ushortref', 0x339914: 'i:ReadInt',
    0x3399D4: 'i:Read_intref', 0x339AB4: 'i:Read_uintref',
    0x339B94: 'f:ReadFloat', 0x339C58: 'f:Read_floatref',
    0x33A0D4: 'STR:ReadString_ref', 0x33AB94: 'STR:ReadString',
    0x33AD74: 'STR:ReadStringC_ref', 0x33B01C: 'STR:ReadStringW_ref',
    0x33B3D0: 'v3:Read_vector3d', 0x33B4DC: 'v2:Read_vector2d',
    0x33B6AC: 'v4:Read_vector4d',
    0x33BB10: '?:ReadData_ptr', 0x33BB40: '?:ReadData_int',
}
NAMES = {
    0x2069fc: 'str_release', 0x206a60: 'str_assign', 0x206c64: 'str_???',
    0x3e9260: 'operator_delete', 0x3e91f8: 'operator_new',
    0x3e9324: 'glitch_alloc', 0x3e935c: 'glitch_free',
    0xa4ee8: 'memcpy', 0xa4e88: 'memset', 0xa4e1c: 'memcpy_plt',
    0x2d9118: 'CContainerTracksAnimatedObject::Load',
    0x2df108: 'cine_dtor', 0x2d391c: 'vec_helper_391c',
    0x2d4000: 'vec_helper_4000', 0x2ee8b8: 'vec_helper_e8b8',
    0x1efcb4: 'str_init_copy',
}

def parse(path):
    insns = []
    rx = re.compile(r'^(0x[0-9a-f]+):\s+(\S+)\s*(.*?)\s*(?:;\s*(.*))?$')
    for line in open(path):
        m = rx.match(line.rstrip('\n'))
        if m:
            insns.append((int(m.group(1), 16), m.group(2),
                          (m.group(3) or '').strip(), m.group(4) or ''))
    return insns

def main(path, out):
    insns = parse(path)
    idx_of = {a: i for i, (a, *_) in enumerate(insns)}
    lo, hi = insns[0][0], insns[-1][0]
    # branch targets
    btgt = {}
    for addr, mn, ops, ann in insns:
        m = re.match(r'#?(0x[0-9a-f]+)$', ops)
        if m and mn.startswith('b') and mn != 'bic':
            t = int(m.group(1), 16)
            if lo <= t <= hi:
                btgt.setdefault(t, []).append((addr, mn))
    lines = []
    mark = {}
    for t in btgt:
        srcs = btgt[t]
        back = any(a > t for a, _ in srcs)
        mark[t] = f'{"LOOPHEAD" if back else "FWD_TARGET"}(from 0x{srcs[0][0]:x} {srcs[0][1]})'
    for addr, mn, ops, ann in insns:
        if addr in mark:
            lines.append(f'--- {mark[addr]}')
        m = re.match(r'#?(0x[0-9a-f]+)$', ops)
        t = int(m.group(1), 16) if m else None
        tag = ''
        if mn == 'bl' and t is not None:
            if t in READERS:
                tag = f'   <<< READER {READERS[t]}'
            elif t in NAMES:
                tag = f'   <<< {NAMES[t]}'
            else:
                tag = f'   <<< sub_{t:x}'
        lines.append(f'0x{addr:x}: {mn:8s} {ops}{tag}')
    open(out, 'w').write('\n'.join(lines))
    print(f'wrote {out}, {len(lines)} lines')

if __name__ == '__main__':
    main('/tmp/my-project/work/re29/compcine_load.asm',
         '/tmp/my-project/work/TDKR-Game/extraction/re/session30/cine_spine.txt')
    main('/tmp/my-project/work/re29/conttracks_load.asm',
         '/tmp/my-project/work/TDKR-Game/extraction/re/session30/conttracks_spine.txt')
