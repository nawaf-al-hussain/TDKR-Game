#!/usr/bin/env python3
"""T2 engine-driven evidence: dump the skin technique init + the SSkin
structures the bdae loader fills. Also locate the -mesh-skin float clusters
in batman.bdae and validate them as 4x4 inverse-bind matrices.
"""
import struct
import json
from capstone import *

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
so = open(SO, 'rb').read()
syms = json.load(open('/home/z/my-project/work/so_syms.json'))
by_addr = {int(k, 16): v for k, v in syms['by_addr'].items()}
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)


def dis(start, n, label):
    print(f'=== {label} @0x{start:06x}')
    cnt = 0
    for ins in md.disasm(so[start:start + n * 4 + 24], start):
        line = f"0x{ins.address:06x}: {ins.mnemonic} {ins.op_str}"
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                nm = by_addr.get(t, [None])[0] or ''
                line += f"  ; {nm[:56]}"
            except ValueError:
                line += "  ; blx reg"
        print(line)
        cnt += 1
        if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            break
        if cnt >= n:
            break


if __name__ == '__main__':
    dis(0x7cbbfc, 26, 'CHardwareMatrixSkinTechnique::init')
    dis(0x7cbc40, 30, 'CHardwareMatrixSkinTechnique::skin')
