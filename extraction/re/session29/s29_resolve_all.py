#!/usr/bin/env python3
"""S29 T1: resolve ALL remaining component ids via MOVW/MOVT scan + symbol lookup."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
SYMS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
by_addr = SYMS['by_addr']
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
TEXT = (0xa5d80, 0xac2490)

TARGETS = {
    0xC69A6A7: 'ZonesLink?', 0x2AD64F3D: 'PlaneNode?', 0x3377F0E: 'Military?',
    0x295: 'l_menu', 0x433: 'shop', 0x2056: 'Stadion', 0x4E52B: 'Police_Station',
    0x4A2B: 'StockExchange', 0x2A953: 'Underground', 0xBC0: 'Military2',
    0x7F88E44E: 'Military_gctfault', 0x10FF796: 'Dummy', 0x7F8ED4E: 'autofit40B',
    0x288AE7DA: 'WorldBox6', 0x16F31: 'head14body15',
}
lastW = {}
pairs = {}
for i in range(TEXT[0], TEXT[1] - 4, 4):
    w = struct.unpack_from('<I', d, i)[0]
    t = w & 0x0FF00000
    if t == 0x03000000:
        lastW[(w >> 12) & 0xF] = (i, ((w >> 4) & 0xF000) | (w & 0xFFF))
    elif t == 0x03400000:
        rd_ = (w >> 12) & 0xF
        if rd_ in lastW:
            aw, vw = lastW[rd_]
            if 0 < i - aw <= 0x40:
                val = ((((w >> 4) & 0xF000) | (w & 0xFFF)) << 16) | vw
                pairs.setdefault(val, []).append((aw, i))

def sym(a):
    s = by_addr.get(hex(a))
    return s[1] if s and len(s) > 1 else None

def resolve_load_from_case(case_addr, is_beq):
    """Walk case body: find vtable setup (ldr+add pc) then read Load slot."""
    body = case_addr
    sub = list(md.disasm(d[body:body + 0xC0], body))
    lits = []
    for k, s in enumerate(sub[:12]):
        if s.mnemonic == 'ldr' and '[pc, #' in s.op_str:
            off = int(s.op_str.split('#')[1].rstrip(']'), 16)
            pa = ((s.address + 8) & ~3) + off
            lits.append((k, struct.unpack_from('<I', d, pa)[0]))
        if s.mnemonic == 'add' and ', pc,' in s.op_str:
            # vtable = lit + (this add's addr + 8) [+8]
            if lits:
                k2, lit = lits[-1]
                has8 = any(x.mnemonic == 'add' and x.op_str.endswith(', #8') for x in sub[k:k + 4])
                vt = (lit + s.address + 8 + (8 if has8 else 0)) & 0xFFFFFFFF
                return vt
    return None

def vread(v):
    if v >= 0xbbf930: return struct.unpack_from('<I', d, 0xbbe930 + (v - 0xbbf930))[0]
    return struct.unpack_from('<I', d, v)[0]

out = {}
for tid, tag in TARGETS.items():
    locs = pairs.get(tid, [])
    info = {'tag': tag, 'sites': [(hex(a), hex(b)) for a, b in locs[:6]], 'nsites': len(locs)}
    loads = set()
    for aw, at in locs[:6]:
        # what follows the pair: cmp r0,rX ; beq/bne -> case body
        sub = list(md.disasm(d[at + 4:at + 0x14], at + 4))
        tgt = None; sense = None; body = None
        for k, s in enumerate(sub[:3]):
            if s.mnemonic == 'cmp': continue
            if s.mnemonic in ('beq', 'bne') and s.op_str.startswith('#'):
                tgt = int(s.op_str[1:], 16); sense = s.mnemonic
                body = tgt if sense == 'beq' else sub[k + 1].address if k + 1 < len(sub) else None
                break
            if s.mnemonic in ('b', 'bl'): break
        if body:
            vt = resolve_load_from_case(body, sense == 'beq')
            if vt:
                for slot in (0x8, 0x10, 0xc, 0x14):
                    fn = vread(vt + slot)
                    nm = sym(fn)
                    if nm and 'LoadEP13CMemoryStream' in nm:
                        loads.add((hex(vt), hex(slot), hex(fn), nm))
                    elif nm and nm.startswith('_ZN'):
                        loads.add((hex(vt), hex(slot), hex(fn), nm))
    info['loads'] = sorted(loads)
    out[hex(tid)] = info
    print(f"{tid:#010x} {tag:18s} sites={len(locs)}")
    for a, b in locs[:3]: print(f"    pair {a}/{b}")
    for vt, slot, fn, nm in sorted(loads)[:3]:
        print(f"    vt {vt} slot+{slot} -> {fn} {nm[:64]}")
json.dump(out, open('/tmp/my-project/work/re29/s29_id_resolution.json', 'w'), indent=1)
