#!/usr/bin/env python3
"""S30 T2 goal script — everything CONFIRMED this round, one place:
  1. descriptor table (file SoA + engine case map)
  2. second-tangent-frame anomaly (786/1449 -> handedness flips)
  3. UV location + verification (4.12 fixed point, 4x4 atlas, nulls)
  4. skin per-vertex records [u8 bone x4][f32 w x4], sums, histogram
  5. inverse-bind matrix dump (38 @0x5a210) + one skinned-vertex record
Verdict: PARTIAL (bind-pose reproduction blocked on skeleton<->matrix
axis/order association; resisting block named in the notes).
"""
import struct, statistics, random, collections

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
BASE = 0x4b5c          # vertex 0, stride 80
N = 1449
SKIN = 0x31774         # 1449 x 20 B = [u8 bone x4][f32 w x4]
BINDS = 0x5a210        # 38 x 64 B row-major affine, w = [0,0,0,1]

print('=== 1. descriptor table (mesh 1, 1449 verts, stride 80) ===')
print('file layout @0x4afc: 8 x (u32 offset, u32 fmt, u32 comps) SoA')
offs = struct.unpack_from('<8I', d, 0x4afc)
fmts = struct.unpack_from('<8I', d, 0x4b1c)
comp = struct.unpack_from('<8I', d, 0x4b3c)
for o, f, c in zip(offs, fmts, comp):
    print(f'  stream @+{o:2d}: fmt {f} x {c} comps -> {f*c*2 if f==2 else f*c*4} B'
          if f == 2 else f'  stream @+{o:2d}: fmt {f} x {c} comps -> {f*c*4} B')
print('engine case map (@0x7ad92c switch): attr 0/15..26 -> f32x3; '
      '1..14 -> f32x2; 16(Normal) -> f32x3; 17/18(Color) -> u8x4; '
      '27 SkinWeights / 28 SkinIndices -> SKIP (no vertex stream)')
print('vertex = Pos@0 + Normal@12 + Tan0@24 + Bin0@36 + Tan1@48 + Bin1@60 '
      '+ 2x 4-B streams @72/@76 (two UV sets, see 3)')

print('\n=== 2. second tangent frame anomaly (r19: 786/1449) ===')
def v3(o): return struct.unpack_from('<3f', d, o)
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def nrm(a): return dot(a, a) ** 0.5
plus = minus = other = 0
for i in range(N):
    vo = BASE + i * 80
    n = v3(vo + 12)
    t2, b2 = v3(vo + 48), v3(vo + 60)
    c = cross(t2, b2)
    nn = nrm(n)
    if nn < 0.5 or nrm(c) < 0.5:
        other += 1
        continue
    cs = dot(c, n) / (nrm(c) * nn)
    if cs > 0.99: plus += 1
    elif cs < -0.99: minus += 1
    else: other += 1
print(f'  T2 x B2 == +N: {plus}, == -N: {minus}, other: {other} (of {N})')
print('  -> the second frame is a SECOND UV-SET tangent frame; its handedness')
print('     flips where the UV-1 mapping mirrors (frame1 TxB == -N dominant '
      '2028/2896 for pair@24/36)')

print('\n=== 3. UVs: two 4.12 fixed-point streams @+72/+76 ===')
uvs = [struct.unpack_from('<4H', d, BASE + i*80 + 72) for i in range(N)]
allv = [x for q in uvs for x in q]
print(f'  u16/4096 range [{min(allv)/4096:.3f}, {max(allv)/4096:.3f}] (expect [0,16))')
tiles = collections.Counter((q[0]//4096//4, q[1]//4096//4) for q in uvs)
print(f'  4x4 tile atlas usage: {len(tiles)}/16 tiles occupied')
IDX = 0x210bc
ids = [struct.unpack_from('<H', d, IDX + 2*i)[0] for i in range(5655)]
adj = collections.defaultdict(set)
for t in range(225, 225+5430, 3):
    a, b, c = ids[t], ids[t+1], ids[t+2]
    for x, y in ((a, b), (b, c), (a, c)):
        if x < N and y < N: adj[x].add(y); adj[y].add(x)
same = sum(1 for a, nb in adj.items() for b in nb if b > a and
           (uvs[a][0]//16384, uvs[a][1]//16384) == (uvs[b][0]//16384, uvs[b][1]//16384))
tot = sum(len([b for b in nb if b > a]) for a, nb in adj.items())
random.seed(5)
nsame = sum(1 for _ in range(tot) if
            (random.choice(uvs)[0]//16384, random.choice(uvs)[1]//16384) ==
            (random.choice(uvs)[0]//16384, random.choice(uvs)[1]//16384))
print(f'  adjacent same-tile {same}/{tot} = {100*same/tot:.1f}%  '
      f'(shuffled null {100*nsame/tot:.1f}%)')
print('  refuted: f16 decode (6.3% in [0,1] vs null 28.3%); plain u16 UV '
      '(coherence ratio only 0.4-0.5)')

print('\n=== 4. skin per-vertex records @0x31774 (1449 x 20 B) ===')
recs = [(struct.unpack_from('<4B', d, SKIN + i*20),
         struct.unpack_from('<4f', d, SKIN + i*20 + 4)) for i in range(N)]
sums = [sum(w) for _, w in recs]
print(f'  weight sums == 1.0: {sum(1 for s in sums if abs(s-1) < 0.02)}/{N}')
bones = collections.Counter(b for q, _ in recs for b in q if b)
print(f'  distinct bones {len(bones)}, ids {sorted(bones)[:8]}..{sorted(bones)[-4:]}, '
      f'max id {max(bones)}')
print(f'  vertex 0: bones {recs[0][0]} weights {[round(x,3) for x in recs[0][1]]}')

print('\n=== 5. inverse bind matrices @0x5a210 (38 x 64 B, row-major) ===')
mats = [struct.unpack_from('<16f', d, BINDS + k*64) for k in range(38)]
for k in range(3):
    m = mats[k]
    print(f'  M{k}: rot rows ({m[0]:.4f},{m[1]:.4f},{m[2]:.4f}) ({m[4]:.4f},{m[5]:.4f},{m[6]:.4f}) '
          f'({m[8]:.4f},{m[9]:.4f},{m[10]:.4f})  t=({m[12]:.4f},{m[13]:.4f},{m[14]:.4f})')
print(f'  one skinned vertex (bind data ready, pose association pending):')
b, w = recs[0]
v = v3(BASE)
print(f'  v0 = {tuple(round(x,4) for x in v)}, bones {b}, weights {[round(x,3) for x in w]}')
print('\nVERDICT: PARTIAL — descriptors/frames/UVs/skin-records/binds located;')
print('bind-pose reproduction blocked on the skeleton<->matrix axis/order')
print('association (see RE_NOTES_session30.md T2).')
