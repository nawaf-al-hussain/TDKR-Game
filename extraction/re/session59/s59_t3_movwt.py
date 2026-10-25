#!/usr/bin/env python3
"""s59 T3: scan .text for movw/movt immediate pairs matching blocker ids."""
import struct, subprocess, re, bisect

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
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

def imm12(w):
    # MOVW/MOVT: imm16 = imm4:imm12 (rotate-free): imm16 = ((w>>4)&0xF000) | (w & 0xFFF)
    rd = (w >> 12) & 0xF
    imm16 = ((w >> 4) & 0xF000) | (w & 0xFFF)
    return rd, imm16

IDS = {0x4cc04ddb: 59, 0x43c8a8d1: 24, 0x67c82e62: 14, 0x0e1f5b6f: 2,
       0x0116a6fa: 18, 0x7d561d33: 18, 0x4cc07242: 11, 0x0e31d4a0: 10,
       0x28091330: 10, 0x0dd583de: 9, 0x2c9a0e3f: 6, 0x519ad19b: 5,
       0x5e46be31: 3, 0x4ab8a7cd: 2, 0x454206a4: 1, 0x4cbfd885: 1, 0x1b2aa571: 1}
# map: (low16, high16) -> id
want = {}
for cid in IDS:
    want[(cid & 0xFFFF, cid >> 16)] = cid
# collect all movw in .text, then check next few insns for matching movt (same Rd)
found = {}
movws = []
for off in range(0x0a5d80, 0xac2190, 4):
    w = struct.unpack_from('<I', data, off)[0]
    if (w & 0x0FF00000) == 0x03000000:  # MOVW
        rd, imm = imm12(w)
        movws.append((off, rd, imm))
print(f'movw count: {len(movws)}')
for off, rd, lo in movws:
    if (lo, None) not in [(k[0], None) for k in want]: continue
    for k in range(1, 8):
        w2 = struct.unpack_from('<I', data, off + 4*k)[0]
        if (w2 & 0x0FF00000) == 0x03400000:  # MOVT
            rd2, hi = imm12(w2)
            if rd2 == rd and (lo, hi) in want:
                cid = want[(lo, hi)]
                f = func_of(off)
                found.setdefault(cid, []).append((off, f[1] if f else '?'))
for cid, hits in sorted(found.items(), key=lambda kv: -IDS[kv[0]]):
    print(f'0x{cid:08x} (n={IDS[cid]}):')
    for h in hits[:6]:
        print(f'   0x{h[0]:x} in {h[1][:85]}')
if not found: print('no movw/movt pairs found for any blocker id')
