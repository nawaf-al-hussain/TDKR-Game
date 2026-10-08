#!/usr/bin/env python3
"""Extract literal-pool constants referenced by CZone::ChangeLightMap."""
import struct

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
blob = open(SO, 'rb').read()

def v2f(v):
    # single LOAD segment covers 0x8000..; vaddr==file offset for this lib (verified)
    return v

# literal pool words
lits = {
    'L0x2b95d0 (sp+8)':  (0x2b95d0, 0x2b9290),  # (lit addr, add-instr addr)
    'L0x2b95d4 (fp)':    (0x2b95d4, 0x2b92a0),
    'L0x2b95d8 (sp+0xc)':(0x2b95d8, 0x2b92a4),
}
for name, (la, addra) in lits.items():
    val = struct.unpack_from('<I', blob, v2f(la))[0]
    pc = addra + 8
    target = val + pc
    # read string at target
    s = blob[v2f(target):v2f(target)+48]
    s = s.split(b'\x00')[0]
    print(f'{name}: lit={val:#x} pc={pc:#x} -> str@{target:#x} = {s!r}')
