#!/usr/bin/env python3
"""s44 T1: find CODE xrefs to the Lua error strings in libKRHP.so.
PIC idioms scanned: add/sub rd, pc, #imm; ldr rd, [pc, #imm] literal loads;
movw+movt pairs. Also maps which functions reference luaT_eventname."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
data = open(SO, 'rb').read()

TARGETS = {
    0xbb2154: 'typeerror_fmt("attempt to %s a %s value")',
    0xbb217c: 'arith_op("perform arithmetic on")',
    0xbb2170: 'concat_op("concatenate")',
    0xbb2194: 'order_fmt("attempt to compare two %s values")',
    0xbb21b8: 'order_fmt("attempt to compare %s with %s")',
    0xbb2be4: 'parser("unexpected symbol")',
    0xbb19ec: 'auxlib_panic("PANIC: unprotected...")',
    0xbb1e24: 'lua_version("Lua 5.1...")',
}
POOL_RANGE = (0xbcdb00, 0xcde000)   # data.rel.ro pools of interest (eventname etc.)

LO, HI = 0x8001, 0xbbe1ec
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False
hits = {}
movw = {}
addr = LO
nins = 0
while addr < HI:
    ended = True
    for ins in md.disasm(data[addr:HI], addr):
        ended = False
        nins += 1
        m = ins.mnemonic
        op = ins.op_str
        if m in ('add', 'sub') and 'pc' in op:
            parts = op.split(', ')
            if len(parts) == 3 and parts[1] == 'pc':
                try:
                    imm = int(parts[2].replace('#', ''), 0)
                except ValueError:
                    continue
                t = ins.address + 4 + (imm if m == 'add' else -imm)
                if t in TARGETS:
                    hits.setdefault(TARGETS[t], []).append((hex(ins.address), f'{m} pc'))
        elif m == 'ldr' and '[pc' in op:
            try:
                imm = int(op.split('#')[1].rstrip(']'), 0)
            except (IndexError, ValueError):
                continue
            t = (ins.address + 4 + imm) & ~3
            if t < len(data):
                w = struct.unpack_from('<I', data, t)[0]
                if w in TARGETS:
                    hits.setdefault(TARGETS[w], []).append((hex(ins.address), f'ldr ->pool {hex(t)}'))
                if POOL_RANGE[0] <= w < POOL_RANGE[1]:
                    hits.setdefault(f'pool-ptr {hex(w)}', []).append((hex(ins.address), 'ldr pool'))
        elif m == 'movw' and '#:' not in op:
            try:
                rd = op.split(',')[0].strip()
                imm = int(op.split('#')[1], 0)
                movw[rd] = (ins.address, imm)
            except (IndexError, ValueError):
                continue
        elif m == 'movt':
            try:
                rd = op.split(',')[0].strip()
                imm = int(op.split('#')[1], 0)
                if rd in movw:
                    a, lo16 = movw[rd]
                    val = (imm << 16) | lo16
                    if val in TARGETS:
                        hits.setdefault(TARGETS[val], []).append((hex(a), 'movw+movt'))
            except (IndexError, ValueError):
                continue
        addr = ins.address + ins.size
    if ended:
        addr += 4
print('instructions scanned:', nins)
import json
json.dump({k: v for k, v in hits.items()}, open('/home/z/my-project/scripts/s44_t1_xrefs.json', 'w'), indent=0)
tgt_hits = {k: v for k, v in hits.items() if not k.startswith('pool-ptr')}
print('=== DIRECT TARGET HITS ===')
for k, v in sorted(tgt_hits.items()):
    print(k)
    for a, kind in v[:12]:
        print('   ', a, kind)
pool_keys = [k for k in hits if k.startswith('pool-ptr')]
print('pool-ptr distinct targets:', len(pool_keys))
print('scan range', hex(LO), hex(HI))
