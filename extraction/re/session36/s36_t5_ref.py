#!/usr/bin/env python3
"""S36 T5 reference: compute Python-side digests for the node-vs-Python test.
- lvc: per-island record/token digests (10 islands)
- anims: 921 clips (ts/te/nseg) + per-clip channel key/tick digest
- skin: 1449 verts + skinning rest digest"""
import sys, json, struct, hashlib, glob, os
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

out = {}
# ---- lvc digests (10 islands + menu + shop) ----
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
lvc_files = sorted(glob.glob('/tmp/my-project/work/data/*.lvc'))
lvcd = {}
for p in lvc_files:
    name = os.path.basename(p)
    try:
        res = lvc_pure.parse(p, tab, templates, None)
    except Exception as e:
        lvcd[name] = {'error': f'{type(e).__name__}: {e}'[:120]}
        print(name, 'PARSE ERROR (documented anomaly class)')
        continue
    d, strings = res['data'], res['strings']
    h = hashlib.sha256()
    h.update(str(len(res.get('records', res.get('census', {})))).encode())
    # digest: census (class -> count), string table size, script count
    cens = {k: len(v) for k, v in res['census'].items()}
    body = json.dumps(cens, sort_keys=True).encode()
    h.update(body)
    h.update(str(len(strings)).encode())
    import re
    nscripts = 0
    for m in re.finditer(rb'function\s+[A-Za-z_][A-Za-z0-9_]*\s*\(', d):
        ln = d[m.start() - 1]
        if ln >= 16 and m.start() + ln <= len(d) and b'\x00' not in d[m.start():m.start() + ln] \
           and d[m.start():m.start() + ln].rstrip().endswith(b'end'):
            nscripts += 1
    lvcd[name] = {'census': cens, 'nstrings': len(strings), 'nscripts': nscripts,
                  'digest': h.hexdigest()[:16]}
    print(name, lvcd[name]['digest'], 'census classes', len(cens))
out['lvc'] = lvcd

# ---- anims digest ----
exec(open('/home/z/my-project/scripts/s35_t1_decode.py').read().split('def chan(')[0])
anim = {'nseg': nseg, 'fails': {}, 'clips': []}
h_seg = hashlib.sha256()
for s in segs:
    h_seg.update(struct.pack('<7I', s['k'], s['start'], s['end'], s['tbl'], s['dist'], len(seg_streams.get(s['k'], ())), 0))
anim['seg_digest'] = h_seg.hexdigest()[:16]
h_cl = hashlib.sha256()
for cl in clips:
    st = seg_streams
    cov = [s for s in segs if s['start'] < cl['te'] and s['end'] > cl['ts']]
    nch = 0; keysum = 0; valsum = 0.0
    for s in cov:
        stream = st.get(s['k'])
        if stream is None: continue
        for c in range(78):
            tw = stream[2 * c]; vw = stream[2 * c + 1]
            nt = len(tw)
            if nt == 0: continue
            vdim = 3 if CH[c][1] == 1 else 4
            nv = len(vw) * 4 // (vdim * 4)
            n = min(nt, nv)
            m = (tw[:n] >= cl['ts'] - 120) & (tw[:n] <= cl['te'] + 120)
            if not m.any(): continue
            nch += 1
            keysum += int(m.sum())
            valsum += float(np.asarray(vw.view('<f4').reshape(-1, vdim)[:n][m], np.float64).sum())
    h_cl.update(struct.pack('<5I', cl['i'], cl['ts'], cl['te'], nch, 0))
    h_cl.update(struct.pack('<d', valsum))
    anim['clips'].append([nch, valsum])
anim['clip_digest'] = h_cl.hexdigest()[:16]
anim['nclips'] = len(clips)
print('anims seg digest', anim['seg_digest'], 'clip digest', anim['clip_digest'])
out['anims'] = anim

# ---- skin digest ----
MD = '/tmp/my-project/work/data/batman.bdae'
d = open(MD, 'rb').read()
NV = 1449
verts = np.array([struct.unpack_from('<3f', d, 0x4b5c + i * 80) for i in range(NV)])
skin = hashlib.sha256()
skin.update(verts.astype('<f4').tobytes())
invb = np.array([np.frombuffer(d, '<f4', 16, 0x30e30 + k * 64) for k in range(31)])
skin.update(invb.tobytes())
recs = np.frombuffer(d, '<u8', NV * 20, 0x31774)  # raw bytes digest
skin.update(d[0x31774:0x31774 + NV * 20])
idx = np.frombuffer(d, '<u2', 5431, 0x210ba)
skin.update(idx.tobytes())
out['skin'] = {'digest': skin.hexdigest()[:16], 'vert0': [round(float(x), 6) for x in verts[0]],
               'nv': NV, 'nidx': 5431}
print('skin digest', out['skin']['digest'], 'vert0', out['skin']['vert0'])

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t5_ref.json', 'w'), indent=1)
print('reference written')
