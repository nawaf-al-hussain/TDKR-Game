#!/usr/bin/env python3
"""S29 T1: extract reader-call sequences for the cinematic chain."""
import json, struct, sys
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
SYMS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
by_name = SYMS['by_name']
by_addr = SYMS['by_addr']

READER_SHORT = {
    0x339510: 'B', 0x339574: 'b', 0x3395D8: 'c', 0x339634: 'c',
    0x339690: 'B', 0x3396EC: 'B', 0x339758: 's', 0x3397DC: 's',
    0x339868: 's', 0x339914: 'i', 0x3399D4: 'i', 0x339AB4: 'i',
    0x339B94: 'f', 0x339C58: 'f', 0x33A0D4: 'STR', 0x33AB94: 'STR',
    0x33AD74: 'STR', 0x33B01C: 'STR', 0x33B3D0: 'v3', 0x33B4DC: 'v2',
    0x33B6AC: 'v4', 0x33BB10: 'data', 0x33BB40: 'data',
}
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def fn_bounds(start):
    addrs = sorted(int(v, 16) for v in by_addr if v.startswith('0x'))
    import bisect
    i = bisect.bisect_right(addrs, start) - 1
    return start, addrs[i + 1]

def seq(start, label, maxn=500):
    s, e = fn_bounds(start)
    print(f'\n; {label} {s:#x} .. {e:#x} ({e-s} B)')
    out = []
    for ins in md.disasm(d[s:s + (e - s)], s):
        if ins.mnemonic in ('bl', 'blx'):
            try: t = int(ins.op_str.lstrip('#'), 0)
            except ValueError: continue
            if t in READER_SHORT:
                out.append(f'{READER_SHORT[t]}@{ins.address:#x}')
            else:
                syms_t = by_addr.get(hex(t))
                nm = syms_t[1] if syms_t and len(syms_t) > 1 else '?'
                if nm and not nm.startswith('$'):
                    out.append(f'CALL:{nm.split("(")[0].split(".")[-1][:44]}@{ins.address:#x}')
        if len(out) > maxn: break
    for l in out: print('  ' + l)

seq(int(by_name['_ZN19CCinematicComponent4LoadEP13CMemoryStream'], 16), 'CCinematicComponent::Load')
seq(0x2dce20, 'CComponentCinematic::Load (tid 0x2b)')
seq(0x2d9118, 'CContainerTracksAnimatedObject::Load')
