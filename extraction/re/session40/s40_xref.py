#!/usr/bin/env python3
"""Correct ARM/Thumb xref scanner (BL/BLX) for libKRHP.so."""
import struct, json, sys

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    t, off, va, _, fs, _ = struct.unpack_from('<6I', d, o)
    if t == 1: segs.append((va, off, fs))

def callers_of(tgt):
    """Returns list of (mode, addr) calling tgt."""
    found = []
    for va, off, fs in segs:
        # ARM BL (cond!=F, 101L) / BLX (cond==F, 101H): opcode in HIGH halfword
        # imm24 = (w2 & 0xff) << 16 | w1   (w2 = cond|101L|imm[23:16], w1 = imm[15:0])
        for o in range(off, off + fs - 4, 4):
            w1, w2 = struct.unpack_from('<HH', d, o)  # w1=low, w2=high
            if (w2 & 0x0F00) == 0x0B00:
                cond = w2 >> 12
                imm = ((w2 & 0xff) << 16) | (w1 & 0xffff)
                if imm & 0x800000: imm -= 0x1000000
                pc = va + (o - off) + 8
                if cond == 0xF:  # BLX: H bit (w2 bit8) adds +2
                    t2 = pc + imm * 4 + ((w2 & 0x100) >> 7)
                    if t2 == tgt: found.append(('arm-blx', hex(va + (o - off))))
                else:
                    if pc + imm * 4 == tgt: found.append(('arm-bl', hex(va + (o - off))))
        # Thumb BL/BLX
        o = off
        while o < off + fs - 4:
            w1 = struct.unpack_from('<H', d, o)[0]
            if (w1 & 0xf800) == 0xf000:
                w2 = struct.unpack_from('<H', d, o + 2)[0]
                if (w2 & 0xd800) in (0xd000, 0xc800):
                    imm = ((w1 & 0x7ff) << 12) | ((w2 & 0x7ff) << 1)
                    if imm & 0x400000: imm -= 0x800000
                    pc = va + (o - off) + 4
                    if pc + imm == tgt:
                        found.append(('thumb-bl' if (w2 & 0x1000) else 'thumb-blx', hex(va + (o - off))))
            o += 2
    return found

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        t = int(arg, 0)
        print(f'callers of {hex(t)}:', callers_of(t))
