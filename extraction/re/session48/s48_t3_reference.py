#!/usr/bin/env python3
"""s48 T3: parse the COMPILED scene-material instance table in
little_endian_not_quantized.bdae directly (301 entries x 36 B @0x5fea0; profile
SNewParam blocks hold u32 image indices; image table 176 x 12 B @0x22a9c) and
build the engine binding table [name, DiffuseMap tga, LightMap tga].
Outputs: canonical digest (sorted by name), per-id mapping (id word ->
geometry material id), and the cross-compare vs the source.dae authoring table.
The JS page (city_slice7.html) repeats this parse in the browser and must
reproduce the digest byte-for-byte."""
import io, zipfile, json, hashlib
import numpy as np
import xml.etree.ElementTree as ET

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t3_compiled.json'
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}

LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
u32 = np.frombuffer(LE, '<u4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn:
        return None
    try:
        t = LE[off:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

IMG_BASE, IMG_N = 0x22a9c, 176
imgs = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    imgs.append((int(w[0]), int(w[2])))

INST_BASE, INST_N, INST_REC = 0x5fea0, 307, 36
rows = []
for i in range(INST_N):
    a = INST_BASE + i * INST_REC
    w = [int(u32[(a + k * 4) // 4]) for k in range(9)]
    name = cstr(w[0])
    effect = cstr(w[3])
    np_count, prof_ptr, ident = w[4], w[5], w[6]
    sam = {}
    for j in range(np_count):
        pa = prof_ptr + j * 24
        pw = [int(u32[(pa + k * 4) // 4]) for k in range(6)]
        pname = cstr(pw[0])
        if pw[2] != 13 or pw[3] != 1:
            continue
        v1 = pw[4]
        if int(u32[v1 // 4]) != 1 or int(u32[v1 // 4 + 1]) != v1 + 24:
            continue
        idx = int(u32[(v1 + 24) // 4])
        if 0 <= idx < IMG_N:
            nmptr, tgptr = imgs[idx]
            sam[pname] = cstr(tgptr) or ''
        elif idx == 0xffffffff:
            sam[pname] = ''
    rows.append({'i': i, 'name': name, 'effect': effect, 'id': ident,
                 'np_count': np_count,
                 'diff': sam.get('DiffuseMap', ''), 'lm': sam.get('LightMap', ''),
                 'n_sam': len(sam)})

print('instance rows:', len(rows), 'names resolved:', sum(1 for r in rows if r['name']))
canon = json.dumps(sorted([[r['name'], r['diff'], r['lm']] for r in rows],
                          key=lambda x: x[0]), separators=(',', ':'))
digest = hashlib.sha256(canon.encode()).hexdigest()
print('COMPILED table digest:', digest)
print('diff bound:', sum(1 for r in rows if r['diff']), 'lm bound:', sum(1 for r in rows if r['lm']))

# id word == entry index; every DB material id 0..306 has an instance row
ids = sorted(r['id'] for r in rows)
missing = [i for i in range(307) if i not in set(ids)]
print('ids: min', ids[0], 'max', ids[-1], 'count', len(set(ids)), 'missing from 0..306:', missing)

# authoring table (independent source.dae parse)
z = zipfile.ZipFile(P)
root = ET.fromstring(z.read('source.dae'))
imgs_d = {}
for im in root.find('c:library_images', NS).findall('c:image', NS):
    iid = im.get('id')
    init = im.find('c:init_from', NS)
    imgs_d[iid] = init.text.strip() if init is not None and init.text else ''
arows = []
for md in root.find('c:library_materials', NS).findall('c:material', NS):
    inst = md.find('c:instance_effect', NS)
    sam = {}
    if inst is not None:
        surf = {}
        for sp in inst.findall('c:setparam', NS):
            sf = sp.find('c:surface/c:init_from', NS)
            if sf is not None and sf.text:
                surf[sp.get('ref')] = imgs_d.get(sf.text.strip(), sf.text.strip())
        for sp in inst.findall('c:setparam', NS):
            s2 = sp.find('c:sampler2D/c:source', NS)
            if s2 is not None and s2.text and s2.text.strip() in surf:
                sam[sp.get('ref')] = surf[s2.text.strip()]
    arows.append([md.get('id'), sam.get('DiffuseMap') or '', sam.get('LightMap') or ''])
by_name = {r[0]: r for r in arows}
matched = 0
row_ok = 0
diffs = []
no_scene = []
for r in rows:
    a = by_name.get(r['name'])
    if a is None:
        diffs.append({'name': r['name'], 'issue': 'no authoring row'})
        continue
    matched += 1
    if [a[1], a[2]] == [r['diff'], r['lm']]:
        row_ok += 1
    else:
        diffs.append({'name': r['name'], 'authoring': [a[1], a[2]],
                      'compiled': [r['diff'], r['lm']]})
for a in arows:
    if not any(r['name'] == a[0] for r in rows):
        no_scene.append(a[0])
print('name match: %d/%d  full-row agreement: %d/%d' % (matched, len(rows), row_ok, len(rows)))
print('row diffs:', json.dumps(diffs))
print('authoring rows without scene entry (%d):' % len(no_scene), no_scene)
# mat 302 resolution: instance row 302 exists (effect AlphaMasking, not the
# s46-record's SimpleAdditive — the 260-B records are NOT keyed by material id)
r302 = [r for r in rows if r['id'] == 302]
print('instance row id==302:', json.dumps(r302))

out = {'digest': digest, 'rows': rows, 'n': len(rows),
       'matched': matched, 'row_ok': row_ok, 'diffs': diffs,
       'no_scene': no_scene,
       'authoring_digest_note': 'authoring canonical digest = 4f6e2d070e7ea2201d9e81cd67502e6e8a27b4f3a2a7160ac28d7a7835fbb26c (s45/s47)'}
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
