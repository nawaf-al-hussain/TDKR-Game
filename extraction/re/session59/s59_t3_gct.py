#!/usr/bin/env python3
"""s59 T3: disassemble GenerateComponentTemplate (0x368ac0, 11308 B) —
extract per-id cases: movw/movt id + the Read* call sequence between the case
entry and the next. This IS the template-stream reader the task asks about."""
import struct, subprocess, re, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
out = subprocess.run(['readelf', '-sW', SO], capture_output=True, text=True).stdout
funcs = {}
for ln in out.splitlines():
    m = re.match(r'\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)', ln)
    if not m: continue
    va, size, name = int(m.group(1), 16), int(m.group(2)), m.group(3)
    if size == 0 or not name or name.startswith('$'): continue
    funcs.setdefault(va, (name, size))
fstarts = sorted(funcs.items()); addrs = [a for a, _ in fstarts]
def func_of(a):
    i = bisect.bisect_right(addrs, a) - 1
    if i < 0: return None
    va, (n, s) = fstarts[i]
    return (va, n, s) if a < va + s else None

START, SIZE = 0x368ac0, 11308
READ = {0x339510: 'ReadBool&', 0x3395d8: 'ReadChar', 0x339690: 'ReadByte', 0x339758: 'ReadShort',
        0x339868: 'ReadUShort', 0x339914: 'ReadInt', 0x3399d4: 'Read(int&)', 0x339ab4: 'Read(uint&)',
        0x339b94: 'ReadFloat', 0x339c58: 'Read(float&)', 0x33a0d4: 'ReadString', 0x33ab94: 'ReadString()',
        0x33b3d0: 'Read(float3&)'}
insns = list(md.disasm(data[START:START+SIZE], START))
# walk: find movw+movt pairs (id compare), then collect the bl targets until the next id compare / branch
cur_id = None
seqs = {}
pending_rd = None
for idx, ins in enumerate(insns):
    w = struct.unpack_from('<I', data, ins.address)[0]
    if (w & 0x0FF00000) == 0x03000000:  # MOVW
        rd = (w >> 12) & 0xF
        imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
        pending_rd = (ins.address, rd, imm16)
    elif (w & 0x0FF00000) == 0x03400000 and pending_rd:  # MOVT
        rd = (w >> 12) & 0xF
        hi = ((w >> 4) & 0xF000) | (w & 0xFFF)
        if rd == pending_rd[1]:
            cid = (hi << 16) | pending_rd[2]
            cur_id = cid
            seqs.setdefault(cid, [])
    elif ins.mnemonic == 'bl' and cur_id is not None:
        try:
            t = int(ins.op_str.lstrip('#'), 16)
        except ValueError:
            continue
        f = func_of(t)
        nm = f[1] if f else hex(t)
        tag = READ.get(t)
        seqs[cur_id].append((hex(ins.address), nm[:70], tag))
print('ids with template cases in GenerateComponentTemplate:')
for cid, calls in sorted(seqs.items()):
    reads = [c[2] if c[2] else c[1].split('(')[0].split('::')[-1] for c in calls]
    print(f'  0x{cid:08x}: {len(calls)} calls: {reads[:26]}')
json_out = {hex(k): v for k, v in seqs.items()}
import json
json.dump(json_out, open('/home/z/my-project/scripts/s59_t3_gct_cases.json', 'w'), indent=1)
print('saved s59_t3_gct_cases.json')
