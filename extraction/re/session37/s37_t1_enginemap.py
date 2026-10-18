#!/usr/bin/env python3
"""S37 T1c: engine-side navmesh call-graph + writer hunt, part 2.
- full disasm: CTemplateNavMesh::Load, EnablePortal, DisablePortal,
  GetNeigh, AppendPath head (edge source), SearchPortalPath edge source
- caller census: bl/blx to Create, SetNavMesh, CanReachCellFrom,
  SearchPortalPath, AppendPath(0x1d4aa8), FindClosestCellInRegion, GetNeigh
- any 'add rX, rY, #0x5c/0x60' + bl memcpy/memset in 0x1c0000-0x210000
"""
import struct, json, bisect
import capstone
from collections import defaultdict

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    t, off, va, pa, fsz, msz = struct.unpack_from('<6I', d, o)
    if t == 1 and fsz:
        segs.append((va, off, fsz, msz))

def v2f(v):
    for va, off, fsz, msz in segs:
        if va <= v < va + max(fsz, msz):
            return off + (v - va)
    return None

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)

def dis(lo, size, title):
    print(f'--- {title} 0x{lo:08x} (+{size}) ---')
    f = v2f(lo)
    out = []
    for ins in md.disasm(d[f:f + size], lo):
        out.append((ins.address, ins.mnemonic, ins.op_str))
        print(f'  0x{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}')
    return out

# text segment for bl scan
TEXT_VA, TEXT_OFF, TEXT_FSZ = None, None, None
for va, off, fsz, msz in segs:
    if va <= 0x1d17cc < va + fsz:
        TEXT_VA, TEXT_OFF, TEXT_FSZ = va, off, fsz
        break

def bl_targets():
    """all bl sites -> target"""
    res = defaultdict(list)
    blob = d[TEXT_OFF:TEXT_OFF + TEXT_FSZ]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0F000000) == 0x0B000000:
            imm = w & 0x00FFFFFF
            if imm & 0x800000:
                imm -= 0x1000000
            tgt = (TEXT_VA + i + 8 + imm * 4) & 0xFFFFFFFF
            res[tgt].append(TEXT_VA + i)
    return res

CALLERS = {
    0x1d17cc: 'CNavMeshNova::Create',
    0x484ac0: 'CLevel::SetNavMesh',
    0x1d2c28: 'CNavMeshNova::CanReachCellFrom',
    0x1d44b0: 'CNavMeshQuery::SearchPortalPath',
    0x1d4aa8: 'CNavMeshQuery::AppendPath(big)',
    0x1d41c4: 'CNavMeshQuery::AppendPath(small)',
    0x1d2550: 'CNavMeshNova::FindClosestCellInRegion',
    0x1d2c14: 'CNavMeshNova::GetNeigh',
    0x1d2eb8: 'CNavMeshNova::GetPortalId',
    0x1d3f78: 'CNavMeshQuery::AppendForcePath',
    0x1d42d0: 'CNavMeshQuery::HasPath',
    0x1d43dc: 'CNavMeshQuery::HasPathExact',
    0x484ac8: 'CLevel::GetNavMesh',
}
bt = bl_targets()
print('=== caller census (direct bl) ===')
for tgt, name in CALLERS.items():
    sites = bt.get(tgt, [])
    print(f'  {name} 0x{tgt:08x}: {len(sites)} direct call sites')
    for s in sites[:14]:
        print(f'    from 0x{s:08x}')

# who is at each call site
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
sa = sorted((int(k, 16), str(v[0])) for k, v in syms.items())
keys = [x[0] for x in sa]

def who(a):
    i = bisect.bisect_right(keys, a) - 1
    return sa[i] if i >= 0 else (0, '?')

for tgt in (0x1d2c28, 0x1d44b0, 0x1d4aa8, 0x1d2550, 0x1d17cc, 0x484ac0):
    sites = bt.get(tgt, [])
    if sites:
        fns = sorted({who(s)[1] for s in sites})
        print(f'  -> {CALLERS[tgt]} called from {len(fns)} functions: ' +
              '; '.join(f'{f[:64]}' for f in fns[:8]))

print()
dis(0x2059a8, 216, 'CTemplateNavMesh::Load')
dis(0x159c44, 56, 'EnablePortal (Lua)')
dis(0x159c7c, 56, 'DisablePortal (Lua)')
dis(0x1d2c14, 20, 'CNavMeshNova::GetNeigh')

# add rX, rY, #0x5c/0x60 followed by bl memcpy in navmesh range
print("=== add rX, rY, #0x5c/0x60 in 0x1c0000-0x210000 (potential memcpy dst) ===")
f0 = v2f(0x1c0000)
code = d[f0:f0 + 0x50000]
add_hits = []
for ins in md.disasm(code, 0x1c0000):
    if ins.mnemonic == 'add' and (ins.op_str.endswith('#0x5c') or ins.op_str.endswith('#0x60')):
        add_hits.append((ins.address, ins.mnemonic, ins.op_str))
for a, m, o in add_hits:
    print(f'  0x{a:08x} {m} {o}  in {who(a)[1][:60]}')
