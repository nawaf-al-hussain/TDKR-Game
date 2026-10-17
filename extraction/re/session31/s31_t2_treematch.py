#!/usr/bin/env python3
"""S31 T2 v4: convention-free bone mapping.
1. mesh bbox (vertex space sanity)
2. palette tree edge lengths from node locals
3. bind-translation distance matrix vs tree — greedy/Hungarian-ish matching
4. least-squares rigid map bind_space -> model_space over matched pairs
5. bind-pose test with the solved map + axis convention report
"""
import struct, math, json, collections

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]


def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v:
            return d[v:e].decode('latin1')
    return None


# ---- nodes (same parse as v3) ----
nodes = []
o = 0x2760
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
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s,
                      ccount=u32(o + 0x38), child=u32(o + 0x3c)))
    o += 0x50
by_alias = {n['alias']: n for n in nodes if n['alias'].startswith('Bone')}
by_name = {n['name']: n for n in nodes}

# ---- palette ----
pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8

BIPED = {
    'Bone58': None,        # Pelvis (parent Bip01 - outside palette)
    'Bone57': 'Bone58', 'Bone36': 'Bone57', 'Bone56': 'Bone36',
    'Bone55': 'Bone56',
    'Bone44': 'Bone58', 'Bone43': 'Bone44', 'Bone42': 'Bone43',
    'Bone41': 'Bone58', 'Bone40': 'Bone41', 'Bone39': 'Bone40',
    'Bone37': 'Bone36', 'Bone54': 'Bone37', 'Bone53': 'Bone54',
    'Bone52': 'Bone53',
    'Bone38': 'Bone36', 'Bone49': 'Bone38', 'Bone48': 'Bone49',
    'Bone47': 'Bone48',
    'Bone51': 'Bone52', 'Bone59': 'Bone51', 'Bone50': 'Bone52',
    'Bone60': 'Bone50',
    'Bone61': 'Bone52', 'Bone62': 'Bone61',
    'Bone46': 'Bone47', 'Bone63': 'Bone46', 'Bone45': 'Bone47',
    'Bone64': 'Bone45',
    'Bone65': 'Bone47', 'Bone66': 'Bone65',
}


def normq(q):
    n = math.sqrt(sum(x * x for x in q))
    return tuple(x / n for x in q)


def qmat_rows(q):
    x, y, z, w = q
    return ((1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)),
            (2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)),
            (2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)))


def compose_locals(alias):
    """local matrix chain from Pelvis down to alias (model space) -> world t"""
    chain = []
    a = alias
    while a is not None:
        chain.append(a)
        a = BIPED.get(a)
    chain.reverse()          # root..alias
    # start at Bip01 root (t=(0,0,0.98038), q=-90deg about Z), then Pelvis..
    root = by_name['Bip01']
    rq = normq(root['q'])
    RR = qmat_rows(rq)
    M = tuple(tuple(RR[i][j] * root['s'][j] for j in range(3)) for i in range(3))
    t = root['t']
    for a in chain:
        n = by_alias[a]
        q = normq(n['q'])
        R = qmat_rows(q)
        lM = tuple(tuple(R[i][j] * n['s'][j] for j in range(3))
                   for i in range(3))
        lt = n['t']
        Mw = tuple(tuple(sum(M[i][k]*lM[k][j] for k in range(3))
                         for j in range(3)) for i in range(3))
        tw = tuple(M[i][0]*lt[0] + M[i][1]*lt[1] + M[i][2]*lt[2] + t[i]
                   for i in range(3))
        M, t = Mw, tw
    return t


model_t = {p: compose_locals(p) for p in pal}
print('model-space palette positions (composed, Bip01 root at z=0.98):')
for p in pal[:8]:
    print(f'  {p} {by_alias[p]["name"]:20s} {tuple(round(x, 4) for x in model_t[p])}')

# ---- mesh bbox ----
BASE = 0x4b5c
N = 1449
zs = []
xs = []
ys = []
for i in range(N):
    x, y, z = struct.unpack_from('<3f', d, BASE + i * 80)
    xs.append(x); ys.append(y); zs.append(z)
print(f'\nmesh bbox: x [{min(xs):.3f},{max(xs):.3f}] '
      f'y [{min(ys):.3f},{max(ys):.3f}] z [{min(zs):.3f},{max(zs):.3f}]')

# ---- inverse binds ----
BINDS = 0x30e30   # BATMAN body palette-ordered binds (CAPE=0x5a210, CAPE_down=0x675a4)
NB = 38
bt = []
for k in range(NB):
    m = struct.unpack_from('<16f', d, BINDS + k * 64)
    bt.append((m[12], m[13], m[14]))
print('\nbind translations:')
for k in range(10):
    print(f'  B{k}: {tuple(round(x, 4) for x in bt[k])}')

# ---- tree edges from node locals (translation lengths) ----
edges = {}
for kid, par in BIPED.items():
    if par is None:
        continue
    n = by_alias[kid]
    L = math.sqrt(sum(x * x for x in n['t']))
    edges[(par, kid)] = L
print('\ntree edge lengths (node locals):')
for (a, b), L in list(edges.items())[:10]:
    print(f'  {a}->{b}: {L:.4f}')

# ---- matching: for each tree edge (par, kid) with length L, find bind pairs
# with |bt[i]-bt[j]| ~ L; vote for consistent permutation ----
print('\n=== bind-space pairwise distance vs tree edges ===')
# For each tree edge, the distribution of |bt_i - bt_j| over all bind pairs:
import itertools
match_votes = collections.Counter()
for (a, b), L in edges.items():
    best = []
    for i, j in itertools.combinations(range(31), 2):
        dd = abs(math.dist(bt[i], bt[j]) - L)
        if dd < 0.01:
            best.append((dd, i, j))
    best.sort()
    print(f'  edge {a}->{b} L={L:.4f}: {len(best)} bind pairs within 1cm; '
          f'top: {[(i, j, round(dd, 4)) for dd, i, j in best[:3]]}')

# ---- global rigid solve attempt via RANSAC over edge-consistent triples ----
# Try: assume bind[k] <-> pal[k] (identity order) first, solve rigid map,
# check residuals.
def solve_rigid(src, dst):
    """least-squares rigid: dst = R src + t (Kabsch, no reflection)"""
    n = len(src)
    cs = [sum(s[i] for s in src) / n for i in range(3)]
    cd = [sum(s[i] for s in dst) / n for i in range(3)]
    H = [[sum((src[k][i]-cs[i])*(dst[k][j]-cd[j]) for k in range(n))
          for j in range(3)] for i in range(3)]
    # SVD via numpy-free 3x3 Jacobi
    import itertools as it
    # power iteration on H^T H for eigendecomposition is messy; use numpy if available
    try:
        import numpy as np
        A = np.array(src) - np.array(cs)
        B = np.array(dst) - np.array(cd)
        U, S, Vt = np.linalg.svd(A.T @ B)
        d = np.sign(np.linalg.det(Vt.T @ U.T))
        Rm = Vt.T @ np.diag([1, 1, d]) @ U.T
        tm = np.array(cd) - Rm @ np.array(cs)
        return Rm, tm
    except ImportError:
        return None, None

import numpy as np
print('\n=== identity-order rigid solve (bind[k] -> pal[k]) ===')
src = np.array(bt[:31])
dst = np.array([model_t[p] for p in pal])
Rm, tm = solve_rigid(src, dst)
pred = src @ Rm.T + tm
res = np.linalg.norm(pred - dst, axis=1)
print(f'residuals: median {np.median(res):.4f} max {res.max():.4f} '
      f'mean {res.mean():.4f}')

print('\n=== permutation search via edge-length voting (greedy) ===')
# build cost: for the tree, each edge (a,b,L); binds i->j distance must equal L.
# Start: root Bone58 (Pelvis) unknown; try all 31 binds as Pelvis, propagate.
best_overall = None
for root_k in range(31):
    assign = {('Bone58'): root_k}
    used = {root_k}
    # BFS the tree; for each child edge L, pick unused bind j minimizing
    # | |bt[j]-bt[assign[par]]| - L |
    ok = True
    frontier = ['Bone58']
    while frontier:
        a = frontier.pop()
        for (p, k), L in edges.items():
            if p != a or k in assign:
                continue
            ai = assign[a]
            cands = sorted(((abs(math.dist(bt[j], bt[ai]) - L), j)
                            for j in range(31) if j not in used))
            if not cands:
                ok = False
                break
            dd, j = cands[0]
            if dd > 0.05:
                ok = False
                break
            assign[k] = j
            used.add(j)
            frontier.append(k)
        if not ok:
            break
    if ok and len(assign) == 31:
        # score = sum of edge errors
        sc = sum(abs(math.dist(bt[assign[k]], bt[assign[p]]) - L)
                 for (p, k), L in edges.items())
        if best_overall is None or sc < best_overall[0]:
            best_overall = (sc, root_k, dict(assign))
if best_overall:
    sc, root_k, assign = best_overall
    print(f'consistent tree match FOUND: root bind[{root_k}], '
          f'total edge error {sc:.4f}')
    inv = {v: k for k, v in assign.items()}
    print('bind[k] -> bone:')
    for k in range(31):
        print(f'  bind[{k:2d}] = {inv.get(k, "?")} ({by_alias[inv[k]]["name"] if k in inv else ""})')
    # rigid solve with this assignment
    dst2 = np.array([model_t[inv[k]] for k in range(31)])
    Rm, tm = solve_rigid(src, dst2)
    pred = src @ Rm.T + tm
    res = np.linalg.norm(pred - dst2, axis=1)
    print(f'\nrigid solve residuals: median {np.median(res):.4f} '
          f'max {res.max():.4f}')
    print('R =')
    print(np.round(Rm, 4))
    print('t =', np.round(tm, 4))
    json.dump(dict(assign={k: inv[k] for k in range(31)},
                   R=Rm.tolist(), t=tm.tolist(),
                   resid=dict(median=float(np.median(res)),
                              max=float(res.max()))),
              open('/tmp/s31_t2_treematch.json', 'w'), indent=1)
else:
    print('NO consistent tree match within 5 cm per edge')
