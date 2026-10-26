#!/usr/bin/env python3
"""S61 T1 step 5: robust xref with restart-on-invalid disasm.
Callers of GOM::Load 0x365780 / Reload 0x366104 / GCT 0x368ac0 / CreateObject 0x367fdc.
Plus: .rodata string search for 'gol' filenames and their xrefs."""
import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    pt, po, pv, _, ps = struct.unpack_from('<5I', data, p)
    if pt == 1:
        segs.append((pv, po, ps))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)

TEXT_LO, TEXT_HI = 0xa5d80, 0xac2190
nm = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for l in nm.splitlines():
    p = l.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

def dem(n):
    return subprocess.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def scan_calls():
    """Disassemble .text with restart-on-invalid; collect all BL targets."""
    calls = {}  # target -> [sites]
    pos = TEXT_LO
    end = TEXT_HI
    o = v2o(TEXT_LO)
    buf = data[o:o + (end - TEXT_LO)]
    while pos < end:
        off = pos - TEXT_LO
        chunk = buf[off:off + 0x8000]
        restarted = False
        for ins in md.disasm(chunk, pos):
            if ins.mnemonic in ('bl', 'b', 'blx') and ins.op_str.startswith('#'):
                try:
                    t = int(ins.op_str[1:], 0)
                    calls.setdefault(t, []).append((ins.address, ins.mnemonic))
                except ValueError:
                    pass
            pos = ins.address + ins.size
        if not restarted:
            if len(chunk) == 0:
                break
            # capstone stopped at invalid byte: skip 2 bytes and retry
            pos += 2
    return calls

calls = scan_calls()
print(f"total direct branch/call sites collected: {sum(len(v) for v in calls.values())}")

for name, tgt in (('GOM::Load', 0x365780), ('GOM::Reload', 0x366104),
                  ('GCT', 0x368ac0), ('GOM::CreateObject', 0x367fdc)):
    sites = calls.get(tgt, [])
    print(f"\n=== callers of {name} {tgt:#x}: {len(sites)}")
    for a, m in sites[:20]:
        s = sym_of(a)
        print(f"  {a:#x} {m} in {dem(s[0])} +{s[1]:#x}")

# find .rodata strings mentioning gol
print("\n=== 'gol' strings in the file ===")
import re
for m in re.finditer(rb'[ -~]{4,}', data):
    s = m.group().decode('latin1')
    if ('gol' in s.lower() and ('.bin' in s.lower() or 'game_config' in s.lower() or s.lower().endswith('.gol') or 'gol.' in s.lower())):
        va = None
        for v_, o_, sz in segs:
            if o_ <= m.start() < o_ + sz:
                va = v_ + (m.start() - o_)
        print("  %s: %s" % (hex(va) if va is not None else "?", s[:80]))
