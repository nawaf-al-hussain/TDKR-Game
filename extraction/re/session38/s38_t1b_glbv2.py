#!/usr/bin/env python3
"""S38 T1b: rebuild batman.glb v2 for the live page.
- TRIM tail-overrun indices (index 5430 = 31904 >= NV) at the source
- embed chara_Batman_DIFFUSE (RGB888 1024x1024) as PNG with REPEAT sampler
- add POSITION min/max (loader warning), keep the verified anim set
- convention untouched: numpy row-form pipeline (proven == three.js this round)
"""
import struct, json, io
import numpy as np
import numpy as np

SRC = open('/home/z/my-project/scripts/s36_t3_export.py').read()
head = SRC.split('# ---------- GLB assembly ----------')[0]
g = {'__name__': 's38_ctx'}
exec(head, g)

verts = g['verts']; uvs = g['uvs']; w4s = g['w4s']; b4s = g['b4s']; ids = g['ids']
bd = open('/tmp/my-project/work/data/batman.bdae', 'rb').read()
nrms = np.array([struct.unpack_from('<3f', bd, 0x4b5c + i*80 + 12) for i in range(g['NV'])], np.float32)
NV = g['NV']; invB = g['invB']; joint_nodes = g['joint_nodes']
node_of = g['node_of']; order = g['order']; node_trs = g['node_trs']; gnodes = g['gnodes']
anims = g['anims']; parent_name = g['parent_name']; NEED = g['need']

# --- 1. trim to the TRUE index count: the mesh record header at IDX_OFF-28
# ("Batman", 0, 0, stride=20, INDEX_COUNT=5430, MAX_VERT_IDX=1448, 0) — s38 finding.
# 5430 = 1810 tris; everything after belongs to the next mesh record (global pool).
NIDX_TRUE = 5430
assert NIDX_TRUE % 3 == 0
ids = np.asarray(ids).reshape(-1)[:NIDX_TRUE]
n_tri = len(ids) // 3
tri = ids[:n_tri * 3].reshape(n_tri, 3)
bad = (tri >= NV).any(1)
print(f'indices: {len(ids)} ({n_tri} tris); bad tris (idx >= NV={NV}): {int(bad.sum())}')
if bad.sum():
    bi = np.where(bad)[0]
    print('  bad tri rows:', bi[:10].tolist(), 'their max idx:', tri[bad].max())
    raise SystemExit('UNEXPECTED bad indices within the true count — header model wrong')
tri_ok = tri[~bad]
print(f'kept {len(tri_ok)} tris, max idx {tri_ok.max()}')

# --- 2. texture -> PNG
from PIL import Image
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_batman_diffuse_src.bin', 'rb').read()
tex = np.frombuffer(src, np.uint8).reshape(1024, 1024, 3)
img = Image.fromarray(tex, 'RGB')
pngbuf = io.BytesIO()
img.save(pngbuf, 'PNG', optimize=True)
png = pngbuf.getvalue()
print(f'texture PNG: {len(png)} B, mean rgb {tex.reshape(-1,3).mean(0).round(1)}')
print(f'UV range: u [{uvs[:,0].min():.3f}, {uvs[:,0].max():.3f}] v [{uvs[:,1].min():.3f}, {uvs[:,1].max():.3f}]')

# --- 3. GLB v2 assembly (extends the s36 export verbatim)
ibm_bytes = b''.join(np.asarray(invB[b], np.float32).tobytes() for b in range(31))
jindices = [node_of[joint_nodes[b]] for b in range(31)]
pos_b = verts.astype(np.float32).tobytes()
nrm_b = nrms.tobytes()
uv_b = uvs.astype(np.float32).tobytes()
wt_b = w4s.astype(np.float32).tobytes()
jn_b = b4s.astype(np.uint16).tobytes()
idx_b = tri_ok.astype(np.uint16).tobytes()
NIDX = int(tri_ok.size)  # flat index count (3 per tri)

anim_bins = []
def anim_accessors(channels, blob_off):
    sams = []
    for cd in channels:
        tb = np.asarray(cd['times'], np.float32).tobytes()
        ob = np.asarray(cd['out'], np.float32).tobytes()
        t_off = blob_off
        anim_bins.append(tb); blob_off += len(tb)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        o_off = blob_off
        anim_bins.append(ob); blob_off += len(ob)
        while blob_off % 4: anim_bins.append(b'\0'); blob_off += 1
        sams.append((t_off, len(tb), len(cd['times']), o_off, len(ob), len(cd['out']),
                     cd['out'].shape[1]))
    return sams, blob_off

blob_off = 0
sams_all = []
for label, channels in anims:
    sams, blob_off = anim_accessors(channels, blob_off)
    sams_all.append(sams)
anim_buf = b''.join(anim_bins)

parts = []
base = 0
offs = {}
for k, seg in (('pos', pos_b), ('nrm', nrm_b), ('uv', uv_b), ('wt', wt_b), ('jn', jn_b),
               ('idx', idx_b), ('ibm', ibm_bytes), ('png', png)):
    padn = (4 - base % 4) % 4
    if padn: parts.append(b'\0' * padn); base += padn
    offs[k] = base; parts.append(seg); base += len(seg)
buf = b''.join(parts)

gltf = {
    'asset': {'version': '2.0', 'generator': 'tdkr-s38'},
    'scene': 0, 'scenes': [{'nodes': [0, len(NEED)]}],
    'nodes': [], 'skins': [{'inverseBindMatrices': None, 'joints': jindices}],
    'meshes': [{'primitives': [{'attributes': {
        'POSITION': None, 'NORMAL': None, 'TEXCOORD_0': None, 'WEIGHTS_0': None,
        'JOINTS_0': None}, 'indices': None, 'material': 0, 'doubleSided': True}]}],
    'materials': [{'pbrMetallicRoughness': {'baseColorFactor': [1, 1, 1, 1],
                                            'baseColorTexture': {'index': 0},
                                            'metallicFactor': 0.0,
                                            'roughnessFactor': 0.9}}],
    'textures': [{'sampler': 0, 'source': 0}],
    'samplers': [{'wrapS': 10497, 'wrapT': 10497}],   # REPEAT (UV atlas [0,16))
    'images': [{'bufferView': None, 'mimeType': 'image/png'}],
    'animations': [{'name': lb, 'channels': [], 'samplers': []} for lb, _ in anims],
    'accessors': [], 'bufferViews': [],
    'buffers': [{'byteLength': base + len(anim_buf)}],
}
for nm, gi in order.items():
    t, q, s = node_trs[nm]
    gnodes[gi]['translation'] = [float(x) for x in t]
    gnodes[gi]['rotation'] = [float(x) for x in q]
    gnodes[gi]['scale'] = [float(x) for x in s]
gnodes.append(dict(name='BATMAN_mesh', mesh=0, skin=0))
gltf['nodes'] = gnodes

def add_bv(off, ln):
    i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': off, 'byteLength': ln})
    return i
def add_acc(off, ln, count, ctype, typ, mn=None, mx=None):
    bv = add_bv(off, ln)
    i = len(gltf['accessors'])
    a = {'bufferView': bv, 'componentType': ctype, 'count': count, 'type': typ}
    if mn is not None:
        a['min'] = [float(x) for x in mn]; a['max'] = [float(x) for x in mx]
    gltf['accessors'].append(a)
    return i

a_pos = add_acc(offs['pos'], len(pos_b), NV, 5126, 'VEC3',
                mn=verts.min(0), mx=verts.max(0))
a_nrm = add_acc(offs['nrm'], len(nrm_b), NV, 5126, 'VEC3')
a_uv = add_acc(offs['uv'], len(uv_b), NV, 5126, 'VEC2')
a_wt = add_acc(offs['wt'], len(wt_b), NV, 5126, 'VEC4')
a_jn = add_acc(offs['jn'], len(jn_b), NV, 5123, 'VEC4')
a_idx = add_acc(offs['idx'], len(idx_b), NIDX, 5123, 'SCALAR')
a_ibm = add_acc(offs['ibm'], len(ibm_bytes), 31, 5126, 'MAT4')
gltf['skins'][0]['inverseBindMatrices'] = a_ibm
gltf['images'][0]['bufferView'] = add_bv(offs['png'], len(png))
prim = gltf['meshes'][0]['primitives'][0]
prim['attributes']['POSITION'] = a_pos
prim['attributes']['NORMAL'] = a_nrm
prim['attributes']['TEXCOORD_0'] = a_uv
prim['attributes']['WEIGHTS_0'] = a_wt
prim['attributes']['JOINTS_0'] = a_jn
prim['indices'] = a_idx

ANIM_BUF_BASE = base
def add_anim_acc(off_in_anim, ln, count, typ):
    bv_i = len(gltf['bufferViews'])
    gltf['bufferViews'].append({'buffer': 0, 'byteOffset': ANIM_BUF_BASE + off_in_anim,
                                'byteLength': ln})
    ai = len(gltf['accessors'])
    gltf['accessors'].append({'bufferView': bv_i, 'componentType': 5126,
                              'count': count, 'type': typ})
    return ai

for (label, channels), sams in zip(anims, sams_all):
    ga = next(a for a in gltf['animations'] if a['name'] == label)
    for cd, (t_off, t_ln, t_n, o_off, o_ln, o_n, ncomp) in zip(channels, sams):
        ti = add_anim_acc(t_off, t_ln, t_n, 'SCALAR')
        oi = add_anim_acc(o_off, o_ln, o_n, 'VEC4' if ncomp == 4 else 'VEC3')
        ga['samplers'].append({'input': ti, 'output': oi, 'interpolation': 'LINEAR'})
        ga['channels'].append(dict(sampler=len(ga['samplers']) - 1,
                                   target=dict(node=node_of[cd['node']],
                                               path=cd['path'])))

js = json.dumps(gltf, separators=(',', ':')).encode()
jpad = js + b' ' * ((4 - len(js) % 4) % 4)
bin_all = buf + anim_buf
bpad = bin_all + b'\0' * ((4 - len(bin_all) % 4) % 4)
out = (struct.pack('<3I', 0x46546C67, 2, 12 + 8 + len(jpad) + 8 + len(bpad)) +
       struct.pack('<II', len(jpad), 0x4E4F534A) + jpad +
       struct.pack('<II', len(bpad), 0x004E4942) + bpad)
for p in ('/home/z/my-project/download/batman_s38_textured.glb',):
    open(p, 'wb').write(out)
print(f'wrote batman_s38_textured.glb ({len(out)} B)')

# quick numeric self-check: rest anchor + idle t=0 pose vs numpy truth (row-form fk)
V = np.hstack([verts, np.ones((NV, 1))])
W_rest = {}
def world_rest(nm):
    if nm in W_rest: return W_rest[nm]
    M = g['Lrow'](nm) @ (world_rest(parent_name(nm)) if parent_name(nm) else np.eye(4))
    W_rest[nm] = M
    return M
sp = np.zeros((NV, 3))
for j in range(4):
    sel_ids = np.clip(b4s[:, j], 0, 30)
    for b in range(31):
        sel = sel_ids == b
        if not sel.any(): continue
        M = invB[b] @ world_rest(joint_nodes[b])
        sp[sel] += w4s[sel][:, j][:, None] * (V @ M)[sel][:, :3]
e = np.linalg.norm(sp - verts, axis=1)
print(f'REST anchor: <0.1mm {int((e < 1e-4).sum())}/{NV}, max {e.max()*100:.4f} cm')
