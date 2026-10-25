#!/usr/bin/env python3
"""S60 T1 step 1 (v2): COMPLETE case extraction from GenerateComponentTemplate 0x368ac0.
Handles: beq <case> AND cmp;bne default (fallthrough = case body).
Classifies case bodies: vtable-direct literal OR ctor-call (scans past operator new).
Output: s60_gct_cases.json
"""
import struct, subprocess, bisect, json, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

def rd32(v):
    o = v2o(v)
    return struct.unpack_from('<I', data, o)[0] if o is not None else None

nmout = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for line in nmout.splitlines():
    p = line.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

def dem(n):
    return subprocess.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

GCT = 0x368ac0
GCT_END = 0x36b6e0
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
o = v2o(GCT)
insns = list(md.disasm(data[o:o + (GCT_END - GCT)], GCT))
print('disasm insns:', len(insns))

# id constants: movw rX,#imm ; movt rX,#imm within 6 insns
const = {}  # addr_of_movw -> (reg, val)
for idx, ins in enumerate(insns):
    if ins.mnemonic == 'movw' and '#' in ins.op_str:
        reg = ins.op_str.split(',')[0].strip()
        try:
            lo = int(ins.op_str.split('#')[1].split(',')[0], 16)
        except Exception:
            continue
        for j in range(idx + 1, min(idx + 7, len(insns))):
            i2 = insns[j]
            if i2.mnemonic == 'movw':
                break
            if i2.mnemonic == 'movt' and i2.op_str.split(',')[0].strip() == reg:
                try:
                    hi = int(i2.op_str.split('#')[1], 16)
                except Exception:
                    break
                const[ins.address] = (reg, (hi << 16) | lo)
                break

# cmp r0, rX  -> find recent const for rX ; branch beq TGT (case) or bne DEF (fallthrough case)
cases = {}
for idx, ins in enumerate(insns):
    if ins.mnemonic != 'cmp' or not ins.op_str.startswith('r0, '):
        continue
    reg = ins.op_str.split(',')[1].strip()
    best = None
    for a, (r, val) in const.items():
        if r == reg and 0 < ins.address - a <= 0x14:
            if best is None or a > best[0]:
                best = (a, val)
    if best is None:
        continue
    for j in range(idx + 1, min(idx + 7, len(insns))):
        i2 = insns[j]
        if i2.mnemonic == 'beq' and i2.op_str.startswith('#'):
            cases[best[1]] = int(i2.op_str.lstrip('#'), 16)
            break
        if i2.mnemonic == 'bne' and i2.op_str.startswith('#'):
            # default branch; case body = fallthrough = next insn addr
            cases[best[1]] = insns[idx + 1].address
            break

print('cases found:', len(cases))

NEW_SYMS = ('_Znwj', '_Znwm', '_Znam', '_ZdaPv', '_ZdlPv')
out = {}
for cid, tgt in sorted(cases.items()):
    body_o = v2o(tgt)
    body = list(md.disasm(data[body_o:body_o + 0x80], tgt))
    info = {'id': '0x%08x' % cid, 'case_addr': '0x%x' % tgt, 'kind': None,
            'vtable': None, 'ctor': None, 'reader': None, 'alloc': None}
    vtbl = None
    ctor = None
    is_new = False
    for k, ins in enumerate(body):
        if ins.mnemonic == 'bl' and ins.op_str.startswith('#'):
            t = int(ins.op_str.lstrip('#'), 16)
            s, off = sym_of(t)
            if any(n in s for n in NEW_SYMS):
                is_new = True
                continue
            ctor = t
            break
        if ins.mnemonic == 'b' and ins.op_str.startswith('#') and int(ins.op_str.lstrip('#'), 16) == 0x368bfc:
            break
    for k, ins in enumerate(body):
        if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
            reg = ins.op_str.split(',')[0].strip()
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 16)
            pool = ins.address + 8 + imm
            W = rd32(pool)
            if W is None:
                continue
            for j in range(k + 1, min(k + 6, len(body))):
                i2 = body[j]
                if i2.mnemonic == 'add' and i2.op_str.startswith(reg + ', pc, '):
                    vt = (W + i2.address + 8) & 0xffffffff
                    for j2 in range(j + 1, min(j + 4, len(body))):
                        i3 = body[j2]
                        if i3.mnemonic == 'add' and i3.op_str.startswith(reg + ', ' + reg + ', #8'):
                            vt = (vt + 8) & 0xffffffff
                            break
                        if i3.mnemonic == 'str':
                            break
                    vtbl = vt
                    break
                if i2.mnemonic in ('str', 'b', 'bl', 'blx'):
                    break
            if vtbl:
                break
    if is_new and 'alloc' not in info:
        for ins in body:
            if ins.mnemonic == 'mov' and ins.op_str.startswith('r0, #'):
                info['alloc'] = int(ins.op_str.split('#')[1], 16)
                break
    if ctor:
        s, off = sym_of(ctor)
        info['ctor'] = '0x%x' % ctor
        info['ctor_sym'] = dem(s)[:90]
        info['kind'] = 'CTOR_CALL'
    if vtbl:
        info['kind'] = info['kind'] or 'VTABLE_DIRECT'
        info['vtable'] = '0x%x' % vtbl
        fn = rd32(vtbl + 0x10)
        if fn and 0xa5d80 <= fn <= 0xac2190:
            info['reader'] = '0x%x' % fn
            s, off = sym_of(fn)
            info['reader_sym'] = dem(s) + ('' if off == 0 else ' +0x%x' % off)
        else:
            info['reader_bad'] = hex(fn) if fn else None
        s, off = sym_of(vtbl)
        info['vtable_sym'] = dem(s)[:90]
    if not info['kind']:
        info['kind'] = 'UNCLASSIFIED'
    out['0x%08x' % cid] = info

json.dump(out, open('/tmp/my-project/scripts/s60_gct_cases.json', 'w'), indent=1)
kinds = {}
for v in out.values():
    kinds[v['kind']] = kinds.get(v['kind'], 0) + 1
print('kinds:', kinds)
nr = sum(1 for v in out.values() if v.get('reader'))
print('with reader:', nr)
for k in ('0x2db081e2', '0x6754056b', '0x0ddcd6c4', '0x5441a117', '0x43c8a8d1', '0x67c82e62',
          '0x0e1f5b6f', '0x0116a6fa', '0x4cc04ddb', '0x14ca79', '0x152b87', '0x3ef5108d',
          '0x44c6e9e5', '0x3e2bb040', '0x54989cb1', '0x592ce07c', '0x40c6b80a', '0x33702f4a'):
    v = out.get(k)
    if v:
        print(k, '->', v['kind'], v.get('reader'), (v.get('reader_sym') or '')[:70], '|', (v.get('ctor_sym') or '')[:60])
    else:
        print(k, '-> NO CASE')
