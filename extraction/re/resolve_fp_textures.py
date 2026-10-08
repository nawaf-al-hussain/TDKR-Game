#!/usr/bin/env python3
"""Resolve footprint gt-diffuse names to shipped textures (name-based, no heuristics).

Game chain: gt diffuse 'X_LongDist[CompleteMap|DiffuseMap]' = runtime Beast bake
target. Shipped night bakes = textures named X (no suffix) in l_gothamcity_tex.
Verify match rate; propose deterministic fallbacks for the rest.
"""
import struct, re, json, collections

d = open('/home/z/my-project/download/obb_extract/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla','rb').read()
tag, idx_size, table_bytes, n = struct.unpack('>IIII', d[:16])
pool = d[16+n*16:idx_size]
shipped = set()
for i in range(n):
    off, sz, name_off, _ = struct.unpack('>IIII', d[16+i*16:32+i*16])
    end = pool.find(b'\x00', name_off)
    shipped.add(pool[name_off:end].decode('latin1','replace'))
low = {s.lower(): s for s in shipped}

gt = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/scripts/ground_truth_city.json'))
SUF = re.compile(r'_(longdist(completemap|diffusemap|diffuse_map)?|longdistdiffusemap|longdistd\s?iffusemap)$', re.I)

unbound = []   # (fpfile, gt_diffuse) pairs that ended texs:[] in manifest
man = json.load(open('/home/z/my-project/work/ghpages/models/manifest.json'))
bound = {}
for g in man['glbs']:
    for f in g['files']:
        bound[f['name']] = f['texs']
for name, e in gt.items():
    if 'footprint' not in name.lower():
        continue
    if bound.get(name) == []:
        ds = {m.get('diffuse') for m in e.get('meshes', [])}
        unbound.append((name, ds))

def resolve(diffuse):
    if not diffuse:
        return None, 'no-diffuse'
    if diffuse.endswith('Sampler'):
        return None, 'runtime-sampler'
    base = SUF.sub('', diffuse)
    if base.lower() in low:
        return low[base.lower()], 'exact'
    # variants: try _atlas / _T / _TH additions
    for suf in ('_atlas', '_T', '_TH', '_ground'):
        if (base.lower() + suf) in low:
            return low[base.lower() + suf], 'suffix' + suf
    # any shipped texture starting with base
    pref = [s for s in shipped if s.lower().startswith(base.lower() + '_')
            and not re.search(r'(?i)(_nrm|_refl|rfl|_mask|emissive|normal)', s)]
    if pref:
        pref.sort(key=len)
        return pref[0], 'prefix:' + pref[0]
    return None, 'NO-SHIP'

ok = collections.Counter()
fails = []
for name, ds in sorted(unbound):
    for dif in sorted(ds or {None}):
        tex, how = resolve(dif)
        ok[how] += 1
        if tex is None:
            fails.append((name, dif, how))
        else:
            print(f"{name:36s} {str(dif):44s} -> {tex:40s} [{how}]")
print()
print('resolution summary:', dict(ok))
print('FAILS:')
for f in fails:
    print('  ', f)
