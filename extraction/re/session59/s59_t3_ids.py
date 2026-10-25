#!/usr/bin/env python3
"""s59 T3: locate the blocker component ids in .text literal pools -> enclosing
functions -> Load read sequences. Ids: 0x4cc04ddb(59), 0x43c8a8d1(24),
0x67c82e62(14), 0x0e1f5b6f(2), 0x0116a6fa(18), 0x7d561d33(18), 0x4cc07242(11),
0x0e31d4a0(10), 0x28091330(10), 0x0dd583de(9), 0x2c9a0e3f(6), 0x519ad19b(5)."""
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

IDS = {0x4cc04ddb: 59, 0x43c8a8d1: 24, 0x67c82e62: 14, 0x0e1f5b6f: 2,
       0x0116a6fa: 18, 0x7d561d33: 18, 0x4cc07242: 11, 0x0e31d4a0: 10,
       0x28091330: 10, 0x0dd583de: 9, 0x2c9a0e3f: 6, 0x519ad19b: 5,
       0x5e46be31: 3, 0x4ab8a7cd: 2}
for cid, cnt in sorted(IDS.items(), key=lambda kv: -kv[1]):
    pat = struct.pack('<I', cid)
    hits = []
    st = 0
    while True:
        i = data.find(pat, st)
        if i < 0: break
        st = i + 1
        if 0x0a5d80 <= i < 0xac2190:  # .text literal pool
            f = func_of(i)
            hits.append((i, f[1] if f else '?'))
    print(f"0x{cid:08x} (n={cnt}): {len(hits)} .text hit(s)")
    for h in hits[:5]:
        print(f"   0x{h[0]:x} in {h[1][:90]}")
