#!/usr/bin/env python3
"""s51 T4: identify the per-material 10-float runs via the compiled table's
SNewParam float blocks. If the per-material non-sampler float payload sums to
10 for the bulk of materials and correlates with effect family, the runs are
IDENTIFIED; else STOP (s50 already scanned pointer/value-block/stride paths)."""
import struct, io, zipfile, collections, json
import numpy as np

BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)
f32 = np.frombuffer(LE, '<f4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

# type -> component count hypothesis: 13=sampler, 7=vec4, 6=vec3, 5=vec2, 4=float, 3=matrix?
# determine empirically from the census values: LightMapAtlas type7 = (1,1,0,0) vec4
TYPE_COMP = {4: 1, 5: 2, 6: 3, 7: 4, 3: 16, 8: 4, 9: 4, 12: 4}

per_mat = {}
tot_counter = collections.Counter()
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    eff = cstr(ws[3]) or ''
    fam = eff[1:].split('-fx')[0] if eff.startswith('#') else 'none'
    floats = []
    for j in range(ws[4]):
        pa = ws[5] + j * 24
        pw = [int(w32[(pa + k * 4) // 4]) for k in range(6)]
        pname = cstr(pw[0])
        typ, cnt = pw[2], pw[3]
        if typ == 13:
            continue
        comp = TYPE_COMP.get(typ)
        if comp is None:
            continue
        v1 = pw[4]
        # value block: [1, ptr=v1+24] header then count*comp floats at v1+24
        vals = [float(f32[(v1 + 24 + k) // 4]) for k in range(cnt * comp)]
        floats.append({'name': pname, 'type': typ, 'count': cnt, 'vals': vals})
    total = sum(f['count'] * TYPE_COMP[f['type']] for f in floats)
    tot_counter[total] += 1
    per_mat[i] = {'fam': fam, 'total': total, 'params': floats}

print('per-material non-sampler float totals:', dict(sorted(tot_counter.items())))
# the 10-float population: which params compose them?
ten = [m for m in per_mat if per_mat[m]['total'] == 10]
print('materials with total==10: %d / 307' % len(ten))
combo = collections.Counter()
for m in ten:
    combo[tuple((f['name'], f['type'], f['count']) for f in per_mat[m]['params'])] += 1
for k, n in combo.most_common(8):
    print('  x%-4d %s' % (n, k))
# value ranges per position across the 10-float population
if ten:
    pos_vals = collections.defaultdict(list)
    for m in ten:
        flat = []
        for f in per_mat[m]['params']:
            flat.extend(f['vals'])
        for pos, v in enumerate(flat):
            pos_vals[pos].append(v)
    print('per-position stats over %d mats:' % len(ten))
    for pos in sorted(pos_vals):
        arr = np.array(pos_vals[pos])
        print('  pos%d: min %.4f p50 %.4f max %.4f  distinct %d' % (pos, arr.min(), np.median(arr), arr.max(), len(np.unique(arr.round(4)))))
# correlation with effect family
famtot = collections.Counter((per_mat[m]['fam'], per_mat[m]['total']) for m in per_mat)
print('family x total:', dict(famtot))
json.dump({str(m): per_mat[m] for m in per_mat},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t4_params.json', 'w'), indent=0)
