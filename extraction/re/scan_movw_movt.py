#!/usr/bin/env python3
"""
TDKR RE — scan libKRHP.so for MOVW/MOVT immediate pairs forming the 'DICT' FourCC.
movw Rd, #0x4944  ('DI' LE) + movt Rd, #0x5443 ('CT' LE)  =>  u32 0x54434944 = 'DICT'
Covers both ARM (A1) and Thumb-2 (T3/T1) encodings, reports nearby pairs.
Also scans for any other FourCC-looking movw/movt pairs to cross-check (optional).
"""
import struct, sys

SO = "/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so"
data = open(SO, "rb").read()

# --- parse ELF32 program headers to map file offset -> vaddr ---
e_phoff = struct.unpack_from("<I", data, 0x1C)[0]
e_phentsize = struct.unpack_from("<H", data, 0x2A)[0]
e_phnum = struct.unpack_from("<H", data, 0x2C)[0]
segs = []  # (off, vaddr, filesz, flags)
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz, _, _, p_flags = struct.unpack_from("<8I", data, o)
    if p_type == 1:  # PT_LOAD
        segs.append((p_offset, p_vaddr, p_filesz, p_flags))
exec_segs = [s for s in segs if s[3] & 1]

def off2va(off):
    for o, v, sz, f in segs:
        if o <= off < o + sz:
            return v + (off - o)
    return None

def va2ghidra(va):
    return va + 0x10000  # note 19: Ghidra image base = readelf + 0x10000

# --- ARM encodings (instr stored LE32: b3=cond<<4|op hi) ---
# MOVW: cond 0011 0000 imm4 Rd imm12  -> b3&0xF==3, b2&0xF0==0 ; imm16=(b2&0xF)<<12|(b1&0xF)<<8|b0
# MOVT: cond 0011 0100 imm4 Rd imm12  -> b3&0xF==3, b2&0xF0==0x40
def scan_arm():
    hits = []
    n = len(data)
    for i in range(0, n - 4, 4):
        b0, b1, b2, b3 = data[i], data[i+1], data[i+2], data[i+3]
        if (b3 & 0x0F) != 0x03 or (b2 & 0xF0) != 0x00:
            continue
        imm16 = ((b2 & 0x0F) << 12) | ((b1 & 0x0F) << 8) | b0
        rd = (b1 >> 4) & 0x0F
        is_movt = (b2 & 0xF0) == 0x40
        hits.append((i, "ARM", "MOVT" if is_movt else "MOVW", imm16, rd))
    return hits

# --- Thumb-2 (halfwords LE): MOVW T3 hw1=F240|(i<<10)|imm4 ; MOVT T1 hw1=F2C0|(i<<10)|imm4
# hw2 = 0 imm3(3) Rd(4) imm8(8); imm16 = imm4:i:imm3:imm8
def scan_thumb():
    hits = []
    n = len(data)
    for i in range(0, n - 4, 2):
        hw1 = data[i] | (data[i+1] << 8)
        hw2 = data[i+2] | (data[i+3] << 8)
        top = hw1 & 0xFFC0
        if top != 0xF240 and top != 0xF2C0:
            continue
        if (hw1 & 0x0300) != 0x0200:   # bits 9:8 must be '10'
            continue
        is_movt = (top == 0xF2C0)
        imm4 = hw1 & 0xF
        iv = (hw1 >> 10) & 1
        imm3 = (hw2 >> 12) & 0x7
        rd = (hw2 >> 8) & 0xF
        imm8 = hw2 & 0xFF
        imm16 = (imm4 << 12) | (iv << 11) | (imm3 << 8) | imm8
        hits.append((i, "THUMB", "MOVT" if is_movt else "MOVW", imm16, rd))
    return hits

arm_hits = scan_arm()
thumb_hits = scan_thumb()

def report(hits, label, want=(0x4944, 0x5443)):
    print(f"=== {label}: {len(hits)} movw/movt immediates total ===")
    # all hits for the two DICT halves
    for target, kind in ((want[0], "MOVW"), (want[1], "MOVT")):
        sel = [h for h in hits if h[2] == kind and h[3] == target]
        print(f"  {kind} #{target:#06x}: {len(sel)}")
        for off, mode, k, imm, rd in sel:
            va = off2va(off)
            print(f"    off={off:#010x} va={va:#010x} ghidra={va2ghidra(va):#010x} Rd=r{rd} [{mode}]")
    # pair them up: any MOVW-want and MOVT-want within 120 bytes
    movs = [h for h in hits if h[2] == "MOVW" and h[3] == want[0]]
    movts = [h for h in hits if h[2] == "MOVT" and h[3] == want[1]]
    pairs = []
    for m in movs:
        for t in movts:
            if 0 <= abs(t[0] - m[0]) <= 120:
                pairs.append((m, t))
    print(f"  -> {len(pairs)} pair(s) within 120 bytes:")
    for m, t in pairs:
        lo = min(m[0], t[0]); hi = max(m[0], t[0]) + 4
        print(f"    PAIR off {m[0]:#x}+{t[0]:#x}  (span {hi-lo}B)  va {off2va(m[0]):#x}/{off2va(t[0]):#x}")
    return pairs

pairs_arm = report(arm_hits, "ARM")
pairs_thm = report(thumb_hits, "THUMB-2")

# quick sanity: known movw pair sanity — dump 8 instructions around each pair center
import subprocess
print("\n=== context dump (first 3 pairs, hex + vaddr) ===")
allpairs = pairs_arm + pairs_thm
for m, t in allpairs[:3]:
    lo = max(0, min(m[0], t[0]) - 24); hi = min(len(data), max(m[0], t[0]) + 28)
    print(f"-- around off {min(m[0],t[0]):#x} va {off2va(min(m[0],t[0])):#x}")
    for o in range(lo, hi, 4):
        va = off2va(o)
        w = struct.unpack_from("<I", data, o)[0]
        tag = " <<<" if o in (m[0], t[0]) else ""
        print(f"   {va:#010x}: {w:08x}{tag}")
