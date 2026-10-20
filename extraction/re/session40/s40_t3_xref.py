#!/usr/bin/env python3
"""S40 T3: Thumb-2 literal-pool xref scanner over libKRHP.so.

For each constant-name string (and every occurrence of it in .rodata), find
code sites that load its ADDRESS via:
  - Thumb LDR literal (LDR rX, [pc, #imm]) whose pool word == string address
  - Thumb MOVW/MOVT pairs building the address
  - ARM LDR literal pools + ADD pc (ADR-style)
Positive control: FACE_HOSTAGE (s39: 6 string hits, shared pool 0xc0b018-50).
Negative control: MC_MAX_DISTANCE (s39: zero pool refs).
If a registrant function is found, dump its disasm for the hook decision.
"""
import struct, json, sys
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    t, off, va, _, fs, _ = struct.unpack_from('<6I', d, o)
    if t == 1: segs.append((va, off, fs))

def v2o(va):
    for v, o, s in segs:
        if v <= va < v + s: return o + (va - v)
    return None

def o2v(o):
    for v, oo, s in segs:
        if oo <= o < oo + s: return v + (o - oo)
    return None

NAMES = ["ACTIVE", "CAMERA_SHAKE_BOMB", "DISABLED", "ENABLED", "FACE_BATMAN",
         "FACE_HOSTAGE", "FACE_MERCENARY", "FACE_NONE", "KILLED",
         "MC_MAX_DISTANCE", "NUMBERED", "UNDERGROUND", "ZONE"]
STR_HITS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t4_consts.json'))['so_string_hits']

# 1. locate every occurrence of each name in the image, note vaddr
str_locs = {}
for nm in NAMES:
    p = nm.encode() + b'\x00'
    locs = []
    o = 0
    while True:
        i = d.find(p, o)
        if i < 0: break
        va = o2v(i)
        if va is not None: locs.append(va)
        o = i + 1
    str_locs[nm] = locs

# 2. build literal-pool value map: scan whole image for the string addrs as words
pool_refs = {nm: [] for nm in NAMES}
addr2name = {}
for nm, locs in str_locs.items():
    for va in locs:
        addr2name[va] = nm
# scan data words equal to string addrs
for nm, locs in str_locs.items():
    for va in locs:
        p = struct.pack('<I', va)
        o = 0
        while True:
            i = d.find(p, o)
            if i < 0: break
            pool_refs[nm].append(o2v(i) or ('fileoff', i))
            o = i + 1

# 3. Thumb LDR-literal scan: LDR rX, [pc, #imm] encodes 01001 rt(3) imm8.
# find code that loads each pool word: pool vaddr -> (code addr that references it)
def thumb_ldr_literal_sites():
    """Map pool-vaddr -> [pc sites] for Thumb LDR literal across executable segs."""
    sites = {}
    for va, off, fs in segs:
        # executable check: skip if not in text — approximate: scan all, filter later
        o = off
        end = off + fs - 2
        while o < end:
            hw = struct.unpack_from('<H', d, o)[0]
            if (hw >> 11) == 0b01001:  # T1 LDR literal
                rt = (hw >> 8) & 7
                imm8 = hw & 0xff
                pc = va + (o - off) + 4
                tgt = (pc + imm8 * 4) & ~3
                sites.setdefault(tgt, []).append(va + (o - off))
            o += 2
    return sites

ldr_sites = thumb_ldr_literal_sites()
print(f'Thumb LDR-literal sites: {len(ldr_sites)} pool targets')

# 4. for each name: string locs, pool words that are CODE-REFERENCED
report = {}
for nm in NAMES:
    pools = pool_refs[nm]
    code_ref_pools = []
    for pv in pools:
        if isinstance(pv, tuple): continue
        if pv in ldr_sites:
            code_ref_pools.append((hex(pv), [hex(x) for x in ldr_sites[pv][:4]]))
    report[nm] = {'str_locs': [hex(x) for x in str_locs[nm]],
                  'pool_words': [str(x) for x in pools][:8],
                  'code_ref_pools': code_ref_pools}
    print(f'{nm}: str@{[hex(x) for x in str_locs[nm]]} pool_words={len(pools)} '
          f'code_ref={code_ref_pools[:2]}')

json.dump(report, open('/tmp/my-project/scripts/s40_t3_xref.json', 'w'), indent=1)
