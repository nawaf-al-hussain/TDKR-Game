#!/usr/bin/env python3
"""Extract per-class Load read sequences -> the LVC generic-record framing table.
Join: gol component typeIds -> vtable_classes.json -> Load fn -> disasm read seq.
Special in-loop components (0x14ca79 base TRS, 0x152b87 name+4bools) hardcoded
from CreateObject @0x36774c disasm."""
import struct, re, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

SO = '/home/z/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
syms = {}
for line in open('/home/z/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[2] == 'FUNC':
        syms[int(p[0], 16)] = (p[3], int(p[1]))

md_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
md_thm = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)

READERS = {
    0x339510: ('B', 1), 0x339574: ('B', 1),          # ReadBool
    0x3395d8: ('c', 1), 0x339634: ('c', 1),          # ReadChar
    0x339690: ('u8', 1), 0x3396ec: ('u8', 1),        # ReadByte
    0x339758: ('s16', 2), 0x3397dc: ('s16', 2), 0x339868: ('u16', 2),
    0x339914: ('i', 4), 0x3399d4: ('i', 4), 0x339ab4: ('i', 4),  # ReadInt
    0x339b94: ('f', 4), 0x339c58: ('f', 4),          # ReadFloat
    0x33a0d4: ('STR', None), 0x33ab94: ('STR', None), 0x33ad74: ('STR', None),
    0x33b3d0: ('v3', 12), 0x33b4dc: ('v2', 8), 0x33b6ac: ('v4', 16),
    0x33b6e8: ('BLK', None), 0x33b718: ('BLKEND', 0), 0x33b728: ('SKIPBLK', None),
}
NEW = 0x3e9204

def disasm(va, size):
    thumb = va & 1
    v = va & ~1
    md = md_thm if thumb else md_arm
    out = []
    for i in md.disasm(d[v:v+size], v):
        out.append((i.address, i.mnemonic, i.op_str))
    return out

def fn_end(va):
    nxt = min((a for a in syms if a > (va & ~1)), default=(va & ~1) + 0x3000)
    return min(nxt, (va & ~1) + 0x3000)

SKIP_TARGETS = {0x3e9204, 0x3e91f8, 0x3e9260, 0x3e9324, 0x3e935c}  # allocators

def read_seq(load_va, depth=0):
    """Walk a Load fn; return [(reader, size)], fixed_total, has_var, has_block.
    If the body itself has NO reader calls, expand bl/b tail-call targets one
    level (the CComponentBuiltin*::Load delegation pattern)."""
    va = load_va & ~1
    size = syms.get(va, (0, 0))[1]
    end = va + (size if size else (fn_end(va) - va))
    seq = disasm(va, end - va)
    out = []
    fixed = 0
    var = False
    blk = False
    callees = []
    for a, m, o in seq:
        if m == 'bl':
            t = int(o.lstrip('#'), 16)
            r = READERS.get(t)
            if r:
                out.append((r[0], r[1]))
                if r[1] is None:
                    var = True
                    if r[0] in ('BLK', 'SKIPBLK'):
                        blk = True
                else:
                    fixed += r[1]
            elif t == NEW:
                out.append(('NEW', 0))
            elif t not in SKIP_TARGETS and depth < 2:
                callees.append(t)
        elif m == 'b' and o.startswith('#0x') and depth < 2:
            t = int(o.lstrip('#'), 16)
            if t not in SKIP_TARGETS and t != a + 4:
                callees.append(t)
    if not [x for x in out if x[0] not in ('NEW',)] and callees:
        for t in callees:
            try:
                s2, f2, v2, b2 = read_seq(t, depth + 1)
            except Exception:
                continue
            if s2:
                out.extend(s2)
                fixed += f2
                var = var or v2
                blk = blk or b2
                break  # first reading callee wins (delegation)
    return out, fixed, var, blk

classes = json.load(open('/home/z/work/tdkr/vtable_classes.json'))
gol = json.load(open('/home/z/work/tdkr/gol_templates.json'))
tids = sorted({t for v in gol['templates'].values() for f, t in v})
use = {}
for v in gol['templates'].values():
    for f, t in v:
        use.setdefault(t, [0, 0])
        use[t][f] += 1

table = {}
for t in tids:
    k = f'{t:#x}'
    e = classes.get(k)
    entry = {'load_sym': None, 'read_seq': None, 'fixed': None, 'var': None, 'block': None,
             'n_flag0': use[t][0], 'n_flag1': use[t][1]}
    if e:
        entry['load_sym'] = e['load_sym']
        load = int(e['load'], 16)
        if load & ~1 in syms or True:
            try:
                seq, fixed, var, blk = read_seq(load)
                entry['read_seq'] = [s for s, _ in seq]
                entry['fixed'] = fixed
                entry['var'] = var
                entry['block'] = blk
                entry['load_addr'] = hex(load)
            except Exception as ex:
                entry['err'] = str(ex)
    table[f'{t:#010x}'] = entry

# special in-loop components from CreateObject disasm:
table['0x0014ca79'].update({'load_sym': 'SPECIAL CComponentBase::Load @0x1fe924 (bool,int objId,9f TRS,3b)',
                            'read_seq': ['B', 'i', 'f']*1 + ['f']*9 + ['B', 'B', 'B'],
                            'fixed': 1 + 4 + 36 + 3, 'var': False, 'block': False})
table['0x00152b87'].update({'load_sym': 'SPECIAL name component @0x367d18 (ReadString + 4 bools)',
                            'read_seq': ['STR', 'B', 'B', 'B', 'B'],
                            'fixed': 4, 'var': True, 'block': False})
json.dump(table, open('/home/z/work/tdkr/component_loads.json', 'w'), indent=1)

need = [t for t, e in table.items() if e['n_flag0'] > 0]
print(f'typeIds needing stream reads (flag0>0): {len(need)}')
print(f'  with decoded read_seq: {len([t for t in need if table[t].get("read_seq")])}')
for t in need:
    e = table[t]
    print(f'{t} n0={e["n_flag0"]:3d} n1={e["n_flag1"]:3d} '
          f'fixed={e["fixed"]} var={e["var"]} blk={e["block"]} {e["load_sym"]}')
