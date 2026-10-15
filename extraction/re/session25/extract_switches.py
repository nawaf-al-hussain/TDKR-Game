#!/usr/bin/env python3
"""Extract dispatch switches: GenerateComponentTemplate @0x368ac0 (factory
miss) and CComponentFactory::CreateComponent @0x223e3c (factory hit).

For every typeId case, resolve the constructed object's vtable pointer and
the Load function the engine calls:
  GCT:     obj[0] = lit + (add+8) + 8 ; Load = [obj[0] + 0x10]
  factory: per-case convention verified below (usually [vt+8])
Output: work/gct_switch.json, work/factory_switch.json
"""
import struct
import json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
so = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
# RW segment: file 0xbbe930 <-> vaddr 0xbbf930 (bias 0 mapping)
RW_V = 0xbbf930
RW_F = 0xbbe930


def vread(v, n=4):
    return struct.unpack_from('<I', so, RW_F + (v - RW_V))[0] \
        if v >= RW_V else struct.unpack_from('<I', so, v)[0]


def extract(fn_start, fn_end, load_off, name):
    ins_list = list(md.disasm(so[fn_start:fn_end], fn_start))
    consts = []
    movw = {}
    for i, ins in enumerate(ins_list):
        m = ins.mnemonic
        if m == 'movw' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            movw[reg] = int(imm, 16)
        elif m == 'movt' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            if reg in movw:
                movw[reg] = (movw[reg] & 0xFFFF) | (int(imm, 16) << 16)
        elif m == 'mov' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            if reg in ('r3', 'r2', 'r1') and reg not in movw:
                movw[reg] = int(imm, 16)
        elif m == 'cmp':
            parts = ins.op_str.split(', ')
            if len(parts) == 2 and parts[0] == 'r0' and parts[1] in movw:
                for j in range(i + 1, min(i + 4, len(ins_list))):
                    if ins_list[j].mnemonic == 'beq':
                        consts.append((movw[parts[1]],
                                       int(ins_list[j].op_str.replace('#', ''),
                                           16)))
                        break
                    if ins_list[j].mnemonic in ('cmp', 'b'):
                        break
    out = {}
    for val, tgt in consts:
        sub = list(md.disasm(so[tgt:tgt + 160], tgt))
        lit = add_addr = None
        for ins in sub[:14]:
            if ins.mnemonic == 'ldr' and '[pc, #' in ins.op_str and lit is None:
                try:
                    off = int(ins.op_str.split('#')[1].rstrip(']'), 16)
                    lit_addr = ((ins.address + 8) & ~3) + off
                    lit = struct.unpack_from('<I', so, lit_addr)[0]
                except Exception:
                    pass
            elif ins.mnemonic == 'add' and ', pc,' in ins.op_str and \
                    add_addr is None:
                add_addr = ins.address
        if lit is None:
            out[val] = dict(case=hex(tgt), vt=None, load=None)
            continue
        if add_addr is None:
            add_addr = tgt + 8
        has_add8 = any(ins.mnemonic == 'add' and ins.op_str.endswith(', #8')
                       for ins in sub[:10])
        vt = (lit + add_addr + 8 + (8 if has_add8 else 0)) & 0xFFFFFFFF
        try:
            load = vread(vt + load_off)
        except Exception:
            load = None
        out[val] = dict(case=hex(tgt), vt=hex(vt),
                        load=hex(load) if load else None)
    print(f'{name}: {len(out)} cases')
    return out


def extract_factory(fn_start, fn_end, name):
    """Factory cases construct an object; the stream Load happens via the
    object's vtable ([vt+8]). Extract ctor -> vtable -> Load."""
    ins_list = list(md.disasm(so[fn_start:fn_end], fn_start))
    consts = []
    movw = {}
    for i, ins in enumerate(ins_list):
        m = ins.mnemonic
        if m == 'movw' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            movw[reg] = int(imm, 16)
        elif m == 'movt' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            if reg in movw:
                movw[reg] = (movw[reg] & 0xFFFF) | (int(imm, 16) << 16)
        elif m == 'mov' and '#0x' in ins.op_str:
            reg, imm = ins.op_str.split(', #')
            if reg in ('r3', 'r2', 'r1') and reg not in movw:
                movw[reg] = int(imm, 16)
        elif m == 'cmp':
            parts = ins.op_str.split(', ')
            if len(parts) == 2 and parts[0] == 'r0' and parts[1] in movw:
                for j in range(i + 1, min(i + 4, len(ins_list))):
                    if ins_list[j].mnemonic == 'beq':
                        consts.append((movw[parts[1]],
                                       int(ins_list[j].op_str.replace('#', ''),
                                           16)))
                        break
                    if ins_list[j].mnemonic in ('cmp', 'b'):
                        break
    out = {}
    for val, tgt in consts:
        sub = list(md.disasm(so[tgt:tgt + 120], tgt))
        new_seen = False
        ctor = None
        for ins in sub[:20]:
            if ins.mnemonic != 'bl':
                continue
            t2 = int(ins.op_str.replace('#', ''), 16)
            if not new_seen:
                if t2 in (0x3E91F8, 0x3E9204):
                    new_seen = True
                continue
            ctor = t2
            break
        vt = None
        if ctor:
            csub = list(md.disasm(so[ctor:ctor + 120], ctor))
            lit = add_addr = None
            for ins in csub[:16]:
                if ins.mnemonic == 'ldr' and '[pc, #' in ins.op_str and \
                        lit is None:
                    try:
                        off = int(ins.op_str.split('#')[1].rstrip(']'), 16)
                        lit_addr = ((ins.address + 8) & ~3) + off
                        lit = struct.unpack_from('<I', so, lit_addr)[0]
                    except Exception:
                        pass
                elif ins.mnemonic == 'add' and ', pc,' in ins.op_str and \
                        add_addr is None:
                    add_addr = ins.address
            if lit is not None and add_addr is not None:
                has_add8 = any(ins.mnemonic == 'add' and
                               ins.op_str.endswith(', #8')
                               for ins in csub[:12])
                vt = (lit + add_addr + 8 + (8 if has_add8 else 0)) & 0xFFFFFFFF
        load = None
        if vt:
            try:
                load = vread(vt + 8)
            except Exception:
                load = None
        out[val] = dict(case=hex(tgt), ctor=hex(ctor) if ctor else None,
                        vt=hex(vt) if vt else None,
                        load=hex(load) if load else None)
    print(f'{name}: {len(out)} cases')
    return out


gct = extract(0x368AC0, 0x374000, 0x10, 'GCT')
json.dump({hex(k): v for k, v in gct.items()},
          open('/home/z/my-project/work/gct_switch.json', 'w'), indent=0)
fac = extract_factory(0x223E3C, 0x232000, 'Factory')
json.dump({hex(k): v for k, v in fac.items()},
          open('/home/z/my-project/work/factory_switch.json', 'w'), indent=0)

for probe in (0x37883208, 0x31c00731, 0x37883207):
    print(hex(probe), 'GCT:', gct.get(probe), 'FAC:', fac.get(probe))
