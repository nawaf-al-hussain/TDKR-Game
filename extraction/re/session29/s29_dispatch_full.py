#!/usr/bin/env python3
"""S29 T1: complete dispatch extractor over factory + generic switch regions.
Pattern: movw rX,#lo ; movt rX,#hi ; cmp r0,rX ; beq/bne target.
For bne: case body is INLINE (falls through when equal)."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

REGIONS = {
    'factory_CreateComponent': (0x223e3c, 0x225900),
    'generic_CreateObject': (0x368ac0, 0x36b400),
}

def vread(v):
    # vaddr -> file (RW bias: vaddr 0xbbf930 = file 0xbbe930)
    if v >= 0xbbf930: return struct.unpack_from('<I', data, 0xbbe930 + (v - 0xbbf930))[0]
    return struct.unpack_from('<I', data, v)[0]

def cstr(v, m=48):
    o = v if v < 0xbbe1ec else v - 0x1000
    if o is None or o >= len(data) or o < 0: return None
    z = data.find(b'\0', o, o + m)
    s = data[o:z if z >= 0 else o + m]
    if not s or not all(0x20 <= c < 0x7f for c in s): return None
    return s.decode('latin1')

out = {}
for rname, (start, end) in REGIONS.items():
    ins = list(md.disasm(data[start:end], start))
    res = {}
    movw = {}
    for idx, i in enumerate(ins):
        if i.mnemonic == 'movw' and '#0x' in i.op_str:
            reg, imm = i.op_str.split(', #')
            if ',' not in reg:
                movw[reg] = int(imm, 16)
        elif i.mnemonic == 'movt' and '#0x' in i.op_str:
            reg, imm = i.op_str.split(', #')
            if reg in movw and movw[reg] < 0x10000:
                movw[reg] |= int(imm, 16) << 16
            else:
                movw[reg] = int(imm, 16) << 16
        elif i.mnemonic == 'cmp' and ', ' in i.op_str:
            a, b = i.op_str.split(', ')
            if a == 'r0' and b in movw and movw[b] >= 0x100:
                val = movw[b]
                # branch target
                tgt = None; sense = None
                for j in range(idx + 1, min(idx + 3, len(ins))):
                    if ins[j].mnemonic in ('beq', 'bne') and ins[j].op_str.startswith('#'):
                        tgt = int(ins[j].op_str[1:], 16); sense = ins[j].mnemonic; break
                    if ins[j].mnemonic in ('cmp', 'b', 'bl'): break
                if tgt is None: continue
                body = tgt if sense == 'beq' else ins[idx + 1].address  # bne: inline body
                # read case body prologue: bl alloc(0x3e91f8/0x3e9204)? vtable?
                sub = list(md.disasm(data[body:body + 0x90], body))
                alloc = None; vt = None
                for k, s in enumerate(sub[:16]):
                    if s.mnemonic == 'bl' and int(s.op_str[1:], 16) in (0x3e91f8, 0x3e9204):
                        # size in r0 set by preceding mov/movw
                        for kk in range(k - 1, max(k - 6, -1), -1):
                            if sub[kk].mnemonic in ('mov', 'movw') and sub[kk].op_str.startswith('r0, #'):
                                alloc = int(sub[kk].op_str.split('#')[1], 16); break
                    if s.mnemonic == 'ldr' and '[pc, #' in s.op_str and s.op_str.endswith(']'):
                        off = int(s.op_str.split('#')[1].rstrip(']'), 16)
                        pa = ((s.address + 8) & ~3) + off
                        lit = struct.unpack_from('<I', data, pa)[0]
                        # next: add rX, pc / add rX, rX, #8
                        for s2 in sub[k + 1:k + 4]:
                            if s2.mnemonic == 'add' and (', pc,' in s2.op_str or ', r' in s2.op_str):
                                has8 = any(x.mnemonic == 'add' and x.op_str.endswith(', #8') for x in sub[k:k + 5])
                                vt = (lit + s2.address + 8 + (8 if has8 else 0)) & 0xFFFFFFFF
                                break
                    if vt: break
                load = vread(vt + 0x10) if vt else None
                vtname = cstr(vread(vt + 4)) if vt else None
                res[hex(val)] = {'region': rname, 'case': hex(body), 'sense': sense,
                                 'alloc': alloc, 'vt': hex(vt) if vt else None,
                                 'load': hex(load) if load else None, 'vtstr': vtname}
    print(f'{rname}: {len(res)} ids')
    out.update(res)

json.dump(out, open('/tmp/my-project/work/re29/dispatch_complete.json', 'w'), indent=1)
for tid in ('0xc69a6a7', '0x2ad64f3d', '0x3377f0e'):
    print(tid, '->', out.get(tid, 'NOT FOUND'))
