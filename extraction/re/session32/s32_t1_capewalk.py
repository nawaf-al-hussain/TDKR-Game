#!/usr/bin/env python3
"""S32 T1f: find the real cape vertex block + cape node names."""
import struct, math
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
NFILESZ = len(d)
print(f'file size {NFILESZ} = 0x{NFILESZ:x}')

# 1. all node names
names = []
o = 0x2760
import re


def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v:
            return d[v:e].decode('latin1')
    return None


nodes = []
while o < 0x4a58 - 0x50:
    n1, n2, al = pool(u32(o)), pool(u32(o + 4)), pool(u32(o + 8))
    if n1 is None or n2 is None or al is None:
        o += 4
        continue
    t = struct.unpack_from('<3f', d, o + 0x0c)
    q = struct.unpack_from('<4f', d, o + 0x18)
    s = struct.unpack_from('<3f', d, o + 0x28)
    ql = math.sqrt(sum(x * x for x in q))
    if not (0.96 < ql < 1.04) or not all(abs(x) < 1e4 for x in t) or \
       not all(0.01 < abs(x) < 100 for x in s):
        o += 4
        continue
    if u32(o + 0x34) != 1 or u32(o + 0x38) > 32:
        o += 4
        continue
    nodes.append((n1, n2, al, o))
    o += 0x50
print(f'\nnodes {len(nodes)}; names:')
seen = set()
for n1, n2, al, off in nodes:
    if n2 not in seen:
        seen.add(n2)
print(f'  distinct n2 names: {len(seen)}')
print('  sample:', sorted(seen)[:30])
# any name containing 'C' 'cape' 'Cloth'?
capy = [n for n in seen if re.search(r'(?i)cape|cloth|CBone|bone', n)]
print(f'  cape/cloth/bone-ish: {capy[:20]}')

# 2. strings mentioning CBone anywhere
idxs = [m.start() for m in re.finditer(b'CBone', d)]
print(f'\n"CBone" occurrences: {len(idxs)} first at '
      f'{[hex(i) for i in idxs[:10]]}')
for i in idxs[:6]:
    e = d.find(b'\0', i)
    print(f'  @0x{i:x}: {d[i:min(e, i+40)].decode("latin1")}')

# 3. region map 0x388b8..EOF with finer granularity
z = np.frombuffer(d, np.uint8)
inz = z != 0
print('\nnonzero blocks >256 B from 0x388b8:')
start = None
for i in range(0x388b8, NFILESZ, 16):
    any_nz = inz[i:i + 16].any()
    if any_nz and start is None:
        start = i
    elif not any_nz and start is not None:
        if i - start >= 256:
            print(f'  0x{start:x}..0x{i:x}  len {i-start}')
        start = None
if start is not None:
    print(f'  0x{start:x}..EOF len {NFILESZ-start}')

# 4. analyze cape block 0x54d78 (21552 B) as f32 stream
print('\ncape block @0x54d78 f32 dump (first 96):')
f32 = np.frombuffer(d[0x54d78:0x54d78 + 21552], np.float32)
print('  ', np.round(f32[:48], 4))
print('  ...')
print('  ', np.round(f32[48:96], 4))
# histogram of value ranges per 12-f32 group (pos/normal/uv/tan?)
print('\nper-12-f32 stats for stride-48 hypothesis (first 10 groups):')
for g in range(10):
    v = f32[g * 12:(g + 1) * 12]
    print(f'  g{g}: {np.round(v, 3)}')

# try stride 24: pos(3)+normal(3)=24?
print('\nstride-24 hypothesis: vert i pos = f32[6i:6i+3], normal = +3')
for i in range(6):
    v = f32[i * 6:i * 6 + 6]
    print(f'  v{i}: pos {np.round(v[:3], 3)} nrm {np.round(v[3:], 3)} '
          f'|n|={np.linalg.norm(v[3:]):.3f}')

# 5. look at 0x5cc3c..0x675a4 (between cape skin end and CAPE_down)
print('\nblocks between cape skin end 0x5cc3c and CAPE_down 0x675a4:')
seg = z[0x5cc3c:0x675a4]
inzz = seg != 0
start = None
for i in range(0, len(seg), 16):
    if inzz[i:i + 16].any() and start is None:
        start = i
    elif not inzz[i:i + 16].any() and start is not None:
        if i - start >= 64:
            print(f'  0x{0x5cc3c+start:x} len {i-start}')
        start = None
if start is not None:
    print(f'  0x{0x5cc3c+start:x} len {len(seg)-start}')

# 6. after CAPE_down end 0x67f24
print('\nblocks after 0x67f24:')
seg = z[0x67f24:]
inzz = seg != 0
start = None
for i in range(0, len(seg), 16):
    if inzz[i:i + 16].any() and start is None:
        start = i
    elif not inzz[i:i + 16].any() and start is not None:
        if i - start >= 64:
            print(f'  0x{0x67f24+start:x} len {i-start}')
        start = None
if start is not None:
    print(f'  0x{0x67f24+start:x} len {len(seg)-start}')
