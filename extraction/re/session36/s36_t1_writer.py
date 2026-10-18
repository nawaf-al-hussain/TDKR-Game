#!/usr/bin/env python3
"""S36 T1f: find stores to [rX,#0x5c]/[rX,#0x60] in CNavMeshNova/CNavMeshQuery range;
also who calls CanReachCellFrom / AppendPath / SearchPortalPath."""
import capstone, struct, json

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1 and p_filesz:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2f(v):
    for vaddr, off, filesz in segs:
        if vaddr <= v < vaddr + filesz:
            return off + (v - vaddr)
    return None

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

# scan whole text for 'str rX, [rY, #0x5c]' (immediate 0x5c = 92) ARM encoding:
# str imm: cond 010 1 0 0 0 Rn Rt imm12 -> word = c<<28|0x05800000|rn<<16|rt<<12|imm
hits5c, hits60 = [], []
for vaddr, off, filesz in segs:
    blob = d[off:off + filesz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0FF00000) == 0x05800000:
            imm = w & 0xFFF
            if imm == 0x5C: hits5c.append((vaddr + i, (w >> 16) & 0xF, (w >> 12) & 0xF))
            if imm == 0x60: hits60.append((vaddr + i, (w >> 16) & 0xF, (w >> 12) & 0xF))

syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
def who(a):
    # find symbol at or before a
    best = None
    for k, v in syms.items():
        va = int(k, 16)
        if va <= a and (best is None or va > best[0]):
            best = (va, v)
    return best

print('--- str [rn,#0x5c] sites in 0x1d0000-0x1e0000 (Nova/Query range) ---')
for a, rn, rt in hits5c:
    if 0x1d0000 <= a <= 0x1e0000:
        b = who(a)
        print(f'  0x{a:08x} rn=r{rn} rt=r{rt}  near={b[1][1] if b else "?"}')
print('--- str [rn,#0x60] sites in 0x1d0000-0x1e0000 ---')
for a, rn, rt in hits60:
    if 0x1d0000 <= a <= 0x1e0000:
        b = who(a)
        print(f'  0x{a:08x} rn=r{rn} rt=r{rt}  near={b[1][1] if b else "?"}')
