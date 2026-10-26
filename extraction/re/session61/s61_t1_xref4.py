#!/usr/bin/env python3
"""S61 T1 step 8: callers of GOM ctor/CreateObject/CreateObjectFromLibrary via robust scan;
plus pointer-word scan for Reload/CreateObject/GCT addresses in the whole binary."""
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

def v2oseg(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return (va, off, sz)
    return None

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
    calls = {}
    pos = TEXT_LO
    o = v2o(TEXT_LO)
    buf = data[o:o + (TEXT_HI - TEXT_LO)]
    while pos < TEXT_HI:
        off = pos - TEXT_LO
        chunk = buf[off:off + 0x10000]
        if not chunk:
            break
        for ins in md.disasm(chunk, pos):
            if ins.mnemonic in ('bl', 'blx', 'b') and ins.op_str.startswith('#'):
                try:
                    t = int(ins.op_str[1:], 0)
                    calls.setdefault(t, []).append((ins.address, ins.mnemonic))
                except ValueError:
                    pass
            pos = ins.address + ins.size
        pos += 2
    return calls

calls = scan_calls()
targets = {
    'GOM::ctor': 0x365598,
    'GOM::CreateObject': 0x36774c,
    'GOM::CreateObjectFromLibrary(str)': 0x365630,
    'GOM::CreateObjectFromLibrary(int)': 0x366b78,
    'GOM::GetObjectIdFromName': 0x3656ac,
    'GOM::AddExternComponents': 0x368738,
}
for name, tgt in targets.items():
    sites = calls.get(tgt, [])
    print(f"=== callers of {name} {tgt:#x}: {len(sites)}")
    for a, m in sites[:12]:
        s = sym_of(a)
        print(f"  {a:#x} {m} in {dem(s[0])[:80]} +{s[1]:#x}")

# pointer-word scan across ALL segments for function addresses
print("\n=== pointer-word hits (function address as u32 anywhere in file) ===")
for name, tgt in (('Reload', 0x366104), ('CreateObject', 0x36774c), ('GCT', 0x368ac0),
                  ('ctor', 0x365598), ('Load', 0x365780)):
    needle = struct.pack('<I', tgt)
    hits = []
    start = 0
    while True:
        j = data.find(needle, start)
        if j < 0:
            break
        # map to vaddr
        va = None
        for va_, off_, sz_ in segs:
            if off_ <= j < off_ + sz_:
                va = va_ + (j - off_)
                break
        hits.append(va)
        start = j + 1
    txt = [hex(h) for h in hits if h is not None and TEXT_LO <= h < TEXT_HI]
    dat = [hex(h) for h in hits if h is not None and not (TEXT_LO <= h < TEXT_HI)]
    print(f"  {name} {tgt:#x}: {len(hits)} hits; in-text {txt[:6]}; in-data {dat[:10]}")
