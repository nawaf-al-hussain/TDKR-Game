#!/usr/bin/env python3
"""S31 T2 v3: Batman bind pose — FINAL layout:
  node record (base = nameA word):
    +0x00 nameA ('<name>-node')   +0x04 nameB   +0x08 alias ('BoneNN' or '')
    +0x0c t.xyz  +0x18 q.xyzw  +0x28 s.xyz  +0x34 u32 1
    +0x38 childCount  +0x3c firstChildPtr  (+0x44 attachments on containers)
  Skinning (row-vector): v' = sum_i w_i * (v * invBind(b_i)) * world(node(b_i))
  bind pose <=> world(node) == invBind^-1.
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
    child = u32(o + 0x3c)
    if child and not (0x2760 <= child < 0x4a58):
        o += 4
        continue
    nodes.append(dict(off=o, name=n2, alias=al, t=t, q=q, s=s,
                      qlen=ql, ccount=u32(o + 0x38), child=child))
    o += 0x50
bn = [n for n in nodes if n['alias'].startswith('Bone')]
print(f'nodes: {len(nodes)}, bone-aliased: {len(bn)}')
by_name = {n['name']: n for n in nodes}
by_off = {n['off']: n for n in nodes}
by_alias = {n['alias']: n for n in bn}

pal = []
o = 0x3167c
while o < 0x31774:
    blk = d[o:o+8]
    pal.append('Bone' + (blk[0:2] if blk[4:8] == b'Bone' else blk[4:6])
               .decode('latin1'))
    o += 8
print(f'palette: {len(pal)}, missing nodes: {[p for p in pal if p not in by_alias]}')

children = collections.defaultdict(list)
for n in nodes:
    c = by_off.get(n['child'])
    if c is not None and c is not n:
        children[n['name']].append(c['name'])
print('\nchild-ptr links:')
for p, k in children.items():
    print(f'  {p} -> {k}')

BIPED = {
    'Bip01_Pelvis': 'Bip01', 'Bip01_Spine': 'Bip01_Pelvis',
    'Bip01_Spine1': 'Bip01_Spine', 'Bip01_Neck': 'Bip01_Spine1',
    'Bip01_Head': 'Bip01_Neck',
    'Bip01_L_Thigh': 'Bip01_Pelvis', 'Bip01_L_Calf': 'Bip01_L_Thigh',
    'Bip01_L_Foot': 'Bip01_L_Calf', 'Bip01_R_Thigh': 'Bip01_Pelvis',
    'Bip01_R_Calf': 'Bip01_R_Thigh', 'Bip01_R_Foot': 'Bip01_R_Calf',
    'Bip01_L_Clavicle': 'Bip01_Spine1', 'Bip01_L_UpperArm': 'Bip01_L_Clavicle',
    'Bip01_L_Forearm': 'Bip01_L_UpperArm', 'Bip01_L_Hand': 'Bip01_L_Forearm',
    'Bip01_R_Clavicle': 'Bip01_Spine1', 'Bip01_R_UpperArm': 'Bip01_R_Clavicle',
    'Bip01_R_Forearm': 'Bip01_R_UpperArm', 'Bip01_R_Hand': 'Bip01_R_Forearm',
    'Bip01_L_Finger0': 'Bip01_L_Hand', 'Bip01_L_Finger01': 'Bip01_L_Finger0',
    'Bip01_L_Finger1': 'Bip01_L_Hand', 'Bip01_L_Finger11': 'Bip01_L_Finger1',
    'Bip01_L_Finger2': 'Bip01_L_Hand', 'Bip01_L_Finger21': 'Bip01_L_Finger2',
    'Bip01_R_Finger0': 'Bip01_R_Hand', 'Bip01_R_Finger01': 'Bip01_R_Finger0',
    'Bip01_R_Finger1': 'Bip01_R_Hand', 'Bip01_R_Finger11': 'Bip01_R_Finger1',
    'Bip01_R_Finger2': 'Bip01_R_Hand', 'Bip01_R_Finger21': 'Bip01_R_Finger2',
}
# reconcile: ptr-tree wins where present; biped table fills the rest
parent = {}
for p, k in children.items():
    for kk in k:
        parent[kk] = p
for kid, par in BIPED.items():
    parent.setdefault(kid, par)
conflicts = {k: (v, BIPED.get(k)) for k, v in parent.items()
             if k in BIPED and BIPED[k] != v}
print('\nparent conflicts (ptr vs biped-standard):', conflicts or 'NONE')

BINDS = 0x5a210
NB = 38
binds = []
for k in range(NB):
    m = struct.unpack_from('<16f', d, BINDS + k * 64)
    binds.append((m[0:3], m[4:7], m[8:11], m[12:15]))  # rows R0,R1,R2,t


def invbind(k):
    R0, R1, R2, t = binds[k]
    R = [R0, R1, R2]
    det = (R[0][0]*(R[1][1]*R[2][2]-R[1][2]*R[2][1])
           - R[0][1]*(R[1][0]*R[2][2]-R[1][2]*R[2][0])
           + R[0][2]*(R[1][0]*R[2][1]-R[1][1]*R[2][0]))
    Ri = tuple(tuple((R[(j+1)%3][(a+1)%3]*R[(j+2)%3][(a+2)%3]
                      - R[(j+1)%3][(a+2)%3]*R[(j+2)%3][(a+1)%3]) / det
                     for j in range(3)) for a in range(3))
    ti = tuple(-sum(Ri[a][j]*t[j] for j in range(3)) for a in range(3))
    return Ri, ti


def normq(q):
    n = math.sqrt(sum(x * x for x in q))
    return tuple(x / n for x in q)


def qmat_rows(q):
    x, y, z, w = q
    return ((1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)),
            (2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)),
            (2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)))


AXMAPS = {
    'id':     lambda v: (v[0], v[1], v[2]),
    'xz-y':   lambda v: (v[0], v[2], -v[1]),
    'x-zy':   lambda v: (v[0], v[2], v[1]),
    'x-y-z':  lambda v: (v[0], -v[1], -v[2]),
    'xyz-':   lambda v: (v[0], v[1], -v[2]),
    'x-z-y':  lambda v: (v[0], -v[2], v[1]),
    'x-yz':   lambda v: (v[0], -v[1], v[2]),
    '-x-zy':  lambda v: (-v[0], -v[1], v[2]),
    '-xyz-':  lambda v: (-v[0], v[1], -v[2]),
    '-x-yz':  lambda v: (-v[0], -v[2], -v[1]),
    '-x-z-y': lambda v: (-v[0], v[2], v[1]),
}


def compose_world(axf):
    world = {}
    def rec(name, M, tr, depth=0):
        if name in world or depth > 30:
            return
        n = by_name.get(name)
        if n is None:
            return
        q = normq(n['q'])
        R = qmat_rows(q)
        lM = tuple(tuple(R[i][j] * n['s'][j] for j in range(3))
                   for i in range(3))
        lt = n['t']
        Mw = tuple(tuple(sum(M[i][k]*lM[k][j] for k in range(3))
                         for j in range(3)) for i in range(3))
        tw = tuple(M[i][0]*lt[0] + M[i][1]*lt[1] + M[i][2]*lt[2] + tr[i]
                   for i in range(3))
        world[name] = (Mw, tw)
        for kid in children.get(name, []):
            rec(kid, Mw, tw, depth+1)
    rec('Bip01', ((1, 0, 0), (0, 1, 0), (0, 0, 1)), (0, 0, 0))
    # close over biped-parent chains
    changed = True
    guard = 0
    while changed and guard < 10:
        changed = False
        guard += 1
        for name in list(by_name):
            if name in world:
                continue
            p = parent.get(name)
            if p and p in world:
                M, tr = world[p]
                n = by_name[name]
                q = normq(n['q'])
                R = qmat_rows(q)
                lM = tuple(tuple(R[i][j] * n['s'][j] for j in range(3))
                           for i in range(3))
                lt = n['t']
                Mw = tuple(tuple(sum(M[i][k]*lM[k][j] for k in range(3))
                                 for j in range(3)) for i in range(3))
                tw = tuple(M[i][0]*lt[0] + M[i][1]*lt[1] + M[i][2]*lt[2] + tr[i]
                           for i in range(3))
                world[name] = (Mw, tw)
                changed = True
    return world


print('\n=== axis search: world(palette-bone) vs inv(bind[k]) nearest ===')
res = []
for ax, f in AXMAPS.items():
    world = compose_world(f)
    errs = []
    pal_nodes = [(p, by_alias[p]['name']) for p in pal if p in by_alias]
    for k in range(31):
        Ri, ti = invbind(k)
        ti_m = f(ti)
        cands = [(sum((world[pn][1][i]-ti_m[i])**2 for i in range(3)), p)
                 for p, pn in pal_nodes if pn in world]
        if not cands:
            break
        dist, p = min(cands)
        errs.append((dist ** 0.5, p, k))
    if not errs:
        continue
    med = sorted(e[0] for e in errs)[len(errs)//2]
    mx = max(e[0] for e in errs)
    res.append((med, ax, errs))
    print(f'  {ax:8s} median {med:.4f}  max {mx:.4f}')
res.sort()
med, best_ax, errs = res[0]
print(f'\nBEST: {best_ax} median {med:.4f}')
perm = [None] * 38
for d_, p, k in errs:
    perm[k] = p
print('bind[k] -> palette bone assignment (nearest):')
for k in range(31):
    d_ = errs[k][0] if k < len(errs) else -1
    print(f'  bind[{k:2d}] -> {perm[k]}  dist {d_:.4f}')
json.dump(dict(best=best_ax, median=med,
               assignment={str(k): perm[k] for k in range(len(perm)) if perm[k]},
               scores=[(m, a) for m, a, _ in res]),
          open('/tmp/s31_t2_axsearch.json', 'w'), indent=1)
print('\nwrote /tmp/s31_t2_axsearch.json')
