#!/usr/bin/env python3
"""S31 T2 v5: solve the bind<->model correspondence and axis convention.
- candidates: 48 signed permutations (axis convention) x Kabsch rigid solve
- data: binds @0x30e30 (31, palette-ordered) vs composed model positions
- then the bind-pose test on all 1449 vertices with shuffled nulls
"""
import struct, math, json, itertools
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]


def pool(v):
    if 0x868 <= v < 0x22d8:
        e = d.find(b'\0', v)
        if e >= v:
            return d[v:e].decode('latin1')
    return None


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

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o + 8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8

BIPED = {
    'Bone58': None, 'Bone57': 'Bone58', 'Bone36': 'Bone57',
    'Bone56': 'Bone36', 'Bone55': 'Bone56',
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


QCONV = {'xyzw': 0, 'xyzw_conj': 1, 'wxyz': 2, 'wxyz_conj': 3}

def qmat_rows(q, conv='xyzw'):
    if conv == 'wxyz':
        q = (q[1], q[2], q[3], q[0])
    elif conv == 'wxyz_conj':
        q = (q[1], q[2], q[3], q[0])
        q = (-q[0], -q[1], -q[2], q[3])
    elif conv == 'xyzw_conj':
        q = (-q[0], -q[1], -q[2], q[3])
    x, y, z, w = q
    return ((1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)),
            (2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)),
            (2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)))


def compose(alias, conv='xyzw'):
    chain = []
    a = alias
    while a is not None:
        chain.append(a)
        a = BIPED.get(a)
    chain.reverse()
    root = by_name['Bip01']
    rq = normq(root['q'])
    RR = qmat_rows(rq, conv)
    M = tuple(tuple(RR[i][j] * root['s'][j] for j in range(3))
              for i in range(3))
    t = root['t']
    for a in chain:
        n = by_alias[a]
        q = normq(n['q'])
        R = qmat_rows(q, conv)
        lM = tuple(tuple(R[i][j] * n['s'][j] for j in range(3))
                   for i in range(3))
        lt = n['t']
        Mw = tuple(tuple(sum(M[i][k]*lM[k][j] for k in range(3))
                         for j in range(3)) for i in range(3))
        tw = tuple(M[i][0]*lt[0] + M[i][1]*lt[1] + M[i][2]*lt[2] + t[i]
                   for i in range(3))
        M, t = Mw, tw
    return np.array(t)


model = np.array([compose(p) for p in pal])          # 31 x 3

BINDS = 0x30e30
bt = np.array([struct.unpack_from('<16f', d, BINDS + k * 64)[12:15]
               for k in range(31)])

# ---- 48 signed permutations ----
def perm_mats():
    for pr in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            P = np.zeros((3, 3))
            for i, j in enumerate(pr):
                P[i, j] = signs[i]
            yield P, pr, signs


best = None
for conv in ('xyzw', 'xyzw_conj', 'wxyz', 'wxyz_conj'):
    model = np.array([compose(p, conv) for p in pal])
    for P, pr, signs in perm_mats():
        src = bt @ P.T
        cs = src.mean(0)
        cd = model.mean(0)
        U, S, Vt = np.linalg.svd((src - cs).T @ (model - cd))
        d0 = np.sign(np.linalg.det(Vt.T @ U.T))
        R = Vt.T @ np.diag([1, 1, d0]) @ U.T
        t = cd - R @ cs
        res = np.linalg.norm(src @ R.T + t - model, axis=1)
        med = float(np.median(res))
        if best is None or med < best[0]:
            best = (med, P, pr, signs, R, t, res, conv)
med, P, pr, signs, R, t, res, conv = best
print(f'BEST: quat conv={conv}  axis map perm={pr} signs={signs}')
print(f'residuals after Kabsch: median {med*100:.3f} cm  '
      f'max {res.max()*100:.3f} cm  mean {res.mean()*100:.3f} cm')
print('R =', np.round(R, 4).tolist())
print('t =', np.round(t, 4).tolist())
print('\nper-bone residuals (cm):')
for k in range(31):
    print(f'  {pal[k]} {by_alias[pal[k]]["name"]:20s} {res[k]*100:8.2f}')

# ---- full bind-pose test ----
BASE = 0x4b5c
N = 1449
SKIN = 0x31774
verts = np.array([struct.unpack_from('<3f', d, BASE + i * 80)
                  for i in range(N)])
skin = []
for i in range(N):
    b4 = struct.unpack_from('<4B', d, SKIN + i * 20)
    w4 = struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
    skin.append((b4, w4))

# world matrices from the FILE node locals (bind pose):
# world(node) = invBind[bone]^-1 mapped into model space via P and R,t:
# simpler: world_model(node(b)) = (R @ (P @ invBind_b^-1_P) + t)?? no:
# bind space -> model space is exactly (R, t): x_model = R x_bind + t.
# invBind lives in bind space; its inverse (bind-world) too. So
# world_model = R * world_bind + t  (affine, rotation part R @ .)
invB_bind = []
for k in range(31):
    m = struct.unpack_from('<16f', d, BINDS + k * 64)
    Rb = np.array([m[0:3], m[4:7], m[8:11]])
    tb = np.array(m[12:15])
    Ri = Rb.T          # orthonormal
    ti = -Ri @ tb
    invB_bind.append((Ri, ti))


def world_model_rows(Ri, ti):
    """row-vector world in model space: v' = v Mw + tw with
    Mw = R P-mapped... careful: x_model = R x_bind + t (column conv).
    For row-vector matrices: bind-space row affine (Rb, tb) acts
    v_bind = v . Rb + tb.  We want the same map expressed in model space.
    x_bind = P^T (x_model - t)  [since x_model = R (P^T? ...) - use numeric]
    """
    # numeric approach: transform corners
    pass


# Do it fully numerically: build bind-space world = invBind^-1 (already),
# then map its action into model space: for the row-affine (A, a) in bind
# space (v' = v A + a), the model-space equivalent (A', a') satisfies
#   R (v A + a) + t = (v') in bind -> model.  With v = P^T (vm - t)... wait
# x_model = R x_bind + t  =>  x_bind = R^T (x_model - t)
# v'_model = R (v_bind A + a) + t = R (R^T(vm - t) A + a) + t
#          = (vm - t) A R^T? no: R R^T (vm-t) A + R a + t = (vm - t) A + R a + t
# wait R R^T = I: v'_model = (vm - t) A + R a + t = vm A + (R a + t - t A)
# so A' = A (rotation part UNCHANGED as a matrix!), a' = R a + t - t A.
def bind_affine_to_model(A, a, R, t):
    A = np.asarray(A)
    a = np.asarray(a)
    ap = R @ a + t - t @ A
    return A, ap


# world(bind) per palette bone (bind space): inverse of invBind
worlds_bind = []
for k in range(31):
    m = struct.unpack_from('<16f', d, BINDS + k * 64)
    Rb = np.array([m[0:3], m[4:7], m[8:11]])
    tb = np.array(m[12:15])
    Ri = Rb.T
    ti = -Ri @ tb
    worlds_bind.append((Ri, ti))       # (A, a): v_bind = v_bind A + a

worlds_model = [bind_affine_to_model(A, a, R, t) for A, a in worlds_bind]

# skinned position, row-vector: v' = sum w (v invBind) world
# = sum w v (invBind . world)  (row-vector chaining)
maxerr = 0.0
errsum = 0.0
errs = []
for i in range(N):
    b4, w4 = skin[i]
    v = verts[i]
    acc = np.zeros(3)
    for j in range(4):
        if w4[j] == 0.0:
            continue
        b = b4[j]
        A_inv, a_inv = invB_bind[b - 1] if False else (None, None)
        # skin id base test: try 1-based first
        pass
    # (filled below)
    errs.append(0.0)

# try both id bases
for base in (1, 0):
    maxerr = 0.0
    errsum = 0.0
    for i in range(N):
        b4, w4 = skin[i]
        v = verts[i]
        acc = np.zeros(3)
        for j in range(4):
            w = w4[j]
            if w == 0.0:
                continue
            b = b4[j] - base
            if not (0 <= b < 31):
                acc = None
                break
            A_inv, a_inv = invB_bind[b]
            A_w, a_w = worlds_model[b]
            # (v invBind) world in model space:
            # bind-space: u = v invBind (v, invBind in bind space!)
            # but v is MODEL space. u_bind = (v - t) R^T?? no:
            # x_bind = R^T (x_model - t). u = v_bind . Ainv + ainv
            # v'_model = R u + t
            vb = R.T @ (v - t)
            u = vb @ A_inv + a_inv
            vm = R @ u + t
            # apply world: u2_bind = u . Aw + aw (in bind space)
            u2b = u @ A_w + a_w
            v2m = R @ u2b + t
            acc += w * v2m
        if acc is None:
            maxerr = None
            break
        e = float(np.linalg.norm(acc - v))
        errsum += e
        maxerr = max(maxerr, e)
    if maxerr is None:
        print(f'id base {base}: invalid bone index encountered')
    else:
        print(f'\nid base {base}: bind-pose max error {maxerr*100:.3f} cm, '
              f'mean {errsum/N*100:.3f} cm')

# shuffled-weights null (base 1)
random = np.random.default_rng(7)
null_max = []
for trial in range(5):
    mx = 0.0
    for i in range(0, N, 50):
        b4, w4 = skin[i]
        v = verts[i]
        perm = random.permutation(31)
        acc = np.zeros(3)
        for j in range(4):
            w = w4[j]
            if w == 0.0:
                continue
            b = int(perm[b4[j] - 1])
            A_inv, a_inv = invB_bind[b]
            A_w, a_w = worlds_model[b]
            vb = R.T @ (v - t)
            u = vb @ A_inv + a_inv
            u2b = u @ A_w + a_w
            acc += w * (R @ u2b + t)
        mx = max(mx, float(np.linalg.norm(acc - v)))
    null_max.append(mx)
print(f'shuffled-weights null (5 trials, sampled): '
      f'max errors {[round(x*100,1) for x in null_max]} cm')
