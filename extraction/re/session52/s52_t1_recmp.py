#!/usr/bin/env python3
"""s52 T1 recompare (fixed Y-flip) + targeted audit runs (zoom/zone clobber census, gpucheck)."""
import json, sys, os
import importlib.util
spec = importlib.util.spec_from_file_location('r1', '/home/z/my-project/scripts/s52_t1_run.py')
r1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r1)

REFDIR = r1.REFDIR
OUTJSON = r1.OUTJSON
out = json.load(open(OUTJSON))
steps = [1, 2, 3, 4]
cpu_png = {s: REFDIR + 's52_cpu_step%d.png' % s for s in steps}
table = []
for fix in (0, 1):
    for s in steps:
        dump = REFDIR + 's52_gl_fix%d_step%d.png' % (fix, s)
        if not os.path.exists(dump):
            continue
        m = r1.cmp_pair(dump, cpu_png[4] if s == 5 else cpu_png[s])
        m.update({'step': s, 'fix': fix})
        table.append(m)
        print('step %d fix %d: %s' % (s, fix, m), flush=True)
zref = REFDIR + 's50_ref_zbuf_snap.png'
zone = []
for fix in (0, 1):
    dump = REFDIR + 's52_gl_zone_fix%d.png' % fix
    if os.path.exists(dump):
        m = r1.cmp_pair(dump, zref)
        m['fix'] = fix
        zone.append(m)
        print('zone fix %d: %s' % (fix, m), flush=True)
out['bisect_table'] = table
out['zone'] = zone

# ---- targeted runs with the PATCHED page (true draw-time unit audit) ----
BB = r1.BB
runs = [
    ('zoom73-fix0-audit', '?mat=73&bb=%s&nodepth=1&upload=1&step=2&fix=0' % BB),
    ('zone-fix0-audit', '?upload=1&fix=0'),
    ('gpucheck', '?mat=73&bb=%s&nodepth=1&upload=1&step=4&fix=1&gpucheck=1' % BB),
]
extra = {}
for tag, qs in runs:
    print('run', tag, flush=True)
    r = r1.run_gl(qs, 's52_gl_' + tag)
    extra[tag] = {'qs': qs, 'gate': r.get('gate'), 'pageerrs': r.get('pageerrs')}
    if 'upload' in r:
        b = r['upload'].get('batches', [])
        m73 = [x for x in b if x.get('mid') == 73]
        clob = [x.get('mid') for x in b if x.get('CLOBBER')]
        extra[tag]['mat73'] = m73
        extra[tag]['clobbered_mids'] = clob
        extra[tag]['n_lmfx'] = len(b)
        print('  mat73:', m73)
        print('  clobbered:', clob)
    if 'gpucheck' in r:
        extra[tag]['gpucheck'] = r['gpucheck']
        print(r['gpucheck'])
out['targeted'] = extra
json.dump(out, open(OUTJSON, 'w'), indent=1)
print('saved', OUTJSON)
