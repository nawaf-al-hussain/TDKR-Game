#!/usr/bin/env python3
"""S29 T1: decode ARM/Thumb2 MOVW+MOVT pairs referencing string vaddrs."""
import struct, json, sys
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
TEXT = (0xa5d80, 0xac2490)

def off2v(o): return o if o < 0xbbe1ec else o + 0x1000

# decode ARM MOVW/MOVT
movw, movt = {}, {}
for i in range(TEXT[0], TEXT[1], 4):
    w = struct.unpack_from('<I', data, i)[0]
    if (w & 0x0FF00000) == 0x03000000:
        imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
        rd = (w >> 12) & 0xF
        movw[rd] = (off2v(i), imm16)
    elif (w & 0x0FF00000) == 0x04000000:
        imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
        rd = (w >> 12) & 0xF
        movt[rd] = (off2v(i), imm16)
print(f'ARM MOVW {len(movw)} MOVT {len(movt)}')

targets = {}
for name, v in [('Cinematic', 0xb3af68), ('Trigger', 0xb397d8), ('WantedManager', 0xb3998c),
                ('Steammer', 0xb395a0), ('CamEvent', 0xb39634),
                ('CinematicComponent.cpp_full', 0xb3aebc), ('TriggerComponent.cpp_full', 0xb39758)]:
    targets[v] = name
    hi, lo = v >> 16, v & 0xFFFF
    # find MOVT with imm16==hi whose preceding MOVW (same rd) == lo
    for rd, (a_t, ih) in movt.items():
        if ih == hi and rd in movw:
            a_w, il = movw[rd]
            if il == lo and a_w < a_t and a_t - a_w < 0x40:
                print(f'  {name} {v:#x}: MOVW {a_w:#x} + MOVT {a_t:#x} (r{rd})')
json.dump({hex(k): v for k, v in targets.items()}, open('/tmp/my-project/work/re29/targets.json', 'w'), indent=1)
