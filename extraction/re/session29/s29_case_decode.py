#!/usr/bin/env python3
"""S29 T1: manual precise decode of case bodies for 0xc69a6a7 / 0x2ad64f3d / hunt 0x3377f0e."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def lit_of(ins_addr, off):
    pa = ((ins_addr + 8) & ~3) + off
    return pa, struct.unpack_from('<I', data, pa)[0]

print('=== 0xC69A6A7 generic case (body @0x369d68) ===')
pa, l1 = lit_of(0x369d70, -0x1b8)          # ldr r3,[pc,#-0x1b8] @0x369d70
print(f'  pool {pa:#x} lit {l1:#x}; add r3,pc,r3 @0x369d74 -> {l1 + 0x369d7c:#x}; +8 -> vt {(l1 + 0x369d7c + 8):#x}')
vt1 = l1 + 0x369d7c + 8
# vtable inspection: slots
def vread(v):
    if v >= 0xbbf930: return struct.unpack_from('<I', data, 0xbbe930 + (v - 0xbbf930))[0]
    return struct.unpack_from('<I', data, v)[0]
slots = [vread(vt1 + i * 4) for i in range(8)]
print('  vt slots:', [hex(s) for s in slots])

print('=== 0x2AD64F3D factory case (body @0x22454c) ===')
pa, l1 = lit_of(0x22454c, 0x908)           # ldr r1,[pc,#0x908]
s1 = l1 + 0x224560
o = s1 if s1 < 0xbbe1ec else s1 - 0x1000
s = data[o:o + 200]
z = s.find(b'\0')
print(f'  alloc-tag string @ {s1:#x}: {s[:z].decode("latin1")!r} (len field 0xfc)')
pa2, l2 = lit_of(0x224560, 0x8f8)          # ldr r2,[pc,#0x8f8]
vt_a = l2 + 0x224574 + 8                   # add r2,pc,r2 @0x22456c (+8 at 0x22457c)
pa3, l3 = lit_of(0x224564, 0x8f8)          # ldr r3,[pc,#0x8f8]
vt_b = l3 + 0x224578 + 8                   # add r3,pc,r3 @0x224570 (+8 at 0x224580)
print(f'  vt_a {vt_a:#x} slots:', [hex(vread(vt_a + i * 4)) for i in range(6)])
print(f'  vt_b {vt_b:#x} slots:', [hex(vread(vt_b + i * 4)) for i in range(6)])

print('=== hunt 0x3377F0E: cmp with ANY register in whole .text ===')
TARGET = 0x3377F0E
# movw/movt sequences feeding any cmp r?,r? within 8 insns
ins_all = []
start = 0x223000; end = 0x36c000   # factory + generic + GCT regions
ins_list = list(md.disasm(data[start:end], start))
movw = {}
hits = []
for idx, i in enumerate(ins_list):
    if i.mnemonic == 'movw' and '#0x' in i.op_str:
        reg, imm = i.op_str.split(', #')
        if ',' not in reg: movw[reg] = int(imm, 16)
    elif i.mnemonic == 'movt' and '#0x' in i.op_str:
        reg, imm = i.op_str.split(', #')
        if reg in movw: movw[reg] = movw[reg] & 0xFFFF | (int(imm, 16) << 16)
    elif i.mnemonic == 'ldr' and '[pc, #' in i.op_str and i.op_str.endswith(']'):
        off = int(i.op_str.split('#')[1].rstrip(']'), 16)
        pa, _ = lit_of(i.address, off)
        movw[f'lit{i.address}'] = None  # placeholder
    elif i.mnemonic == 'cmp' and ', ' in i.op_str:
        parts = i.op_str.split(', ')
        if len(parts) < 2: continue
        a, b = parts[0], parts[1]
        if b in movw and movw[b] == TARGET:
            hits.append((i.address, a))
print('cmp hits for 0x3377F0E:', [(hex(a), b) for a, b in hits[:10]] or 'NONE in 0x223000..0x36c000')
# also try ldr-literal compare: scan literal pools in 0x223000..0x36c000 for the value
found = False
for i in range(start, end - 4, 4):
    if struct.unpack_from('<I', data, i)[0] == TARGET:
        print(f'  literal {TARGET:#x} at {i:#x} (in code region!)'); found = True
if not found: print('  no literal pool word either')
# and the low-half high-half check with different splits
for lo, hi in [(0x7F0E, 0x337), (0xF0E, 0x3377), (0x3377, 0xF0E)]:
    ws = [i for i in range(0xa5d80, 0xac2490 - 4, 4) if (struct.unpack_from('<I', data, i)[0] & 0x0FF00000) == 0x03000000 and ((struct.unpack_from('<I', data, i)[0] >> 4 & 0xF000) | (struct.unpack_from('<I', data, i)[0] & 0xFFF)) == lo]
    ts = [i for i in range(0xa5d80, 0xac2490 - 4, 4) if (struct.unpack_from('<I', data, i)[0] & 0x0FF00000) == 0x03400000 and ((struct.unpack_from('<I', data, i)[0] >> 4 & 0xF000) | (struct.unpack_from('<I', data, i)[0] & 0xFFF)) == hi]
    print(f'  split {lo:#x}/{hi:#x}: MOVW x{len(ws)} {[hex(x) for x in ws[:4]]}, MOVT x{len(ts)} {[hex(x) for x in ts[:4]]}')
