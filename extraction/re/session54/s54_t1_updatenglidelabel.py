#!/usr/bin/env python3
"""s54 T1 step 27: scan CActorBaseComponent::UpdateNavGlide (0x380e94..0x3836b0)
and PlayerComponent glide funcs for reads of the glide-object fields
(+0x08..+0x5c) and name them. Prints each GetGlide call and the field reads
that follow within 60 instructions."""
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

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

RANGES = [
    ('UpdateNavGlide', 0x380e94, 0x3836b0),
    ('RefreshForcesGlide', 0x3836b0, 0x383a08),
    ('RefreshForcesFallGrapnel', 0x383a08, 0x383c00),
    ('SendGlideEvent', 0x373af0, 0x374040),
    ('GetGlideAttackLandOffset', 0x374040, 0x374200),
    ('PlayerComponent::GlideJump', 0x25f744, 0x25f770),
    ('PlayerComponent::EnterGlideFromGrapnel', 0x25f770, 0x25f818),
    ('PlayerComponent::CanEnterGlideFromGrapnel', 0x25f818, 0x25f8c0),
    ('PlayerComponent::EnterGlideFall', 0x259ba4, 0x25a200),
    ('PlayerComponent::StartQteMotionGlide', 0x2679d4, 0x267a30),
]
FIELD = {0x04: 'int1 slot', 0x08: 'f0', 0x0c: 'f1', 0x10: 'f2', 0x14: 'f3',
         0x18: 'f4', 0x1c: 'f5', 0x20: 'f6', 0x24: 'f7', 0x28: 'f8',
         0x2c: 'f9', 0x30: 'f10 initPitchDeg', 0x34: 'f11', 0x38: 'f12',
         0x3c: 'f13', 0x40: 'f14', 0x44: 'f15', 0x48: 'f16', 0x4c: 'f17',
         0x50: 'f18', 0x54: 'f19', 0x58: 'f20', 0x5c: 'int2'}

for name, lo, hi in RANGES:
    print('\n=== %s ===' % name)
    off = v2o(lo)
    last_getglide = -999
    for ins in md.disasm(data[off:off + (hi - lo)], lo):
        tag = ''
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 16)
                s = sym_of(t)
                if 'GetGlide' in s:
                    last_getglide = ins.address
                    tag = '   ; <<< GetGlide'
                elif 'GetGliderGravity' in s:
                    tag = '   ; <<< gravity upgrade'
            except ValueError:
                pass
        if ins.mnemonic in ('ldr', 'vldr') and last_getglide > 0:
            m = None
            if '#-' in ins.op_str:
                continue
            try:
                m = ins.op_str.split('#')[1].rstrip(']')
            except IndexError:
                m = None
            if m:
                try:
                    imm = int(m, 16) if m.startswith('0x') else int(m)
                except ValueError:
                    imm = None
                if imm in FIELD:
                    print('%08x %-6s glide_obj+%#x (%s)%s' % (
                        ins.address, ins.mnemonic, imm, FIELD[imm], tag))
                    tag = ''
                    last_getglide = -1  # only first read after each GetGlide
                    continue
        if tag:
            print('%08x %-8s %s%s' % (ins.address, ins.mnemonic, ins.op_str, tag))
