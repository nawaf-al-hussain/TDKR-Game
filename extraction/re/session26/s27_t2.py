#!/usr/bin/env python3
"""s27 T2: batman.bdae deep pass — vertex field map, tangent-frame test,
bbox check, -skin section hunt, hierarchy parents."""
import struct
import math
import random

BDAE = '/home/z/my-project/work/data/batman.bdae'
d = open(BDAE, 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
i32 = lambda o: struct.unpack_from('<i', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

print(f'batman.bdae {len(d)} B magic {d[:4]} ver={u16(4)} secs={u16(6)}')

# ---- section names
for nm in (b'BATMAN-mesh-skin', b'BATMAN-mesh', b'CAPE-mesh-skin',
           b'CAPE-mesh', b'BATMAN-skeleton', b'Bip01', b'BATMAN-skin',
           b'CAPE-skin'):
    i = d.find(nm)
    print(f'{nm.decode():18s} @ {i:#x}' if i >= 0 else
          f'{nm.decode():18s} ABSENT')

# ---- mesh block (from afa61bf): header @0x4a68
H = 0x4a68
print('\n=== BATMAN-mesh header words @0x4a68 ===')
for k in range(0, 0x40, 16):
    print(' ', ' '.join(f'{u32(H + k + j):08x}' for j in range(0, 16, 4)))
count = u32(H + 8)
print(f'count(u32@+8) = {count}')

# find the vertex data start: scan for the EIGHT 0x50 stride constants
sig = b'\x50\x00\x00\x00' * 8
data_start = d.find(sig, H)
print(f'eight-0x50 stride constants @ {data_start:#x}')
vdata = data_start + 32
print(f'vertex data starts {vdata:#x}, {count} x 80 B = {count * 80} B, '
      f'ends {vdata + count * 80:#x}')

# ---- dump first 3 vertices in several interpretations
def dump_vertex(v):
    print(f'  vertex @{v:#x}')
    print('    as f32 :', ' '.join(f'{f32(v + 4 * k):+.4f}' for k in range(20)))
    print('    as u16 :', ' '.join(f'{u16(v + 2 * k):04x}' for k in range(40)))
    print('    as u8  :', ' '.join(f'{d[v + k]:02x}' for k in range(80)))

for k in range(2):
    dump_vertex(vdata + 80 * k)

# ---- quaternion candidates: 4-float windows with |q| ~ 1
print('\n=== |q| per 4-float window offset (over 200 vertices) ===')
for off in range(0, 80 - 16 + 1, 4):
    tot = 0.0
    n = 0
    for k in range(200):
        v = vdata + 80 * k
        q = [f32(v + off + 4 * j) for j in range(4)]
        m = math.sqrt(sum(x * x for x in q))
        tot += m
        n += 1
    avg = tot / n
    if 0.9 < avg < 1.1:
        print(f'  off +{off:2d}: mean |q| = {avg:.4f}  <-- unit-quaternion candidate')

# ---- index list: after 225-u16 identity prefix
idx_head = vdata + count * 80
print(f'\nindex region head @ {idx_head:#x}:',
      ' '.join(f'{u16(idx_head + 2 * k):04x}' for k in range(12)))
# locate identity prefix end
p = idx_head
n_ident = 0
while u16(p + 2 * n_ident) == n_ident and n_ident < 1024:
    n_ident += 1
print(f'identity prefix len = {n_ident}')
indices = [u16(idx_head + 2 * (n_ident + k)) for k in range(5430)]
print(f'index max = {max(indices)} (must be < {count})')
tris = [(indices[i], indices[i+1], indices[i+2]) for i in range(0, 5430, 3)]
print(f'triangles = {len(tris)}')

# ---- bbox of position candidates at several offsets vs stored bbox
print('\n=== position-offset sweep vs plausible model bbox ===')
for off in (0, 12, 24, 36, 44, 48, 52):
    xs, ys, zs = [], [], []
    for k in range(0, count, 7):
        v = vdata + 80 * k
        xs.append(f32(v + off)); ys.append(f32(v + off + 4))
        zs.append(f32(v + off + 8))
    print(f'  off +{off:2d}: x[{min(xs):8.2f},{max(xs):8.2f}] '
          f'y[{min(ys):8.2f},{max(ys):8.2f}] z[{min(zs):8.2f},{max(zs):8.2f}]')
