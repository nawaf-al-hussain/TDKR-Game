#!/usr/bin/env python3
"""S32 T4: static Load decodes for priority + remaining fitted classes."""
import json, re, struct, collections
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
so = open(SO, 'rb').read()
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                      'session25/so_syms.json'))
by_addr = syms['by_addr']
fac = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                     'session25/factory_switch.json'))

PRIORITIES = [0x729EC572, 0xF5F8CFD, 0xDFE2718, 0x2CA13C06, 0x37F7A8AE,
              0xDDCD6C4]
remaining = json.load(open('/tmp/s32_remaining_fitted.json'))
targets = [str(x) for x in PRIORITIES] + remaining
print(f'targets: {len(targets)}')

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
# CMemoryStream read methods: find their addresses by symbol
readers = {}
for k, v in syms['by_name'].items():
    m = re.search(r'CMemoryStream\d+(\w+)E', k)
    if m and int(v, 16) < len(so):
        readers[int(v, 16)] = m.group(1)
print(f'CMemoryStream methods: {collections.Counter(readers.values())}')


def decode_load(addr, maxins=400):
    """walk the Load; collect BL targets -> reader names; count loops."""
    seq = []
    n = 0
    for i in md.disasm(so[addr:addr + maxins * 4], addr):
        n += 1
        if i.mnemonic in ('bl',):
            mm = re.search(r'0x([0-9a-f]+)', i.op_str)
            if mm:
                t = int(mm.group(1), 16)
                nm = readers.get(t)
                if nm:
                    seq.append(nm)
                elif t in by_addr:
                    nm2 = by_addr[t]
                    mm2 = re.search(r'CMemoryStream\d+(\w+)E', nm2)
                    if mm2:
                        seq.append(mm2.group(1))
                        readers[t] = mm2.group(1)
        if i.mnemonic == 'pop' and 'pc' in i.op_str:
            break
        if n >= maxins:
            break
    return seq


out = {}
for cid in targets:
    ent = fac.get(cid) or {}
    load = ent.get('load')
    if not load:
        out[cid] = dict(load=None)
        continue
    a = int(load, 16)
    seq = decode_load(a)
    # compress: count runs
    comp = collections.Counter(seq)
    out[cid] = dict(load=load, seq=seq, counts=dict(comp))
    print(f'{cid}: load @0x{a:x} -> {seq}')
json.dump(out, open('/home/z/my-project/download/s32_t4_loads.json', 'w'),
          indent=1)
print('wrote s32_t4_loads.json')
