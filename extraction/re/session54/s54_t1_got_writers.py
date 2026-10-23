#!/usr/bin/env python3
"""s54 T1 step 24: for all 94 GOT-ref sites, disassemble forward from the ldr
and classify read (ldr [rX]) vs write (str ..., [rX]). Dump write sites fully."""
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

GOT_SLOTS = {0xc080c8 + 4 * k: n for k, n in enumerate(
    ['s_glidePitchMin', 's_glidePitchMax', 's_glideRollMax', 's_glideDeltaYawMax',
     's_glideYawCoef', 's_glidePitchCoef', 's_glideRollCoef',
     's_glidePitchAutoLevelingCoef', 's_glideRollAutoLevelingCoef', 's_glideDeadAngle'])}

TEXT = (0xa5d80, 0xac2190)
sites = []
for P in range(TEXT[0], TEXT[1], 4):
    L = struct.unpack_from('<i', data, v2o(P))[0]
    tgt = P + 8 + L
    if tgt in GOT_SLOTS:
        sites.append((P, tgt))

# reconstruct instruction list around each site
def insns_around(lo, hi):
    return list(md.disasm(data[v2o(lo):v2o(hi)], lo))

writes = []
for P, tgt in sites:
    lo = P - 0x10
    ins_list = insns_around(lo, P + 0x14)
    # find the ldr using this pool word, then the register it loads
    reg = None
    for i, ins in enumerate(ins_list):
        if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
            except Exception:
                continue
            if P + 8 + 0 == 0:
                pass
            # the literal VALUE at P: for this site, the ldr operand is the pool word
            if base + imm == P:
                reg = ins.op_str.split(',')[0].strip()
                # now scan forward for ldr [reg] (read) or str [reg] (write)
                act = None
                for ins2 in ins_list[i + 1:]:
                    ops = ins2.op_str.replace('[', ' ').replace(']', ' ').split(',')
                    if any(o.strip() == reg for o in ops[1:]) if len(ops) > 1 else False:
                        if ins2.mnemonic == 'ldr':
                            act = 'read'
                        elif ins2.mnemonic == 'str':
                            act = 'write'
                        break
                if act == 'write':
                    writes.append((P, tgt))
                break

print('write sites (%d):' % len(writes))
for P, tgt in writes:
    print('  pool@%#x -> %s in %s' % (P, GOT_SLOTS[tgt], sym_of(P)))
    lo = P - 0x18
    for ins in md.disasm(data[v2o(lo):v2o(P + 0x20)], lo):
        note = ''
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
                base = (ins.address + 8) & ~3
                val = struct.unpack_from('<I', data, v2o(base + imm))[0]
                fv = struct.unpack_from('<f', data, v2o(base + imm))[0]
                note = '   ; =%#x' % val
                if 0x2f000000 < val < 0x50000000:
                    note += ' (float %g)' % fv
            except Exception:
                pass
        print('    %08x %-8s %-32s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
