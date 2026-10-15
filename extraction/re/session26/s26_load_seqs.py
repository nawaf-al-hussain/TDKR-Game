#!/usr/bin/env python3
"""Extract reader-call sequences from Load functions (disasm level)."""
import struct, json, sys

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'
d = open(SO, 'rb').read()
syms = json.load(open(SYMS))['by_name']
items = sorted((int(v, 16), k) for k, v in syms.items())
addrs = [a for a, _ in items]
names = {a: k for a, k in items}

READER_SHORT = {
    0x339510: 'B', 0x339574: 'b', 0x3395D8: 'c', 0x339634: 'c',
    0x339690: 'B', 0x3396EC: 'B', 0x339758: 's', 0x3397DC: 's',
    0x339868: 's', 0x339914: 'i', 0x3399D4: 'i', 0x339AB4: 'i',
    0x339B94: 'f', 0x339C58: 'f', 0x33A0D4: 'STR', 0x33AB94: 'STR',
    0x33AD74: 'STR', 0x33B01C: 'STR', 0x33B3D0: 'v3', 0x33B4DC: 'v2',
    0x33B6AC: 'v4', 0x33BB10: 'data', 0x33BB40: 'data',
}

def trace_loads(START, label, maxn=400):
    i0 = __import__('bisect').bisect_right(addrs, START) - 1
    END = addrs[i0 + 1]
    print(f'\n; {label} {START:#x} .. {END:#x} ({END-START} B)')
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    seq = []
    for ins in md.disasm(d[START:START + (END - START)], START):
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.lstrip('#'), 0)
            except ValueError:
                continue
            if t in READER_SHORT:
                seq.append(f'{READER_SHORT[t]}@{ins.address:#x}')
            elif t in names:
                seq.append(f'CALL:{names[t].split("(")[0].split(".")[-1][:40]}@{ins.address:#x}')
        if len(seq) > maxn:
            break
    print('  ' + '\n  '.join(seq))

trace_loads(0x390750, 'CAnimationComponent::Load (0xf5f8cfd)')
trace_loads(int(syms['_ZN19CCinematicComponent4LoadEP13CMemoryStream'], 16),
            'CCinematicComponent::Load (0x17ac851f)')
trace_loads(int(syms['_ZN15CTrafficSetting4LoadEP13CMemoryStream'], 16),
            'CTrafficSetting::Load (0x3189e053)')
