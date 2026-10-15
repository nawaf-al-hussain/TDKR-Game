#!/usr/bin/env python3
"""Vtable scan v2: .data holds vtables whose fn entries may be even (no thumb bit).
Run of >=6 words that are .text addresses; run[2]=Load ([vptr+8]), run[9]=GetClassId
([vptr+0x24]). GetClassId fn disasm -> movw/movt constant = classId."""
import struct, re, json
import numpy as np
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

SO = '/home/z/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
TEXT_LO, TEXT_HI = 0x8000, 0xbbe1ec

syms = {}
for line in open('/home/z/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[2] == 'FUNC':
        syms[int(p[0], 16)] = (p[3], int(p[1]))

n_total = len(d) // 4
w = np.frombuffer(d[:n_total*4], dtype='<u4')
mask = (w >= TEXT_LO) & (w < TEXT_HI)
idx = np.flatnonzero(mask)
breaks = np.flatnonzero(np.diff(idx) != 1)
starts = np.concatenate(([0], breaks + 1))
ends = np.concatenate((breaks, [len(idx) - 1]))

md_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
md_thm = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)

def get_clsid(fn_va):
    """Disasm tiny GetClassId fn: movw r0,#lo(,movt r0,#hi); ret.
    Also handles: ldr r0,[pc,#imm] literal loads, movw-only small ids."""
    thumb = fn_va & 1
    va = fn_va & ~1
    md = md_thm if thumb else md_arm
    lo = hi = None
    try:
        for i in md.disasm(d[va:va+40], va):
            mm = re.match(r'(\w+), #?(0x[0-9a-f]+|\d+)$', i.op_str or '')
            if i.mnemonic == 'movw' and mm:
                lo = int(mm.group(2), 0)
            elif i.mnemonic == 'movt' and mm and lo is not None:
                hi = int(mm.group(2), 0)
                break
            elif i.mnemonic == 'ldr' and '[pc' in (i.op_str or ''):
                m2 = re.search(r'\[pc, #(\d+)\]', i.op_str)
                lit = (i.address + 8 + int(m2.group(1))) & ~3
                w2 = struct.unpack_from('<I', d, lit)[0]
                lo = w2 & 0xffff
                hi = w2 >> 16
                break
            elif i.mnemonic in ('bx', 'pop'):
                break
    except Exception:
        return None
    if lo is None:
        return None
    if hi is None:
        hi = 0
    return lo | (hi << 16)

classes = {}   # clsid -> info
runs = 0
for s, e in zip(starts, ends):
    ln = int(e - s + 1)
    if ln < 6:
        continue
    runs += 1
    base_file = int(idx[s]) * 4
    vt = w[int(idx[s]):int(idx[s])+ln]
    clsid = get_clsid(int(vt[9])) if ln > 9 else None
    if clsid is not None:
        load = int(vt[2])
        classes[f'{clsid:#x}'] = {
            'vtable_file': hex(base_file),
            'vslots': ln,
            'load': hex(load),
            'load_sym': syms.get(load, ('?', 0))[0],
            'clsid_fn': hex(int(vt[9])),
        }
print(f'runs>=6: {runs}, classes with classid: {len(classes)}')
json.dump(classes, open('/home/z/work/tdkr/vtable_classes.json', 'w'), indent=1)

gol = json.load(open('/home/z/work/tdkr/gol_templates.json'))
tids = sorted({t for v in gol['templates'].values() for f, t in v})
hit = [t for t in tids if f'{t:#x}' in classes]
print(f'gol typeIds matched: {len(hit)}/{len(tids)}')
for t in tids[:10]:
    e = classes.get(f'{t:#x}')
    print(f'{t:#010x} -> {(e or {}).get("load_sym", "?")}')
