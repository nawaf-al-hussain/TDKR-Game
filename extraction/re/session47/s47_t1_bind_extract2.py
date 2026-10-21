#!/usr/bin/env python3
"""s47 T1 extraction v2: decode BOTH setparam schemas
  material-level: {name*, 13, 2, 1, v1, v2}
  profile-level:  {name*, semantic*, 13, 1, v1, v2}
value header at v1 {1, v1+24}, node at v1+24 = image index.
Assign profile entries to materials via the record technique intervals
(records 0..306 @0x23308 stride 260; ws[13]=tech ptr, ws[14]=count).
Compare the resulting per-material table with the source.dae authoring table."""
import io, zipfile, json, bisect
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
u32 = np.frombuffer(LE, '<u4', NB // 4)
N = NB // 4

def cstr(off, maxn=80):
    if not (0 < off < NB):
        return None
    e = LE.find(b'\0', off)
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
    imgs.append((i, int(w[0]), int(w[2])))

BASE, REC = 0x23308, 260
recs = []
for i in range(307):
    a = BASE + i * REC
    ws = [int(u32[(a + k * 4) // 4]) for k in range(REC // 4)]
    recs.append(ws)

# technique intervals per record
tech_starts = []
for i, ws in enumerate(recs):
    tp, tc = ws[13], ws[14]
    if 0 < tp < NB and 0 < tc <= 8:
        tech_starts.append((tp, i))
tech_starts.sort()
starts = [t[0] for t in tech_starts]

def owner_of(addr):
    j = bisect.bisect_right(starts, addr) - 1
    if j < 0:
        return None
    return tech_starts[j][1]

mat_entries = []   # material-level
prof_entries = []  # profile-level
for k in range(N - 6):
    w0, w1, w2, w3, v1, v2 = (int(u32[k + j]) for j in range(6))
    if v2 != v1 + 4 or not (0 < v1 < NB - 32):
        continue
    if int(u32[v1 // 4]) != 1 or int(u32[v1 // 4 + 1]) != v1 + 24:
        continue
    idx = int(u32[(v1 + 24) // 4])
    schema = None
    if w1 == 13 and w2 == 2 and w3 == 1:
        schema = 'mat'
        nm = cstr(w0)
    elif w2 == 13 and w3 == 1 and w1 != 13:
        schema = 'prof'
        nm = cstr(w0)
    if schema is None or nm is None or len(nm) > 40:
        continue
    rec = {'entry': k * 4, 'schema': schema, 'name': nm, 'v1': v1, 'idx': idx}
    if 0 <= idx < 176:
        i, nmptr, tgptr = imgs[idx]
        rec['image'] = cstr(nmptr)
        rec['tga'] = cstr(tgptr)
    if schema == 'mat':
        mat_entries.append(rec)
    else:
        ow = owner_of(k * 4)
        rec['owner'] = ow
        prof_entries.append(rec)

print('material-level entries:', len(mat_entries),
      'real:', sum(1 for r in mat_entries if 0 <= r['idx'] < 176))
print('profile-level entries:', len(prof_entries),
      'real:', sum(1 for r in prof_entries if 0 <= r['idx'] < 176),
      'none:', sum(1 for r in prof_entries if r['idx'] == 0xffffffff))

# build per-material table from profile entries
table = {}
for r in prof_entries:
    if 0 <= r['idx'] < 176 and r['owner'] is not None:
        m = table.setdefault(r['owner'], {})
        m.setdefault(r['name'], []).append(r['tga'])
print('materials with >=1 profile binding:', len(table))
for probe in (73, 302):
    print(f'material {probe}:', json.dumps(table.get(probe, {})))
# distribution
import collections
c = collections.Counter(tuple(sorted(m.keys())) for m in table.values())
print('binding-shape census:', c.most_common(6))

json.dump({'mat_entries': mat_entries, 'prof_entries': prof_entries,
           'table': {str(k): v for k, v in table.items()}},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t1_bindings_v2.json', 'w'), indent=1)
print('saved s47_t1_bindings_v2.json')
