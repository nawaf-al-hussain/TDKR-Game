#!/usr/bin/env python3
"""S62 T2 step 3: numpy side of the bisection.
Parses Bane_mercenary.bdae (s60_t3_mercval read_bdae2), computes the FK world
matrices at rest from the file TRS, compares vs the page's dumped boneMatrixWorld /
boneInverses (as loaded by GLTFLoader), per bone; finds the convention gap."""
import struct, json, sys
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session60')
import importlib.util
spec = importlib.util.spec_from_file_location(
    'mv', '/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t3_mercval.py')
mv = importlib.util.module_from_spec(spec)
import types
# the module runs assertions on import? read only the functions we need via exec
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t3_mercval.py').read()
# cut off the main section (everything after 'def main' or top-level calls)
head = src.split("if __name__")[0]
ns = {}
exec(head, ns)
read_bdae2 = ns['read_bdae2']

BDAE = '/tmp/my-project/work/data/Bane_mercenary.bdae'
import os
if not os.path.exists(BDAE):
    # find it in the zip extraction
    for cand in ('/tmp/my-project/work/TDKR_data/Bane_mercenary.bdae',
                 '/tmp/my-project/raw/Bane_mercenary.bdae'):
        if os.path.exists(cand):
            BDAE = cand
            break
print('bdae:', BDAE, os.path.exists(BDAE))
skin = read_bdae2(BDAE)

def quat_to_mat(x, y, z, w):
    """bdae quat (x,y,z,w) -> 3x3 rotation."""
    m = np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
    return m

def trs_to_mat4(t, q, s):
    M = np.eye(4)
    R = quat_to_mat(*q)
    M[:3, :3] = R @ np.diag(s)
    M[:3, 3] = t
    return M

# numpy FK: nodes by name, parent chain (bdae parent name = pnameOf?)
nodes = {n['name']: n for n in skin['nodes']}
parents = skin.get('pnameOf', {})
# skin joint order
joints = skin['jointNodes']
print('nJoints:', len(joints), 'nNodes:', len(skin['nodes']))

# FK: world matrix per joint (rest)
world = {}
def fk(name):
    if name in world:
        return world[name]
    nd = nodes[name]
    M = trs_to_mat4(nd['t'], nd['q'], nd['s'])
    pr = parents.get(name)
    if pr and pr in nodes:
        M = fk(pr) @ M
    world[name] = M
    return M
for j in joints:
    fk(j)

bis = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_bisect.json'))
bb = bis['bindBisect']
bn = bb['boneNames']  # page bone names (GLB node names)
print('page bones:', bn[:6], '...')

# compare per bone: page matrixWorld vs numpy FK world (same name)
rows = []
for i, nm in enumerate(bn):
    mw = np.array(bb['boneMatrixWorld'][i]).reshape(4, 4).T  # THREE column-major -> row-major
    inv = np.array(bb['boneInverses'][i]).reshape(4, 4).T
    if nm in world:
        F = world[nm]
        dev_mw = np.abs(mw - F).max()
        dev_inv = np.abs(inv - np.linalg.inv(F)).max()
        rows.append((nm, dev_mw, dev_inv))
    else:
        rows.append((nm, None, None))
bad = [r for r in rows if r[1] is None]
print('bones not in bdae nodes:', [r[0] for r in bad][:8])
okrows = [r for r in rows if r[1] is not None]
okrows.sort(key=lambda r: -max(r[1], r[2] or 0))
print('\nworst bones by |page - numpyFK|:')
for nm, dm, di in okrows[:10]:
    print(f'  {nm:24s} matrixWorld_dev={dm:.4f} boneInverse_dev={di:.4f}')
print(f'\nmedian devs: mw={np.median([r[1] for r in okrows]):.5f} inv={np.median([r[2] for r in okrows]):.5f}')
exact_mw = sum(1 for r in okrows if r[1] < 1e-4)
exact_inv = sum(1 for r in okrows if (r[2] or 9) < 1e-4)
print(f'exact (<1e-4): matrixWorld {exact_mw}/{len(okrows)}, boneInverses {exact_inv}/{len(okrows)}')

# also: node TRS page vs bdae (b)
print('\nnode TRS diffs (page vs bdae rest locals):')
worst_t = 0; worst_q = 0; worst_s = 0
for tr in bb['nodeTRS']:
    nm = tr['name']
    if nm not in nodes:
        continue
    nd = nodes[nm]
    dt = np.abs(np.array(tr['pos']) - np.array(nd['t'])).max()
    dq = np.abs(np.array(tr['quat']) - np.array(nd['q'])).max()
    ds = np.abs(np.array(tr['scl']) - np.array(nd['s'])).max()
    worst_t = max(worst_t, dt); worst_q = max(worst_q, dq); worst_s = max(worst_s, ds)
print(f'  max TRS deltas: t={worst_t:.6f} q={worst_q:.6f} s={worst_s:.6f}')

# position attribute sanity: vertex bbox from the page GLB vs numpy skin.verts
print('\npage oneVertexRest out:', bb['oneVertexRest']['out'])
sv = np.array(skin['verts']).reshape(-1, 3)
print('numpy skin.verts bbox:', sv.min(0).round(2), sv.max(0).round(2), 'n=', len(sv))
