#!/usr/bin/env python3
"""Extract the TRUE per-typeId read sequences from CLevel::LoadNextObject's
dispatcher: for each `cmp r5, rX / beq T` pair, disasm T..(loopback) and list
CMemoryStream reader calls (incl. helpers that recurse into readers)."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN

d = open('/home/z/work/TDKR-Game/extraction/lib_libKRHP.so', 'rb').read()
syms = {}
for line in open('/home/z/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[2] == 'FUNC':
        syms[int(p[0], 16)] = (p[3], int(p[1]))
md = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
md.skipdata = True

names = {0x339510: 'B', 0x339574: 'B', 0x3395d8: 'c', 0x339690: 'u8',
         0x339758: 's16', 0x3397dc: 's16', 0x339868: 'u16',
         0x339914: 'i', 0x3399d4: 'i', 0x339ab4: 'i',
         0x339b94: 'f', 0x339c58: 'f',
         0x33a0d4: 'STR', 0x33ab94: 'STR', 0x33ad74: 'STR',
         0x33b3d0: 'v3', 0x33b4dc: 'v2', 0x33b6ac: 'v4',
         0x33b6e8: 'BLK', 0x33b718: 'BLKEND', 0x33b728: 'SKIPBLK'}
LOADER_FNS = {  # known sub-load fns to mark (not expand)
    0x36774c: 'CreateObject', 0x48d5f4: 'ZoneLoad', 0x48d708: 'MetaZoneLoad',
    0x48d870: 'BakeGroupLoad', 0x1fe924: 'CompBaseLoad', 0x2d6ddc: 'CompMeshLoad',
    0x2023bc: 'LevelPropsLoad', 0x202000: 'GlobalIllumLoad', 0x2018f0: 'LevelInitLoad',
    0x2230a8: 'CollisionLoad', 0x2b56f4: 'dbbb8Ctor', 0x1d17cc: 'h267dLoad',
    0x33b01c: 'ReadStringW',
}

# pass 1: collect (const -> beq target)
pairs = []
cur = {}
last_cmp = None
for i in md.disasm(d[0x489d00:0x48b400], 0x489d00):
    if i.mnemonic == 'movw':
        m = i.op_str.split(',')
        if len(m) == 2:
            try:
                cur[m[0].strip()] = int(m[1].strip().lstrip('#'), 0)
            except ValueError:
                pass
    elif i.mnemonic == 'movt':
        m = i.op_str.split(',')
        if len(m) == 2 and m[0].strip() in cur:
            try:
                cur[m[0].strip()] |= int(m[1].strip().lstrip('#'), 0) << 16
            except ValueError:
                pass
    elif i.mnemonic == 'add' and i.op_str.endswith(', r3, #2'):
        # 0x2662 + 2 = 0x2664 pattern
        pass
    elif i.mnemonic == 'cmp':
        m = i.op_str.split(',')
        if len(m) == 2 and m[1].strip() in cur:
            last_cmp = cur[m[1].strip()]
    elif i.mnemonic == 'beq' and last_cmp is not None:
        try:
            t = int(i.op_str.lstrip('#'), 16)
            pairs.append((last_cmp, t, i.address))
        except ValueError:
            pass
        last_cmp = None

def walk(start, limit=0x600):
    """Collect reader calls from start until 'b 0x489f70' (handler return)."""
    seq = []
    a = start
    seen = set()
    for i in md.disasm(d[start:start+limit], start):
        a = i.address
        if i.mnemonic == 'b' and i.op_str == '#0x489f70':
            break
        if i.mnemonic == 'bl':
            t = int(i.op_str.lstrip('#'), 16)
            if t in names:
                seq.append(names[t])
            elif t in LOADER_FNS:
                seq.append(f'<{LOADER_FNS[t]}>')
        if a in seen:
            break
        seen.add(a)
    return seq

out = {}
for const, tgt, at in sorted(pairs):
    seq = walk(tgt)
    if const not in out or len(seq) > len(out[const][0]):
        out[const] = (seq, hex(tgt))
for const, (seq, tgt) in sorted(out.items()):
    print(f'{const:#x} -> {tgt}: {seq}')
json.dump({hex(k): {'seq': v[0], 'handler': v[1]} for k, v in out.items()},
          open('/home/z/work/tdkr/dispatcher_handlers.json', 'w'), indent=1)
