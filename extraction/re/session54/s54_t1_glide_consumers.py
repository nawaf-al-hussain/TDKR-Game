#!/usr/bin/env python3
"""s54 T1 step 15: find CComponentGlide consumers.
(a) scan .text for movw/movt pairs building 0x110ce1f (component lookup by id)
(b) disassemble the player glide functions and dump float immediates:
    PlayerComponent::StartGlide/CActorBaseComponent::StartGlide @0x380590,
    CanEnterGlide @0x380cbc, SetGlideSpeed @0x38a120, SendGlideEvent @0x373af0,
    PlayerComponent::EnterGlideFall @0x259ba4, EnterGlideFromGrapnel @0x25f770,
    GlideJump @0x25f744, StartQteMotionGlide @0x2679d4,
    UpgradesManager::GetGliderGravityHelper @0x1e1508
"""
import struct
import subprocess
import bisect

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
segs = [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)]

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    pr = line.split()
    if len(pr) == 3:
        try:
            a = int(pr[0], 16)
        except ValueError:
            continue
        syms.append((a, pr[2]))
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

# (a) movw/movt building 0x110ce1f across .text (ARM encodings)
# ARM movw: cond 0011 0000 imm4 rd imm12 ; movt: cond 0011 0100 ...
def movw_imm(w):
    return ((w >> 4) & 0xf000) | (w & 0xfff)

hits = []
lo, hi = 0x8000, 0xbbe000
for a in range(lo, hi, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    if (w & 0x0ff00000) == 0x03000000 and (movw_imm(w) | 0x1100000) == 0x110ce1f - (0x1100000 if False else 0):
        pass
# simpler: collect movw/movt per reg in a sliding window
import collections
state = {}  # reg -> (imm, addr)
for a in range(lo, hi, 4):
    w = struct.unpack_from('<I', data, v2o(a))[0]
    t = (w >> 20) & 0x0fff
    rd = (w >> 12) & 0xf
    if t == 0x300:
        state[rd] = (movw_imm(w), a)
    elif t == 0x304:
        if rd in state:
            val = (movw_imm(w) << 16) | state[rd][0]
            if val == 0x110ce1f:
                hits.append((state[rd][1], a))
print('movw/movt 0x110ce1f sites:', [(hex(x), hex(y)) for x, y in hits])
for lw, ht in hits:
    print('  in function ~', sym_of(ht))

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dis(vaddr, nbytes, label, floats_only=False):
    print('\n=== %s @%#x ===' % (label, vaddr))
    off = v2o(vaddr)
    n = 0
    for ins in md.disasm(data[off:off + nbytes], vaddr):
        n += 1
        note = ''
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                note = '   ; -> %s' % sym_of(t)
            except ValueError:
                pass
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                f = struct.unpack_from('<f', data, v2o(base + imm))[0]
                note = '   ; =%#x' % val
                if 0x30000000 < val < 0x4f000000 or val == 0:
                    note += ' (float %g)' % f
            except Exception:
                pass
        if floats_only:
            if '(float' in note or 'ReadFloat' in note or 'ReadInt' in note:
                print('%08x %-8s %-36s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
        else:
            print('%08x %-8s %-36s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
        if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
            break

dis(0x1e1508, 0x40, 'UpgradesManager::GetGliderGravityHelper')
dis(0x38a120, 0x60, 'CActorBaseComponent::SetGlideSpeed')
